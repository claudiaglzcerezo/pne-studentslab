import http.client
import json

PORT = 8080
SERVER = "localhost"
PARAMS = "?json=1"


# Función de ayuda para realizar peticiones HTTP de forma segura y limpia
def make_request(path_with_params):
    try:
        conn = http.client.HTTPConnection(SERVER, PORT)
        conn.request("GET", path_with_params)
        response = conn.getresponse()
        print(f"Requested {path_with_params.split('?')[0]} -> {response.status} {response.reason}")
        data = response.read().decode("utf-8")
        conn.close()
        return data
    except ConnectionRefusedError:
        print("ERROR: Cannot connect to the Server. Is server.py running?")
        exit()


print(f"\nConnecting to server: {SERVER}:{PORT}\n")

# Ejecución secuencial y segura de peticiones limpiando la conexión en cada ciclo
data1 = make_request(f"/listSpecies{PARAMS}&limit=10")
data2 = make_request(f"/karyotype{PARAMS}&species=shrew-mouse")
data3 = make_request(f"/chromosomeLength{PARAMS}&species=mouse&chromo=11")
data4 = make_request(f"/geneLookup{PARAMS}&gene=FRAT1")
data5 = make_request(f"/geneSeq{PARAMS}&gene=FRAT1")
data6 = make_request(f"/geneInfo{PARAMS}&gene=FRAT1")
data7 = make_request(f"/geneCalc{PARAMS}&gene=FRAT1")
data8 = make_request(f"/geneList{PARAMS}&chromo=9&start=22125500&end=22136000")

print("\n========================")
print("Basic Level Exercises")
print("========================\n")

print("--- 1) LIST OF SPECIES ---")
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
print(f"Sequence of gene {d5.get('gene')}: {d5.get('seq')[:60]}...")  # Mostramos solo el inicio para no inundar la consola

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
for base, count in d7.get("seq_count", {}).items():
    percent = (count / int(d7.get("length", 1))) * 100
    print(f"  - {base}: {count} ({round(percent, 1)}%)")

print("\n--- 8) GENES OVERLAPPING A REGION ---")
d8 = json.loads(data8)
print(f"Overlapped genes in the chromosome {d8.get('chromosome')}")
print(f"From {d8.get('start')} to {d8.get('end')}:")
for gene in d8.get("genes", []):
    print(f"  - {gene}")