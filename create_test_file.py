import os 

files_dir = "server_files"


filename = os.path.join(files_dir, "test.txt")    

file = open(filename, "w")
i = 0

while i < 32617:
    file.write(f"Line {i}\n")
    i += 1

    