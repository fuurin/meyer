# encoding: utf-8
from .basic_constructs import Choi, Comp
from .program import Program

class AtomicConcurrency(Program):
	def __init__(self, p1, p2):
		part1 = Comp(p1, p2)
		part2 = Comp(p2, p1)
		self.definition = Choi(part1, part2)
	
	def _set(self, x):
		return self.definition.set(x)

	def _pre(self, x):
		return self.definition.pre(x)

	def _post(self, x, y):
		return self.definition.post(x, y)

class Atom(AtomicConcurrency):
	"""This is short name for AtomicConcurrency"""

class NonAtomicConcurrency(Program):
	def __init__(self, p1, p2, q):
		left = Comp(Atom(p1, q), p2)
		right = Comp(p1, Atom(p2, q))
		self.definition = Choi(left, right)
	
	def _set(self, x):
		return self.definition.set(x)

	def _pre(self, x):
		return self.definition.pre(x)

	def _post(self, x, y):
		return self.definition.post(x, y)

class NAtom(NonAtomicConcurrency):
	"""This is short name for NonAtomicConcurrency"""