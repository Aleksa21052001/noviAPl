import pickle
datoteka = '../datoteke/lekar.pickle'

def sacuvaj_lekare(lekari):
    with open(datoteka, "wb") as f:
        pickle.dump(lekari, f)

def ucitaj_lekare():
    with open(datoteka,"rb") as f:
        lekari = pickle.load(f)
        return lekari

