class Seq:
    """A class for representing sequences"""

    def __init__(self, strbases):
        # Initialize the sequence with the value
        # passed as argument when creating the object
        bases = "AGCT"
        valid = True
        for base in strbases:
            if base not in bases:
                valid = False
        if valid:
            self.strbases = strbases
            print("New sequence created!")
        else:
            self.strbases = "ERROR"
            print("ERROR!!")

    def __str__(self):
        """Method called when the object is being printed"""
        # -- We just return the string with the sequence
        return self.strbases

    def len(self):
        """Calculate the length of the sequence"""
        return len(self.strbases)

def print_seqs(seq_l) :
    i = 1
    for sequence in seq_l:
        print(f"Index {i} --> Lenght {sequence.len()} --> {sequence}")
        i = i + 1

def generate_seqs(pattern, number):
    i = 0
    lst = []
    seq = ""
    while i < number:
        seq = seq + pattern
        lst.append(Seq(seq))
        i = i + 1
    return lst

seq_list1 = generate_seqs("A", 3)
seq_list2 = generate_seqs("AC", 5)


print("List 1:")
print_seqs(seq_list1)

print()
print("List 2:")
print_seqs(seq_list2)

