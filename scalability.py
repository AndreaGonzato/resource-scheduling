import os
import re

"""
This script analise all the solution and create a plot to know how the resolution time grow with the complexity of the problem
"""
# Specify the directory you want to list files from
directory = 'solutions/'

# List all files in the directory
file_list = os.listdir(directory)

complexity_time_data = {}

solutions = len(file_list)-1
print(solutions)

for i in range(len(file_list)):

    if file_list[i] == "infeasible":
        continue


    pattern = r'complexity([\d.]+)'
    match = re.search(pattern, file_list[i])
    if match:
        # Extract the number from the matched group
        complexity = int(match.group(1))
    else:
        raise ValueError(f"incorrect file name: {file_list[i]}")


    with open(f"solutions/{file_list[i]}", "r") as file:
        file.readline()
        file.readline()
        file.readline()
        content = file.readline()

        # Regular expression to match the number
        pattern = r'Solver runtime: ([\d.]+) seconds'

        # Search for the pattern in the text
        match = re.search(pattern, content)

        if match:
            # Extract the number from the matched group
            time = float(match.group(1))
            if complexity not in complexity_time_data:
                complexity_time_data[complexity] = []
            complexity_time_data[complexity].append(time)
        else:
            raise ValueError(f"no found runtime time for file: {file_list[i]}")

# compute the average
data = {}
print(complexity_time_data)
for k, times_list in complexity_time_data.items():
    average = sum(times_list) / len(times_list)
    data[k] = average

print(data)

import matplotlib.pyplot as plt

# Keys and values
keys = data.keys()
values = data.values()

# Create a line plot
plt.plot(keys, values, marker='o', linestyle='none')  # 'o' adds markers to each point

# Adding labels (optional)
plt.xlabel('Complexity')
plt.ylabel('Time')

filename = 'img/scalability.png'

# Save the plot to the file
plt.savefig(filename)

# Show plot
plt.show()