import http.client
import json


# (I take the same Seq Class in e4)
class Seq:
    def __init__(self, sequence):
        self.str_seq = sequence

    def get_stats(self):
        length = len(self.str_seq)
        bases = ['A', 'C', 'G', 'T']
        stats = {};
        most_frequent = "";
        max_count = -1
        for b in bases:
            count = self.str_seq.count(b)
            stats[b] = (count, (count / length) * 100 if length > 0 else 0)
            if count > max_count: max_count = count; most_frequent = b
        return length, stats, most_frequent


GENES = {
    "FRAT1": "ENSG00000165879", "ADA": "ENSG00000196839", "FXN": "ENSG00000165060",
    "RNU6-269P": "ENSG00000212379", "MIR633": "ENSG00000207552", "TTTY4C": "ENSG00000228296",
    "RBMY2YP": "ENSG00000227633", "FGFR3": "ENSG00000068078", "KDR": "ENSG00000128052",
    "ANK2": "ENSG00000145362"
}

server = "rest.ensembl.org"

for name, stable_id in GENES.items():
    endpoint = f"/sequence/id/{stable_id}"
    params = "?content-type=application/json"

    conn = http.client.HTTPSConnection(server)
    conn.request("GET", endpoint + params)
    res = conn.getresponse()

    data = json.loads(res.read().decode("utf-8"))
    s = Seq(data['seq'])
    total_len, stats, top_base = s.get_stats()

    print("-" * 30)
    print(f"Gene: {name}")
    print(f"Description: {data['desc']}")
    print(f"Total length: {total_len}")
    for b, (c, p) in stats.items():
        print(f"{b}: {c} ({p:.1f}%)")
    print(f"Most frequent Base: {top_base}")