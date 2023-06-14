import ast
from utils import compare_ast

class Separator(ast.NodeVisitor):
    def __init__(self):
        self.functions = []
        self.rest = []

    def generic_visit(self, node):
        super().generic_visit(node)

        if isinstance(node, ast.FunctionDef):
            self.functions.append(node)

class Remover(ast.NodeTransformer):
    def __init__(self, functions):
        self.functions = functions
    
    def visit_FunctionDef(self, node):
        for function in self.functions:
            if compare_ast(node, function):
                return None
        return node