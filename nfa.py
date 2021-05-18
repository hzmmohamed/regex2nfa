from utils import alphabet
import json
from graphviz import Source
class nfa:
    def __init__(self):
        self.states = []
        self.starting_state = None
        self.transitions = dict()
        self.terminating_states = []
    
    def add_state(self, state):
        if not (isinstance(state, str) or isinstance(state, int)):
            raise Exception('State name must be a string or int')
        elif state in self.states:
            raise Exception('State already exists')
        else:   
            self.states.append(state)
            self.transitions[state] = dict()
    
    def set_starting(self, state):
        if state not in self.states:
            raise Exception('Provide an existing state.')
        else:
            self.starting_state = state

    def make_non_terminating(self, state):
        if state not in self.terminating_states:
            raise Exception('State is already non-terminating')
        else:
            self.terminating_states.remove(state)

    def set_terminating(self, state):
        if state not in self.states:
            raise Exception('Make sure all specified states exist in the NFA.')
        else:
            self.terminating_states.append(state)

    def add_transition(self, from_state, to_states, input):
        if not((from_state in self.states) and \
            (set(to_states).issubset(set(self.states)))):
            raise Exception('Make sure all specified states exist in the NFA.')
        elif input not in alphabet:
            raise Exception('Invalid input parameter.')
        elif input in self.transitions[from_state].keys():
            self.transitions[from_state][input].extend(to_states)
        else:
            self.transitions[from_state][input] = to_states


    def to_numeric_states(self, starting_index):
        new_nfa = nfa()
        new_indices = {}
        for state in self.states:
            new_indices[state] = starting_index
            new_nfa.add_state(starting_index)
            starting_index +=1

        for state, index in new_indices.items():
            for input, to_states in self.transitions[state].items():
                new_nfa.add_transition(index, [new_indices[to_state] for to_state in to_states], input)

        
        new_nfa.set_starting(new_indices[self.starting_state])
        new_nfa.set_terminating(new_indices[self.terminating_states[0]])
        return new_nfa, starting_index


    def to_json(self):
        # nfa = self.to_numeric_states(0)
        nfa = self
        nfa_json = {}
        nfa_json['startingState'] = 'S' + str(self.starting_state)
        
        for state in nfa.states:
            s = {}
            if state in nfa.terminating_states:
                s['isTerminatingState'] = True
            else:
                s['isTerminatingState'] = False
            for input, to_states in nfa.transitions[state].items():
                s[input] = ['S'+str(to_state) for to_state in to_states]
            nfa_json['S'+str(state)] = s
        nfa_json_str =  json.dumps(nfa_json, indent=3,)
        return nfa_json_str

    def to_dot_format(self):
        dot_file = "digraph DFA {\nrankdir=LR\n"
        if len(self.states) != 0:
            dot_file += "root=S1\nstart [shape=point]\nstart->S%d\n" % self.starting_state
            for state in self.states:
                if state in self.terminating_states:
                    dot_file += "S%d [shape=doublecircle]\n" % state
                else:
                    dot_file += "S%d [shape=circle]\n" % state
            for from_state, trns in self.transitions.items():
                for input, to_states in trns.items():
                    for to_state in to_states:
                        dot_file += 'S%d->S%d [label="%s"]\n' % (from_state, to_state, input)
        dot_file += "}"
        return dot_file

    def save_to_png(self, filename):
        source = Source(self.to_dot_format(), filename=filename + ".gv", format="png")
        source.render(filename, directory='out')
