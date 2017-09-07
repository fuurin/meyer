# encoding: utf-8
from z3 import ForAll, Exists, And, Implies
from .program import U
from .util.z3py_util import const, consts

def is_invariant_of(I, p):
	x, y = consts('x y', U)
	return ForAll(y, Implies(
		# 二項関係のran, domにはExistsが必要．他の定義でも注意
		Exists(x, And(I.has(x), p.pre(x), p.post(x,y))), 
		I.has(y)
	))

def is_ivr_of(I, p):
	return is_invariant_of(I, p)

# Actually this doesn't use C, b
def is_loop_invariant_of(I, a, C, b):
	x, y = consts('x y', U)
	return ForAll(y, Implies(
		I.has(y),
		Exists(x, And(a.pre(x), a.post(x,y))) 
	))

def is_livr_of(I, a, C, b):
	return is_livr_of(I, a, C, b)