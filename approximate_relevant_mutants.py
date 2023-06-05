from ast import AST, NodeVisitor
from diff_processor import generate_diff, mark_ast_on_diff, parse_diff_lineno

# by using ast.walk, mark id starting from 1 to the all the mutators in the ast
# and save the id and the corresponding mutator in a dictionary

pre_commit_nodes_dict = {}
post_commit_nodes_dict = {}

class InitMutatorId(NodeVisitor):
    def visit(self, node: AST) -> AST:
        node.mutator_id = -1
        return super().generic_visit(node)


class MutatorMarker(NodeVisitor):
    def __init__(self, mutator_dict: dict = {}):
        self.mutator_id = 1
        self.mutator_dict = mutator_dict

    def generic_visit(self, node: AST) -> AST:
        if hasattr(node, "mutator_id"):
            node.mutator_id = self.mutator_id
            self.mutator_dict[self.mutator_id] = node
            # print(self.mutator_id)
            self.mutator_id += 1
        return super().generic_visit(node)


if __name__ == "__main__":
    generate_diff("c5118dd", "8fb7d5d")
    added_list, removed_list = parse_diff_lineno("diff/approximate_post_commit.txt")
    print(added_list, removed_list)
    post_commit_root = mark_ast_on_diff("approximate/post_commit.py", added_list)
    pre_commit_root = mark_ast_on_diff("approximate/pre_commit.py", removed_list)


    init_mutator_id = InitMutatorId()
    mutator_marker = MutatorMarker(pre_commit_nodes_dict)
    init_mutator_id.visit(pre_commit_root)
    mutator_marker.visit(pre_commit_root)

    mutator_marker = MutatorMarker(post_commit_nodes_dict)
    init_mutator_id.visit(post_commit_root)
    mutator_marker.visit(post_commit_root)

    print(len(pre_commit_nodes_dict.keys()))
    print(len(post_commit_nodes_dict.keys()))




