from pathlib import Path

def seq_ping():
    print("OK")

def seq_read_fasta(filename):
    folder = "sequences/"
    file_contents = Path(folder + filename).read_text()
    split_content = file_contents.split("\n")
    result = "".join(split_content[1:-1])
    print(result[:20])

def  seq_len(seq):
    folder = "sequences/"
    seq_contents = Path(folder + seq).read_text()
    split_content = seq_contents.split("\n")
    result = ("".join(split_content[1:-1]))
    return len(result)

def seq_count_base(seq, base):
    folder = "sequences/"
    seq_contents = Path(folder + seq).read_text()
    split_content = seq_contents.split("\n")
    result = ("".join(split_content[1:-1]))
    count = 0
    for base in result:
        count = count + 1
    return count

