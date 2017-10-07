# encoding: utf-8
from z3 import ForAll, Implies, And, Not
from .program import U, prog, Program
from .util.z3py_util import const, consts

## @file special_program.py
#  Module used to define special programs according to meyer's article.
#  
#  

# Each classes are equivalence to restricted special program instances.
# However, one way may cause unknown. Then try another way.

class Fail(Program):
	def set(self, x):
		return False

	def pre(self, x):
		return False

	def post(self, x, y):
		return False

class Havoc(Program):
	def set(self, x):
		return True

	def pre(self, x):
		return True

	def post(self, x, y):
		return True

class Skip(Program):
	def set(self, x):
		return True

	def pre(self, x):
		return True

	def post(self, x, y):
		return x == y

def fail(solver):
	p = prog('fail')
	a, x, y = consts('a x y',U)
	solver.add(And(
		ForAll(a, Not(p.set(a))), 
		ForAll(a, Not(p.pre(a))),
		ForAll([x,y], Not(p.post(x, y)))
	))
	return p

def havoc(solver):
	havoc = prog(solver, 'havoc')
	a, x, y = consts('a x y',U)
	solver.add(
		ForAll(a, havoc.set(a)),
		ForAll(a, havoc.pre(a)),
		ForAll([x,y], havoc.post(x, y))
	)
	return havoc

def skip(solver):
	skip = prog(solver, 'skip')
	a, x, y = consts('a x y',U)
	# Skip is always feasible
	# solver.add(feasible(skip))
	solver.add(And(
		ForAll(a, skip.set(a)),
		ForAll(a, skip.pre(a)),
		ForAll([x,y], And(skip.post(x, y), x == y))
	))
	return skip

def total(solver):
	p = prog(solver, 'total')
	a = const('a', U)
	solver.add(ForAll(a, p.pre(a)))
	return p

def is_total(p):
	x = const('x', U)
	return ForAll(x, p.pre(x))