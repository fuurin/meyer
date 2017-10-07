# encoding: utf-8
from z3 import ForAll, Exists, Implies, And, Not
from .program import U
from .util.z3py_util import consts
from .util.z3py_set import set
## @file functionality.py
#  Module used to define the condition of functionality on a program.
# 
#  A program is functional if every subset C of S is disjoint from post_p(C). A program that is not functional is called imperative.

## Creates the assumption of functionality on a program.
#  @param p The program that needs to be functional.
#  @return The assumption.
def functional(p):
	c = set('c', U)
	x,y = consts('x y', U)
	return	And(
				ForAll(x, Implies(c(x), p.set(x))),
				Not(Exists(x, 
					And(c(x), ForAll(y, And(p.post(y, x), c(y))))
				))
			)

## Creates the assumption of an imperative program.
#  @param p The program that needs to be imperative.
#  @return The assumption.
def imperative(p):
	return Not(functional(p))