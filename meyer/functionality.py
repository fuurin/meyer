# encoding: utf-8
from z3 import And, Not
from .util.z3py_set import set
from .util.z3py_rel import Img
## @file functionality.py
#  Module used to define the condition of functionality on a program.
# 
#  A program is functional if every subset C of S is disjoint from post_p(C). A program that is not functional is called imperative.

## Creates the assumption of functionality on a program.
#  @param p The program that needs to be functional.
#  @return The assumption.
def functional(p):
	c = set('c')
	return	And(c <= p.set, c | Img(p.post, c))

## Creates the assumption of an imperative program.
#  @param p The program that needs to be imperative.
#  @return The assumption.
def imperative(p):
	return Not(functional(p))