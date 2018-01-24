# encoding: utf-8
from z3 import Datatype, BoolSort, IntSort, ArraySort, And, Not
from .meyer import U
from .util.z3py_set import Set
from .util.z3py_rel import Rel
from .util.z3py_util import const, consts, show_record_element


## @file program.py
#  This module can be used for definition of specification/program instance
#
#

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

class Program():
	"""Base class for Program instance."""
	#  @param p A program instance created by Z3.py.
	def __init__(self, p):
		self.p = p

	#  @param x An element that is included in Set of this program.
	#  @return The constraint that x is included in Set of this program.
	def set(self, x=None):
		return Set(self._set) if x is None else self._set(x)

	def _set(self, x):
		return set_(self.p)[x]

	#  @param x An element that is included in Pre of this program.
	#  @return The constraint that x is included in Pre of this program.
	def pre(self, x=None):
		return Set(self._pre) if x is None else self._pre(x) 

	def _pre(self, x):
		return pre_(self.p)[x]
	
	#  @param x An element that is included in post of this program.
	#  @param y An element that is included in the range of this program.
	#  @return The constraint that x is included in Set of this program.
	def post(self, x=None, y=None):
		return Rel(self._post) if x is None and y is None else self._post(x, y) 

	def _post(self, x, y):
		return post_(self.p)[x][y]

	#  @param x An element that is included in the domain of this program.
	#  @return The constraint that x is included in the domain of this program.
	def dom(self, x=None):
		return self.pre(x)

	#  @param y An element that is included in the range of this program.
	#  @return The constraint that x is included in the range of this program.
	def ran(self, y=None):
		return Set(self._ran) if y is None else self._ran(y) 
		
	def _ran(self, y):
		return (self.post() >> self.dom())(y)
		
	#  @param x An element that is included in the domain of post of this program.
	#  @return The constraint that x is included in the domain of post of this program.
	def dom_post(self, x=None):
		return Set(self._dom_post) if x is None else self._dom_post(x) 

	def _dom_post(self, x):
		y = const('y', U)
		return self.post().dom(x)

	#  @param y An element that is included in the range of post of this program.
	#  @return The constraint that x is included in the range of post of this program.
	def ran_post(self, y=None):
		return Set(self._ran_post) if y is None else self._ran_post(y) 
	
	def _ran_post(self, y):
		return self.post().ran(y)

	def __pos__(self):
		from .feasibility import feasible
		return feasible(self)

	def __invert__(self):
		from .feasibility import feasible
		return feasible(self, strong=True)		

	def __truediv__(self, C):
		from .basic_constructs import Restriction
		return Restriction(C, self)

	def __floordiv__(self, C):
		from .basic_constructs import Corestriction
		return Corestriction(self, C)

	def __and__(self, p):
		from .concurrency import AtomicConcurrency
		return AtomicConcurrency(self, p)

	def __or__(self, p):
		from .basic_constructs import Choice
		return Choice(self, p)

	def __xor__(self, p):
		from .basic_constructs import Composition, SoftComposition
		# return SoftComposition(self, p)
		return Composition(self, p)

	def __lt__(self, p):
		from .implementation import is_implementation_of
		return is_implementation_of(self, p)

	def __gt__(self, p):
		from .implementation import is_contract_of
		return is_contract_of(self, p)

	def __le__(self, p):
		from .refinement import is_refinement_of
		return is_refinement_of(self, p)

	def __ge__(self, p):
		from .refinement import is_abstract_of
		return is_abstract_of(self, p)
	
	def __eq__(self, p):
		from .equivalence import equivalent
		return equivalent(self, p)

	def __ne__(self, p):
		return Not(self.__eq__(p))

## Use prog/progs _constraint to Prog constants.
#  @param prog The prog that needs constraints.
#  @return The constraints linked to a program.
def prog_constraint(p):
	return And(p.pre() <= p.set(), p.post() <= p.set() ^ p.set())
	"""
	from z3 import ForAll, And, Implies
	x, y, z = consts('x y z', U)
	return ForAll([x, y], And(
		Implies(p.pre(x), p.set(x)),
		Implies(p.post(z, y), And(p.set(z), p.set(y))),
	))
	"""

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
	p = Program(const(name, PROG))
	solver.add(prog_constraint(p))
	return p

## Creates multiple new programs, adding the constraints to the solver.
#  @param solver The solver in which the program will be added.
#  @param names The names of the created programs, separated by space character.
#  @return The map of the program instances created.
def progs(solver, names):
	ps = [prog(solver, name) for name in names.split(' ')]
	return ps[0] if len(ps) == 1 else ps

## Prints a program
#  @param solver The solver in which the program is.
#  @param prog The program that needs to be printed.
def show_prog(solver, prog):
	if isinstance(prog, Program):
		show_record_element(solver, prog.z3(), set_)
		show_record_element(solver, prog.z3(), pre_)
		show_record_element(solver, prog.z3(), post_)
	else:
		show_record_element(solver, prog, set_)
		show_record_element(solver, prog, pre_)
		show_record_element(solver, prog, post_)

def show_progs(solver, *progs):
	for p in progs: show_prog(solver, p)

def show_prog_models(solver):
	is_prog = lambda elt: elt.range() == PROG
	progs = list(filter(is_prog, solver.model()))
	show_progs(solver, *progs)