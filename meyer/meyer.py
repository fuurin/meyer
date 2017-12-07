# encoding: utf-8
from z3 import EnumSort, IntSort, RealSort, Not, sat
from .util.z3py_set import set_sort as set_set_sort, show_set
from .util.z3py_rel import set_sort as set_rel_sort
from .util.z3py_util import proof as super_proof, evaluate, show_record_element
 
## @file meyer.py
#  This module can be used for basics of meyer's definition.
#
#

U, (A, B, C) = EnumSort('U', ('A', 'B', 'C')) # U has 3 elements
# U, UALL = EnumSort('U', ['U'+str(n) for n in range(0,100)])
# U = IntSort()
# U = RealSort()

## Sets universe state u to set module and bin-relation module.
def set_universe_state(u):
	global U
	set_set_sort(u)
	set_rel_sort(u, u)
	U = u

## Returns a string which contains informations about the universe used.
#  @return The string which contains the universe.
def universe_state():
	if hasattr(U, 'num_constructors'):
		num = str(U.num_constructors())
		return 'Universe = U, has ' + num + ' element(s)'
	return 'Universe = ' + str(U)

set_universe_state(U)

## Prints a program
#  @param solver The solver in which the program is.
#  @param prog The program that needs to be printed.
def show_prog(solver, prog):
	from .program import Program, set_, pre_, post_
	if isinstance(prog, Program):
		show_record_element(solver, prog.z3(), set_)
		show_record_element(solver, prog.z3(), pre_)
		show_record_element(solver, prog.z3(), post_)
	else:
		show_record_element(solver, prog, set_)
		show_record_element(solver, prog, pre_)
		show_record_element(solver, prog, post_)
	
## Starts the proof of a theorem thanks to its solver
#  @param solver The solver which contains all the assuptions.
#  @param title The title of the theorem.
#  @param reset Boolean that indicates if the solver will be reset after the proof, true is reset.
#  @return The result (sat, unsat or unknown) of the proof.
def proof(solver, title=None, reset=True, show_solver=False):
	if title != None:
		title = title + '\n' + universe_state()
	else:
		title = universe_state()
	result = super_proof(solver, title, False, show_solver)
	if result == sat:
		from .program import SET, PROG
		is_set = lambda elt: elt.range() == SET
		sets = filter(is_set, solver.model())
		for s in sets:
			show_set(solver, s)
		is_prog = lambda elm: elm.range() == PROG
		progs = filter(is_prog, solver.model())
		for p in progs:
			show_prog(solver, p)
	if reset:
		solver.reset()
	return result

## Proof of the conclusion which will be nagated and added to the solver.
#  @param solver The solver which contains all the premises.
#  @param conclusion The conclusion constraint that you'd like to proof.
#  @param title The title of the theorem.
#  @param reset Boolean that indicates if the solver will be reset after the proof, true is reset.
#  @return The result (sat, unsat or unknown) of the proof.
def conclude(solver, conclusion, title=None, reset=True, show_solver=False):
	solver.add(Not(conclusion))
	# import pdb; pdb.set_trace()
	proof(solver, title, reset, show_solver)