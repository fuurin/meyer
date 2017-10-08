# encoding: utf-8
from z3 import And
from .util.z3py_rel import Rest, eq as eq_r
from .util.z3py_set import eq as eq_s

## @file equivalence.py
#  Module used to define the condition of equivalence between two programs.
# 
#  Two programs are equivalent if their preconditions and their postconditions are the same.

## Creates the assumption of equivalence between two programs.
#  @param p1 The first program.
#  @param p2 The second program.
#  @return The assumption of equivalence between two programs.
def equivalent(p1, p2):
	return And(eq_pre(p1, p2), eq_actual_post(p1, p2))
def equal(p1, p2):
	return And(eq_set(p1, p2), eq_pre(p1, p2), eq_post(p1, p2))

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
	return eq_s(p1.set, p2.set)

## Creates the assumption of equality between two preconditions of programs.
#  @param p1 The first program.
#  @param p2 The second program.
#  @return The assumption of equality between two preconditions of programs.
def eq_pre(p1, p2):
	return eq_s(p1.pre, p2.pre)

## Creates the assumption of equality between two postconditions of programs.
#  @param p1 The first program.
#  @param p2 The second program.
#  @return The assumption of equality between two postSconditions of programs.
def eq_post(p1, p2):
	return eq_r(p1.post, p2.post)

## Creates the assumption of equality between two ranges of postconditions of programs.
#  @param p1 The first program.
#  @param p2 The second program.
#  @return The assumption of equality between two ranges of postconditions of programs.
def eq_ran(p1, p2):
	return eq_s(p1.ran, p2.ran)

## Creates the assumption of equality between two postconditions of actual program I/O.
#  @param p1 The first program.
#  @param p2 The second program.
#  @return The assumption of equality between two postSconditions of feasible programs.
def eq_actual_post(p1, p2):
	return Rest(p1.post, p1.pre) == Rest(p2.post, p2.pre)