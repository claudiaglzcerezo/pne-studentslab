from Seq0 import seq_reverse, seq_complement
if __name__ == "__main__":
    print("-----| Exercise 7 |------")
    gene = "U5"
    filename = gene + ".txt"
    n = 20
    fragment, _ =seq_reverse(filename, n)
    complement = seq_complement(fragment)
    print(f"Gene {gene}:")
    print(f"Frag:{fragment}")
    print(f"Comp:{complement}")