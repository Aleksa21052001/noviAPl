import pickle
datoteka = '../datoteke/recepti.pickle'

def sacuvaj_recepte(recepti):
    with open(datoteka, "wb") as f:
        pickle.dump(recepti, f)

def ucitaj_recepte():
    with open(datoteka,"rb") as f:
        recepti = pickle.load(f)
        return recepti

