from Seq1 import Seq
gen_list = ["FRAT1", "U5", "ADA", "FXN", "RNU6_269P"]
print("-----| Practice 1, Exercise 10 |------")
for gen in gen_list:
    s = Seq()
    filename = gen + ".txt"
    s.read_fasta(filename)
    most_frequent = s.frequent_base()
    print(f"Gene {gen}: Most frequent Base: {most_frequent}")