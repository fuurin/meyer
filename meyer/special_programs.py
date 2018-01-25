# encoding: utf-8
from z3 import ForAll, And, Not
from .util.z3py_util import elms
from .util.z3py_set import Universe, Empty
from .program import prog, Program

## @file special_program.py
#  Module used to define special programs according to meyer's article.
#  
#  

# Each classes are equivalence to restricted special program instances.
# However, one way may cause unknown. Then try another way.

class Fail(Program):
	def __init__(self):
		pass

	def _set(self, x):
		return False

	def _pre(self, x):
		return False

	def _post(self, x, y):
		return False

def fail(s):
	p = prog(s, "fail")
	x, y = elms("x y")
	s.add(ForAll([x, y], Not(Or(p.set(x), p.pre(x), p.post(x, y)))))
	return p

class Havoc(Program):
	def __init__(self):
		pass

	def _set(self, x):
		return True

	def _pre(self, x):
		return True

	def _post(self, x, y):
		return True

def havoc(s):
	p = prog(s, "havoc")
	x, y = elms("x y")
	s.add(ForAll([x, y], And(p.set(x), p.pre(x), p.post(x, y))))
	return p

class Skip(Program):
	def __init__(self):
		pass

	def _set(self, x):
		return True

	def _pre(self, x):
		return True

	def _post(self, x, y):
		return x == y

def skip(s):
	p = prog(s, "skip")
	x, y = elms("x y")
	s.add(ForAll([x, y], And(p.set(x), p.pre(x), p.post(x, y) == (x == y))))
	return p

def total(solver):
	p = prog(solver, 'total')
	solver.add(p.pre() == Universe())
	return p

def is_total(p):
	return p.pre() == Universe()