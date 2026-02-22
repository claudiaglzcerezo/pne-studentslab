from Seq0 import seq_reverse, complement_fragment
if __name__ == "__main__":
    print("-----| Exercise 7 |------")
    gene = "U5"
    filename = gene + ".txt"
    n = 20
    fragment, _ =seq_reverse(filename, n)
    complement = complement_fragment(fragment)
    print(f"Gene {gene}:")
    print(f"Frag:{fragment}")
    print(f"Comp:{complement}")