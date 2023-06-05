import numpy as np

f="kills/post_commits/kill_matrix.npy"
kill_matrix = np.loadtxt(f )
# kill_matrix = np.load(f )


print(kill_matrix.shape)

# find index of kill_matrix where value of element is 1
def find():
    for i in range(kill_matrix.shape[0]):
        if kill_matrix[i] == 1:
            print(i)
            
find()