# encoding: utf-8
from z3 import And
from .feasibility import feasible
from .refinement import is_ref_of
## @file implementation.py
#  Module used to define the operation of implementation between two programs.
# 
#  A program p' is an implementation of p if p' refines p and if p' is feasible.

## Creates the operation of implementation between two programs.
#  @param p1 The program that is the implementation of p2.
#  @param p2 The program which is a contract of is p1.
#  @return The Z3 assumptions of the implementation operation.
def is_implementation_of(p1, p2):
	return And(feasible(p1), is_ref_of(p1,p2))

## This is short name for a relation is_implementation_of
#  @param p1 The program that is the implementation of p2.
#  @param p2 The program which is a contract of is p1.
#  @return The Z3 assumptions of the implementation operation.
def is_impl_of(p1, p2):
	return is_implementation_of(p1, p2)

## Creates the operation of contract (inverse implementation) between two programs.
#  @param p1 The program that is the contract of p2.
#  @param p2 The program which is an implementation of p1.
#  @return The Z3 assumptions of the contract operation.
def is_contract_of(p1, p2):
	return And(feasible(p2), is_ref_of(p2,p1))

## This is short name for a relation is_contract_of
#  @param p1 The program that is the contract of p2.
#  @param p2 The program which is an implementation of p1.
#  @return The Z3 assumptions of the contract operation.
def is_ctrt_of(p1, p2):
	return is_contract_of(p1, p2)