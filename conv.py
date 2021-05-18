from preprocess import preprocess_regex
from nfa import nfa
from thompson_rules import *


def create_single_char_nfa(char):
    nfa_ = nfa()
    nfa_.add_state(0)
    nfa_.set_starting(0)

    nfa_.add_state(1)
    nfa_.set_terminating(1)

    nfa_.add_transition(0,[1], char)

    return nfa_

def regex_to_nfa(re):
    postfix_re = preprocess_regex(re)
    stack = []
    for i, token in enumerate(postfix_re):
        if token == '.':
            right = stack.pop()
            left = stack.pop()
            stack.append(concat_rule(left, right))
        elif token == '|':
            right = stack.pop()
            left = stack.pop()
            stack.append(or_rule(left, right))
        elif token == '*':
            stack.append(star_rule(stack.pop()))
        else:
            stack.append(create_single_char_nfa(token))

    return postfix_re, stack.pop()
