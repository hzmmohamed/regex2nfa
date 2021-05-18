from  conv import regex_to_nfa
import click
import json

@click.command()
@click.option('--exp', help='Regular Expression to be converted')
def regex2nfa(exp):
    postfix_regex, nfa = regex_to_nfa(exp)
    with open('out/nfa.json', 'w') as f:
        f.write(nfa.to_json())
    nfa.save_to_png('nfa')


if __name__ == '__main__':
    regex2nfa()
