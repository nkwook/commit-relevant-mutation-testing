from itertools import zip_longest
from typing import Union
import ast

# thanks to https://stackoverflow.com/questions/3312989/elegant-way-to-test-python-asts-for-equality-not-reference-or-object-identity
def compare_ast(node1: Union[ast.expr, list[ast.expr]], node2: Union[ast.expr, list[ast.expr]]) -> bool:
    if type(node1) is not type(node2):
        return False

    if isinstance(node1, ast.AST):
        for k, v in vars(node1).items():
            if k in {"lineno", "end_lineno", "col_offset", "end_col_offset", "ctx"}:
                continue
            if not compare_ast(v, getattr(node2, k)):
                return False
        return True

    elif isinstance(node1, list) and isinstance(node2, list):
        return all(compare_ast(n1, n2) for n1, n2 in zip_longest(node1, node2))
    else:
        return node1 == node2

def relevant(node, varname):
    """
    Check if a node is relevant to a variable.
    """
    class RelevantVisitor(ast.NodeVisitor):
        def __init__(self):
            self.relevant = False

        def visit_Name(self, node):
            if node.id == varname:
                self.relevant = True

    visitor = RelevantVisitor()
    visitor.visit(node)
    return visitor.relevant

def get_vars(node):
    """
    Get all variables in a node.
    """
    class VarVisitor(ast.NodeVisitor):
        def __init__(self):
            self.vars = set()

        def visit_Name(self, node):
            self.vars.add(node.id)

    visitor = VarVisitor()
    visitor.visit(node)
    return visitor.vars