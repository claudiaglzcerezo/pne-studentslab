def count(sequence):
    bases = {"A": 0, "C": 0, "G": 0, "T": 0}
    for base in sequence:
        if base in bases:
            bases[base] += 1
    return bases

if __name__ == "__main__":

    sequence = input("Enter a DNA sequence: ").upper()
    print("Total lenght", len(sequence))

    for base, count in bases.items():
        print(f'{base} : {count}')

#muy importante escribirlo
