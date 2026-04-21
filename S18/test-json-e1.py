import json
import termcolor
from pathlib import Path

# -- Read the json file
try:
    jsonstring = Path("people-e1.json").read_text()
    data = json.loads(jsonstring)
except FileNotFoundError:
    print("Error: No se encuentra el archivo 'people-e1.json'")
    exit()

# El JSON es un diccionario de listas. Iteramos sobre cada clave (p1, p2...)
for key in data:
    # 'data[key]' es la lista que contiene a la persona
    for person in data[key]:
        termcolor.cprint(f" Registro: {key} ", 'white', 'on_blue')
# Create the object person from the json string

# Person is now a dictionary. We can read the values
# Print the information on the console, in colors
print()
termcolor.cprint("Name: ", 'green', end="")
print(person['Firstname'], person['Lastname'])
termcolor.cprint("Age: ", 'green', end="")
print(person['age'])

# Get the phoneNumber list
phoneNumbers = person['phoneNumber']

# Print the number of elements in the list
termcolor.cprint("Phone numbers: ", 'green', end='')
print(len(phoneNumbers))

# Print all the numbers
for i, dictnum in enumerate(phoneNumbers):
    termcolor.cprint("  Phone " + str(i + 1) + ": ", 'blue')

    # The element num contains 2 fields: number and type
    termcolor.cprint("\t- Type: ", 'red', end='')
    print(dictnum['type'])
    termcolor.cprint("\t- Number: ", 'red', end='')
    print(dictnum['number'])
