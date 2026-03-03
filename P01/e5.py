from Seq1 import Seq
print("-----| Practice 1, Exercise 5 |------")
s1 = Seq()
s2 = Seq("ACTGA")
s3 = Seq("Invalid sequence")
sequences = [s1, s2, s3]
for i, seq in enumerate(sequences):
    print(f"Sequence {i}: (Length: {seq.len()}) {seq}")
    print(f" A:{seq.count("A")}, C:{seq.count("C")}, T:{seq.count("T")}, G:{seq.count("G")}")
