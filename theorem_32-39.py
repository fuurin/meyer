# encoding: utf-8
from z3 import Solver, ForAll, Exists, Not, And, Or, Implies
from meyer.util.z3py_util import const, consts
from meyer.util.z3py_set import set, sets
from meyer.program import U, conclude, prog, progs
from meyer.equivalence import eq
from meyer.feasibility import feasible
from meyer.refinement import is_ref_of
from meyer.basic_constructs import Choi, Comp, Rest, Corest
from meyer.concurrency import Atom
from meyer.commute import commute

s = Solver()

def P32_commutative():
	title = "P32 Atomic concurrency “||” is commutative. -> (p1 || p2) = (p2 || p1)"
	p1, p2 = progs(s, 'p1 p2')
	conclude(s, eq(Atom(p1, p2), Atom(p2, p1)), title)

def P32_associative():
	title = "P32 Atomic concurrency “||” is associative. (p1 || p2) || p3 = p1 || (p2 || p3)"
	p1, p2, p3 = progs(s, 'p1 p2 p3')
	s.add(feasible(p1,p2,p3))
	lhs = Atom(Atom(p1, p2), p3)
	rhs = Atom(p1, Atom(p2, p3))
	conclude(s, eq(lhs, rhs), title)

def P32_refinement_safe():
	title = "P32 Atomic concurrency “||” is refinement-safe. -> if q1 ⊆ p1 and q2 ⊆ p2, then (q1 || q2) ⊆ (p1 || p2)"
	q1, q2, p1, p2 = progs(s, 'q1 q2 p1 p2')
	s.add(is_ref_of(q1, p1), is_ref_of(q2, p2))
	conclude(s, is_ref_of(Atom(q1, q2), Atom(p1, p2)), title)

def P33():
	title = "P33 p1 || (p2 ∪ p3) = (p1 || p2) ∪ (p1 || p3)"
	p1, p2, p3 = progs(s, 'p1 p2 p3')
	s.add(feasible(p1,p2,p3))
	lhs = Atom(p1, Choi(p2, p3))
	rhs = Choi(Atom(p1, p2), Atom(p2, p3))
	conclude(s, eq(lhs, rhs), title)

def P34():
	title = "P34 (p1 ∪ p2) || p3 = (p1 || p3) ∪ (p2 || p3)"
	p1, p2, p3 = progs(s, 'p1 p2 p3')
	lhs = Atom(Choi(p1, p2), p3)
	rhs = Choi(Atom(p1, p3), Atom(p2, p3))
	conclude(s, eq(lhs, rhs), title)

def P35():
	title = "P35 C: (p1 || p2) = (C: p1) || (C: p2)"
	p1, p2 = progs(s, 'p1 p2')
	C = set('C', U)
	lhs = Rest(C, Atom(p1, p2))
	rhs = Atom(Rest(C, p1), Rest(C, p2))
	conclude(s, eq(lhs, rhs), title)

def P36():
	title = "P36 (p1 || p2) \ C = (p1 \ C) || (p2 \ C)"
	p1, p2 = progs(s, 'p1 p2')
	C = set('C', U)
	lhs = Corest(Atom(p1, p2), C)
	rhs = Atom(Corest(p1, C), Corest(p2, C))
	conclude(s, eq(lhs, rhs), title)

def P37():
	title = "P37 (p1 ; p2) ⊆ (p1 || p2)"
	p1, p2 = progs(s, 'p1 p2')
	conclude(s, is_ref_of(Comp(p1, p2), Atom(p1, p2)), title)

def P38():
	title = "P38 (p2 ; p1) ⊆ (p1 || p2)"
	p1, p2 = progs(s, 'p1 p2')
	conclude(s, is_ref_of(Comp(p1, p2), Atom(p1, p2)), title)

def P39():
	title = "P39 If p1 and p2 commute, then (p1 || p2) = (p1 ; p2)."
	p1, p2 = progs(s, 'p1 p2')
	s.add(commute(p1, p2))
	conclude(s, eq(Atom(p1, p2), Comp(p1, p2)), title)

P32_commutative()
P32_associative() # counter example when feasible
P32_refinement_safe() # counter example
P33() # counter example when feasible
P34() # counter example
P35() # counter example
P36() # counter example
P37() # counter example
P38() # counter example
P39()