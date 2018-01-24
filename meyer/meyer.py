# encoding: utf-8
from z3 import Not, sat
from .util.z3py_util import proof as util_proof, U
from .util.z3py_set import show_set_models
from .program import show_prog_models

## Proof of the conclusion which will be nagated and added to the solver.
#  @param solver The solver which contains all the premises.
#  @param conclusion The conclusion constraint that you'd like to proof.
#  @param title The title of the theorem.
#  @param reset Boolean that indicates if the solver will be reset after the proof, true is reset.
#  @return The result (sat, unsat or unknown) of the proof.
def conclude(solver, conclusion, title=None, reset=True, show_solver=False):
	solver.add(Not(conclusion))
	result = util_proof(solver, title=title, reset=False, show_solver=show_solver, show_model=False)
	if result == sat:
		show_set_models(solver)
		show_prog_models(solver)
	if reset:
		solver.reset()
	# return result