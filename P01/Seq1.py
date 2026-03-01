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
