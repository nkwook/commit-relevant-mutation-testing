import ast
import sys
import os

from dependency.data_dependency import get_dd
from dependency.control_dependency import CDVisitor
from utils import compare_ast, relevant, Printer

class Marker():
    def __init__(self, tree):
        self.tree = tree
        self.data_deps = get_dd(tree)
        #self.cond_deps = get_cd(tree)
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
    
    def mark_dd_function(self, node):

        marked_nodes_in_f = []
        for x in node.body:
            for y in self.marked_nodes:
                if compare_ast(x, y):
                    marked_nodes_in_f.append(x)
                    break
    
        marked_vars = set()
        for marked_node in marked_nodes_in_f:
            for varname in self.data_deps[node.name]:
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

    def mark_dd(self):
        to_mark_nodes = []

        for node in ast.iter_child_nodes(self.tree):
            if isinstance(node, ast.FunctionDef):
                to_mark_nodes += self.mark_dd_function(node)
            #TODO: handle main
            '''else:
                for varname in self.data_deps["main"]:
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

    def mark_cd_function(self, node):

        marked_nodes_in_f = []

        for x in ast.walk(node):
            for y in self.marked_nodes:
                if compare_ast(x, y):
                    marked_nodes_in_f.append(x)
                    break
    
        visitor = CDVisitor(marked_nodes_in_f)
        visitor.visit(node)

    def mark_cd(self):
        to_mark_nodes = []

        for node in ast.iter_child_nodes(self.tree):
            if isinstance(node, ast.FunctionDef):
                self.mark_cd_function(node)
            #TODO: handle main


    def execute(self):
        self.retrieve_marked_nodes()
        self.mark_dd()
        self.mark_cd()

# TODO: Move to tests
def main():
    if len(sys.argv) < 2:
        print("Usage: python marker.py <file>")
        sys.exit(1)

    filename = sys.argv[1]
    if not os.path.isfile(filename):
        print("File not found!")
        sys.exit(1)

    with open(filename, "r") as f:
        tree = ast.parse(f.read())

    class InitMark(ast.NodeVisitor):
        def generic_visit(self, node):
            if ast.unparse(node) == "L = 1":
                node.commit_relevant = True
            super().generic_visit(node)

    visitor = InitMark()
    visitor.visit(tree)

    marker = Marker(tree)
    marker.execute()

    printer = Printer()
    printer.visit(tree)

if __name__ == "__main__":
    main()