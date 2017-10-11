# encoding: utf-8
from z3 import And, Not

## @file feasibility.py
#  Module used to define the condition of feasibility on a program.
# 
#  A program is feasible if all the elements of its precondition are included in the left side of its postcondition.

## Creates the assumption of feasibility on a program.
#  @param p The program that needs to be feasible.
#  @param strong Let it be True if you need pre_p = dom(post_p) assumption.
#  @return The assumption.
def is_feasible(p, strong=False):
	if strong:
		return p.pre() == p.dom_post()
	else:
		return p.pre() <= p.dom_post()

def feasible(*progs, strong=False):
	if len(progs) == 0:
		raise Exception("feasible is receiving nothing.")
	if len(progs) == 1:
		return is_feasible(progs[0])
	return [is_feasible(p, strong) for p in list(progs)]

## Creates the assumption of infeasibility on a program.
#  @param p The program that needs to be infeasible.
#  @param strong Let it be True if you need pre_p != dom(post_p) assumption.
#  @return The assumption.
def infeasible(*progs, strong=False):
	if len(progs) == 0:
		raise Exception("feasible is receiving nothing.")
	if len(progs) == 1:
		return Not(is_feasible(progs[0]))
	return [Not(is_feasible(p, strong)) for p in list(progs)]