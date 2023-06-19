python mutation_testing.py --action execute --source samples/post_commits/case1 --kill ./kills/case1/cd_to_dd --commit_aware  --parent 6c246de --child e067967 --cd_to_dd
python mutation_testing.py --action execute --source samples/post_commits/case1 --kill ./kills/case1/no_cd_to_dd --commit_aware  --parent 6c246de --child e067967 --no-cd_to_dd
python mutation_testing.py --action mutate --source samples/post_commits/case1 --mutants ./mutation_diffs/non_aware_case1
python mutation_testing.py --action execute --source samples/post_commits/case2 --kill ./kills/case2/cd_to_dd --commit_aware  --parent e067967 --child faca8c0 --cd_to_dd
python mutation_testing.py --action execute --source samples/post_commits/case2 --kill ./kills/case2/no_cd_to_dd --commit_aware  --parent e067967 --child faca8c0 --no-cd_to_dd
python mutation_testing.py --action mutate --source samples/post_commits/case2 --mutants ./mutation_diffs/non_aware_case2
python mutation_testing.py --action execute --source samples/post_commits/case3 --kill ./kills/case3/cd_to_dd --commit_aware  --parent faca8c0 --child ab60c0b --cd_to_dd
python mutation_testing.py --action execute --source samples/post_commits/case3 --kill ./kills/case3/no_cd_to_dd --commit_aware  --parent faca8c0 --child ab60c0b --no-cd_to_dd
python mutation_testing.py --action mutate --source samples/post_commits/case3 --mutants ./mutation_diffs/non_aware_case3
python mutation_testing.py --action execute --source samples/post_commits/case4 --kill ./kills/case4/cd_to_dd --commit_aware  --parent ab60c0b --child fe157cf --cd_to_dd
python mutation_testing.py --action execute --source samples/post_commits/case4 --kill ./kills/case4/no_cd_to_dd --commit_aware  --parent ab60c0b --child fe157cf --no-cd_to_dd
python mutation_testing.py --action mutate --source samples/post_commits/case4 --mutants ./mutation_diffs/non_aware_case4
python mutation_testing.py --action execute --source samples/post_commits/case5 --kill ./kills/case5/cd_to_dd --commit_aware  --parent fe157cf --child f37d61d --cd_to_dd
python mutation_testing.py --action execute --source samples/post_commits/case5 --kill ./kills/case5/no_cd_to_dd --commit_aware  --parent fe157cf --child f37d61d --no-cd_to_dd
python mutation_testing.py --action mutate --source samples/post_commits/case5 --mutants ./mutation_diffs/non_aware_case5
python mutation_testing.py --action execute --source samples/post_commits/case6 --kill ./kills/case6/cd_to_dd --commit_aware  --parent f37d61d --child 1b7ec33 --cd_to_dd
python mutation_testing.py --action execute --source samples/post_commits/case6 --kill ./kills/case6/no_cd_to_dd --commit_aware  --parent f37d61d --child 1b7ec33 --no-cd_to_dd
python mutation_testing.py --action mutate --source samples/post_commits/case6 --mutants ./mutation_diffs/non_aware_case6
python mutation_testing.py --action execute --source samples/post_commits/case7 --kill ./kills/case7/cd_to_dd --commit_aware  --parent 1b7ec33 --child 203a49c --cd_to_dd
python mutation_testing.py --action execute --source samples/post_commits/case7 --kill ./kills/case7/no_cd_to_dd --commit_aware  --parent 1b7ec33 --child 203a49c --no-cd_to_dd
python mutation_testing.py --action mutate --source samples/post_commits/case7 --mutants ./mutation_diffs/non_aware_case7


python approximate_mutation_testing.py --action execute --kill ./kills/approximation/case1 --parent 6c246de --child e067967 --diff diff/samples_post_commits_case1_case1.txt --pre_commit samples/pre_commits/case1/case1.py --post_commit samples/post_commits/case1/case1.py 
python approximate_mutation_testing.py --action execute --kill ./kills/approximation/case2 --parent e067967 --child faca8c0 --diff diff/samples_post_commits_case2_case2.txt --pre_commit samples/pre_commits/case2/case2.py --post_commit samples/post_commits/case2/case2.py 
python approximate_mutation_testing.py --action execute --kill ./kills/approximation/case3 --parent faca8c0 --child ab60c0b --diff diff/samples_post_commits_case3_case3.txt --pre_commit samples/pre_commits/case3/case3.py --post_commit samples/post_commits/case3/case3.py
python approximate_mutation_testing.py --action execute --kill ./kills/approximation/case4 --parent ab60c0b --child fe157cf --diff diff/samples_post_commits_case4_case4.txt --pre_commit samples/pre_commits/case4/case4.py --post_commit samples/post_commits/case4/case4.py 
python approximate_mutation_testing.py --action execute --kill ./kills/approximation/case5 --parent fe157cf --child f37d61d --diff diff/samples_post_commits_case5_case5.txt --pre_commit samples/pre_commits/case5/case5.py --post_commit samples/post_commits/case5/case5.py 
python approximate_mutation_testing.py --action execute --kill ./kills/approximation/case6 --parent f37d61d --child 1b7ec33 --diff diff/samples_post_commits_case6_case6.txt --pre_commit samples/pre_commits/case6/case6.py --post_commit samples/post_commits/case6/case6.py 
python approximate_mutation_testing.py --action execute --kill ./kills/approximation/case7 --parent 1b7ec33 --child 203a49c --diff diff/samples_post_commits_case7_case7.txt --pre_commit samples/pre_commits/case7/case7.py --post_commit samples/post_commits/case7/case7.py 
