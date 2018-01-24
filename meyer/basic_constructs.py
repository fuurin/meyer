# encoding: utf-8
from z3 import Or, And
from .program import Program

class Choice(Program):
	"""Choice, performs like p1 or p2 or ..."""
	def __init__(self, *p):
		self.p = list(p)

	def _set(self, x):
		return Or([p.set(x) for p in self.p])

	def _pre(self, x):
		return Or([p.pre(x) for p in self.p])

	def _post(self, x, y):
		# return Or([p.post(x, y) for p in self.p])
		return Or([(p.post()/p.pre())(x, y) for p in self.p])


class Choi(Choice):
	"""This is short name for Choice"""



class Composition(Program):
	"""Composition, performs like p1 then like p2."""
	def __init__(self, p1, p2):
		self.p1 = p1
		self.p2 = p2

	def _set(self, x):
		return Or(self.p1.set(x), self.p2.set(x))

	def _pre(self, x):
		return (self.p1.pre() & self.p1.post() << self.p2.pre())(x) 
	
	def _post(self, x, y):
		return (self.p1.post() // self.p2.pre() ^ self.p2.post())(x, y)
	
class Comp(Composition):
	"""This is short name for Composition"""



class SoftComposition(Program):
	"""Composition, performs like p1 then like p2."""
	def __init__(self, p1, p2):
		self.p1 = p1
		self.p2 = p2

	def _set(self, x):
		return Or(self.p1.set(x), self.p2.set(x))

	def _pre(self, x):
		return (self.p1.post() << self.p2.pre())(x)

	def _post(self, x, y):
		return (self.p1.post() ^ self.p2.post())(x, y)

class SComp(SoftComposition):
	"""This is short name for Composition"""


class Restriction(Program):
	"""Restriction, performs like a set c on program p."""
	def __init__(self, c, p):
		self.c = c
		self.p = p

	def _set(self, x):
		return self.p.set(x)

	def _pre(self, x):
		# return self.p.pre(x) # This causes counter example in P6
		# return And(self.p.pre(x)) # interesting result; this causes unknown
		return And(self.p.pre(x), self.c(x))

	def _post(self, x, y):
		return And(self.p.post(x, y), self.c(x))

class Rest(Restriction):
	"""This is short name for Restriction"""


class MeyerRestriction(Program):
	"""Restriction on Meyer's paper, performs like a set c on program p."""
	def __init__(self, c, p):
		self.c = c
		self.p = p

	def _set(self, x):
		return self.p.set(x)

	def _pre(self, x):
		return self.p.pre(x) # This causes counter example in P6
		# return And(self.p.pre(x)) # interesting result; this causes unknown
		# return And(self.p.pre(x), self.c(x))

	def _post(self, x, y):
		return And(self.p.post(x, y), self.c(x))

class MRest(MeyerRestriction):
	"""This is short name for MeyerRestriction"""
	

class Corestriction(Program):
	"""
	Corestriction, performs like 
	p applied only when results satisfy a set C.
	"""
	def __init__(self, p, c):
		self.p = p
		self.c = c

	def _set(self, x):
		return self.p.set(x)

	def _pre(self, x):
		return (self.p.pre() & self.p.post() << self.c)(x)

	def _post(self, x, y):
		return And(self.p.post(x, y), self.c(y))

class Corest(Corestriction):
	"""This is short name for Corestriction"""