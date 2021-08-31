import pickle
datoteka = '../datoteke/pacijenti.pickle'

def sacuvaj_pacijente(pacijenti):
    with open(datoteka, "wb") as f:
        pickle.dump(pacijenti, f)

def ucitaj_pacijente():
    with open(datoteka,'rb') as f:
        pacijenti = pickle.load(f)
        return pacijenti

