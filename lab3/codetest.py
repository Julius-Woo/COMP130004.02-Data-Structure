from infix2post import in2post
from postfixeval import postfixeval
# # infix to postfix conversion test
# with open (".\lab3\code1test.txt", "r") as file1:
#     lines = file1.readlines()
#     for line in lines:
#         line = line.strip()
#         print('Infix:', line)
#         ans = ''.join(in2post(line))
#         print('Postfix:', ans)


# postfix expression evaluation test
with open (".\lab3\code2test.txt", "r") as file2:
    lines = file2.readlines()
    for line in lines:
        line = line.strip()
        print('Postfix:', line)
        ans = postfixeval(line)
        print('Result:', ans)