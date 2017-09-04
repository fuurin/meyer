# encoding: utf-8
from abc import ABCMeta, abstractmethod
from z3 import Datatype, BoolVal
from z3 import EnumSort, BoolSort, IntSort, RealSort, ArraySort
from z3 import ForAll, And, Not, Implies
from z3 import sat
from .util.z3py_set import show_set
from .util.z3py_util import const, consts, show_record_element
from .util.z3py_util import evaluate, proof as super_proof
 
## @file program.py
#  This module can be used to define and create programs according to meyer's definition.
#
#  It defines the new Datatype called Prog, that is composed of a set, a precondition and a postcondition, and operations that can be useful when working with those programs.

U, (A, B, C) = EnumSort('U', ('A', 'B', 'C')) # U has 3 elements
# U, UALL = EnumSort('U', ['U'+str(n) for n in range(0,100)])
# U = IntSort()
# U = RealSort()

SET = ArraySort(U, BoolSort())
# OOPSet = ArraySort(IntSort(), ArraySort(U, BoolSort()))
PRE = ArraySort(U, BoolSort())
POST = ArraySort(U, ArraySort(U, BoolSort()))

PROG = Datatype('Prog')
PROG.declare('mk_prog', ('set', SET), ('pre', PRE), ('post', POST))
PROG = PROG.create()
set_ = PROG.set
pre_ = PROG.pre
post_ = PROG.post

class ProgramBase():
	"""Abstract Base Class for program instance."""
	__metaclass__ = ABCMeta

	#  @param x An element that is included in Set of this program.
	#  @return The constraint that x is included in Set of this program.
	@abstractmethod
	def set(self, x):
		pass
	
	#  @param x An element that is included in Pre of this program.
	#  @return The constraint that x is included in Set of this program.
	@abstractmethod
	def pre(self, x):
		pass

	#  @param x An element that is included in post of this program.
	#  @return The constraint that x is included in Set of this program.
	@abstractmethod
	def post(self, x, y):
		pass

class Program(ProgramBase):
	__metaclass__ = ABCMeta

	"""Base class for Program instance."""
	#  @param p A program instance created by Z3.py.
	def __init__(self, p):
		self.p = p

	#  @return A program instance created by Z3.py.
	def z3(self):
		return self.p

	#  @param x An element that is included in Set of this program.
	#  @return The constraint that x is included in Set of this program.
	def set(self, x):
		return set_(self.p)[x]
	
	#  @param x An element that is included in Pre of this program.
	#  @return The constraint that x is included in Set of this program.
	def pre(self, x):
		return pre_(self.p)[x]
	
	#  @param x An element that is included in post of this program.
	#  @param y An element that is included in the range of this program.
	#  @return The constraint that x is included in Set of this program.
	def post(self, x, y):
		return post_(self.p)[x][y]
	
## Use prog/progs _constraint to Prog constants.
#  @param prog The prog that needs constraints.
#  @return The constraints linked to a program.
def prog_constraint(prog):
	x,y = consts('x y', U)
	return 	ForAll([x,y], And(
				Implies(pre_(prog)[x], set_(prog)[x]),
				Implies(
					post_(prog)[x][y], 
					And(set_(prog)[x], set_(prog)[y])
				)
			))

## Maps the constraints of progs to the progs.
#  @param progs A list of progs that is used.
#  @return The Z3 And condition that maps constraints and progs.
def progs_constraint(*progs):
	return And([progs_constraint(p) for p in progs])

## Creates a new program, adding the constraints to the solver.
#  @param solver The solver in which the programwill be added.
#  @param name The name of the created program.
#  @return The program instance created.
def prog(solver, name):
	p = const(name, PROG)
	solver.add(prog_constraint(p))
	return Program(p)

## Creates multiple new programs, adding the constraints to the solver.
#  @param solver The solver in which the program will be added.
#  @param names The names of the created programs, separated by space character.
#  @return The map of the program instances created.
def progs(solver, names):
	return [prog(solver, name) for name in names.split(' ')]

## Prints a program
#  @param solver The solver in which the program is.
#  @param prog The program that needs to be printed.
def show_prog(solver, prog):
	if isinstance(prog, ProgramBase):
		show_record_element(solver, prog.z3(), set_)
		show_record_element(solver, prog.z3(), pre_)
		show_record_element(solver, prog.z3(), post_)
	else:
		show_record_element(solver, prog, set_)
		show_record_element(solver, prog, pre_)
		show_record_element(solver, prog, post_)

## Returns a string which contains informations about the universe used.
#  @return The string which contains the universe.
def universe_state():
	if hasattr(U, 'num_constructors'):
		num = str(U.num_constructors())
		return 'Universe = U, has ' + num + ' element(s)'
	return 'Universe = ' + str(U)
	
## Starts the proof of a theorem thanks to its solver
#  @param solver The solver which contains all the assuptions.
#  @param title The title of the theorem.
#  @param reset Boolean that indicates if the solver will be reset after the proof, true is reset.
#  @return The result (sat, unsat or unknown) of the proof.
def proof(solver, title=None, reset=True):
	if title != None:
		title = title + '\n' + universe_state()
	else:
		title = universe_state()
	result = super_proof(solver, title, False)
	if result == sat:
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
def conclude(solver, conclusion, title=None, reset=True):
	solver.add(Not(conclusion))
	# import pdb; pdb.set_trace()
	proof(solver, title, reset)