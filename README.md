# commit-relevant-mutation-testing

## Without commit-aware
```bash
# mutate
python3 mutation_testing.py --action mutate --source sample --mutants ./mutation_diffs 
# execute
python mutation_testing.py --action execute --source sample --kill ./kills 
```

## With commit-aware
```bash
# mutate
python3 mutation_testing.py --action mutate --source sample --mutants ./mutation_diffs --commit_aware --parent [PARENT_COMMIT_HASH] --child [CHILD_COMMIT_HASH]
# execute
python mutation_testing.py --action execute --source sample --kill ./kills --commit_aware  --parent [PARENT_COMMIT_HASH] --child [CHILD_COMMIT_HASH]
```