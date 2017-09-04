from .util.z3py_set import Inter, Union, Cpl, included, Empty, Universe
from .program import U

def And(s1, s2):
	return Inter(s1, s2)

def Or(s1, s2):
	return Union(s1, s2)

def Not(s):
	return Cpl(s)

def Implies(s1, s2):
	return included(s1, s2)

def true():
	return Universe(U)

def false():
	return Empty(U)