from Seq0 import seq_len
gen_list = ["FRAT1", "U5", "ADA", "FXN"]
if __name__ == "__main__":
    print("-----| Exercise 3 |------")
    for gen in gen_list:
        gent = gen + ".txt"
        print("Gene", gen, "--> Lenght", seq_len(gent))