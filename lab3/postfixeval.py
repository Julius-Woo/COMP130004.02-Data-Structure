# input: string, postfix expression
# output: int, result of the expression
def postfixeval(postfixExpr):
    stack = []
    for token in postfixExpr.split(): # split the postfix expression by space
        if token.isdigit():  # meeting operand, push into stack
            stack.append(int(token))
        # meeting operator, pop two operands and compute
        elif stack:
            try:
                operand2 = stack.pop()
                operand1 = stack.pop()
                result = computing(token, operand1, operand2)
                stack.append(result)
            except:
                print('Error: invalid expression')
                return None
	# finish computing, return the result
    result = stack.pop()
    return result

def computing(operator, oprand1, oprand2):
    if operator == '*':
        return oprand1 * oprand2
    elif operator == '/':
        return oprand1 // oprand2
    elif operator == '+':
        return oprand1 + oprand2
    elif operator == '-':
        return oprand1 - oprand2
    elif operator == '%':
        return oprand1 % oprand2
    elif operator == '^':
        return oprand1 ** oprand2