# encoding: utf-8
from z3 import ForAll, Implies, And
from .program import U
from .util.z3py_util import consts
## @file refinement.py
#  Module used to define the operation of refinement between two programs.
# 
#  A program p2 refines a program p1 if :
#  Set_p2 ⊇ Set_p1
#  Pre_p2 ⊇ Pre_p1
#  (Post_p2 / Pre_p1) ⊆ Post_p1

## Creates the operation of refinement between two programs.
#  @param p2 The program that refines p1.
#  @param p1 The program that specifies (or abstracts) p2.
#  @return The Z3 assumption used for refinement.
def is_refinement_of(p2, p1):
	a,b,c,d = consts("a b c d", U)
	return	And(
				ForAll(a, Implies(p1.set(a), p2.set(a))),
				ForAll(b, Implies(p1.pre(b), p2.pre(b))),
				ForAll((c,d), Implies(
					And(p2.post(c,d), p1.pre(c)), p1.post(c,d)
				))
			)

## This is short name for a relation is_refinement_of
#  @param p2 The program that refines p1.
#  @param p1 The program that specifies (or abstracts) p2.
#  @return The Z3 assumption used for refinement.
def is_ref_of(p2, p1):
	return is_refinement_of(p2, p1)