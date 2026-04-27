import http.client
import json

SERVER = "rest.ensembl.org"
# ID de MIR633 sacado del ejercicio anterior
ENDPOINT = "/sequence/id/ENSG00000207552"
PARAMS = "?content-type=application/json"

print(f"Server: {SERVER}")
print(f"URL: {SERVER}{ENDPOINT}{PARAMS}")

conn = http.client.HTTPSConnection(SERVER)
conn.request("GET", ENDPOINT + PARAMS)

r1 = conn.getresponse()
print(f"Response received!: {r1.status} {r1.reason}\n")

data = json.loads(r1.read().decode("utf-8"))

print(f"Gene: MIR633")
print(f"Description: {data['desc']}") #desc is for the info
print(f"Bases: {data['seq']}") #sequence