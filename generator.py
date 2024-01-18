# Writing to a text file in Python

# Define the filename
filename = "data/instance_1.txt"

# Define the text to be written
text = "Hello, this is a sample text written to the file."

# Open the file in write mode
with open(filename, "w") as file:
    # Write the text to the file
    file.write(text)

print(f"Text written to {filename}")