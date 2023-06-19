import ast
from copy import deepcopy

from .common import Separator, Remover
from utils import relevant, get_vars, compare_ast


class CDVisitor(ast.NodeVisitor):
    def __init__(self, marked_nodes, bounded_set):
        self.marked_nodes = marked_nodes
        self.bounded_set = bounded_set

    def generic_visit(self, node):
        # if the node has test attribute
        if hasattr(node, "test"):
            for x in ast.walk(node):
                for y in self.marked_nodes:
                    if compare_ast(x, y):
                        for test_item in ast.walk(node.test):
                            test_item.commit_relevant = True
                            if type(test_item) is ast.Name:
                                self.bounded_set.add(test_item)

        ast.NodeVisitor.generic_visit(self, node)
