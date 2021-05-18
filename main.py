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




# class string_processor:
#     def __init__(self, regex_str):
#         this.str = regex_str
#         this.idx = 0

#     def get_next_token(self):

def preprocess_regex(regex):
        store = list()
        temp = ""
        new_regex = ""
        pos = 0
        last_char_index = -1
        for char_index, char in enumerate(regex):
            if char == "[":
                while regex[char_index + 1] != "]":
                    temp += regex[char_index + 1]
                    char_index += 1
                store.append(temp)
                new_regex += "[" + str(pos)
                last_char_index = char_index
                pos += 1
                temp = ""
            else:
                if char_index <= last_char_index:
                    continue
                else:
                    new_regex += char
        return store, new_regex



print(preprocess_regex('[A-Za-z]+[0-9]'))


for c in enumerate('text'):
    print(c)
        
        


# print(preprocess_regex("DADA|(AB|C(D|B))|2*"))
print(preprocess_regex('(ab)*'))