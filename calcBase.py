# -----------------------------------------------------------------------------
# calc.py
#
# Expressions arithmétiques sans variables
# -----------------------------------------------------------------------------
from genereTreeGraphviz2 import printTreeGraph

# 001
# 011
# 001

reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'print': 'PRINT',
    'fonctionVoid': 'FONCVOID',
    'T': 'TRUE',
    'F': 'FALSE',
    'return': 'RETURN',
}

tokens = [
    'NUMBER','MINUS',
    'PLUS','TIMES','DIVIDE','PLUSPLUS',
    'AND','OR',
    'LESSTHAN','BIGGERTHAN','EQEQ','DIF','LESSEQ','GREATEQ',
    'LPAREN','RPAREN','SEMICOLON','EQUAL','PLUSEQ','MODULO','LBRACE','COMMA',
    'NAME','RBRACE','QUOTE','STRING','LBRACKET','RBRACKET',
 ] + list(reserved.values())


# Tokens
t_PLUS = r'\+'
t_PLUSPLUS = r'\+\+'
t_PLUSEQ = r'\+='
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MODULO = r'%'
t_LBRACE = r'{'
t_RBRACE = r'}'
t_QUOTE = r'"'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'

t_AND = r'&'
t_OR = r'\|'

t_LESSTHAN = r'<'
t_BIGGERTHAN = r'>'

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_SEMICOLON = r';'
t_COMMA = r','
t_EQUAL = r'='
t_EQEQ = r'=='
t_GREATEQ = r'>='
t_LESSEQ = r'<='
t_DIF = r'!='

vars = {}
func = {}
waitingvar = []
funcvar = {}
tabs = {}

def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'NAME')
    return t

def t_STRING(t):
    r'\"[a-zA-Z_0-9]+\"'
    t.type = reserved.get(t.value, 'STRING')
    return t
  

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


# Ignored characters
t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
import ply.lex as lex

lex.lex()

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('nonassoc', 'LESSTHAN', 'BIGGERTHAN', 'EQUAL', 'GREATEQ', 'LESSEQ', 'EQEQ', 'DIF'),
    ('left', 'PLUS', 'MINUS', 'MODULO'),
    ('left', 'TIMES', 'DIVIDE'),
)


def p_start(p):
    'start : bloc'
    p[0] = ('start', p[1])
    print('Arbre de dérivation = ', p[0])
    printTreeGraph(p[1])
    evalInst(p[1])


def p_bloc(p):
    '''bloc : bloc statement SEMICOLON
                | statement SEMICOLON'''
    if len(p) == 4:
        p[0] = ('bloc', p[1], p[2])
    else:
        p[0] = ('bloc', p[1], 'None')


def p_out_expr(p):
    """out : return
        | bloc"""
    p[0] = (p[1])

def p_return_expr(p):
    """return : RETURN SEMICOLON
        | RETURN expression SEMICOLON"""
    if len(p) == 4:
        p[0] = ('return', p[2])
    else:
        p[0] = ('return', 'empty')

def p_statement_print(p):
    '''statement : PRINT LPAREN expression RPAREN
                | PRINT LPAREN expression COMMA expression RPAREN'''
    if len(p) == 5:
        p[0] = (p[1], p[3])
    else :
        p[0] = (p[1], p[3], p[5])


def p_statement_if(p):
    'statement : IF LPAREN expression RPAREN LBRACE bloc RBRACE'
    p[0] = ('if', p[3], p[6])


def p_statement_if_else(p):
    '''statement : IF LPAREN expression RPAREN LBRACE bloc RBRACE ELSE LBRACE bloc RBRACE'''
    p[0] = ('if', p[3], p[6], ('else', p[10]))


def p_statement_while(p):
    'statement : WHILE LPAREN expression RPAREN LBRACE bloc RBRACE'
    p[0] = ('while', p[3], p[6])

def p_list_affect(p):
    '''listaffect : expression
                  | expression COMMA expression'''
    p[0] = ('listaffect', p[1])

def p_statement_call_fonction(p):
    '''statement : NAME LPAREN RPAREN
                 | NAME LPAREN listaffect RPAREN'''
    if p[1] in func:
        if len(p) == 4:
            p[0] = ('fonction', p[1], func.get(p[1]))
        if len(p) == 5:
            p[0] = ('fonction', p[1],func.get(p[1]), p[3])

def p_statement_fonction_void(p):
    '''statement : FONCVOID NAME LPAREN RPAREN LBRACE bloc RBRACE
                 | FONCVOID NAME LPAREN listparam RPAREN LBRACE bloc RBRACE'''
    if len(p) == 8:
        func[p[2]] = p[6]
        p[0] = ('fonctionVoid', p[2], p[6])
    elif len(p) == 9:
        func[p[2]] = p[7]
        p[0] = ('fonctionVoid', p[2], p[7], p[4])

def p_list_param(p):
    '''listparam : NAME
                 | NAME COMMA listparam'''
    p[0] = ('listparam', p[1])
    print(p[1])

def p_statement_for(p):
    '''statement : FOR LPAREN NAME EQUAL expression SEMICOLON statement SEMICOLON NAME EQUAL expression PLUS expression SEMICOLON RPAREN LBRACE bloc RBRACE
                 | FOR LPAREN NAME EQUAL expression SEMICOLON statement SEMICOLON NAME EQUAL expression MINUS expression SEMICOLON RPAREN LBRACE bloc RBRACE'''

    p[0] = ('for', (p[4], p[3], p[5]), p[7], (p[10], p[9], (p[12], p[11], p[13])), p[17])


def p_statement_var(p):
    '''statement : NAME EQUAL expression
                | NAME EQUAL STRING'''
    p[0] = ('=', p[1], p[3])


def p_statement_tab(p):
    'statement : NAME LBRACKET expression RBRACKET EQUAL expression'
    p[0] = ('tab', p[1], p[3], p[6])

def p_create_tab(p):
    'statement : NAME LBRACKET expression RBRACKET'
    p[0] = ('createtab', p[1], p[3])


def p_expression_var(p):
    '''expression : NAME'''
    p[0] = p[1]

    
def p_statement_expr(p):
    '''statement : expression'''
    p[0] = p[1]


def p_expression_pluseq(p):
    '''expression : NAME PLUSEQ expression'''
    p[0] = (p[2], p[1], p[3])


def p_incr_var(p):
    '''expression : NAME PLUSPLUS'''
    p[0] = (p[2], p[1])
    

def p_expression_binop(t):
    '''expression : expression PLUS expression
                | expression MINUS expression
                | expression TIMES expression
                | expression OR expression
                | expression EQEQ expression
                | expression DIF expression
                | expression LESSEQ expression
                | expression GREATEQ expression
                | expression AND expression
                | expression EQUAL expression
                | expression LESSTHAN expression
                | expression BIGGERTHAN expression
                | expression MODULO expression
                | expression DIVIDE expression'''
    t[0] = (t[2], t[1], t[3])


def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]


def p_expression_number(p):
    'expression : NUMBER'
    p[0] = p[1]


def p_expression_bool(p):
    '''expression : TRUE
                | FALSE'''
    if p[1] == 'T':
        p[0] = True
    else:
        p[0] = False


def p_error(p):
    print("Syntax error at '%s'" % p.value)


import ply.yacc as yacc

yacc.yacc()


def eval(t):
    if type(t) is int : return t
    if type(t) is str : 
        if t.startswith('\"'):
           t = t.replace('\"', '')
           return t
        return vars.get(t)
    if type(t) is tuple : 
        if t[0] == '+':     return eval(t[1]) + eval(t[2])
        if t[0] == '*':     return eval(t[1]) * eval(t[2])
        if t[0] == '/':     return eval(t[1]) / eval(t[2])
        if t[0] == '-':     return eval(t[1]) - eval(t[2])
        if t[0] == '&':     return bool(eval(t[1])) and bool(eval(t[2]))
        if t[0] == '|':     return bool(eval(t[1])) or bool(eval(t[2]))
        if t[0] == '<':     return eval(t[1]) < eval(t[2])
        if t[0] == '>':     return eval(t[1]) > eval(t[2])
        if t[0] == '==':     return eval(t[1]) == eval(t[2])
        if t[0] == '!=':     return eval(t[1]) != eval(t[2])
        if t[0] == '%':     return eval(t[1]) % eval(t[2])
    return 'UNK'


def evalInst(t):
    if t == 'empty': return
    if t[0] == '++':
        vars[t[1]] = vars[t[1]] + 1
    if t[0] == 'createtab':
        tabs[t[1]] = list()
        for i in range(t[2]):
            tabs[t[1]].append(0)
    if t[0] == 'tab':
        tabs[t[1][0]][t[2]] = t[3]
        print(tabs[t[1]])
    if t[0] == '=':
        vars[t[1]] = eval(t[2])
    if t[0] == '+=':
        vars[t[1]] = eval(t[1]) + eval(t[2])
    if t[0] == 'print': 
        if(len(t) > 2):
            print('CALC>',eval(t[1]), eval(t[2]))
        else :
            print('CALC>',eval(t[1]))
    if t[0] == 'bloc': 
        evalInst(t[1])
        evalInst(t[2])
    if t[0] == 'if':
        if eval(t[1]):
            evalInst(t[2])
        elif eval(t[1]) == False and t[3][0] == 'else':
            evalInst(t[3][1])
    if t[0] == 'while':
        while eval(t[1]):
            evalInst(t[2])
    if t[0] == 'for':
        evalInst(t[1])
        while eval(t[2]):
            evalInst(t[4])
            evalInst(t[3])
    if t[0] == 'fonction':
        if len(t) == 3:
            evalInst(t[2])
        if len(t) == 4:
            evalInst(t[3])
            for k in range(0, len(funcvar[t[1]])):
                vars[funcvar[t[1]][k]] = waitingvar[k]
            evalInst(t[2])
    if t[0] == 'fonctionVoid':
        if len(t) > 3:
            evalInst(t[3])
            tpl = ()
            for var in waitingvar:
                tpl = tpl + (var,)
            funcvar[t[1]] = tpl
            waitingvar.clear()
    if t[0] == 'listparam':
        waitingvar.append(t[1])
        print(waitingvar)
    if t[0] == 'listaffect':
        waitingvar.append(eval(t[1]))

s = input('calc > ')
yacc.parse(s)