from datetime import datetime


class Korisnik:

    @property
    def ime(self):
        return self.__ime

    @ime.setter
    def ime(self, novo_ime):
        self.__ime = novo_ime

    @property
    def prezime(self):
        return self.__prezime

    @prezime.setter
    def prezime(self, novo_preime):
        self.__ime = novo_preime

    @property
    def jmbg(self):
        return self.__jmbg

    @jmbg.setter
    def jmbg(self, novi_jmbg):
        self.__ime = novi_jmbg

    @property
    def datum_rodjenja(self):
        return self.__datum_rodjenja

    @datum_rodjenja.setter
    def datum_rodjenja(self, novi_datum):
        self.__ime = novi_datum

    def __init__(self, jmbg, ime, prezime, datum_rodjenja):
        self.__jmbg = jmbg
        self.__ime = ime
        self.__prezime = prezime
        self.__datum_rodjenja = datum_rodjenja

    def __str__(self):
        format_linije = "{:>14}: {}"

        return "\n".join([
            "",
            format_linije.format("JMBG", self.__jmbg),
            format_linije.format("Ime", self.__ime),
            format_linije.format("Prezime", self.__prezime),
            format_linije.format("God. rođenja", self.__datum_rodjenja)
        ])

