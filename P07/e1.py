import http.client
import json

SERVER = "rest.ensembl.org"
ENDPOINT = "/info/ping"
PARAMS = "?content-type=application/json" # I put this parameter so I receive the response in jdon format
URL = SERVER + ENDPOINT + PARAMS

print(f"Server: {SERVER}")
print(f"URL: {URL}")

conn = http.client.HTTPSConnection(SERVER)
conn.request("GET", ENDPOINT + PARAMS)

r1 = conn.getresponse()
print(f"Response received!: {r1.status} {r1.reason}") #status classify the response, reason "Ok" (explanation)

data = r1.read().decode("utf-8")
response = json.loads(data) #I change it to a python dictionary

if response['ping'] == 1:
    print("\nPING OK! The database is running!")