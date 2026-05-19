import http.client
import json

PORT = 8080
SERVER = "localhost"
PARAMS = "?json=1"

print(f"\nConnecting to server: {SERVER}:{PORT}\n")

try:
    conn = http.client.HTTPConnection(SERVER, PORT)

    # 1) LIST OF SPECIES
    conn.request("GET", f"/listSpecies{PARAMS}&limit=10")
    r1 = conn.getresponse()
    print(f"Response 1 received: {r1.status} {r1.reason}")
    data1 = r1.read().decode("utf-8")

    # 2) KARYOTYPE
    conn.request("GET", f"/karyotype{PARAMS}&species=shrew-mouse")
    r2 = conn.getresponse()
    print(f"Response 2 received: {r2.status} {r2.reason}")
    data2 = r2.read().decode("utf-8")

    # 3) CHROMOSOME LENGTH
    conn.request("GET", f"/chromosomeLength{PARAMS}&species=mouse&chromo=11")
    r3 = conn.getresponse()
    print(f"Response 3 received: {r3.status} {r3.reason}")
    data3 = r3.read().decode("utf-8")

    # 4) ID OF A HUMAN GENE
    conn.request("GET", f"/geneLookup{PARAMS}&gene=FRAT1")
    r4 = conn.getresponse()
    print(f"Response 4 received: {r4.status} {r4.reason}")
    data4 = r4.read().decode("utf-8")

    # 5) SEQUENCE OF A HUMAN GENE
    conn.request("GET", f"/geneSeq{PARAMS}&gene=FRAT1")
    r5 = conn.getresponse()
    print(f"Response 5 received: {r5.status} {r5.reason}")
    data5 = r5.read().decode("utf-8")

    # 6) INFORMATION ABOUT A HUMAN GENE
    conn.request("GET", f"/geneInfo{PARAMS}&gene=FRAT1")
    r6 = conn.getresponse()
    print(f"Response 6 received: {r6.status} {r6.reason}")
    data6 = r6.read().decode("utf-8")

    # 7) CALCULATIONS ON A HUMAN GENE
    conn.request("GET", f"/geneCalc{PARAMS}&gene=FRAT1")
    r7 = conn.getresponse()
    print(f"Response 7 received: {r7.status} {r7.reason}")
    data7 = r7.read().decode("utf-8")

    # 8) GENES OVERLAPPING A REGION
    conn.request("GET", f"/geneList{PARAMS}&chromo=9&start=22125500&end=22136000")
    r8 = conn.getresponse()
    print(f"Response 8 received: {r8.status} {r8.reason}")
    data8 = r8.read().decode("utf-8")

    conn.close()

except ConnectionRefusedError:
    print("ERROR: Cannot connect to the Server")
    exit()


print("\nBasic Level Exercises")

print("\n--- 1) LIST OF SPECIES ---")
d1 = json.loads(data1)
print(f"Limit of species: {d1.get('Limit', 10)}")
for species in d1.get("names", []):
    print(f"  - {species}")
print(f"Total number of species: {d1.get('num_species')}")

print("\n--- 2) KARYOTYPE ---")
l2 = json.loads(data2)
for chromo in l2:
    print(f"  - {chromo}")

print("\n--- 4) ID OF A HUMAN GENE ---")
d4 = json.loads(data4)
print(f"ID of gene {d4.get('gene')}: {d4.get('gene_id')}")

print("\n--- 5) SEQUENCE OF A HUMAN GENE ---")
d5 = json.loads(data5)
print(f"Sequence of gene {d5.get('gene')}: {d5.get('seq')}")

print("\n--- 6) INFORMATION ABOUT A HUMAN GENE ---")
d6 = json.loads(data6)
print(f"Information about gene {d6.get('gene')}:")
print(f"  - Start: {d6.get('start')}")
print(f"  - End: {d6.get('end')}")
print(f"  - Length: {d6.get('length')}")
print(f"  - Id: {d6.get('id')}")
print(f"  - Name of the chromosome: {d6.get('chromo')}")

print("\n--- 7) CALCULATIONS ON A HUMAN GENE ---")
d7 = json.loads(data7)
print(f"Calculations on gene {d7.get('gene')}")
print(f"Length: {d7.get('length')}")
print("Percentage of each nitrogenous base in the sequence:")
for base, count in d7.get('seq_count', {}).items():
    percent = (count / int(d7.get('length', 1))) * 100
    print(f"  - {base}: {count} ({round(percent, 1)}%)")

print("\n--- 8) GENES OVERLAPPING A REGION ---")
d8 = json.loads(data8)
print(f"Overlapped genes in the chromosome {d8.get('chromo')}")
print(f"From {d8.get('start')} to {d8.get('end')}:")
for gene in d8.get('region', []):
    print(f"  - {gene}")