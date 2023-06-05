from ast import AST, NodeTransformer, NodeVisitor, parse, walk
from typing import List
from astpretty import pprint
import subprocess

# generated diff between two commits using git diff commit_id1 commit_id2 > diff.txt
def generate_diff(commit_hash_1, commit_hash_2):
    command = f"git diff {commit_hash_1} {commit_hash_2} | ./showlinenum.awk > diff.txt"
    output = subprocess.run(command, shell=True, capture_output=True, text=True)
    return output


def save_diff_lineno():
    with open("diff.txt", "r") as f:
        diff = f.readlines()

    # gather lineno of added/removed lines which is formed line {lineno}:+ or {lineno}:-
    added_lineno = []
    removed_lineno = []
    curr_lineno = -1
    for line in diff:
        if len(line.split(":")) <= 1:
            continue
        if len(line.split(":")[0].strip()) > 0:
            curr_lineno = int(line.split(":")[0])
        if line.split(":")[1][0] == "+":
            added_lineno.append(curr_lineno)
        elif line.split(":")[1][0] == "-":
            removed_lineno.append(curr_lineno)
    return added_lineno, removed_lineno

# mark the variables in the AST which included in changed_lineno
def mark_ast_on_diff(changed_lineno):
    # read sample.py
    code_list=[]
    with open("sample.py", "r") as f:
        code_list = f.readlines()

    root=parse("".join(code_list))
    pprint(root)
    init_commit_flag = InitCommitFlag()
    init_commit_flag.visit(root)
    lineno_checker = LinenoChecker(added_list)
    lineno_checker.visit(root)

    for node in walk(root):
        if hasattr(node, "commit_relevant"):
            if node.commit_relevant:
                pprint(node)
                print(f'commit relevant: {node.lineno}')




class InitCommitFlag(NodeVisitor):
    def visit(self, node: AST) -> AST:
        node.commit_relevant = False
        return super().generic_visit(node)


class LinenoChecker(NodeVisitor):
    def __init__(self, commit_aware_list: List[int]):
        self.commit_aware_list = commit_aware_list
        
    def generic_visit(self, node: AST) -> AST:
        if hasattr(node, "lineno"):
            if node.lineno in self.commit_aware_list:
                # mark the node as commit relevant
                node.commit_relevant = True
                print(node.lineno)
        return super().generic_visit(node)
    
    # def visit(self, node: AST) -> AST:
        # node.lineno = -1
        # return super().generic_visit(node)



if __name__ == "__main__":
    # diff = generate_diff('7023d9642e47e643416e1f349ad7d9213c80d7f6', '3fb923593b7817390bde9ed4f7799886d0c7d5c6')
    added_list, removed_list= save_diff_lineno()
    mark_ast_on_diff(added_list)
    


    # print(diff)
