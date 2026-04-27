import http.client
import json


class Seq:
    def __init__(self, sequence):
        self.str_seq = sequence

    def get_stats(self):
        length = len(self.str_seq)
        bases = ['A', 'C', 'G', 'T']
        stats = {}
        most_frequent = ""
        max_count = -1

        for b in bases:
            count = self.str_seq.count(b)
            stats[b] = (count, (count / length) * 100 if length > 0 else 0)
            if count > max_count:
                max_count = count
                most_frequent = b
        return length, stats, most_frequent


GENES = {
    "FRAT1": "ENSG00000165879", "ADA": "ENSG00000196839", "FXN": "ENSG00000165060",
    "RNU6-269P": "ENSG00000212379", "MIR633": "ENSG00000207552", "TTTY4C": "ENSG00000228296",
    "RBMY2YP": "ENSG00000227633", "FGFR3": "ENSG00000068078", "KDR": "ENSG00000128052",
    "ANK2": "ENSG00000145362"
}

gene_name = input("Write the gene name: ").upper()

if gene_name in GENES:
    server = "rest.ensembl.org"
    endpoint = f"/sequence/id/{GENES[gene_name]}"
    params = "?content-type=application/json"

    conn = http.client.HTTPSConnection(server)
    conn.request("GET", endpoint + params)
    res = conn.getresponse()

    print(f"Server: {server}")
    print(f"URL: {server}{endpoint}{params}")
    print(f"Response received!: {res.status} {res.reason}")

    data = json.loads(res.read().decode("utf-8"))
    s = Seq(data['seq'])
    total_len, stats, top_base = s.get_stats()

    print(f"\nGene: {gene_name}")
    print(f"Description: {data['desc']}")
    print("New sequence created!")
    print(f"Total length: {total_len}")
    for base, (count, perc) in stats.items():
        print(f"{base}: {count} ({perc:.1f}%)")
    print(f"Most frequent Base: {top_base}")
else:
    print("Gene not found in dictionary.")