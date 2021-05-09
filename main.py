from nfa import nfa
from thompson_rules import *

nfa1 = nfa()
nfa1.add_state(0)
nfa1.add_state(1)

nfa1.set_starting(0)
nfa1.set_terminating(1)

nfa2, _ = nfa1.to_numeric_states(0)

nfa1.add_transition(0, [1], 'a')


nfa2.add_transition(0, [1], 'b')
nfa3 = or_rule(nfa1, nfa2)
print(nfa3.to_json())