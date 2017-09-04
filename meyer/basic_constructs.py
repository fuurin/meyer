# encoding: utf-8
from z3 import Exists, Or, And
from .program import U, ProgramBase
from .util.z3py_util import const
from .util.z3py_set import SetBase

class Choice(ProgramBase):
	"""Choice, performs like p1 or p2 or ..."""
	def __init__(self, *p):
		self.p = list(p)

	def set(self, x):
		return Or([p.set(x) for p in self.p])

	def pre(self, x):
		return Or([p.pre(x) for p in self.p])

	def post(self, x, y):
		return Or([p.post(x, y) for p in self.p])

class Choi(Choice):
	"""This is short name for Choice"""



class Composition(ProgramBase):
	"""Composition, performs like p1 then like p2."""
	def __init__(self, p1, p2):
		self.p1 = p1
		self.p2 = p2

	def set(self, x):
		return Or(self.p1.set(x), self.p2.set(x))

	def pre(self, x):
		y = const('y', U)
		return Exists(y, And(
			self.p1.pre(x), self.p1.post(x, y), self.p2.pre(y)
		))

	def post(self, x, y):
		z = const('z', U)
		return Exists(z, And(
			self.p1.post(x, z), self.p2.pre(z), self.p2.post(z, y)
		))

class Comp(Composition):
	"""This is short name for Composition"""



class Restriction(ProgramBase):
	"""Restriction, performs like a set c on program p."""
	def __init__(self, c, p):
		self.c = c
		self.p = p

	def set(self, x):
		return self.p.set(x)

	def pre(self, x):
		# return self.p.pre(x) # This causes counter example in P6
		# return And(self.p.pre(x)) # interesting result; this causes unknown
		return And(self.p.pre(x), self.c.has(x))

	def post(self, x, y):
		return And(self.p.post(x, y), self.c.has(x))

class Rest(Restriction):
	"""This is short name for Restriction"""


class RestrictionPre(ProgramBase):
	"""PreRestriction, performs like a Pre_p on program p."""
	def __init__(self, p_for_pre, p):
		self.pp = p_for_pre
		self.p = p

	def set(self, x):
		return self.p.set(x)

	def pre(self, x):
		return And(self.p.pre(x), self.pp.pre(x))

	def post(self, x, y):
		return And(self.p.post(x, y), self.pp.pre(x))

class RestPre(RestrictionPre):
	"""This is short name for RestrictionPre"""


class RestrictionDomainPost(ProgramBase):
	"""PreRestriction, performs like a domain of post_p on program p."""
	def __init__(self, p_for_dom, p):
		self.pd = p_for_dom
		self.p = p

	def set(self, x):
		return self.p.set(x)

	def pre(self, x):
		y = const('y', U)
		return And(self.p.pre(x), Exists(y, self.pd.post(x, y)))

	def post(self, x, y):
		z = const('z', U)
		return And(self.p.post(x, y), Exists(z, self.pd.post(x, z)))

class RestDom(RestrictionDomainPost):
	"""This is short name for RestrictionDomainPost"""


class RestrictionRangePost(ProgramBase):
	"""PreRestriction, performs like a range of post_p on program p."""
	def __init__(self, p_for_ran, p):
		self.pr = p_for_ran
		self.p = p

	def set(self, x):
		return self.p.set(x)

	def pre(self, x):
		y = const('y', U)
		return And(self.p.pre(x), Exists(y, self.pr.post(x, y)))

	def post(self, x, y):
		z = const('z', U)
		return And(self.p.post(x, y), Exists(z, self.pr.post(x, z)))

class RestRan(RestrictionRangePost):
	"""This is short name for RestrictionRangePost"""


class Corestriction(ProgramBase):
	"""
	Corestriction, performs like 
	p applied only when results satisfy a set C.
	"""
	def __init__(self, p, c):
		self.p = p
		self.c = c

	def set(self, x):
		return self.p.set(x)

	def pre(self, x):
		y = const('y', U)
		return Exists(y, And(
			self.p.pre(x), self.p.post(x, y), self.c.has(y)
		))

	def post(self, x, y):
		return And(self.p.post(x, y), self.c.has(y))

class Corest(Corestriction):
	"""This is short name for Corestriction"""