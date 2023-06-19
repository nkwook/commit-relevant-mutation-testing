import argparse
import json
import os
import subprocess
from ast import unparse
from collections import defaultdict
from typing import Dict, List

import numpy as np
from pprint import pprint

from approximate_relevant_mutants import InitMutatorId, MutantIdMarker
from diff_processor import generate_diff, mark_ast_on_diff, parse_diff_lineno
from mutation_testing import Mutation, generate_diffs, generate_mutation_metadata, generate_test_metadata

PARENT_COMMIT_HASH = "f4d0f77"
CHILD_COMMIT_HASH = "9500577"
# DIFF_FILE = "diff/samples_case7_case7.txt"
DIFF_FILE = "diff/samples_case7_case7.txt"
PRE_COMMIT_SOURCE_FILE = "samples/pre_commits/case7/case7.py"
POST_COMMIT_SOURCE_FILE = "samples/case7/case7.py"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mutation Testing Tool.")
    parser.add_argument("-a", "--action", choices=["mutate", "execute"], required=True)
    # parser.add_argument("-s", "--source", type=str, required=True)
    parser.add_argument("-m", "--mutants", type=str, required=False)
    parser.add_argument("-k", "--kill", type=str)

    args = parser.parse_args()
    # python pmut.py --action execute --source target/bar --kill ./kills
    if args.action == "execute" and not args.kill:
        parser.error("Mutant execution action requires -k/--kill")

    if args.action == "execute" and not os.path.exists(args.kill):
        os.mkdir(args.kill)
        os.mkdir(args.kill + "/0")
        os.mkdir(args.kill + "/1")

    if args.action == "mutate" and not os.path.exists(args.mutants):
        os.mkdir(args.mutants)

    # source = args.source

    # files = []
    # for f in os.listdir(source):
    #     if f.endswith(".py"):
    #         files.append(os.path.join(source, f))

    for i, f in enumerate([POST_COMMIT_SOURCE_FILE, PRE_COMMIT_SOURCE_FILE]):
        num_mutants = 0
        mutation_index = {}
        global_mutant_records = defaultdict(dict)
        source = "/".join(f.split("/")[:-1])


        mutant_records = defaultdict(list)
        generate_diff(PARENT_COMMIT_HASH, CHILD_COMMIT_HASH)
        modified_list = parse_diff_lineno(DIFF_FILE)[i]
        print(modified_list)

        root = mark_ast_on_diff(f, modified_list)

        nodes_dict = {}

        init_mutator_id = InitMutatorId()
        mutator_marker = MutantIdMarker(nodes_dict)

        init_mutator_id.visit(root)
        mutator_marker.visit(root)

        mutation = Mutation(root, mutant_records, commit_aware=False, mark_mutant_id=True)
        mutation.visit(root)

        target_filename = f.split("/")[-1].split(".")[0]

        if args.action == "mutate":
            num_mutants += sum([len(mutants) for mutants in mutant_records.values()])

            diff_dir = args.mutants + "/" + str(i) + "/" + target_filename
            generate_diffs(f, diff_dir, root, mutant_records)
            # generate_diffs(f, diff_dir, pre_commit_root, mutant_records)
            # print(f"Total number of mutated files: {len(files)}")
            print(f"Total number of mutants generated: {num_mutants}")

        elif args.action == "execute":
            global_mutant_records[target_filename] = mutant_records

            mutation_metadata_dict, mutation_index_dict = generate_mutation_metadata(global_mutant_records)

            test_metadata_dict, test_index_dict = generate_test_metadata(f)
            print(test_metadata_dict, test_index_dict)

            # exec test codes with mutants
            killed_dict: Dict[str, int] = dict()
            global_killed_dict: List[Dict] = list()

            # {'mutated_root': <ast.Module object at 0x1164f9b20>, 'mutated_code': '    for i in range(n + 1):', 'type': 'MATH', 'key': 'lazy_MATH_03_00'}

            total_tests = 0
            total_killed_mutants = 0
            kill_matrix = np.zeros((len(test_index_dict.keys()), len(mutation_index_dict.keys())), dtype=int)
            output = []
            for target_file_name, mutation_metadata_list in mutation_metadata_dict.items():
                print(f"execute target: {target_file_name}")
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

                        test_num_line = [line for line in result_lines if "collected" and "item" in line]
                        total_killed_mutants += len(failed_test_indicies)
                        total_tests += int(test_num_line[0].split(" ")[1])

                        os.chdir(curr)

                    kill_matrix[failed_test_indicies, mutation_index_dict[mutation_metadata["key"]]] = 1

                    with open(file_path_to_mutate, "w") as f:
                        f.write(original_code)

            # with open("output.txt", "w") as f:
            #     f.write("\n".join(output))
            kill_dir = args.kill + "/" + str(i)
            with open(os.path.join(kill_dir, "test_index.json"), "w") as f:
                json.dump(test_index_dict, f)
            with open(os.path.join(kill_dir, "mutation_index.json"), "w") as f:
                json.dump(mutation_index_dict, f)
            np.savetxt(os.path.join(kill_dir, "kill_matrix.np"), kill_matrix, fmt="%d")
            print(f"Total test functions found: {len(test_index_dict.keys())}")

            kill_aggregate = list(kill_matrix.sum(axis=0))
            num_killed_mutants = 0
            for k in kill_aggregate:
                if k > 0:
                    num_killed_mutants += 1
            print(f"Total killed mutants: {num_killed_mutants}")

            mutation_score = f"{(num_killed_mutants/len(mutation_index_dict.keys()))*100:05.2f}"

            print(f"Mutation score: {mutation_score}% ({num_killed_mutants} / {len(mutation_index_dict.keys())})")
