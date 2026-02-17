from pathlib import Path
FILENAME = "sequences/ADA.txt"
file_contents = Path(FILENAME).read_text()
split_content = file_contents.split("\n")
body = split_content[1:-1]
sequence = "".join(body)
print(len(sequence))
