from Seq0 import seq_count_base
gen_list = ["FRAT1", "U5", "ADA", "FXN"]
if __name__ == "__main__":
    basis = input("Enter a base: ").upper()
    print("-----| Exercise 4 |------")
    for gen in gen_list:
        gent = gen + ".txt"
        print("Base", basis, "number", seq_count_base(gent, basis))