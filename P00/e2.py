from Seq0 import seq_read_fasta
if __name__ == "__main__":
    filename = input("Enter the file: ")
    name = filename + ".txt"
    print("The first 20 bases of", filename, "are:\n", seq_read_fasta(name))