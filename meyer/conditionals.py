# encoding: utf-8
from .program import Program
from .basic_constructs import Rest, Choi

class GuardedConditional(Program):
	def __init__(self, C1, p1, C2, p2):
		part1 = Rest(C1, p1)
		part2 = Rest(C2, p2)
		self.definition = Choi(part1, part2)
	
	def _set(self, x):
		return self.definition.set(x)

	def _pre(self, x):
		return self.definition.pre(x)

	def _post(self, x, y):
		return self.definition.post(x, y)

class GCond(GuardedConditional):
	"""This is short name for GuardedConditional"""

class IfThenElse(Program):
	def __init__(self, C, p1, p2):
		part1 = Rest(C, p1)
		part2 = Rest(-C, p2)
		self.definition = Choi(part1, part2)
	
	def _set(self, x):
		return self.definition.set(x)

	def _pre(self, x):
		return self.definition.pre(x)

	def _post(self, x, y):
		return self.definition.post(x, y)

class Ite(IfThenElse):
	"""This is short name for IfThenElse"""