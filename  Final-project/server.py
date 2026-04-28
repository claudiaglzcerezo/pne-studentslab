import http.client
import http.server
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import jinja2 as j
from pathlib import Path
import os

class Seq:
    def list_species(self):
server = "rest.ensembl.org"
endpoint = f"/info/species"
params = "?content-type=application/json"

conn = http.client.HTTPSConnection(server)
conn.request("GET", endpoint + params)
res = conn.getresponse()
print(f"Response received!: {res.status} {res.reason}")
data = json.loads(res.read().decode("utf-8"))
s = Seq(data['seq'])


    def length(self):
        for b in bases:
            count = self.str_seq.count(b)
            stats[b] = (count, (count / length) * 100 if length > 0 else 0)
            if count > max_count:
                max_count = count
                most_frequent = b
        return length, stats, most_frequent


if gene_name in GENES:
    server = "rest.ensembl.org"
    endpoint = f"/info/species/"
    params = "/info/species?content-type=application/json"

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