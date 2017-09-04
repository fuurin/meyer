# _*_ coding: utf-8 _*_
from z3 import Solver, ForAll, Exists, Not, And, Or, Implies
from meyer.util.z3py_util import const, consts
from meyer.util.z3py_set import set, sets, included
from meyer.program import U, prog, progs, conclude
from meyer.equivalence import eq, eq_set, eq_pre, eq_post
from meyer.feasibility import feasible
from meyer.basic_constructs import Choi, Comp, Rest, Corest
from meyer.refinement import is_ref_of
from meyer.special_programs import Fail, Havoc, Skip, total

s = Solver()

def P26():
	# set is not same, but they're equivalence.
	title = "P26 (p \ C) = (p; (C: Skip))"
	p = prog(s, 'p')
	C = set('C', U)
	lhs = Corest(p, C)
	rhs = Comp(p, Rest(C, Skip()))
	conclude(s, eq(lhs, rhs), title)


def P27():
	title = "P27 (p1 ∪ p2) \ C = (p1 \ C) ∪ (p2 \ C)"
	p1, p2 = progs(s, 'p1 p2')
	C = set('C', U)
	s.add(eq_pre(p1, p2)) # Additional assumption
	lhs = Corest(Choi(p1, p2), C)
	rhs = Choi(Corest(p1, C), Corest(p2, C))
	conclude(s, eq(lhs, rhs), title)


def P28():
	title = "P28 (p1 ; p2) \ C = p1 ; (p2 \ C)"
	p1, p2 = progs(s, 'p1 p2')
	C = set('C', U)
	lhs = Corest(Comp(p1, p2), C)
	rhs = Comp(p1, Corest(p2, C))
	conclude(s, eq(lhs, rhs), title)

def P29():
	title = "P29 (p \ C) ⊆ p but (p \ C) ⊆ C"
	p = prog(s, 'p')
	C = set('C', U)
	# Additional assumption
	x, y = consts('x y', U)
	s.add(ForAll(x, Implies(p.pre(x), Exists(y, And(p.post(x,y), C.has(y))))))
	conclude(s, is_ref_of(Corest(p, C), p), title)

def P30():
	title = "P30 If D ⊆ C then (p \ D) ⊆ (p \ C)"
	p = prog(s, 'p')
	D, C = sets('D C', U)
	s.add(included(D, C))
	# Additional assumption
	x, y, z = consts('x y z', U)
	s.add(ForAll(x, Implies(
		p.pre(x), 
		And(
			Exists(y, And(p.post(x,y), C.has(y))),
			Exists(z, And(p.post(x,z), D.has(z)))
		)
	)))
	conclude(s, is_ref_of(Corest(p, D), Corest(p, C)), title)

P26()
P27() # pre_p1 == pre_p2 is needed
P28()
P29() # Pre_p ⊆ inv(post_p, C) is needed
P30() # Pre_p ⊆ inv(post_p, C) ∪ inv(post_p, D) is needed
# P31 is same as P21 as of now.