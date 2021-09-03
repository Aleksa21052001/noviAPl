from klase.korisnik import Korisnik

class Pacijent(Korisnik):

    @property
    def lbo(self):
        return self.__lbo

    @lbo.setter
    def lbo(self, novi_lbo):
        self.__ime = novi_lbo
    @property
    def recepti(self):
        return self.__recepti

    def __init__(self, jmbg, ime, prezime, datum_rodjenja, lbo, recepti):
        super().__init__(jmbg, ime, prezime, datum_rodjenja)
        self.__lbo = lbo
        self.__recepti = recepti #lista recepata

    def dodaj_recept(self,recept):
        self.__recepti.append(recept)

    def __str__(self):
        format_linije = "{:>14}: {}"

        return "\n".join([
            super().__str__(),
            format_linije.format("LBO", self.__lbo)
            ])


class Lekar(Korisnik):

    @property
    def specijalizacija(self):
        return self.__specijalizacija


    @specijalizacija.setter
    def specijalizacija(self, noca_spec):
        self.__specijalizacija = noca_spec

    @property
    def recepti(self):
        return self.__recepti


    def __init__(self, jmbg, ime, prezime, datum_rodjenja, specijalizacija, recepti):
        super().__init__(jmbg, ime, prezime, datum_rodjenja)
        self.__specijalizacija = specijalizacija
        self.__recepti = recepti



class Lek:

    @property
    def jkl(self):
        return self.__jkl

    @property
    def naziv(self):
        return self.__naziv

    @property
    def proizvodjac(self):
        return self.__proizvodjac

    @property
    def tip_leka(self):
        return self.__tip_leka

    @property
    def recepti(self):
        return self.__recepti


    def __init__(self, jkl, naziv, proizvodjac, tip_leka, recepti):
        self.__jkl = jkl
        self.__naziv = naziv
        self.__proizvodjac = proizvodjac
        self.__tip_leka = tip_leka
        self.__recepti = recepti




class Recept:
    # def __str__(self):
    #     return self.pacijent.ime + " " + self.lekar.ime + " " + self.lek.naziv + " " + self.kolicina
    @property
    def pacijent(self):
        return self.__pacijent

    @pacijent.setter
    def pacijent(self, novi_pacijent):
        self.__pacijent = novi_pacijent

    @property
    def datum(self):
        return self.__datum

    @property
    def izvestaj(self):
        return self.__izvestaj

    @izvestaj.setter
    def izvestaj(self, novi_izvestaj):
        self.__izvestaj = novi_izvestaj

    @property
    def lekar(self):
        return self.__lekar

    @lekar.setter
    def lekar(self, novi_lekar):
        self.__lekar = novi_lekar

    @property
    def lek(self):
        return self.__lek

    @lek.setter
    def lek(self, novi_lek):
        self.__lek = novi_lek

    @property
    def kolicina(self):
        return self.__kolicina

    @kolicina.setter
    def kolicina(self, kolicina):
        self.__kolicina = kolicina

    def sadrzi(self, pacijent):
        return pacijent in self.__pacijent


    def __init__(self, pacijent, datum_i_vreme, izvestaj, lekar, lek, kolicina):
        self.__pacijent = pacijent
        self.__datum = datum_i_vreme
        self.__izvestaj = izvestaj
        self.__lekar = lekar
        self.__lek = lek
        self.__kolicina = kolicina






def test():
    p1 = Pacijent('1111111111111', 'Aleksa', 'Cosovic', '21.05.2001', 'r2r3', 'nema recepta')
    p2 = Pacijent('2222222222222', 'Danilo', 'Cosovic', '22.05.2001','r2r23', 'nema recepta')
    p3 = Pacijent('3333333333333', 'Veljko', 'Cosovic', '23.05.2001','r2r33', 'nema recepta')

    print(p1,p2,p3)

if __name__ == "__main__":
    test()
