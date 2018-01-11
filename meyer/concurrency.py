# encoding: utf-8
from .program import Program

class AtomicConcurrency(Program):
	def __init__(self, p1, p2):
		self.definition = (p1 ^ p2) | (p2 ^ p1)
	
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
		self.definition = (Atom(p1, q) ^ p2) | (p1 ^ Atom(p2, q))
	
	def _set(self, x):
		return self.definition.set(x)

	def _pre(self, x):
		return self.definition.pre(x)

	def _post(self, x, y):
		return self.definition.post(x, y)

class NAtom(NonAtomicConcurrency):
	"""This is short name for NonAtomicConcurrency"""

def commute(p1, p2):
	return p1 ^ p2 == p2 ^ p1