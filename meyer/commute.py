from .equivalence import eq
from .basic_constructs import Comp

def commute(p1, p2):
	return eq(Comp(p1, p2), Comp(p2, p1))