from Seq0 import seq_count, frequent_base
gen_list = ["FRAT1", "U5", "ADA", "FXN"]
if __name__ == "__main__":
    print("-----| Exercise 8 |------")
    for gen in gen_list:
        filename = gen + ".txt"
        counts = seq_count(filename)
        most_frequent = frequent_base(counts)
        print(f"Gene {gen}: Most frequent base: {most_frequent}")