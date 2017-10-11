# encoding: utf-8
from z3 import ForAll
from .program import U, prog, Program
from .util.z3py_set import Universe

## @file special_program.py
#  Module used to define special programs according to meyer's article.
#  
#  

# Each classes are equivalence to restricted special program instances.
# However, one way may cause unknown. Then try another way.

class Fail(Program):
	def __init__(self):
		pass

	def _set(self, x):
		return False

	def _pre(self, x):
		return False

	def _post(self, x, y):
		return False

class Havoc(Program):
	def __init__(self):
		pass

	def _set(self, x):
		return True

	def _pre(self, x):
		return True

	def _post(self, x, y):
		return True

class Skip(Program):
	def __init__(self):
		pass

	def _set(self, x):
		return True

	def _pre(self, x):
		return True

	def _post(self, x, y):
		return x == y

def total(solver):
	p = prog(solver, 'total')
	solver.add(p.pre() == Universe())
	return p

def is_total(p):
	return p.pre() == Universe()