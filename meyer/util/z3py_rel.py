# encoding: utf-8
import inspect
from z3 import ArraySort, BoolSort, ForAll, Exists, And, Or, Not, Implies
from .z3py_set import Set
from .z3py_util import const, unveil

SORT_DOM = None
SORT_RAN = None

def set_sort(sort_dom, sort_ran):
	global SORT_DOM
	SORT_DOM = sort_dom
	global SORT_RAN
	SORT_RAN = sort_ran

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

	def __add__(self, other):
		return Union(self, other)

	def __sub__(self, other):
		return Subtraction(self, other)

	def __mul__(self, other):
		return Intersection(self, other)

	def __neg__(self):
		return Complement(self)

	def __truediv__(self, other):
		return Restriction(self, other)

	def __mod__(self, other):
		return Corestriction(self, other)

	def __lshift__(self, other):
		return InverseImage(self, other)

	def __rshift__(self, other):
		return Image(self, other)

	def __eq__(self, other):
		return eq(self, other)

	def __contains__():
		return included(self, other)

	def __le__(self, other):
		return included(self, other)

	def __ge__(self, other):
		return includes(self, other)

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
	return Rel(
		const(
			name, 
			ArraySort(
				get_sort_dom(), 
				ArraySort(get_sort_ran(), BoolSort())
			)
		)
	)

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

## Prints a set
#  @param solver The solver in which the set is.
#  @param set The set that need to be printed.
def show_set(solver, rel):
	if isinstance(rel, Relation):
		rel = rel.z3()
	if not str(rel)[1] == '!':
		unveil(solver, rel)

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

	# @param x An element that is included in this Intersection of sets.
	# @return The constraint that x is included in this set.
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

	# @param x An element that is included in this Intersection of sets.
	# @return The constraint that x is included in this set.
	def has(self, x, y):
		return And(self.s1(x, y), Not(self.s2(x, y)))

	def z3(self):
		return (self.r1, self.r2)

class Sub(Subtraction):
	"""This is short for Subtraction"""

class Restriction(Rel):
	"""Restriction for a relation instance and a set instance."""
	
	def __init__(self, r, s):
		self.r = r
		self.s = s

	# @param x An element that is included in this Intersection of sets.
	# @return The constraint that x is included in this set.
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

	# @param x An element that is included in this Intersection of sets.
	# @return The constraint that x is included in this set.
	def has(self, x, y):
		return And(self.r(x, y), self.s(y))

	def z3(self):
		return (self.r, self.s)

class Corest(Corestriction):
	"""This is short for Corestriction"""

class Image(Set):
	"""Image for a relation instance and a set instance."""
	
	def __init__(self, r, s):
		self.r = r
		self.s = s

	# @param y An element that is included in this Image of the relation.
	# @return The constraint that x is included in this set.
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

	# @param x An element that is included in this Inverse image of the relation.
	# @return The constraint that x is included in this set.
	def has(self, x):
		y = const('y', get_sort_ran())
		return Exists(y, And(self.r(x, y), self.s(y)))

	def z3(self):
		return (self.r, self.s)

class Inv(InverseImage):
	"""This is short for InverseImage"""

class Complement(Rel):
	"""Complement for a set instance."""
	
	# @param p A set instance created by Z3.py.
	def __init__(self, r):
		self.r = r

	# @param x An element that is NOT included in this set.
	# @return The constraint that x is NOT included in this set.
	def has(self, x, y):
		return Not(self.r(x, y))

class Cpl(Complement):
	"""This is short name for Complement"""

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