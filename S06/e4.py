import termcolor
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

def print_seqs(seq_l, color) :
    i = 0
    for sequence in seq_l:
        print(termcolor.colored(f"Index {i} --> Lenght {sequence.len()} --> {sequence}", color))
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

termcolor.cprint("List 1", "blue")
print_seqs(seq_list1, "blue")

print()
termcolor.cprint("List 2", "green")
print_seqs(seq_list2, "green")