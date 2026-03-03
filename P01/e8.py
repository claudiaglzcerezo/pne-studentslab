from Seq1 import Seq
print("-----| Practice 1, Exercise 6 |------")
s1 = Seq()
s2 = Seq("ACTGA")
s3 = Seq("Invalid sequence")
sequences = [s1, s2, s3]
for i, seq in enumerate(sequences):
    print(f"Sequence {i}: (Length: {seq.len()}) {seq}")
    print(f"{seq.count_dict()}")
    print(f"Rev:{seq.reverse()}")
    print(f"Com:{seq.complement()}")