import ast
from copy import deepcopy

from .common import Separator, Remover

class CDVisitor(ast.NodeVisitor):
    def __init__(self):
        self.deps = {}

    def add_dependency(self, key, value):
        if key not in self.deps:
            self.deps[key] = []
        if value not in self.deps[key]:
            self.deps[key].append(value)
        if value in self.deps:
            self.deps[key] += self.deps[value]

    def generic_visit(self, node):

        # if the node has test attribute
        if hasattr(node, "test"):
            # add dependency between the variables used in the body and the variables used in the test
            for var in node.test.variables:
                for body_var in node.body.variables:
                    self.add_dependency(body_var, var)

        ast.NodeVisitor.generic_visit(self, node)

def get_cd(code):

    res = {}

    tree = ast.parse(code)

    separator = Separator()
    separator.visit(tree)
    
    rest_tree = deepcopy(tree)
    remover = Remover(separator.functions)
    remover.visit(rest_tree)

    for x in separator.functions + [rest_tree]:
        dep_visitor = CDVisitor()
        dep_visitor.visit(x)

        if isinstance(x, ast.FunctionDef):
            res[x.name] = dep_visitor.deps
        else:
            res["main"] = dep_visitor.deps

    return res