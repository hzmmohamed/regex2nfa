import copy
operator_precedence = {
    '|':0,
    '+':0,
    '.':1,
    '*':2
}

def validate_regex(regex):
    square = 0
    pnths = 0
    for c in regex:
        if c == '[': square+=1
        elif c == ']': square-=1
        elif c == '(': pnths+=1
        elif c == ')': pnths-=1

        if square < 0 or pnths < 0: 
            return False
    return True

def insert_or_symbols_in_square_brackets(re_str):
    # Replace all square barckets with OR operators
    re = copy.deepcopy(re_str)
    start = None
    end = None
    pos = 0
    or_list = []
    while pos < len(re):
        if re[pos] == '[':
            start = pos
            pos+=1
            while re[pos] != ']':
                if re[pos] != '-':
                    or_list.append(re[pos])
                else:
                    or_list.pop()
                    interval = [chr(i) for i in range(ord(re[pos-1]), ord(re[pos+1]))]
                    or_list.extend(interval)
                pos+=1

            end = pos
            re = re[:start] + '(' + '|'.join(or_list) + ')' + re[end+1:]
            or_list = []
            pos-=1
        else:
            pos+=1

    return re


def insert_concat_symbols(re):
    new_re = ''
    for i, token in enumerate(re):
        new_re+=token
        if token == '(' or token == '|':
            continue
        if i < (len(re)-1):
            lookahead = re[i+1]
            if lookahead in ['*', '|', '+', ')']:
                continue
            else:
                new_re+='.'
    return new_re


# def remove_pnths(re):
#     new_re = copy.deepcopy(re)
#     pos = 0
#     while pos < len(new_re):
#         token = new_re[pos]
#         if token == '(' or token == ')':
#             start = pos
#             while pos < len(new_re) and new_re[pos] == token:
#                 pos+=1
#             # if new_re[start-1] != '.'
#             new_re = new_re[:start] + '.' + new_re[pos:]
#             pos-=1
#         pos+=1
#     return new_re



def to_postfix(re):
    operator_stack = []
    output = ''
    for i, token in enumerate(re):
        if token in operator_precedence.keys():
            while operator_stack[-1] != '(' and operator_precedence[token] < operator_precedence[operator_stack[-1]]:
                output+=operator_stack.pop()
            operator_stack.append(token)
        elif token == '(':
            operator_stack.append(token)
        elif token == ')':
            while operator_stack[-1] != '(':
                output+=operator_stack.pop()
            operator_stack.pop()
        else:
            output+=token
    
    # Exhaust operator stack
    while len(operator_stack) > 0:
        output+=operator_stack.pop()
    
    return output



def preprocess_regex(re):
    if  validate_regex(re) is False:
        raise BaseException('Invalid input expression')
    new_re = '(' + re + ')'
    new_re = insert_or_symbols_in_square_brackets(new_re)
    new_re = insert_concat_symbols(new_re)
    new_re = to_postfix(new_re)
    return new_re
