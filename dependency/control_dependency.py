import ast
from copy import deepcopy

from .common import Separator, Remover
from utils import relevant, get_vars

class CDVisitor(ast.NodeVisitor):
    def __init__(self, marked_vars):
        self.marked_vars = marked_vars

    def generic_visit(self, node):

        # if the node has test attribute
        if hasattr(node, "test"):
            for marked_var in self.marked_vars:
                if relevant(node.test, marked_var):
                    node.commit_relevant = True

        ast.NodeVisitor.generic_visit(self, node)