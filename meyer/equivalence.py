# encoding: utf-8
from z3 import ForAll, And
from .program import U
from .util.z3py_util import const, consts
## @file equivalence.py
#  Module used to define the condition of equivalence between two programs.
# 
#  Two programs are equivalent if their preconditions and their postconditions are the same.

## Creates the assumption of equivalence between two programs.
#  @param p1 The first program.
#  @param p2 The second program.
#  @return The assumption of equivalence between two programs.
def equivalent(p1, p2):
	x,y,z = consts('x y z', U)
	return ForAll([x,y,z], And(
		And(p1.pre(x), p1.post(x, y)) == 
		And(p2.pre(x), p2.post(x, y)),
		p1.pre(z) == p2.pre(z)
	))

def equal(p1, p2):
	x, y, z, w = consts('x y z w', U)
	return ForAll([x,y,z,w], And(
		p1.set(x) == p2.set(x),
		p1.pre(y) == p2.pre(y),
		p1.post(z, w) == p2.post(z, w)
	))

## Short name for equivalent.
#  @param p1 The first program.
#  @param p2 The second program.
#  @return The assumption of equivalence between two programs.
def eq(p1, p2):
	return equivalent(p1, p2)

## Creates the assumption of equality between two state sets of programs.
#  @param p1 The first program.
#  @param p2 The second program.
#  @return The assumption of equality between two state sets of programs.
def eq_set(p1, p2):
	x = const('x', U)
	return ForAll(x, p1.set(x) == p2.set(x))

## Creates the assumption of equality between two preconditions of programs.
#  @param p1 The first program.
#  @param p2 The second program.
#  @return The assumption of equality between two preconditions of programs.
def eq_pre(p1, p2):
	x = const('x', U)
	return ForAll(x, p1.pre(x) == p2.pre(x))

## Creates the assumption of equality between two postconditions of programs.
#  @param p1 The first program.
#  @param p2 The second program.
#  @return The assumption of equality between two postSconditions of programs.
def eq_post(p1, p2):
	x, y = consts('x y', U)
	return ForAll([x, y], p1.post(x, y) == p2.post(x, y))

## Creates the assumption of equality between two postconditions of feasible programs.
#  @param p1 The first program.
#  @param p2 The second program.
#  @return The assumption of equality between two postSconditions of feasible programs.
def eq_feasible_post(p1, p2):
	x, y = consts('x y', U)
	return ForAll([x, y], 
		And(p1.post(x, y), p1.pre(x)) == 
		And(p2.post(x, y), p2.pre(x))
	)