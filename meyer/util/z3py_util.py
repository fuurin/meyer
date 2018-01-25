# encoding: utf-8
from .color import red, cyan, yellow
from z3 import IntSort, EnumSort, Not
from z3 import Const, Consts, Function, is_ast, is_bool, is_as_array
from z3 import simplify, get_as_array_func
from z3 import sat, unsat, unknown
## @file z3py_util.py
#  This module is used to construct special variables that are needed in theorem proving.
#
#  This module attributes an ID to each element used in the proof of a theorem. It also allows the construction of consts, functions and permits to print them.

# U = IntSort()
U, (A, B, C) = EnumSort('U', ('A', 'B', 'C'))
# U, UALL = EnumSort('U', ['U'+str(n) for n in range(1,9)])

## Returns a string which contains informations about the universe used.
#  @return The string which contains the universe.
def universe_state():
	if hasattr(U, 'num_constructors'):
		num = str(U.num_constructors())
		return 'Universe = U, has ' + num + ' element(s)'
	return 'Universe = ' + str(U)

## Sets universe state u to set module and bin-relation module.
def set_universe_state(u):
	global U
	set_set_sort(u)
	set_rel_sort(u, u)
	U = u

_ID = 0

## Creates a new ID that will be incremented and given to each element in the theorem proving. It is used to avoid conflicts of the same name in Z3Py.
def _id():
	global _ID
	while True:
		_ID += 1
		yield _ID

## Concatenates the name of the element with its ID, and return the string result.
#  @param name Name of the element
#  @return The name concatenated with the current ID value.
def id_name(name):
	if ' ' in name:
		raise ValueError("name mustn't include space")
	return name + '_' + str(next(_id()))

## Concatenates the names of the elements with their IDs, and return the string result.
#  @param names Names of the element separated by space character.
#  @return The concatenated names of the element with the ID, all separated by space character.
def id_names(names):
	names = names.split(" ")
	for idx, name in enumerate(names):
		names[idx] = id_name(name)
	return ' '.join(names)


## Creates a new const element.
#  @param name Name of the const element.
#  @param sort Type of the const element.
#  @return A new const element.
def const(name, sort):
	return Const(id_name(name), sort)

## Creates multiple new consts elements of the same type.
#  @param names Names of the const elements, separated by space character.
#  @param sort Type of the const elements (all consts must have the same type when using this function.
#  @return New const elements.
def consts(names, sort):
	return Consts(id_names(names), sort)

def element(name):
	return const(name, U)

def elm(name):
	return element(name)

def elements(names):
	return consts(names, U)

def elms(names):
	return elements(names)

## Creates a function element.
#  @param name Name of the function element.
#  @param sort Type of the function element.
#  @return A new function element.
def function(name, *sort):
	return Function(id_name(name), sort)

## Creates multiple functions elements.
#  @param names Names of the function elements, separated by space character.
#  @param sort Type of the function elements (all functions must have the same type when using this function.
#  @return New function elements.
def functions(names, *sort):
	names = id_names(names).split(" ")
	return [function(name, *sort) for name in names]

## Returns the model of a solver after checking whether its result.
#  @param solver The currently used solver.
#  @param instance The instance that is needed.
#  @return The model of the instance in the solver.
def model(solver, instance):
	return solver.model()[instance]

## Evaluates the content of an element.
#  @param solver The currently used solver.
#  @param function The function that needs to be evaluated
#  @return The evaluated function, in general it will return the value of the booleans in the function.
def evaluate(solver, function):
	return solver.model().evaluate(function)

## Returns the list corresponding to an array of an element of the solver.
#  @param solver The currently used solver.
#  @param as_array The array that needs to be converted in a list.
#  @return The list that corresponds to the array passed as parameter.
def as_list(solver, as_array):
	array = get_as_array_func(as_array)
	return model(solver, array).as_list()

## Recursive function that prints the elements of an element.
#  @param solver The solver currently used.
#  @param item The item that needs to be printed
#  Recursive functions that can be used to print the composition of an item used in the theorem (such as a program)
ITE = ('if', 'then', 'else')
def unveil(solver, item, phase=0):
	if type(item) == list:
		for i in item:
			indent = lambda n: ''.join(['\t']*(n))
			if type(i) != list: i = ["else", i]
			if is_bool(i[1]):
				print(indent(phase), i[0], '->', evaluate(solver, i[1]))
			else:
				print(indent(phase), i[0], '->')
				unveil(solver, i[1], phase+1)
	else:
		if is_bool(item): 
			return item
		elif is_as_array(item): 
			return unveil(solver, as_list(solver, item), phase)
		elif item.decl().name() == 'if':
			return unveil(solver, [list(i) for i in zip(ITE, item.children())], phase)
		elif is_ast(item): 
			return unveil(solver, evaluate(solver, item), phase)
		else: 
			return "#unspecified"

## Prints the name of an element and call unveil to print its content
#  @param solver The solver currently used.
#  @param record The name of the record.
#  @param element The element that needs to be printed.
def show_record_element(solver, record, element):
	print(element, 'of', record)
	elm = simplify(element(model(solver, record)))
	elm_list = as_list(solver, elm)
	unveil(solver, elm_list)
	print()

## Checks if a solver instance is sat, unsat or unknown, returns the result.
#  @param solver The solver that is used to make the proof.
#  @param title The title of the theorem.
#  @param reset Indicates if the solver will be reset after the proof or not, True by default.
#  @return The result of the theorem (sat, unsat or unknown)
def proof(solver, title=None, reset=True, show_solver=False, show_model=True):
	if show_solver: print(solver)
	if title != None: print(yellow(title))
	print(yellow(universe_state()))

	result = solver.check()
	if result == unsat:
		print(cyan("Holds: " + str(result)), "\n")
	else:
		print(red("Unholds: " + str(result)))
		if result == sat and show_model:
			from .z3py_set import show_set_models
			from .z3py_rel import show_rel_models
			show_set_models(solver)
			show_rel_models(solver)
		if result == unknown: 
			print(red(solver.reason_unknown()), "\n")
	
	if reset: solver.reset()
	
	return result

def conclude(solver, conclusion, title=None, reset=True, show_solver=False):
	solver.add(Not(conclusion))
	proof(solver, title=title, reset=reset, show_solver=show_solver, show_model=True)