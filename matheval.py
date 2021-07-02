# Portions of code used under license from https://github.com/danthedeckie/simpleeval/

import ast
import operator as op
import math
import random
from fractions import Fraction

MAX_LIST_LEN = 250

def safepower(a, b):
    if hasattr(a, "__abs__") and hasattr(b, "__abs__"):
        if abs(a) > 256 or abs(b) > 128:
            raise ValueError("{}^{} is too large".format(a, b))
    return op.pow(a, b)

def safemult(a, b):
    if hasattr(a, '__len__') and b * len(a) > MAX_LIST_LEN:
        raise ValueError("iterable of length {} is too long".format(b * len(a)))
    if hasattr(b, '__len__') and a * len(b) > MAX_LIST_LEN:
        raise ValueError("iterable of length {} is too long".format(a * len(b)))
    return op.mul(a, b)

def safeadd(a, b):
    if hasattr(a, '__len__') and hasattr(b, "__len__") and len(a) + len(b) > MAX_LIST_LEN:
        raise ValueError("iterable of length {} is too long".format(len(a) + len(b)))
    return op.add(a, b)

def fracdiv(a, b):
    return Fraction(a, b)

def numer(x):
    if hasattr(x, "numerator"):
        return x.numerator
    else:
        raise ValueError("cannot access numerator")

def denom(x):
    if hasattr(x, "denominator"):
        return x.denominator
    else:
        raise ValueError("cannot access denominator")

def fraction(a, b=None):
    return Fraction(a, b).limit_denominator()

def rand(l=None):
    if l is None:
        return random.random()
    else:
        return int(random.random()*l)

operators = {
    ast.Add: safeadd, 
    ast.Sub: op.sub, 
    ast.Mult: safemult,
    ast.Div: op.truediv, 
    ast.FloorDiv: fracdiv,
    ast.Pow: safepower,
    ast.USub: op.neg,
    ast.UAdd: op.pos,
    ast.Eq: op.eq,
    ast.NotEq: op.ne,
    ast.Gt: op.gt,
    ast.Lt: op.lt,
    ast.GtE: op.ge,
    ast.LtE: op.le,
    ast.Not: op.not_,
}

names = {
    "True": True, 
    "False": False, 
    "None": None, 
    "e": math.e, 
    "pi": math.pi,
    "tau": math.tau,

    "random": rand,
    "sqrt": math.sqrt,
    "gcd": math.gcd, "lcm": math.lcm,
    "floor": math.floor, "ceil": math.ceil, "round": round,
    "exp": math.exp, "log": math.log, 
    "sin": math.sin, "cos": math.cos, "tan": math.tan,
    "asin": math.asin, "acos": math.acos, "atan": math.atan,
    "sinh": math.sin, "cosh": math.cos, "tanh": math.tan,
    "asinh": math.asin, "acosh": math.acos, "atanh": math.atan,
    "atan2": math.atan2,
    "int": int,
    "float": float,
    "complex": complex,
    "fraction": fraction,
    "str": str,
    "numer": numer, "denom": denom,
}

def eval_expr(expr):
    if len(expr) > 1000:
        raise ValueError("expression is too long")
    return _eval(ast.parse(expr, mode='eval').body)

def _eval(node):
    if isinstance(node, ast.Num):
        return node.n
    elif isinstance(node, ast.Str):
        if len(node.s) > MAX_LIST_LEN:
            raise ValueError("string literal is too long")
        return node.s
    elif isinstance(node, ast.Name):
        try:
            return names[node.id]
        except KeyError:
            raise NameError("unknown variable: {}".format(node.id))
    elif isinstance(node, ast.Call):
        try:
            fn = names[node.func.id]
            return fn(
                *(_eval(a) for a in node.args),
                **dict(_eval(k) for k in node.keywords)
            )
        except KeyError:
            raise NameError("unknown function: {}".format(node.func.id))
    elif isinstance(node, ast.BinOp):
        try:
            return operators[type(node.op)](_eval(node.left), _eval(node.right))
        except KeyError:
            raise SyntaxError("unsupported operation: {}".format(node.op.__class__.__name__))
    elif isinstance(node, ast.BoolOp):
        if isinstance(node.op, ast.And):
            res = False
            for value in node.values:
                res = _eval(value)
                if not res:
                    return res
            return res
        elif isinstance(node.op, ast.Or):
            for value in node.values:
                res = _eval(value)
                if res:
                    return res
            return res
    elif isinstance(node, ast.UnaryOp):
        try:
            return operators[type(node.op)](_eval(node.operand))
        except KeyError:
            raise SyntaxError("unsupported operation: {}".format(node.op.__class__.__name__))
    elif isinstance(node, ast.Compare):
        try:
            right = _eval(node.left)
            ret = True
            for operation, comp in zip(node.ops, node.comparators):
                if not ret:
                    break
                left = right
                right = _eval(comp)
                ret = operators[type(operation)](left, right)
            return ret
        except KeyError:
            raise SyntaxError("unsupported operation: {}".format(node.op.__class__.__name__))
    elif isinstance(node, ast.List):
        if len(node.elts) > MAX_LIST_LEN:
            raise ValueError("iterable of length {} is too long".format(len(node.elts)))
        return list(_eval(x) for x in node.elts)
    elif isinstance(node, ast.Tuple):
        if len(node.elts) > MAX_LIST_LEN:
            raise ValueError("iterable of length {} is too long".format(len(node.elts)))
        return tuple(_eval(x) for x in node.elts)
    elif isinstance(node, ast.Set):
        if len(node.elts) > MAX_LIST_LEN:
            raise ValueError("iterable of length {} is too long".format(len(node.elts)))
        return set(_eval(x) for x in node.elts)
    elif isinstance(node, ast.Dict):
        if len(node.keys) > MAX_LIST_LEN:
            raise ValueError("iterable of length {} is too long".format(len(node.elts)))
        return {_eval(k): _eval(v) for (k, v) in zip(node.keys, node.values)}
    else:
        raise TypeError("unsupported syntax: {}".format(node.__class__.__name__))




