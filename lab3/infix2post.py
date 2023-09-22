# input: string, infix expression
# output: list, postfix expression
import re

def in2post(infix):
    op_stack = [] # stack to store operators
    result = []  # list to store postfix expression
    ops = ['+', '-', '*', '/', '%', '^', '(', ')', '[', ']', '{', '}']
    op_pri = {
        '+': 1, '-': 1, 
        '*': 2, '/': 2, '%': 2, 
        '^': 3, 
        '(': 0, ')': 0, 
        '[': 0, ']': 0, 
        '{': 0, '}': 0
    }  # updated operator priority
    infix = re.sub(r'(\(|\)|\[|\]|\{|\})', r' \1 ', infix)  # add space around all kinds of brackets
    for token in infix.split(): # split the infix expression by space
        if token not in ops:
            result.append(token)
        elif token in ['(', '[', '{']:
            op_stack.append(token)
        elif token in [')', ']', '}']:
            if token == ')':
                while op_stack[-1] != '(':
                    result.append(op_stack.pop())
            elif token == ']':
                while op_stack[-1] != '[':
                    result.append(op_stack.pop())
            else: # token == '}'
                while op_stack[-1] != '{':
                    result.append(op_stack.pop())
            op_stack.pop()
        else:
            while len(op_stack) != 0 and op_pri[op_stack[-1]] >= op_pri[token]:
                result.append(op_stack.pop())
            op_stack.append(token)
    while len(op_stack) != 0:
        result.append(op_stack.pop())
    return result