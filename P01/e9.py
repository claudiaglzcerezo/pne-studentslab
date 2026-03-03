from Seq1 import Seq
print("-----| Practice 1, Exercise 9 |------")
s = Seq()
gene = "U5"
filename = gene + ".txt"
s.read_fasta(filename)
print(f"Sequence: (Lenght: {s.len()}) {s}")
print(f"Bases: {s.count_dict()}")
print(f"Rev:{s.reverse()}")
print(f"Com:{s.complement()}")