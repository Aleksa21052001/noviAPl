from klase.ostakeklase import *
import pickle


class Podaci:

    @property
    def pacijenti(self):
        return self.__pacijenti

    @property
    def lekari(self):
        return self.__lekari

    @property
    def recepti(self):
        return self.__recepti

    @property
    def lekovi(self):
        return self.__lekovi


    def __init__(self):
        self.__pacijenti = []
        self.__lekari = []
        self.__recepti = []
        self.__lekovi = []

    def dodaj_pacijente(self, pacijent):
        self.__pacijenti.append(pacijent)


    __naziv_datoteke = "svi-podaci"

    @classmethod
    def sacuvaj(cls, podaci):
        datoteka = open(cls.__naziv_datoteke, "wb")
        pickle.dump(podaci, datoteka)
        datoteka.close()

    @classmethod
    def ucitaj(cls):
        datoteka = open(cls.__naziv_datoteke, "rb")
        podaci = pickle.load(datoteka)
        datoteka.close()
        return podaci












        # @classmethod
        # def napravi_pocetne(cls):
        #
        #     podaci = Podaci()
        #
        #     pacijenti = podaci.pacijenti
        #     pacijenti.append(Pacijent('1111111111111', 'Aleksa', 'Cosovic', '21.05.2001', 'r2r3', 'nema recepta'))
        #     pacijenti.append(Pacijent('2222222222222', 'Danilo', 'Cosovic', '22.05.2001','r2r23', 'nema recepta'))
        #     pacijenti.append(Pacijent('3333333333333', 'Veljko', 'Cosovic', '23.05.2001','r2r33', 'nema recepta'))
        #
        #     return podaci
        #
        # __naziv_datoteke = "podaci.txt"

def test():
    podaci = Podaci.napravi_pocetne()

    print()
    print("Čuvanje...")
    Podaci.sacuvaj(podaci)

    print("Učitavanje...")
    podaci = Podaci.ucitaj()

    print(podaci.pacijenti)
