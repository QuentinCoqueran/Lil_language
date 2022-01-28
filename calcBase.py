# -----------------------------------------------------------------------------
# calc.py
#
# Expressions arithmétiques sans variables
# -----------------------------------------------------------------------------
from genereTreeGraphviz2 import printTreeGraph

#001
#011
#001

reserved = {
    'if' : 'IF',
    'else' : 'ELSE',
    'while' : 'WHILE',
    'for'    : 'FOR',
    'print' : 'PRINT',
    'fonctionVoid' : 'FONCVOID',
    'T': 'TRUE',
    'F': 'FALSE',
}

tokens = [
    'NUMBER','MINUS',
    'PLUS','TIMES','DIVIDE','PLUSPLUS',
    'AND','OR',
    'LESSTHAN','BIGGERTHAN','EQEQ','DIF','LESSEQ','GREATEQ',
    'LPAREN','RPAREN','SEMICOLON','EQUAL','PLUSEQ','MODULO','LBRACE','COMMA',
    'NAME','RBRACE',
 ] + list(reserved.values())

# Tokens
t_PLUS    = r'\+'
t_PLUSPLUS    = r'\+\+'
t_PLUSEQ  = r'\+='
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_MODULO  = r'%'
t_LBRACE = r'{'
t_RBRACE = r'}'

t_AND  = r'&'
t_OR  = r'\|'

t_LESSTHAN  = r'<'
t_BIGGERTHAN  = r'>'

t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_SEMICOLON  = r';'
t_COMMA     =r','
t_EQUAL = r'='
t_EQEQ = r'=='
t_GREATEQ = r'>='
t_LESSEQ  = r'<='
t_DIF   = r'!='

vars = {}
funcs = {}

def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'NAME')
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
    ('nonassoc', 'LESSTHAN', 'BIGGERTHAN', 'EQUAL','GREATEQ', 'LESSEQ', 'EQEQ', 'DIF'),
    ('left','PLUS','MINUS','MODULO'),
    ('left','TIMES','DIVIDE'),
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
    else :
        p[0] = ('bloc', p[1], 'None')

def p_statement_expr(p):
    'statement : PRINT LPAREN expression RPAREN'
    p[0] = (p[1], p[3])

def p_statement_if(p):
    'statement : IF LPAREN expression RPAREN LBRACE bloc RBRACE'
    p[0] = ('if', p[3], p[6])

def p_statement_if_else(p):
    '''statement : IF LPAREN expression RPAREN LBRACE bloc RBRACE ELSE LBRACE bloc RBRACE'''
    p[0] = ('if', p[3], p[6], ('else', p[10]))

def p_statement_while(p):
    'statement : WHILE LPAREN expression RPAREN LBRACE bloc RBRACE'
    p[0] = ('while', p[3], p[6])

def p_list(p):
    '''list : NAME COMMA NAME
            | list COMMA NAME'''
    p[0] = p[1] + p[2] + p[3]

def p_statement_call_fonction(p):
    '''statement : NAME LPAREN RPAREN'''
    if p[1] in funcs :
        p[0] = ('fonction', p[1], funcs.get(p[1]))

def p_statement_fonction_void(p):
    '''statement : FONCVOID NAME LPAREN RPAREN LBRACE bloc RBRACE'''
    if len(p) == 8:
        funcs[p[2]] = (p[6])
    p[0] = ('fonctionVoid', p[2], p[6])

def p_statement_for(p):
    '''statement : FOR LPAREN NAME EQUAL expression SEMICOLON statement SEMICOLON NAME EQUAL expression PLUS expression SEMICOLON RPAREN LBRACE bloc RBRACE
                 | FOR LPAREN NAME EQUAL expression SEMICOLON statement SEMICOLON NAME EQUAL expression MINUS expression SEMICOLON RPAREN LBRACE bloc RBRACE'''
    p[0] = ('for', (p[4],p[3],p[5]), p[7], (p[10],p[9],(p[12],p[11],p[13])), p[17])
def p_statement_var(p):
    '''statement : NAME EQUAL expression'''
    p[0] = ('=', p[1], p[3])

def p_expression_var(p):
    '''expression : NAME'''
    p[0] = p[1]



def p_test(p):
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
    if p[1] == 'T': p[0] = True
    else : p[0] = False

def p_error(p):
    print("Syntax error at '%s'" % p.value)

import ply.yacc as yacc
yacc.yacc()

def eval(t):
    if type(t) is int : return t
    if type(t) is str : return vars.get(t)
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
    if t == 'empty' : return
    if t[0] == '++':
        vars[t[1]] = vars[t[1]] + 1
    if t[0] == '=':
        vars[t[1]] = eval(t[2])
    if t[0] == '+=':
        vars[t[1]] = eval(t[1]) + eval(t[2])
    if t[0] == 'print' : 
        print('CALC>',eval(t[1]))
    if t[0] == 'bloc' : 
        evalInst(t[1])
        evalInst(t[2])
    if t[0] == 'if' :
        if eval(t[1]) == True :
            evalInst(t[2])
        elif eval(t[1]) == False and t[3][0] == 'else':
            evalInst(t[3][1])
    if t[0] == 'while' :
        while(eval(t[1])) :
            evalInst(t[2])
    if t[0] == 'for' :
        evalInst(t[1])
        while eval(t[2]):
            evalInst(t[4])
            evalInst(t[3])
    if t[0] == 'fonction' :
        evalInst(t[2])
s = input('calc > ')
yacc.parse(s)