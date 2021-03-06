# encoding: utf-8
from z3 import And

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
	return And(
		p2.set() >= p1.set(),
		p2.pre() >= p1.pre(),
		p2.post() / p1.pre() <= p1.post()
	)

## This is short name for a relation is_refinement_of
#  @param p2 The program that refines p1.
#  @param p1 The program that specifies (or abstracts) p2.
#  @return The Z3 assumption used for refinement.
def is_ref_of(p2, p1):
	return is_refinement_of(p2, p1)

## Creates the operation of abstract between two programs.
#  @param p1 The program that specifies (or abstracts) p2.
#  @param p2 The program that refines p1.
#  @return The Z3 assumption used for abstract.
def is_abstract_of(p1, p2):
	return And(
		p2.set() >= p1.set(),
		p2.pre() >= p1.pre(),
		p2.post() / p1.pre() <= p1.post()
	)

## This is short name for a relation is_abstract_of
#  @param p1 The program that specifies (or abstracts) p2.
#  @param p2 The program that refines p1.
#  @return The Z3 assumption used for abstract.
def is_abs_of(p1, p2):
	return is_abstract_of(p1, p2)