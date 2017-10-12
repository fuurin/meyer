# encoding: utf-8
from z3 import ForAll, Exists, Not
from .meyer import U
from .util.z3py_util import const, consts

def trivial(s, post):
	s1 = const('s1', U)
	return ForAll(s1, post(s, s1))

def irrelevant(s, post):
	s1, s2 = consts('s1 s2', U)
	return ForAll([s1, s2], post(s, s1) == post(s, s2))

def relevant(s, post):
	s1, s2 = consts('s1 s2', U)
	return Exists([s1, s2], Not(post(s, s1) == post(s, s2)))