# encoding: utf-8
from .program import Program

class GuardedConditional(Program):
	def __init__(self, C1, p1, C2, p2):
		self.definition = p1 / C1 | p2 / C2
	
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
		self.definition = p1 / C | p2 / -C
	
	def _set(self, x):
		return self.definition.set(x)

	def _pre(self, x):
		return self.definition.pre(x)

	def _post(self, x, y):
		return self.definition.post(x, y)

class Ite(IfThenElse):
	"""This is short name for IfThenElse"""