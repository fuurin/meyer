from .program import U, ProgramBase
from .util.z3py_set import Cpl
from　.special_programs import Skip
from .basic_constructs import Choi, Comp, Rest, RestDom

LOOP_NUM = 10

def fixed_repetition(p, i):
	if i==0:
		return RestDom(p, Skip())
	else:
		return Comp(p, fixed_repetition(p, i-1))

def fix_rep(p, i):
	return fixed_repetition(p, i)

# def arbitrary_repetition(p):
# 	for i in range(LOOP_NUM):
		