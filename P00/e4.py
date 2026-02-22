from Seq0 import seq_count_base
gen_list = ["FRAT1", "U5", "ADA", "FXN"]
bases = ["A", "G", "C", "T"]
if __name__ == "__main__":
    print("-----| Exercise 4 |------")
    for gen in gen_list:
        filename = gen + ".txt"
        print(f"\nGene {gen}:")
        for base in bases:
            count = seq_count_base(filename, base)
            print(f"{base}: {count}")