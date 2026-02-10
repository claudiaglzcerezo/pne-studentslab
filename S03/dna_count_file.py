lines = ["AGTACACTGGT", "ACCAGTGTACT", "ATGGCCATTGTAATGGGCCGCTGAAAGGGTGCCCGATAG"]
print("From variable", lines)
from dna_count import count
#Option 1
f = open("dna.txt", "r")
lines = f.readlines()
#Es muy importante cerrar el archivo si utilizas esta forma
f.close()
print("From file: ", lines)

#Option 2
#otra forma de abrir archivos, en ella no hace falta cerrar
with open("dna.txt", "r") as f:
    lines = f.readlines()

total_number = 0

bases = {"A": 0, "C": 0, "G": 0, "T": 0}
for sequence in lines:
    sequence = sequence.strip() #Remove spaces and newline characters at the end of the string
    total_number += len(sequence)
    for base in sequence:
        if base in bases:
            bases[base] += 1
print("The total number of bases is: ", total_number)
for base, count in bases.items():
    print(f'{base} : {count}')
#Esta es la versión incorrecta
f