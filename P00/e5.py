from Seq0 import seq_count
gen_list = ["FRAT1", "U5", "ADA", "FXN"]
if __name__ == "__main__":
    print("-----| Exercise 5 |------")
    for gen in gen_list:
        filename = gen + ".txt"
        counts = seq_count(filename)
        print(f"Gene {gen}: {counts}")