import random
import string
from sympy import *
import math


def generate_eq_question(eq):

    expr = sympify(f'Eq({eq.replace("=", ",")})', evaluate=False)


    variables_set = list(expr.free_symbols)

    choosen_one = random.choice(variables_set)

    constants = [x for x in variables_set if x != choosen_one]

    values_dict = {}


    for s in constants:
        n = random.randint(1, 100)
        values_dict[s] = n

    subs_list = [(k,v) for k,v in values_dict.items()]

    with evaluate(False):
        expr = expr.subs(subs_list)
    print(expr)



    answer = solve(expr)[0].evalf()
    return str(expr)[3:-1].replace(", ", "="), values_dict, answer, choosen_one


def check_answer(answer, user_answer):
    user_answer_symp = sympify(user_answer)
    if math.isclose(user_answer_symp.evalf(), answer, rel_tol=0.1):
        return True
    return False

# def generate_eq_question(eq):
#     raw_formula = eq

#     variables_list = []

#     for s in raw_formula:
#         if s in string.ascii_letters:
#             variables_list.append(s)


#     variables_set = list(set(variables_list))

#     choosen_one = random.choice(variables_set)

#     constants = [x for x in variables_set if x != choosen_one]

#     values_dict = {}


#     for s in constants:
#         n = random.randint(1, 100)
#         values_dict[s] = n

#     completed_formula = ""

#     for s in raw_formula:
#         replace_char = s
#         if s in constants:
#             replace_char = str(values_dict[s])
#         completed_formula += replace_char



#     sympy_eq = sympify("Eq(" + completed_formula.replace("=", ",") + ")")
#     answer = eval(str(solve(sympy_eq)[0]))
#     return completed_formula, values_dict, answer
