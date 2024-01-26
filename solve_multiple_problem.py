import os
from solver import solve_problem

# Specify the directory you want to list files from
directory = 'problems/'

# List all files in the directory
file_list = os.listdir(directory)

print(f"found {len(file_list)} problems")

for i in range(len(file_list)):
    if file_list[i] not in os.listdir("solutions/") and file_list[i] not in os.listdir("solutions/infeasible/"):
        # new problem to solve
        solve_problem(filename=file_list[i])
    if (i+1) % 5 == 0:
        print(f"solved\t{i+1} / {len(file_list)} problems")
print(f"solved all the problems")

