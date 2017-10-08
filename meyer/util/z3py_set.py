# encoding: utf-8
from abc import ABCMeta, abstractmethod
from z3 import ArraySort, BoolSort, ForAll, And, Or, Not, Implies
from .z3py_util import const, show_set_element

SORT = None

def set_sort(sort):
	global SORT
	SORT = sort

def get_sort():
	global SORT
	return SORT
	
class SetBase():
	"""Abstract Base Class for set instance."""
	__metaclass__ = ABCMeta

	# @param x An element that is included in this set.
	# @return The constraint that x is included in this set.
	@abstractmethod
	def has(self, x):
		pass

class Set(SetBase):
	"""Base class for set instance."""
	
	# @param p A set instance created by Z3.py.
	def __init__(self, s):
		self.s = s

	def __call__(self, x):
		return self.has(x)

	# @param x An element that is included in this set.
	# @return The constraint that x is included in this set.
	def has(self, x):
		return self.s[x]

	def __add__(self, other):
		return Union(self, other)

	def __sub__(self, other):
		return Subtraction(self, other)

	def __mul__(self, other):
		return Intersection(self, other)

	def __neg__(self):
		return Complement(self)

	def __eq__(self, other):
		return eq(self, other)

	def __contains__():
		return included(self, other)

	def __le__(self, other):
		return included(self, other)

	def __ge__(self, other):
		return includes(self, other)

	# @return A set instance created by Z3.py.
	def z3(self):
		return self.s

## Creates a new set.
#  @param name The name of the created set.
#  @param name The sort of the created set.
#  @return The set instance created.
def set(name, sort=SORT):
	return Set(const(name, ArraySort(sort, BoolSort())), sort)

## Creates multiple new sets.
#  @param names The names of the created sets, separated by space character.
#  @return a list of the set instances created.
def sets(names, sort=SORT):
	names = names.split(' ')
	return [set(name, sort) for name in names]

## Returns a constraint that two sets are same.
# @param s1 A set that will be same as s2.
# @param s2 A set that will be same as s1.
# @return A constraint that two sets are same.
def eq(s1, s2, sort=SORT):
	x = const('x', sort)
	return ForAll(x, s1(x) == s2(x))

## Returns a constraint that two sets are same.
# @param s1 A set that will be same as s2.
# @param s2 A set that will be same as s1.
# @return A constraint that two sets are same.
def includes(s1, s2, sort=SORT):
	x = const('x', sort)
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
	if isinstance(set, SetBase):
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

class Empty(SetBase):
	"""An empty set"""
	def __init__(self, sort=SORT):
		self.sort = sort

	def has(self, x):
		return False

class Universe(SetBase):
	""" An Universe set"""
	def __init__(self, sort=SORT):
		self.sort = sort

	def has(self, x):
		return True