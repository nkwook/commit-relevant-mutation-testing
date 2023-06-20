# Commit-aware Selective Mutation Testing

## Abstract

Mutation testing is one of the most powerful testing methods that can check the quality of the existing test sets. However, In today’s frequent distribution situations using CI/CD, naive random mutation testing is neither feasible nor scalable as it creates mutations not only from changed code but also from the parts irrelevant with the changes.  
As a result, many studies related to the reduced cost of mutation testing are underway, but we can’t use them directly in CI/CD because most of them depend on machine learning or the whole execution of mutation.  
We start with changed parts of the source code and gradually expand to parts that are relevant to changes. By only creating mutations from the “commit-relevant” part, our method can reduce the cost of mutation testing and we think this is more suitable testing for the CI/CD environment.

## Experiments

Basically, run `experiment.sh`. Source codes are located in `samples` directory.

### Mutation Testing without Commit Relevant Option
```bash
# mutate
python3 mutation_testing.py --action mutate --source [SOURCE_DIR] --mutants [DIR_TO_SAVE_MUTANTS] 
# execute
python mutation_testing.py --action execute --source [SOURCE_DIR] --kill [DIR_TO_SAVE_TEST_METADATA] 
```

### Commit-relevant Mutation Testing
```bash
# mutate
python3 mutation_testing.py --action mutate --source [SOURCE_DIR] --mutants [DIR_TO_SAVE_MUTANTS] --commit_aware --parent [PARENT_COMMIT_HASH] --child [CHILD_COMMIT_HASH] --cd_to_dd | --no-cd_to_dd
# execute
python mutation_testing.py --action execute --source [SOURCE_DIR] --kill [DIR_TO_SAVE_TEST_METADATA] --commit_aware  --parent [PARENT_COMMIT_HASH] --child [CHILD_COMMIT_HASH] --cd_to_dd | --no-cd_to_dd
```
- `--cd_to_dd` is for S4 algorithm in the work, and `--no-cd_to_dd` is for S3.

### Extracting metadata for obtaining Commit-relevant Mutants in *Ma et al(2020).*
```bash
python approximate_mutation_testing.py --action execute --kill [DIR_TO_SAVE_TEST_METADATA --parent [PARENT_COMMIT_HASH] --child [CHILD_COMMIT_HASH] --diff [DIFF_FILE_PATH] --pre_commit [PRE_COMMIT_SOURCE_PATH] --post_commit [POST_COMMIT_SOURCE_PATH]
```

### Analyze Test Metadata(Result for RQ1)
```bash
python kill_matrix_analyzer.py
```

## PS
- We added the final presentation slides and the report under the `pdf` repository.
