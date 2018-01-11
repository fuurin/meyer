from .util.z3py_set import Empty, Universe
from .util.z3py_rel import Empty as RelEmpty, Universe as RelUniverse

def And(s1, s2):
	return s1 & s2

def Or(s1, s2):
	return s1 | s2

def Not(s):
	return -s

def Implies(s1, s2):
	return s1 <= s2

def true():
	return Universe()

def false():
	return Empty()

def havoc():
	return RelUniverse()

def fail():
	return RelEmpty()