# encoding: utf-8
from z3 import Solver, Not
from meyer.util.color import yellow
from meyer.util.z3py_set import set
from meyer.util.z3py_util import const
from meyer.program import U, prog, progs, conclude
from meyer.feasibility import feasible
from meyer.equivalence import eq
from meyer.refinement import is_ref_of
from meyer.implementation import is_impl_of
from meyer.basic_constructs import Choi, Comp, Rest

s = Solver()

def P4():
	print(yellow("P4: Refinement is a preorder\nAnd it's an order relation when equal is equivalent."))

	title = "reflexive"
	p = prog(s, 'p')
	conclude(s, is_ref_of(p, p), title)
	
	title = "antisymmetric"
	p1, p2 = progs(s, 'p1 p2')
	s.add(is_ref_of(p1, p2), is_ref_of(p2, p1))
	conclude(s, eq(p1, p2), title)
	
	title = "transitive"
	p1, p2, p3 = progs(s, 'p1 p2 p3')
	s.add(feasible([p1,p2,p3]))
	s.add(is_ref_of(p1, p2), is_ref_of(p2, p3))
	conclude(s, is_ref_of(p1, p3), title)

def P5():
	title = "P5: A specification/program having an implementation is feasible"
	p1, p2 = progs(s, 'p1 p2')
	s.add(is_impl_of(p1, p2))
	conclude(s, feasible(p1), title)

def P6_choice():
	title = "P6(Choice): If p1 and p2 are feasible, p1 ∪ p2 is feasible."
	p1, p2 = progs(s, 'p1 p2')
	s.add(feasible(p1), feasible(p2))
	conclude(s, feasible(Choi(p1, p2)), title)

def P6_composition():
	title = "P6(Composition): If p1 and p2 are feasible, p1;p2 is feasible."
	p1, p2 = progs(s, 'p1 p2')
	s.add(feasible(p1), feasible(p2))
	conclude(s, feasible(Comp(p1, p2)), title)

def P6_restriction():
	title = "P6(Restriction): If p is feasible, C:p is feasible."
	p = prog(s, 'p')
	c = set('c', U)
	s.add(feasible(p))
	conclude(s, feasible(Rest(c, p)), title)

P4()
P5()
P6_choice()
P6_composition()
P6_restriction() # Definition error: Pre_(C:p) must be Pre_p ∩ C