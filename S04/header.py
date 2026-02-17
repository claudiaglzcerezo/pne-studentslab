from pathlib import Path
FILENAME = "sequences/RNU6_269P.txt"
file_contents = Path(FILENAME).read_text()
split_content = file_contents.split("\n")
print("First line of the RNU6_269P.txt file: ", split_content[0])