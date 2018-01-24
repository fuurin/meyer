# encoding: utf-8
import inspect
from z3 import ArraySort, BoolSort, EnumSort, ForAll, Exists, And, Or, Not, Implies
from .z3py_set import Set
from .z3py_util import U, const, unveil, model

SORT_DOM = U
SORT_RAN = U
REL_SORT = ArraySort(U, ArraySort(U, BoolSort()))

def set_sort(sort_dom, sort_ran):
	global SORT_DOM
	SORT_DOM = sort_dom
	global SORT_RAN
	SORT_RAN = sort_ran
	global REL_SORT
	REL_SORT = ArraySort(
		sort_dom, 
		ArraySort(sort_ran, BoolSort())
	)

def get_sort_dom():
	global SORT_DOM
	sort_dom = SORT_DOM
	return sort_dom

def get_sort_ran():
	global SORT_RAN
	sort_ran = SORT_RAN
	return sort_ran

class Relation():
	"""Base class for relation instance."""
	
	# @param r A relation instance created by Z3.py.
	def __init__(self, r):
		self.r = r

	def __call__(self, x, y):
		return self.has(x, y)

	def __neg__(self):
		return Complement(self)

	def __truediv__(self, other):
		return Restriction(self, other)

	def __floordiv__(self, other):
		return Corestriction(self, other)

	def __sub__(self, other):
		return Subtraction(self, other)

	def __lshift__(self, other):
		return InverseImage(self, other)

	def __rshift__(self, other):
		return Image(self, other)

	def __and__(self, other):
		return Intersection(self, other)

	def __or__(self, other):
		return Union(self, other)

	def __xor__(self, other):
		return Composition(self, other)

	def __eq__(self, other):
		return eq(self, other)

	def __contains__():
		return included(self, other)

	def __le__(self, other):
		return included(self, other)

	def __ge__(self, other):
		return includes(self, other)

	def __ne__(self, other):
		return Not(self.__eq__(other))

	def dom(self, x=None):
		return Set(self._dom) if x is None else self._dom(x)

	def _dom(self, x):
		y = const('x', get_sort_ran())
		return Exists(y, self.has(x, y))

	def ran(self, y=None):
		return Set(self._ran) if y is None else self._ran(x)
	
	def _ran(self, y):
		x = const('x', get_sort_dom())
		return Exists(x, self.has(x, y))

	def has(self, x, y):
		return self.r(x, y) if inspect.ismethod(self.r) else self.r[x][y]

	def z3(self):
		return self.r

class Rel(Relation):	
	"""This is short for Relation"""

## Creates a new relation.
#  @param name The name of the created set.
#  @param name The sort of the created set.
#  @return The set instance created.
def rel(name):
	return Rel(const(name, REL_SORT))

## Creates multiple new sets.
#  @param names The names of the created sets, separated by space character.
#  @return a list of the set instances created.
def rels(names):
	names = names.split(' ')
	return [rel(name) for name in names]

## Returns a constraint that two sets are same.
# @param s1 A set that will be same as s2.
# @param s2 A set that will be same as s1.
# @return A constraint that two sets are same.
def eq(r1, r2):
	x = const('x', get_sort_dom())
	y = const('y', get_sort_ran())
	return ForAll([x, y], r1(x, y) == r2(x, y))

## Returns a constraint that two sets are same.
# @param s1 A set that will be same as s2.
# @param s2 A set that will be same as s1.
# @return A constraint that two sets are same.
def includes(r1, r2):
	x = const('x', get_sort_dom())
	y = const('y', get_sort_ran())
	return ForAll([x, y], Implies(r2(x, y), r1(x, y)))

## Returns a constraint that two sets are same.
# @param s1 A set that will be same as s2.
# @param s2 A set that will be same as s1.
# @return A constraint that two sets are same.
def included(r1, r2):
	x = const('x', get_sort_dom())
	y = const('y', get_sort_ran())
	return ForAll([x, y], Implies(r1(x, y), r2(x, y)))

## Prints a relation
#  @param solver The solver in which the set is.
#  @param set The set that need to be printed.
def show_rel(solver, rel):
	if isinstance(rel, Relation):
		rel = rel.z3()
	if not str(rel)[1] == '!': 
		print("content of", rel)
		content = model(solver, rel).as_list()
		unveil(solver, content)
		print()

def show_rels(solver, *rels):
	for r in rels: show_rel(solver, r)

def show_rel_models(solver):
	is_rel = lambda elt: elt.range() == REL_SORT
	rels = list(filter(is_rel, solver.model()))
	show_rels(solver, *rels)

class Union(Rel):
	"""Union for relation instances."""
	
	def __init__(self, r1, r2):
		self.r1 = r1
		self.r2 = r2

	def has(self, x, y):
		return Or(self.r1(x, y), self.r2(x, y))

	def z3(self):
		return (self.r1, self.r2)

class Intersection(Rel):
	"""Intersection for relation instances."""
	
	def __init__(self, r1, r2):
		self.r1 = r1
		self.r2 = r2

	def has(self, x, y):
		return And(self.r1(x, y), self.r2(x, y))

	def z3(self):
		return (self.r1, self.r2)

class Inter(Intersection):
	"""This is short for Intersection"""

class Subtraction(Rel):
	"""Subtraction for relation instances."""
	
	def __init__(self, r1, r2):
		self.r1 = r1
		self.r2 = r2

	def has(self, x, y):
		return And(self.r1(x, y), Not(self.r2(x, y)))

	def z3(self):
		return (self.r1, self.r2)

class Sub(Subtraction):
	"""This is short for Subtraction"""

class Restriction(Rel):
	"""Restriction for a relation instance and a set instance."""
	
	def __init__(self, r, s):
		self.r = r
		self.s = s

	def has(self, x, y):
		return And(self.r(x, y), self.s(x))

	def z3(self):
		return (self.r, self.s)

class Rest(Restriction):
	"""This is short for Restriction"""

class Corestriction(Rel):
	"""Corestriction for a relation instance and a set instance."""
	
	def __init__(self, r, s):
		self.r = r
		self.s = s

	def has(self, x, y):
		return And(self.r(x, y), self.s(y))

	def z3(self):
		return (self.r, self.s)

class Corest(Corestriction):
	"""This is short for Corestriction"""

class Composition(Relation):
	"""Composition for relation instances. r;s (= s o r)"""
	
	def __init__(self, r, s):
		self.r = r
		self.s = s

	def has(self, x, y):
		a = const('a', get_sort_ran())
		return Exists(a, And(self.r(x, a), self.s(a, y)))

	def z3(self):
		return (self.r, self.s)

class Comp(Composition):
	"""This is short for Composition"""

class Image(Set):
	"""Image for a relation instance and a set instance."""
	
	def __init__(self, r, s):
		self.r = r
		self.s = s

	def has(self, y):
		x = const('x', get_sort_dom())
		return Exists(x, And(self.r(x, y), self.s(x)))

	def z3(self):
		return (self.r, self.s)

class Img(Image):
	"""This is short for Img"""

class InverseImage(Set):
	"""Inverse image for a relation instance and a set instance."""
	
	def __init__(self, r, s):
		self.r = r
		self.s = s

	def has(self, x):
		y = const('y', get_sort_ran())
		return Exists(y, And(self.r(x, y), self.s(y)))

	def z3(self):
		return (self.r, self.s)

class Inv(InverseImage):
	"""This is short for InverseImage"""

class Complement(Rel):
	"""Complement for a set instance."""
	
	def __init__(self, r):
		self.r = r

	def has(self, x, y):
		return Not(self.r(x, y))

class Cpl(Complement):
	"""This is short name for Complement"""

class Combination(Rel):
	"""Combination made of two set instances."""
	
	def __init__(self, s1, s2):
		self.s1 = s1
		self.s2 = s2

	def has(self, x, y):
		return And(self.s1(x), self.s2(y))

	def z3(self):
		return (self.s1, self.s2)

class Comb(Combination):
	"""This is short for Combination"""

class Empty(Relation):
	"""An empty set"""
	def __init__(self):
		self.sort_dom = get_sort_dom()
		self.sort_ran = get_sort_ran()

	def has(self, x, y):
		return False

class Universe(Relation):
	""" An Universe set"""
	def __init__(self):
		self.sort_dom = get_sort_dom()
		self.sort_ran = get_sort_ran()

	def has(self, x, y):
		return True

def well_founded(r):
	x = const('x', get_sort_dom())
	y = const('y', get_sort_ran())
	return ForAll([x, y], Implies(r(x, y), x != y))