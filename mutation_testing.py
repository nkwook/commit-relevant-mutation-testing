import argparse
import json
import os
import subprocess
from ast import (
    AST,
    Add,
    Assign,
    AugAssign,
    BinOp,
    BitAnd,
    BitOr,
    BitXor,
    Compare,
    Constant,
    Div,
    Eq,
    FunctionDef,
    Gt,
    GtE,
    LShift,
    Lt,
    LtE,
    Mod,
    Mult,
    NodeTransformer,
    NodeVisitor,
    NotEq,
    RShift,
    Return,
    Sub,
    USub,
    UnaryOp,
    copy_location,
    parse,
    unparse,
    walk
)
from copy import deepcopy
from collections import defaultdict
from tempfile import NamedTemporaryFile
from typing import Any, Dict, List, Tuple

import numpy as np

from diff_processor import generate_diff, mark_ast_on_diff, save_diff_lineno
from marker import Marker

CONDITIONALS_BOUNDARY = "CONDITIONALS-BOUNDARY"
INCREMENTS = "INCREMENTS"
INVERT_NEGS = "INVERT-NEGS"
MATH = "MATH"
NEGATE_CONDITONALS = "NEGATE-CONDITIONALS"
FALSE_RETURNS = "FALSE-RETURNS"
TRUE_RETURNS = "TRUE-RETURNS"
NULL_RETURNS = "NULL-RETURNS"
OBBN1 = "OBBN1"
OBBN2 = "OBBN2"
OBBN3 = "OBBN3"
CRCR1 = "CRCR1"
CRCR2 = "CRCR2"
CRCR3 = "CRCR3"
CRCR4 = "CRCR4"
CRCR5 = "CRCR5"
CRCR6 = "CRCR6"


mutant_records = defaultdict(list)
# python3 pmut.py --action mutate --source examples/example4 --mutants ./mutation_diffs


class Mutation(NodeVisitor):
    def __init__(self, root, commit_aware):
        self.root = root
        self.root_lines = unparse(root).split("\n")
        self.commit_aware = commit_aware

    def cond_bound_handler(self, node: Compare, mutations: List[AST]) -> None:
        for i, operator in enumerate(node.ops):
            operator_to_mutate = None
            if isinstance(operator, Lt):
                operator_to_mutate = LtE()
            elif isinstance(operator, LtE):
                operator_to_mutate = Lt()
            elif isinstance(operator, Gt):
                operator_to_mutate = GtE()
            elif isinstance(operator, GtE):
                operator_to_mutate = Gt()

            if operator_to_mutate:
                mutated_ops = deepcopy(node.ops)
                mutated_ops[i] = operator_to_mutate
                mutations.append(
                    (
                        Compare(
                            left=deepcopy(node.left),
                            ops=mutated_ops,
                            comparators=deepcopy(node.comparators),
                        ),
                        CONDITIONALS_BOUNDARY,
                    )
                )

    def neg_cond_handler(self, node: Compare, mutations: List[AST]) -> None:
        for i, operator in enumerate(node.ops):
            operator_to_mutate = None
            if isinstance(operator, Eq):
                operator_to_mutate = NotEq()
            elif isinstance(operator, NotEq):
                operator_to_mutate = Eq()
            elif isinstance(operator, LtE):
                operator_to_mutate = Gt()
            elif isinstance(operator, GtE):
                operator_to_mutate = Lt()
            elif isinstance(operator, Gt):
                operator_to_mutate = LtE()
            elif isinstance(operator, Lt):
                operator_to_mutate = GtE()

            if operator_to_mutate:
                mutated_ops = deepcopy(node.ops)
                mutated_ops[i] = operator_to_mutate
                mutations.append(
                    (
                        Compare(
                            left=deepcopy(node.left),
                            ops=mutated_ops,
                            comparators=deepcopy(node.comparators),
                        ),
                        NEGATE_CONDITONALS,
                    )
                )

    def increments_handler(self, node: AugAssign, mutations: List[AST]) -> None:
        operator_to_mutate = None
        if isinstance(node.op, Add):
            operator_to_mutate = Sub()
        elif isinstance(node.op, Sub):
            operator_to_mutate = Add()

        if operator_to_mutate:
            mutations.append(
                (
                    AugAssign(
                        target=deepcopy(node.target),
                        op=operator_to_mutate,
                        value=deepcopy(node.value),
                    ),
                    INCREMENTS,
                )
            )

    def invert_negs_handler(self, node: UnaryOp, mutations: List[AST]) -> None:
        if isinstance(node.op, USub):
            mutations.append((deepcopy(node.operand), INVERT_NEGS))

    def math_handler(self, node: BinOp, mutations: List[AST]) -> None:
        operator_to_mutate = None
        if isinstance(node.op, Add):
            operator_to_mutate = Sub()
        elif isinstance(node.op, Sub):
            operator_to_mutate = Add()
        elif isinstance(node.op, Mult):
            operator_to_mutate = Div()
        elif isinstance(node.op, (Div, Mod)):
            operator_to_mutate = Mult()
        elif isinstance(node.op, BitAnd):
            operator_to_mutate = BitOr()
        elif isinstance(node.op, (BitOr, BitXor)):
            operator_to_mutate = BitAnd()
        elif isinstance(node.op, LShift):
            operator_to_mutate = RShift()
        elif isinstance(node.op, RShift):
            operator_to_mutate = LShift()

        if operator_to_mutate:
            mutations.append(
                (
                    BinOp(
                        left=deepcopy(node.left),
                        op=operator_to_mutate,
                        right=deepcopy(node.right),
                    ),
                    MATH,
                )
            )

    def obbn_handler(self, node: BinOp, mutations: List[AST]):
        operator_to_mutate = None
        if isinstance(node.op, BitAnd):
            operator_to_mutate = BitOr()
        elif isinstance(node.op, (BitOr, BitXor)):
            operator_to_mutate = BitAnd()

        if operator_to_mutate:
            mutations.extend(
                [
                    (
                        BinOp(
                            left=deepcopy(node.left),
                            op=operator_to_mutate,
                            right=deepcopy(node.right),
                        ),
                        OBBN1,
                    ),
                    (
                        deepcopy(node.left),
                        OBBN2,
                    ),
                    (
                        deepcopy(node.right),
                        OBBN3,
                    ),
                ]
            )

    def false_returns_handler(self, node: Return, mutations: List[AST]) -> None:
        mutations.append((Return(value=Constant(value=False)), FALSE_RETURNS))

    def true_returns_handler(self, node: Return, mutations: List[AST]) -> None:
        mutations.append((Return(value=Constant(value=True)), TRUE_RETURNS))

    def null_returns_handler(self, node: Return, mutations: List[AST]) -> None:
        mutations.append((Return(value=Constant(value=None)), NULL_RETURNS))

    def crcr_handler(self, node: Assign, mutations: List[AST]) -> None:
        def return_assign(value: AST) -> AST:
            return Assign(targets=deepcopy(node.targets), value=value)

        node_value = node.value
        if isinstance(node_value, Constant) and isinstance(node_value.value, (int, float)):
            mutations.extend(
                [
                    (return_assign(Constant(value=1)), CRCR1),
                    (return_assign(Constant(value=0)), CRCR2),
                    (return_assign(Constant(value=-1)), CRCR3),
                    (return_assign(UnaryOp(op=USub(), operand=Constant(value=node_value.value))), CRCR4),
                    (
                        return_assign(BinOp(op=Add(), left=Constant(value=node_value.value), right=Constant(value=1))),
                        CRCR5,
                    ),
                    (
                        return_assign(BinOp(op=Sub(), left=Constant(value=node_value.value), right=Constant(value=1))),
                        CRCR6,
                    ),
                ]
            )
        else:
            mutations.extend(
                [
                    (return_assign(Constant(value=1)), CRCR1),
                    (return_assign(Constant(value=0)), CRCR2),
                    (return_assign(Constant(value=-1)), CRCR3),
                ]
            )

    def generic_visit(self, node: AST) -> None:
        mutations: List[AST] = list()
        if not self.commit_aware or node.commit_relevant:
            if isinstance(node, Compare):
                self.cond_bound_handler(node, mutations)
                self.neg_cond_handler(node, mutations)
            elif isinstance(node, AugAssign):
                self.increments_handler(node, mutations)
            elif isinstance(node, UnaryOp):
                self.invert_negs_handler(node, mutations), INVERT_NEGS
            elif isinstance(node, BinOp):
                self.math_handler(node, mutations)
                self.obbn_handler(node, mutations)
            elif isinstance(node, Return):
                self.false_returns_handler(node, mutations)
                self.true_returns_handler(node, mutations)
                self.null_returns_handler(node, mutations)
            elif isinstance(node, Assign) and isinstance(node.value, Constant):
                self.crcr_handler(node, mutations)

            for mutated_node, mutation_operator in mutations:
                generate_mutants = GenerateMutants(
                    mutated_node,
                    node.lineno,
                    node.col_offset,
                    node.end_lineno,
                    node.end_col_offset,
                )
                mutated_root = generate_mutants.visit(deepcopy(self.root))
                mutated_root_str = unparse(mutated_root)

                mutated_root_lines = mutated_root_str.split("\n")
                if self.root_lines[node.lineno - 1] != mutated_root_lines[node.lineno - 1]:
                    mutant_records[node.lineno].append(
                        {
                            "mutated_root": mutated_root,
                            "mutated_code": mutated_root_lines[node.lineno - 1],
                            "type": mutation_operator,
                        }
                    )

        super().generic_visit(node)


class GenerateMutants(NodeTransformer):
    def __init__(self, new_node, lineno, col_offset, end_lineno, end_col_offset):
        self.new_node = new_node
        self.lineno = lineno
        self.col_offset = col_offset
        self.end_lineno = end_lineno
        self.end_col_offset = end_col_offset

    def check_if_same_position(self, lineno, col_offset, end_lineno, end_col_offset):
        return (
            lineno == self.lineno
            and col_offset == self.col_offset
            and end_lineno == self.end_lineno
            and end_col_offset == self.end_col_offset
        )

    def generic_visit(self, node: AST) -> None:
        super().generic_visit(node)
        if not hasattr(node, "lineno"):
            return node
        if not self.check_if_same_position(node.lineno, node.col_offset, node.end_lineno, node.end_col_offset):
            return node

        copy_location(self.new_node, node)
        return self.new_node


# [target_filename]_[mutation_operator]_[line_number]_[index].diff
def generate_diffs(
    original_path: str, target_filename: str, root: AST, mutant_records: Dict[int, List[Dict[str, Any]]]
):
    unparsed_root = unparse(root)
    root_lines = unparsed_root.split("\n")

    def gen_file_name(target_filename, mutation_operator, lineno):
        str_lineno = str(lineno)
        if lineno < 10:
            str_lineno = f"0{lineno}"
        i = 0
        str_i = str(i)
        if i < 10:
            str_i = f"0{i}"
        file_name = f"{target_filename}_{mutation_operator}_{str_lineno}_{str_i}.diff"
        while os.path.exists(file_name):
            i += 1
            if i < 10:
                str_i = f"0{i}"
            file_name = f"{target_filename}_{mutation_operator}_{str_lineno}_{str_i}.diff"
        return file_name

    for lineno, mutants in mutant_records.items():
        for mutant in sorted(mutants, key=lambda x: x["mutated_code"]):
            # print(f"{lineno} {mutated_code}")
            mutation_operator = mutant["type"]
            diff_output = None
            mutant_path = None
            with NamedTemporaryFile(mode="w+", delete=False) as f:
                f.write(unparse(mutant["mutated_root"]))
                mutant_path = f.name

            diff_output = os.popen(f"diff {os.path.abspath(original_path)} {mutant_path}").read()

            with open(gen_file_name(target_filename, mutation_operator, lineno), "w") as f:
                f.write(diff_output)


def generate_mutation_metadata(
    global_mutation_record: Dict[str, Dict[Tuple[int, int, int, int], List[Dict[str, Any]]]]
) -> Tuple[Dict[str, List], Dict[str, List]]:
    mutation_list = list()
    mutation_metadata = defaultdict(list)

    def gen_key(target_filename, mutation_operator, lineno):
        str_lineno = str(lineno)
        if lineno < 10:
            str_lineno = f"0{lineno}"
        i = 0
        str_i = str(i)
        if i < 10:
            str_i = f"0{i}"
        mutate_key = f"{target_filename}_{mutation_operator}_{str_lineno}_{str_i}"

        while mutate_key in [x["key"] for x in mutation_list]:
            i += 1
            if i < 10:
                str_i = f"0{i}"
            mutate_key = f"{target_filename}_{mutation_operator}_{str_lineno}_{str_i}"
        return mutate_key

    for target_filename, mutant_records in global_mutation_record.items():
        for lineno, mutants in mutant_records.items():
            for mutant in sorted(mutants, key=lambda x: x["mutated_code"]):
                mutation_operator = mutant["type"]
                mutate_key = gen_key(target_filename, mutation_operator, lineno)
                mutant["key"] = mutate_key
                mutation_list.append(mutant)

        mutation_metadata[target_filename] = sorted(
            [x for x in mutation_list if (target_filename in x["key"])], key=lambda x: x["key"]
        )
    mutation_list = sorted(mutation_list, key=lambda x: x["key"])
    mutation_index_dict = {x["key"]: i for i, x in enumerate(mutation_list)}
    return mutation_metadata, mutation_index_dict


# [test function name]@[pytest file name without .py]
def generate_test_metadata(source: str) -> Any:
    def gen_key(test_function_name, test_file_name):
        test_file_name = test_file_name.split("/")[-1].split(".")[0]
        return f"{test_function_name}@{test_file_name}"

    test_index_key_list: List[str] = list()
    test_index: Dict[str, int] = dict()
    test_metadata_dict = dict()

    for root, dirs, files in os.walk(source):
        for f in files:
            test_file = os.path.join(root, f)
            if not ("test" in test_file and test_file.endswith(".py")):
                continue
            lines = open(test_file, "r").readlines()
            # function_names = []
            ast_root = parse("".join(lines), test_file)
            for node in ast_root.body:
                if not isinstance(node, FunctionDef):
                    continue
                test_key = gen_key(node.name, test_file)
                test_index_key_list.append(test_key)

            test_metadata_dict[f] = {"code": ast_root, "path": test_file}

    test_index = {x: i for i, x in enumerate(sorted(test_index_key_list))}
    return test_metadata_dict, test_index


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mutation Testing Tool.")
    parser.add_argument("-a", "--action", choices=["mutate", "execute"], required=True)
    parser.add_argument("-s", "--source", type=str, required=True)
    parser.add_argument("-m", "--mutants", type=str, required=False)
    parser.add_argument("-c", "--commit_aware", action="store_true", required=False)
    parser.add_argument("-k", "--kill", type=str)

    args = parser.parse_args()
    # python pmut.py --action execute --source target/bar --kill ./kills
    if args.action == "execute" and not args.kill:
        parser.error("Mutant execution action requires -k/--kill")

    if args.action == "execute" and not os.path.exists(args.kill):
        os.mkdir(args.kill)

    if args.action == "mutate" and not os.path.exists(args.mutants):
        os.mkdir(args.mutants)

    source = args.source

    files = []
    for f in os.listdir(source):
        if f.endswith(".py"):
            files.append(os.path.join(source, f))

    num_mutants = 0
    global_mutant_records = defaultdict(dict)
    mutation_index = {}
    for f in files:
        mutant_records = defaultdict(list)
        lines = open(f, "r").readlines()
        root = parse("".join(lines), f)
        generate_diff("9919cf5", "7f454a5")

        added_list, removed_list = save_diff_lineno()
        print(added_list)
        marked_root = mark_ast_on_diff(added_list)

        print(args.commit_aware, type(args.commit_aware))

        if args.commit_aware:
            marker = Marker(marked_root)
            marker.execute()
            marked_root = marker.tree

        if args.commit_aware:
            mutation = Mutation(marked_root, True)
            mutation.visit(marked_root)
        else:
            mutation = Mutation(root, False)
            mutation.visit(root)
        target_filename = f.split("/")[-1].split(".")[0]

        if args.action == "mutate":
            num_mutants += sum([len(mutants) for mutants in mutant_records.values()])
            diff_dir = args.mutants + "/" + target_filename
            generate_diffs(f, diff_dir, root, mutant_records)
        elif args.action == "execute":
            global_mutant_records[target_filename] = mutant_records

    if args.action == "mutate":
        print(f"Total number of mutated files: {len(files)}")
        print(f"Total number of mutants generated: {num_mutants}")

    elif args.action == "execute":
        mutation_metadata_dict, mutation_index_dict = generate_mutation_metadata(global_mutant_records)
        test_metadata_dict, test_index_dict = generate_test_metadata(args.source)

        # exec test codes with mutants
        killed_dict: Dict[str, int] = dict()
        global_killed_dict: List[Dict] = list()

        # {'mutated_root': <ast.Module object at 0x1164f9b20>, 'mutated_code': '    for i in range(n + 1):', 'type': 'MATH', 'key': 'lazy_MATH_03_00'}

        total_tests = 0
        total_killed_mutants = 0
        kill_matrix = np.zeros((len(test_index_dict.keys()), len(mutation_index_dict.keys())), dtype=int)
        # print(mutation_metadata_dict.keys())
        output = []
        for target_file_name, mutation_metadata_list in mutation_metadata_dict.items():
            file_path_to_mutate = os.path.abspath(os.path.join(source, target_file_name)) + ".py"

            for mutation_metadata in mutation_metadata_list:
                original_code = None
                with open(file_path_to_mutate, "r") as f:
                    original_code = f.read()

                with open(file_path_to_mutate, "w") as f:
                    f.write(unparse(mutation_metadata["mutated_root"]))

                failed_test_indicies = []
                for test_metadata in test_metadata_dict.values():
                    test_path = test_metadata["path"]
                    env = os.environ.copy()
                    env["PYTHONDONTWRITEBYTECODE"] = "1"
                    env["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"

                    curr = os.getcwd()
                    os.chdir(os.path.abspath(os.path.dirname(test_path)))
                    result = subprocess.run(
                        ["pytest", "-p", "no:cacheprovider", "--color=no"],
                        env=env,
                        capture_output=True,
                    )

                    result_lines = result.stdout.decode("utf-8").split("\n")
                    # for r in result_lines:
                    #     print(r)
                    failed_lines = [line for line in result_lines if "FAILED" in line]
                    failed_tests = [
                        line.split("::")[1].split(" ")[0]
                        + "@"
                        + line.split("::")[0].split(".py")[0].split("FAILED ")[1]
                        for line in failed_lines
                    ]

                    failed_test_indicies.extend([test_index_dict[test] for test in failed_tests])

                    test_num_line = [line for line in result_lines if "collected" and "items" in line]
                    total_killed_mutants += len(failed_test_indicies)
                    total_tests += int(test_num_line[0].split(" ")[1])

                    os.chdir(curr)

                kill_matrix[failed_test_indicies, mutation_index_dict[mutation_metadata["key"]]] = 1

                with open(file_path_to_mutate, "w") as f:
                    f.write(original_code)

        # with open("output.txt", "w") as f:
        #     f.write("\n".join(output))
        with open(os.path.join(args.kill, "test_index.json"), "w") as f:
            json.dump(test_index_dict, f)
        with open(os.path.join(args.kill, "mutation_index.json"), "w") as f:
            json.dump(mutation_index_dict, f)
        np.savetxt(os.path.join(args.kill, "kill_matrix.np"), kill_matrix, fmt="%d")
        print(f"Total test functions found: {len(test_index_dict.keys())}")

        kill_aggregate = list(kill_matrix.sum(axis=0))
        num_killed_mutants = 0
        for k in kill_aggregate:
            if k > 0:
                num_killed_mutants += 1
        print(f"Total killed mutants: {num_killed_mutants}")

        mutation_score = f"{(num_killed_mutants/len(mutation_index_dict.keys()))*100:05.2f}"

        print(f"Mutation score: {mutation_score}% ({num_killed_mutants} / {len(mutation_index_dict.keys())})")
