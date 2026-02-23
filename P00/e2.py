from Seq0 import seq_read_fasta
if __name__ == "__main__":
    filename = input("Enter a file: ")
    name = filename + ".txt"
    seq_read_fasta(name)