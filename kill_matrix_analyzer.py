import json
import numpy as np


def compare_kill_matrices(case: str):
    print(f"Starting case{case}")
    post_commit_file = "kills/approximation/case" + case + "/0/kill_matrix.np"
    post_kill_matrix = np.loadtxt(post_commit_file)
    pre_commit_file = "kills/approximation/case" + case + "/1/kill_matrix.np"
    pre_kill_matrix = np.loadtxt(pre_commit_file)

    mutation_index_json = {}
    with open("kills/approximation/case" + case + "/0/mutation_index.json", "r") as f:
        mutation_index_json = json.load(f)
    index_mutation_mapping = {v: k for k, v in mutation_index_json.items()}
    print(index_mutation_mapping)

    # compare post_kill_matrix, pre_kill_matrix, and record the column index of the element that is different

    record = []
    print(post_kill_matrix.shape)
    for i in range(post_kill_matrix.shape[1]):
        for j in range(post_kill_matrix.shape[0]):
            if post_kill_matrix[j][i] != pre_kill_matrix[j][i]:
                record.append((i, index_mutation_mapping[i]))
                break

    print("==========CD-To-DD==========")
    print(record)
    if len(record)==0:
        print("No difference")
        print(case)
        return
    commit_relevant_mutation_index = {}
    with open("kills/case" + case + "/cd_to_dd/mutation_index.json", "r") as f:
        commit_relevant_mutation_index = json.load(f)
    print(commit_relevant_mutation_index)
    overlapped_mutants = [x for x in record if x[1] in commit_relevant_mutation_index]
    print(overlapped_mutants)

    precision = len(overlapped_mutants) / len(commit_relevant_mutation_index)
    recall = len(overlapped_mutants) / len(record)

    print("precision: ", precision)
    print("recall: ", recall)

    print("==========No-CD-To-DD==========")

    commit_relevant_mutation_index = {}
    with open("kills/case" + case + "/no_cd_to_dd/mutation_index.json", "r") as f:
        commit_relevant_mutation_index = json.load(f)
    print(commit_relevant_mutation_index)
    overlapped_mutants = [x for x in record if x[1] in commit_relevant_mutation_index]
    print(overlapped_mutants)

    precision = len(overlapped_mutants) / len(commit_relevant_mutation_index)
    recall = len(overlapped_mutants) / len(record)

    print("precision: ", precision)
    print("recall: ", recall)


if __name__ == "__main__":
    for i in range(1, 8):
        compare_kill_matrices(str(i))
