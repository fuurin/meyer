# encoding: utf-8
from z3 import ForAll, Exists, Implies, And, Not
from .meyer import U
from .util.z3py_util import consts

## @file determinacy.py
#  This module is used to create deterministic assumptions on programs.
#
#  A program is deterministic is its postcondition is a function.

## Returns the assumption that makes a program deterministic.
#  @param p The program that needs to be deterministic.
#  @return The assumption linked to determinism in a program.
def deterministic(p):
	x,y,z = consts('x y z', U)
	return	And(
				ForAll(x, Exists(y, p.post(x, y))),
				ForAll([x,y,z], Implies(
					And(p.post(x, y), p.post(x, z)),
					y == z
				))
			)

## Returns the assumption that makes a program non-deterministic.
#  @param p The program that needs to be non-deterministic.
#  @return The assumption linked to non-determinism in a program.
def non_deterministic(p):
	return Not(deterministic(p))