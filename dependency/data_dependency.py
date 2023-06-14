import ast
from copy import deepcopy

from .common import Separator, Remover

class DDVisitor(ast.NodeVisitor):
    def __init__(self):
        self.deps = {}

    def add_dependency(self, key, value):
        if key not in self.deps:
            self.deps[key] = []
        if value not in self.deps[key]:
            self.deps[key].append(value)
        if value in self.deps:
            self.deps[key] += self.deps[value]

    def add_assignment(self, target, value):

        if target.id not in self.deps:
            self.deps[target.id] = []
        
        if isinstance(value, ast.Name):
            self.add_dependency(target.id, value.id)

        elif isinstance(value, ast.Call):
            for arg in value.args:
                if isinstance(arg, ast.Name):
                    self.add_dependency(target.id, arg.id)

        elif isinstance(value, ast.BinOp):
            if isinstance(value.left, ast.Name):
                self.add_dependency(target.id, value.left.id)
            if isinstance(value.right, ast.Name):
                self.add_dependency(target.id, value.right.id)

        elif isinstance(value, ast.UnaryOp):
            if isinstance(value.operand, ast.Name):
                self.add_dependency(target.id, value.operand.id)

        elif isinstance(value, ast.Compare):
            if isinstance(value.left, ast.Name):
                self.add_dependency(target.id, value.left.id)
            if isinstance(value.right, ast.Name):
                self.add_dependency(target.id, value.right.id)

        elif isinstance(value, ast.BoolOp):
            for operand in value.values:
                if isinstance(operand, ast.Name):
                    self.add_dependency(target.id, operand.id)

    def generic_visit(self, node):

        if isinstance(node, ast.Assign):
            for target in node.targets:

                if isinstance(target, ast.Name):
                    self.add_assignment(target, node.value)

                elif isinstance(target, ast.Tuple) and not isinstance(node.value, ast.Call):
                    for t_elt, v_elt in zip(target.elts, node.value.elts):
                        if isinstance(t_elt, ast.Name):
                            self.add_assignment(t_elt, v_elt)

        ast.NodeVisitor.generic_visit(self, node)

def get_dd(code):

    res = {}

    tree = ast.parse(code)

    separator = Separator()
    separator.visit(tree)
    
    rest_tree = deepcopy(tree)
    remover = Remover(separator.functions)
    remover.visit(rest_tree)

    for x in separator.functions + [rest_tree]:
        dep_visitor = DDVisitor()
        dep_visitor.visit(x)

        if isinstance(x, ast.FunctionDef):
            res[x.name] = dep_visitor.deps
        else:
            res["main"] = dep_visitor.deps

    return res

# TODO: Move to tests
'''def main():
    
    if len(sys.argv) < 2:   
        print("Usage: python dependency.py <input_file>")
        return
    
    input_file = sys.argv[1]
    
    if not os.path.exists(input_file):
        print("Input file does not exist")
        return
    
    with open(input_file, "r") as f:
        code = f.read()
    
    res = get_dependencies(code)
    print(res)

if __name__ == "__main__":
    main()'''