# encoding: utf-8
from z3 import And
from .program import progs

def contracts(b, p):
	return b < p

def require(pre, b, post):
	return And(b.pre() >= pre, b.post()/pre <= post, +b)

class ContractedProgram():
	"""This class represents a notation of contracted program."""

	def __init__(self, s, b=None, p=None):
		if b is None and p is None:
			self.b, self.p = progs(s, 'b p')
		else:
			self.b, self.p = b, p
		s.add(contracts(self.b, self.p))

	def pre(self):
		return self.p.pre()

	def b(self):
		return self.b

	def post(self):
		return self.p.post()

	def strongest_postcondition(self, C=None):
		if C is None:
			return self.b.post() / self.pre()
		else:
			return self.b.post() / C

	def sp(self, C=None):
		return self.strongest_postcondition(C)

	def weakest_precondition(self, r=None):
		if r is None:
			return self.b.dom() - (self.b.post() - self.post()).dom()
		else:
			return self.b.dom() - (self.b.post() - r).dom()

	def wp(self, r=None):
		return self.weakest_precondition(r)

class CProg(ContractedProgram):
	"""This is short for ContractedProgram"""