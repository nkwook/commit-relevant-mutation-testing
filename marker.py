import ast
import sys
import os

from dependency import get_dependencies
from utils import compare_ast, relevant

class Marker():
    def __init__(self, tree):
        self.tree = tree
        self.deps = get_dependencies(tree)
        self.marked_nodes = []

    def retrieve_marked_nodes(self):
        """
        Retrieve nodes that are marked.
        """
        class MarkedVisitor(ast.NodeVisitor):
            def __init__(self):
                self.marked_nodes = []

            def generic_visit(self, node):
                if hasattr(node, "commit_relevant") and node.commit_relevant:
                    self.marked_nodes.append(node)

                super().generic_visit(node)

        visitor = MarkedVisitor()
        visitor.visit(self.tree)
        self.marked_nodes = visitor.marked_nodes
    
    def mark_function(self, node):

        marked_nodes_in_f = []
        for x in node.body:
            for y in self.marked_nodes:
                if compare_ast(x, y):
                    marked_nodes_in_f.append(x)
                    break
    
        marked_vars = set()
        for marked_node in marked_nodes_in_f:
            for varname in self.deps[node.name]:
                if relevant(marked_node, varname):
                    marked_vars.add(varname)

        class MarkerVisitor(ast.NodeVisitor):
            def __init__(self):
                self.to_mark_nodes = []
            
            def generic_visit(self, node):
                super().generic_visit(node)

                if isinstance(node, ast.FunctionDef):
                    return

                for marked_var in marked_vars:
                    if relevant(node, marked_var):
                        node.commit_relevant = True
                        self.to_mark_nodes.append(node)
                        break
                
        
        visitor = MarkerVisitor()
        visitor.visit(node)

        return visitor.to_mark_nodes

    def mark(self):
        to_mark_nodes = []

        for node in ast.iter_child_nodes(self.tree):
            if isinstance(node, ast.FunctionDef):
                to_mark_nodes += self.mark_function(node)
            #TODO: handle main
            '''else:
                for varname in self.deps["main"]:
                    if relevant(node, varname):
                        to_mark_nodes.append(node)
                        break'''

        class MarkerVisitor(ast.NodeVisitor):
            def generic_visit(self, node):
                for to_mark_node in to_mark_nodes:
                    if compare_ast(node, to_mark_node):
                        node.commit_relevant = True
                        break
                super().generic_visit(node)

        visitor = MarkerVisitor()
        visitor.visit(self.tree)

    def execute(self):
        self.retrieve_marked_nodes()
        self.mark()