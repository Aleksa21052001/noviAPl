import pickle
datoteka = '../datoteke/lek.pickle'

def sacuvaj_lekovi(lekovi):
    with open(datoteka, "wb") as f:
        pickle.dump(lekovi, f)

def ucitaj_lekovi():
    with open(datoteka, "rb") as f:
        lekovi = pickle.load(f)
        return lekovi

