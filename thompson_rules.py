from nfa import nfa

def concat_rule(nfa1, nfa2):
    nfa1_, n = nfa1.to_numeric_states(0)
    nfa2_, _ = nfa2.to_numeric_states(n)

    concat_nfa = nfa()
    # add states from NFAs 1 and 2
    for state in nfa1_.states + nfa2_.states:
        concat_nfa.add_state(state)
    
    # add transitions from NFAs 1 and 2
    for from_state, trns in nfa1_.transitions.items():
        for input, to_state in trns.items():
            concat_nfa.add_transition(from_state, to_state, input)
    
    for from_state, trns in nfa2_.transitions.items():
        for input, to_state in trns.items():
            concat_nfa.add_transition(from_state, to_state, input)

    # set start state and terminating state
    concat_nfa.set_starting(nfa1_.starting_state)
    concat_nfa.set_terminating(nfa2_.terminating_states[0])

    # add epsilon transtion between
    concat_nfa.add_transition(nfa1_.terminating_states[0], nfa2_.starting_state, '\u03B5')

    return concat_nfa







