import json
datoteka = '../datoteke/recepti.json'

def sacuvaj_recepti(recepti):
    with open(datoteka, "w") as f:
        json.dump(recepti, f, indent=4)

def ucitaj_knjige():
    with open(datoteka) as f:
        recepti = json.load(f)
        return recepti

