# encoding: utf-8
from .util.z3py_rel import Img

def is_invariant_of(I, p):
	return Img(p.post, I * p.dom) <= I

def is_ivr_of(I, p):
	return is_invariant_of(I, p)

# Actually this doesn't use C, b
def is_loop_invariant_of(I, a, C, b):
	return I <= a.ran

def is_livr_of(I, a, C, b):
	return is_loop_invariant_of(I, a, C, b)