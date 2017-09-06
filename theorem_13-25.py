# encoding: utf-8
from z3 import Solver, ForAll, Implies, And
from meyer.util.z3py_util import const
from meyer.util.z3py_set import set, sets, Inter, included
from meyer.program import U, prog, progs, conclude
from meyer.feasibility import feasible
from meyer.equivalence import eq, eq_set, eq_pre, eq_post
from meyer.basic_constructs import Choi, Comp, Rest, RestPre
from meyer.special_programs import Fail, Havoc, Skip, total, havoc
from meyer.refinement import is_ref_of

s = Solver()

def P13():
	title1 = "P13 (p ; Skip) = p"
	p = prog(s, 'p')
	s.add(feasible(p)) # Additional assumption
	conclude(s, eq(Comp(p, Skip()), p), title1)
	
	title2 = "P13 (Skip ; p) = p"
	p = prog(s, 'p')
	conclude(s, eq(Comp(Skip(), p), p), title2)

def P14():
	title1 = "P14 (p ∪ Fail) = p"
	p = prog(s, 'p')
	conclude(s, eq(Choi(p, Fail()), p), title1)

	title2 = "P14 (Fail ∪ p) = p"
	p = prog(s, 'p')
	conclude(s, eq(Choi(Fail(), p), p), title2)
	

def P15():
	title1 = "P15 (p ; Fail) = Fail"
	p = prog(s, 'p')
	conclude(s, eq(Comp(p, Fail()), Fail()), title1)
	
	title2 = "P15 (Fail ; p) = Fail"
	p = prog(s, 'p')
	conclude(s, eq(Comp(Fail(), p), Fail()), title2)

def P16():
	title1 = "P16 (p ∪ Havoc) = Havoc"
	p = prog(s, 'p')
	conclude(s, eq(Choi(p, Havoc()), Havoc()), title1)

	title2 = "P16 (Havoc ∪ p) = Havoc"
	p = prog(s, 'p')
	conclude(s, eq(Choi(Havoc(), p), Havoc()), title2)

def P17():
	title = "P17 (p ; Havoc) = (Pre_p: Havoc)"
	p = prog(s, 'p')
	lhs = Comp(p, Havoc())
	rhs = RestPre(p, Havoc())
	s.add(feasible(p)) # Additional assumption
	conclude(s, eq(lhs, rhs), title)	

def P18():
	title = "P18 p ⊆ (C: p)"
	p = prog(s, 'p')
	c = set('c', U)
	conclude(s, is_ref_of(p, Rest(c, p)), title)

def P19():
	title = "P19 If D ⊆ C, then (C:p) ⊆ (D:p)"
	p = prog(s, 'p')
	c, d = sets('c d', U)
	s.add(included(d, c))
	conclude(s, is_ref_of(Rest(c, p), Rest(d, p)), title)

def P20():
	title = "P20 If q ⊆ p, then (C:q) ⊆ (C:p)"
	p, q = progs(s, 'p q')
	c = set('c', U)
	s.add(is_ref_of(q, p))
	conclude(s, is_ref_of(Rest(c,q), Rest(c,p)), title)

def P21_Choi():
	title = "P21 If q1 ⊆ p1 and q2 ⊆ p2, then (q1 ∪ q2) ⊆ (p1 ∪ p2)"
	p1, p2, q1, q2 = progs(s, 'p1 p2 q1 q2')
	# s.add(eq_pre(p1, p2)) # Additional assumption
	# s.add([feasible(p) for p in [p1,p2,q1,q1]]) # Additional assumption
	s.add(is_ref_of(q1, p1), is_ref_of(q2, p2))
	conclude(s, is_ref_of(Choi(q1, q2), Choi(p1, p2)), title)

def P21_Comp():
	title = "P21 If q1 ⊆ p1 and q2 ⊆ p2, then (q1 ; q2) ⊆ (p1 ; p2)"
	p1, p2, q1, q2 = progs(s, 'p1 p2 q1 q2')
	# s.add(eq_pre(q1, q2))
	# s.add([feasible(p, True) for p in [p1,p2,q1,q1]])
	s.add(is_ref_of(q1, p1), is_ref_of(q2, p2))
	conclude(s, is_ref_of(Comp(q1, q2), Comp(p1, p2)), title)
	
def P22():
	title = "P22 p ⊆ (Pre_p: Havoc) for any p"
	p = prog(s, 'p')
	h = havoc(s)
	c = set('c', U)
	# s.add(eq_set(p, h)) # Additional assumption
	conclude(s, is_ref_of(p, RestPre(p, h)), title)

def P23():
	title = "P23 p ⊆ Havoc for any total p"
	p = total(s)
	conclude(s, is_ref_of(p, Havoc()), title)

def P24():
	# if and only if => if, so title1 is ignored.
	title1 = "P24 If p ⊆ Fail then p = Fail"
	p = prog(s, 'p')
	s.add(feasible(p))
	s.add(is_ref_of(p, Fail()))
	conclude(s, eq(p, Fail()), title1)
	
	title2 = "P24 If p = Fail then p ⊆ Fail"
	p = prog(s, 'p')
	s.add(eq(p, Fail()))
	conclude(s, is_ref_of(p, Fail()), title2)

def P25():
	title1 = "P25 If Fail ⊆ p then p = Fail"
	p = prog(s, 'p')
	f = Fail()
	s.add(is_ref_of(f, p))
	conclude(s, eq(p, f), title1)

	title2 = "P25 If p = Fail then Fail ⊆ p"
	p = prog(s, 'p')
	f = Fail()
	s.add(eq(p, f))
	# s.add(eq_set(p, f)) # Additional assumption
	conclude(s, is_ref_of(f, p), title2)

P13() # p must be feasible for (p ; Skip) = p
P14()
P15()
P16()
P17() #counter example, p must be feasible
P18() 
P19()
P20()
P21_Choi() #unknown, feasible:counter example, pre_p1, pre_p2 must be same.
P21_Comp() #unknown, feasible:counter example
P22() # unknown, must be Set_p = Set_havoc
P23()
P24() # unknown, only one way is accepted.
P25() # counter example, Set_p = Set_Fail is needed.