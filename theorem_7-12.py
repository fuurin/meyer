# encoding: utf-8
from z3 import Solver, ForAll
from meyer.util.z3py_util import const
from meyer.util.z3py_set import set, sets, Inter
from meyer.program import U, prog, progs, conclude
from meyer.feasibility import feasible
from meyer.equivalence import eq, eq_pre, eq_post, eq_feasible_post
from meyer.basic_constructs import Choi, Comp, Rest

s = Solver()

def P7():
	title = "P7 c1:(c2:p) = c2:(c1:p)"
	c1, c2 = sets('c1 c2', U)
	p = prog(s, 'p')
	lhs = Rest(c2, Rest(c1, p))
	rhs = Rest(c1, Rest(c2, p))
	conclude(s, eq(lhs, rhs), title)

def P8():
	title = "P8 c1:(c2:p) = (c1∩c2):p"
	c1, c2 = sets('c1 c2', U)
	p = prog(s, 'p')
	lhs = Rest(c1, Rest(c2, p))
	rhs = Rest(Inter(c1, c2), p)
	conclude(s, eq(lhs, rhs), title)

def P9():
	title = "P9 c:(p1∪p2) = (c:p1)∪(c:p2)"
	c = set('c', U)
	p1, p2 = progs(s, 'p1 p2')
	lhs = Rest(c, Choi(p1, p2))
	rhs = Choi(Rest(c, p1), Rest(c, p2))
	conclude(s, eq(lhs, rhs), title)

def P10():
	title = "P10 c:(p1;p2) = (c:p1);p2"
	c = set('c', U)
	p1, p2 = progs(s, 'p1 p2')
	lhs = Rest(c, Comp(p1, p2))
	rhs = Comp(Rest(c, p1), p2)
	conclude(s, eq(lhs, rhs), title)

def P11():
	title = "P11 q;(p1∪p2) = (q;p1)∪(q;p2)"
	q, p1, p2 = progs(s, 'q p1 p2')
	lhs = Comp(q, Choi(p1, p2))
	rhs = Choi(Comp(q, p1), Comp(q, p2))
	s.add(feasible([q, p1, p2], True)) # Additional assumption
	conclude(s, eq(lhs, rhs), title)

def P12():
	title = "P12 (p1∪p2);q = (p1;q)∪(p2;q)"
	q, p1, p2 = progs(s, 'q p1 p2')
	lhs = Comp(Choi(p1, p2), q)
	rhs = Choi(Comp(p1, q), Comp(p2, q))
	s.add(feasible([q, p1, p2], True)) # Additional assumption
	conclude(s, eq(lhs, rhs), title)
	
P7()
P8()
P9()
P10()
P11() # All programs must be strongly feasible.
P12() # All programs must be strongly feasible.