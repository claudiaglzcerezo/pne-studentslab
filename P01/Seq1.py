class Seq:
    def __init__(self, strbases = None):
        if strbases is None:
            print("NULL sequence created")
            self.strbases = "NULL"
            return
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
            print("INVALID sequence!")

    def __str__(self):
        return self.strbases

    def len(self):
        if self.strbases in ["NULL", "ERROR"]:
            return 0
        return len(self.strbases)

    def count(self, base):
        if self.strbases in ["NULL", "ERROR"]:
            return 0
        return self.strbases.count(base)
    def count_dict(self):
        bases_count = {'A': 0, 'T': 0, 'C': 0, 'G': 0}
        if self.strbases in ["NULL", "ERROR"]:
            return bases_count
        for nucleotide in self.strbases:
            if nucleotide in bases_count:
                bases_count[nucleotide] += 1
        return bases_count
    def reverse(self):
        if self.strbases in ["NULL", "ERROR"]:
            return self.strbases
        return self.strbases[::-1]
    def complement(self):
        if self.strbases in ["NULL", "ERROR"]:
            return self.strbases
        comp_dict = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}
        complement = ""
        for base in self.strbases:
            complement += comp_dict[base]
        return complement