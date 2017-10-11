# encoding: utf-8
import inspect
from z3 import ArraySort, BoolSort, ForAll, Exists, And, Or, Not, Implies
from .z3py_util import const, show_set_element

SORT = None

def set_sort(sort):
	global SORT
	SORT = sort

def get_sort():
	global SORT
	sort = SORT
	return sort

class Set():
	"""Base class for set instance."""
	
	# @param p A set instance created by Z3.py.
	def __init__(self, s):
		self.s = s

	def __call__(self, x):
		return self.has(x)

	def __neg__(self):
		return Complement(self)

	def __pow__(self, other):
		from .z3py_rel import Combination
		return Combination(self, other)

	def __sub__(self, other):
		return Subtraction(self, other)

	def __and__(self, other):
		return Intersection(self, other)
	
	def __or__(self, other):
		return Union(self, other)

	def __eq__(self, other):
		return eq(self, other)

	def __contains__():
		return included(self, other)

	def __le__(self, other):
		return included(self, other)

	def __ge__(self, other):
		return includes(self, other)

	def __ne__(self, other):
		return disjoint(self, other)

	# @param x An element that is included in this set.
	# @return The constraint that x is included in this set.
	def has(self, x):
		return self.s(x) if inspect.ismethod(self.s) else self.s[x]

	# @return A set instance created by Z3.py.
	def z3(self):
		return self.s

## Creates a new set.
#  @param name The name of the created set.
#  @param name The sort of the created set.
#  @return The set instance created.
def set(name):
	return Set(const(name, ArraySort(get_sort(), BoolSort())))

## Creates multiple new sets.
#  @param names The names of the created sets, separated by space character.
#  @return a list of the set instances created.
def sets(names):
	names = names.split(' ')
	return [set(name) for name in names]

## Returns a constraint that two sets are same.
# @param s1 A set that will be same as s2.
# @param s2 A set that will be same as s1.
# @return A constraint that two sets are same.
def eq(s1, s2):
	x = const('x', get_sort())
	return ForAll(x, s1(x) == s2(x))

## Returns a constraint that two sets are same.
# @param s1 A set that will be same as s2.
# @param s2 A set that will be same as s1.
# @return A constraint that two sets are same.
def includes(s1, s2):
	x = const('x', get_sort())
	return ForAll(x, Implies(s2(x), s1(x)))

## Returns a constraint that two sets are same.
# @param s1 A set that will be same as s2.
# @param s2 A set that will be same as s1.
# @return A constraint that two sets are same.
def included(s1, s2):
	x = const('x', get_sort())
	return ForAll(x, Implies(s1(x), s2(x)))

## Prints a set
#  @param solver The solver in which the set is.
#  @param set The set that need to be printed.
def show_set(solver, set):
	if isinstance(set, Set):
		set = set.z3()
	if not str(set)[1] == '!':
		show_set_element(solver, set)

class Union(Set):
	"""Union for set instances."""
	
	# @param p A set instance created by Z3.py.
	def __init__(self, s1, s2):
		self.s1 = s1
		self.s2 = s2

	# @param x An element that is included in this union of sets.
	# @return The constraint that x is included in this set.
	def has(self, x):
		return Or(self.s1(x), self.s2(x))

	def z3(self):
		return (self.s1, self.s2)

class Intersection(Set):
	"""Intersection for set instances."""
	
	# @param p A set instance created by Z3.py.
	def __init__(self, s1, s2):
		self.s1 = s1
		self.s2 = s2

	# @param x An element that is included in this Intersection of sets.
	# @return The constraint that x is included in this set.
	def has(self, x):
		return And(self.s1(x), self.s2(x))

	def z3(self):
		return (self.s1, self.s2)

class Inter(Intersection):
	"""This is short for Intersection"""

class Subtraction(Set):
	"""Subtraction for set instances."""
	
	def __init__(self, s1, s2):
		self.s1 = s1
		self.s2 = s2

	# @param x An element that is included in this Intersection of sets.
	# @return The constraint that x is included in this set.
	def has(self, x):
		return And(self.s1(x), Not(self.s2(x)))

	def z3(self):
		return (self.s1, self.s2)

class Sub(Subtraction):
	"""This is short for Subtraction"""

class Complement(Set):
	"""Complement for a set instance."""
	
	# @param p A set instance created by Z3.py.
	def __init__(self, s):
		self.s = s

	# @param x An element that is NOT included in this set.
	# @return The constraint that x is NOT included in this set.
	def has(self, x):
		return Not(self.s(x))

class Cpl(Complement):
	"""This is short name for Complement"""

class Empty(Set):
	"""An empty set"""
	def __init__(self):
		self.sort = get_sort()

	def has(self, x):
		return False

class Universe(Set):
	""" An Universe set"""
	def __init__(self):
		self.sort = get_sort()

	def has(self, x):
		return True

def disjoint(s1, s2):
	x = const('x', get_sort())
	return Not(Exists(x, (s1*s2)(x)))