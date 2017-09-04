# encoding: utf-8
from z3 import ForAll, Exists, Implies, And, Not, Function
from .program import U, pre_, post_
from .util.z3py_util import const, consts
## @file feasibility.py
#  Module used to define the condition of feasibility on a program.
# 
#  A program is feasible if all the elements of its precondition are included in the left side of its postcondition.

## Creates the assumption of feasibility on a program.
#  @param p The program that needs to be feasible.
#  @param strong Let it be True if you need pre_p = dom(post_p) assumption.
#  @return The assumption.
def is_feasible(p, strong=False):
	x,y = consts('x y', U)
	if strong:
		return ForAll(x, p.pre(x) == Exists(y, p.post(x,y)))
	else:
		return ForAll(x, Implies(
			p.pre(x), 
			Exists(y, p.post(x,y))
		))

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
def infeasible(p, strong=False):
	return Not(feasible(p, strong))


def skolemized_feasible(p):
	x = const('x', U)
	f = Function('f', U, U)
	return	ForAll(x, Implies(
				pre_(p)[x], 
				post_(p)[x][f(x)]
			))