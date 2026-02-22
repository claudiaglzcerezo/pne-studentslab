from Seq0 import seq_reverse
if __name__ == "__main__":
    print("-----| Exercise 6 |------")
    n = int(input("Enter a number of bases to reverse in U5: "))
    gene = "U5"
    filename = gene + ".txt"
    fragment, reverse = seq_reverse(filename, n)
    print(f"\nGene U5")
    print(f"Fragment: {fragment}")
    print(f"Reverse: {reverse}")