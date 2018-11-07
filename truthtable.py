#!/usr/bin/python3

import sys
import argparse

parser = argparse.ArgumentParser(description='A LaTeX truthtable generator')
parser.add_argument("inputFile",
                    nargs="?",
                    help="File from which the logical expression is read.")
parser.add_argument("--nohlines",
                    dest="nohlines",
                    default=False,
                    const=True,
                    nargs="?",
                    help="Don't put seperatiing horizontal lines in the output table.")

args = parser.parse_args()

if args.inputFile:
    try:
        text = "\n".join(open(sys.argv[1]).readlines())
    except:
        text = " ".join(sys.argv[1:])
else:
    text = input()

TT_VAR = "variable"
TT_AND = "and"
TT_NOT = "not"
TT_OR = "or"
TT_IMP = "implication"
TT_AEQ = "equivalent"
TT_XOR = "antivalent"
TT_LEFTPAREN = "("
TT_RIGHTPAREN = ")"
TT_EOF = "EOF"

class Token:
    def __init__(self, art, text, pos):
        self.art = art
        self.text = text
        self.pos = pos
    def __str__(self):
        return "Token Type '"+self.art+"', text '"+self.text+"' at char "+str(self.pos+1)
    def __repr__(self):
        return str(self)

def tokenize(text):
    WHITESPACE = [" ", "\t", "\n", "\r"]
    LETTER = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
    START = list("\\")
    SYMBOL = list("!<->=|^&")
    token = []
    i = 0
    text += " "
    while i<len(text):
        if text[i] in WHITESPACE: # Whitespace
            i+=1
            continue
        if text[i] == "(":
            token.append(Token(TT_LEFTPAREN,text[i],i))
            i+=1
            continue
        if text[i] == ")":
            token.append(Token(TT_RIGHTPAREN,text[i],i))
            i+=1
            continue
        if text[i] in LETTER+SYMBOL+START:
            j=i+1
            while text[j] in LETTER and text[i] not in SYMBOL:  j+=1
            t = text[i:j]
            if t.lower() in ["or","|","\\or","\\vee","\\lor"]:
                token.append(Token(TT_OR,t,i))
                i=j
                continue
            if t.lower() in ["not","!","\\neg","\\lnot"]:
                token.append(Token(TT_NOT,t,i))
                i=j
                continue
            if t.lower() in ["and","&","\\and","\\land","\\wedge"]:
                token.append(Token(TT_AND,t,i))
                i=j
                continue
            if t.lower() in ["xor","^","\\oplus","\\veebar"]:
                token.append(Token(TT_XOR,t,i))
                i=j
                continue
            if t.lower() in [">", "\\imp","\\rightarrow"]:
                token.append(Token(TT_IMP,t,i))
                i=j
                continue
            if t.lower() in ["=","\\aeq","\\leftrightarrow"]:
                token.append(Token(TT_AEQ,t,i))
                i=j
                continue
            token.append(Token(TT_VAR,t,i))
            i=j
            continue

        print("unrecognised symbol '"+text[i]+"' got skipped...")
        i+=1
    token.append(Token(TT_EOF, "", len(text)))
    return token

token = tokenize(text)

class Unary():
    def __init__(self,operator,right):
        self.operator=operator
        self.right=right
    def __str__(self):
        return self.operator.text + str(self.right)
class Binary():
    def __init__(self,left,operator,right):
        self.left=left
        self.operator=operator
        self.right=right
    def __str__(self):
        return str(self.left)+self.operator.text+str(self.right)
class Grouping():
    def __init__(self,left,expression,right):
        self.expression=expression
        self.left = left
        self.right = right
    def __str__(self):
        return "("+str(self.expression)+")"
class Variable():
    def __init__(self,expression):
        self.expression=expression
    def __str__(self):
        return self.expression.text
    
def parse(token):
    global current
    current=0

    def consume(tt):
        global current
        if token[current].art == tt:
            current+=1
        else:
            print("--------------------------")
            print("Unexpected Token:", token[current])
            print("Expected Token:",tt)
            print("--------------------------")
            current += 1
    def primary_e():
        global current
        if token[current].art == TT_LEFTPAREN:
            return grouping_e()
        consume(TT_VAR)
        return Variable(token[current-1])

    def grouping_e():
        global current
        consume(TT_LEFTPAREN)
        left = token[current-1]
        inner = aeq_e()
        consume(TT_RIGHTPAREN)
        right = token[current-1]
        return Grouping(left,inner,right)
    def not_e():
        global current
        if token[current].art == TT_NOT:
            operator = token[current]
            consume(TT_NOT)
            right = not_e()
            return Unary(operator,right)
        return primary_e()
    def and_e():
        global current
        expr = not_e()
        while token[current].art == TT_AND:
            operator = token[current]
            current+=1
            right = not_e()
            expr = Binary(expr,operator,right)
        return expr
    def xor_e():
        global current
        expr = and_e()
        while token[current].art == TT_XOR:
            operator = token[current]
            current+=1
            right = and_e()
            expr = Binary(expr,operator,right)
        return expr
    def or_e():
        global current
        expr = xor_e()
        while token[current].art == TT_OR:
            operator = token[current]
            current+=1
            right = xor_e()
            expr = Binary(expr,operator,right)
        return expr
    def imp_e():
        global current
        expr = or_e()
        while token[current].art == TT_IMP:
            operator = token[current]
            current+=1
            right = or_e()
            expr = Binary(expr,operator,right)
        return expr
        
    def aeq_e():
        global current
        expr = imp_e()
        while token[current].art == TT_AEQ:
            operator = token[current]
            current+=1
            right = imp_e()
            expr = Binary(expr,operator,right)
        return expr
    
    expr = aeq_e()

    while current<len(token):
        consume(TT_EOF)

    return expr

top_expr = parse(token)

variables = []
for t in token:
    if t.art == TT_VAR:
        variables.append(t.text)
variables = sorted(list(set(variables)))

def evaluate(expr, varval):
    if type(expr) is Binary:
        vl, sl = evaluate(expr.left, varval)
        vr, sr = evaluate(expr.right, varval)
        if expr.operator.art == TT_AND:
            r = vl and vr
        elif expr.operator.art == TT_XOR:
            r = vl != vr
        elif expr.operator.art == TT_OR:
            r = vl or vr
        elif expr.operator.art == TT_AEQ:
            r = vl == vr
        elif expr.operator.art == TT_IMP:
            r = not vl or vr
        return r, sl + [(expr.operator, r)] + sr
    if type(expr) is Unary:
        vr, sr = evaluate(expr.right, varval)
        if expr.operator.art == TT_NOT:
            r = not vr
        return r, [(expr.operator, r)] + sr
    if type(expr) is Variable:
        r = varval[expr.expression.text]
        return r, [(expr.expression, r)]
    if type(expr) is Grouping:
        r, sr = evaluate(expr.expression, varval)
        return r, [(expr.left, None)] + sr + [(expr.right,None)]
    print("Unsupported type",str(type(expr)))
 
def booln(v):
    if v == None:
        return ""
    elif v:
        return "1"
    else:
        return "0"

rows = []
for row in range(2**len(variables)):
    varval = dict(zip(variables,[row%(2**n)>=2**(n-1) for n in range(len(variables),0,-1)]))
    result, parts = evaluate(top_expr, varval)
    rows.append((varval, result, parts))

out = "\\begin{tabular}{|"
out += "c|" * len(variables) + "c"*(len(parts)) + "|} \\hline\n"

for var in variables:
    out += "$" + var + "$&"
out += "&".join("$"+token.text+"$" for token,_ in parts)
out += "\\\\\hline\n"

for varval, result, parts in rows:
    for var in sorted(varval.keys()):
        out+=booln(varval[var])+"&"
    for index, (token, value) in enumerate(parts):
        if type(top_expr) in [Unary, Binary] and top_expr.operator == token or type(top_expr) in [Grouping, Variable] and top_expr.expression == token:
            out += "\\textbf{"+booln(value)+"}"
        else:
            out += booln(value)
        if index+1<len(parts):
            out += "&"

    if not args.nohlines:
        out += "\\\\\hline\n"
    else:
        out += "\\\\\n"

out += "\\end{tabular}"
print(out)

