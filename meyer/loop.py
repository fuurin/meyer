# encoding: utf-8
from .special_programs import Skip
from .basic_constructs import Choi, Comp, Rest, Corest

LOOP_NUM = 10

def fixed_repetition(p, i):
	if i==0:
		return Rest(p.dom, Skip())
	else:
		return Comp(p, fixed_repetition(p, i-1))

def fix_rep(p, i):
	return fixed_repetition(p, i)

def arbitrary_repetition(p):
	return Choi(*[fix_rep(p, i) for i in range(LOOP_NUM)])

def arb_rep(p):
	return arbitrary_repetition(p)

def while_loop(a, C, b):
	return Corest(Comp(a, arb_rep(Rest(-C, b))), C)

def wloop(a, C, b):
	return while_loop(a, C, b)