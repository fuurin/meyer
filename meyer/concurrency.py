# encoding: utf-8
from .basic_constructs import Choi, Comp
from .program import ProgramBase

class AtomicConcurrency(ProgramBase):
	def __init__(self, p1, p2):
		part1 = Comp(p1, p2)
		part2 = Comp(p2, p1)
		self.definition = Choi(part1, part2)
	
	def set(self, x):
		return self.definition.set(x)

	def pre(self, x):
		return self.definition.pre(x)

	def post(self, x, y):
		return self.definition.post(x, y)

class Atom(AtomicConcurrency):
	"""This is short name for AtomicConcurrency"""

class NonAtomicConcurrency(ProgramBase):
	def __init__(self, p1, p2, q):
		left = Comp(Atom(p1, q), p2)
		right = Comp(p1, Atom(p2, q))
		self.definition = Choi(left, right)
	
	def set(self, x):
		return self.definition.set(x)

	def pre(self, x):
		return self.definition.pre(x)

	def post(self, x, y):
		return self.definition.post(x, y)

class NAtom(NonAtomicConcurrency):
	"""This is short name for NonAtomicConcurrency"""