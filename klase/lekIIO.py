import json
datoteka = './datoteke/lek.json'

def sacuvaj_lekovi(lekovi):
    with open(datoteka, "w") as f:
        json.dump(lekovi, f, indent=4)

def ucitaj_lekovi():
    with open(datoteka) as f:
        lekovi = json.load(f)
        return lekovi

