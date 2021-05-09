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
    concat_nfa.add_transition(nfa1_.terminating_states[0], [nfa2_.starting_state], '\u03B5')

    return concat_nfa



def or_rule(nfa1, nfa2):
    nfa1_, n1 = nfa1.to_numeric_states(1)
    nfa2_, n2 = nfa2.to_numeric_states(n1)

    or_nfa = nfa()
    
    for state in nfa1_.states + nfa2_.states:
        or_nfa.add_state(state)

    # add transitions from NFAs 1 and 2
    for from_state, trns in nfa1_.transitions.items():
        for input, to_states in trns.items():
            or_nfa.add_transition(from_state, to_states, input)
    
    for from_state, trns in nfa2_.transitions.items():
        for input, to_states in trns.items():
            or_nfa.add_transition(from_state, to_states, input)


    # add start and final states and corresponding transitions
    or_nfa.add_state(0)
    or_nfa.set_starting(0)
    or_nfa.add_transition(0, [1], '\u03B5')
    or_nfa.add_transition(0, [n1], '\u03B5')

    or_nfa.add_state(n2)
    or_nfa.set_terminating(n2)
    or_nfa.add_transition(n1-1, [n2], '\u03B5')
    or_nfa.add_transition(n2-1, [n2], '\u03B5')

    return or_nfa


def star_rule(nfa1):
    nfa1_, n = nfa1.to_numeric_states(1)

    star_nfa = nfa()

    for state in nfa1_.states:
        star_nfa.add_state(state)

    for from_state, trns in nfa1_.transitions.items():
        for input, to_state in trns.items():
            star_nfa.add_transition(from_state, to_state, input)

    star_nfa.add_state(0)
    star_nfa.add_state(n)

    star_nfa.add_transition(0, [1], '\u03B5')
    star_nfa.add_transition(n-1, [n], '\u03B5')
    star_nfa.add_transition(0, [n], '\u03B5')
    star_nfa.add_transition(n-1, [1], '\u03B5')


