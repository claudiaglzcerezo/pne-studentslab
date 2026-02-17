from pathlib import Path
FILENAME = "sequences/U5.txt"
file_contents = Path(FILENAME).read_text()
split_content = file_contents.split("\n")
print("The body of U5.txt file: ", split_content[1:-1])