from ast import AST, NodeTransformer, NodeVisitor, parse, walk
import os
from typing import List
from astpretty import pprint
import subprocess
from import_processor import find_relevant_import


# generated diff between two commits using git diff commit_id1 commit_id2 > diff.txt
def generate_diff(commit_hash_1, commit_hash_2, diff_dir="diff"):
    if not os.path.exists(diff_dir):
        os.mkdir(diff_dir)

    command = f"git diff {commit_hash_1} {commit_hash_2} | ./showlinenum.awk"
    output = subprocess.run(command, shell=True, capture_output=True, text=True)
    diffs = [i for i in output.stdout.split("diff --git ") if len(i) > 0]
    # print(type(diffs))
    for diff in diffs:
        file_name = "_".join(diff.split("\n")[0].split(" ")[-1].strip(".py").split("/")[1:]) + ".txt"
        with open(f"{diff_dir}/{file_name}", "w") as f:
            f.write(diff)

def parse_diff_lineno(file_name):
    with open(file_name, "r") as f:
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
def mark_ast_on_diff(file_name, commit_aware_list: List[int]):
    # read sample.py
    code_list = []
    with open(file_name, "r") as f:
        code_list = f.readlines()

    root = parse("".join(code_list))
    # pprint(root)
    init_commit_flag = InitCommitFlag()
    init_commit_flag.visit(root)
    lineno_checker = LinenoChecker(commit_aware_list)
    lineno_checker.visit(root)

    # for node in walk(root):
    #     if hasattr(node, "commit_relevant"):
    #         if node.commit_relevant:
    # pprint(node)
    # print(f'commit relevant: {node.lineno}')
    return root


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
                # print(node.lineno)
        return super().generic_visit(node)

    # def visit(self, node: AST) -> AST:
    # node.lineno = -1
    # return super().generic_visit(node)


if __name__ == "__main__":
    diff = generate_diff("aab2d03", "4c5af64")
    # added_list, removed_list= save_diff_lineno()
    # mark_ast_on_diff(added_list)

    # print(diff)
