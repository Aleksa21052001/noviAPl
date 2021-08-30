from  klase.ostakeklase import *
from klase.podaci import Podaci
from tkinter import *
from tkinter import messagebox

class AppGui(Tk):

    def komanda_prozor_lekovi(self):
        pass

    def komanda_prozor_recepti(self):
        pass

    def komanda_prozor_lekari(self):
        prozor_lekari = DodavanjeProzorLekari(self)
        self.wait_window(prozor_lekari)

    def komanda_prozor_pacijent(self):
        prozor_pacijenti = DodavanjeProzorpacijenti(self)
        self.wait_window(prozor_pacijenti)

    def komanda_izlaz(self):  # ----ne treba da pravimo prozor niti ista slicno
        odgovor = messagebox.askokcancel("Proizvodi", "Da li ste sigurni da želite da napustite aplikaciju?", icon="warning")
        if odgovor:
            self.destroy()  # self pokazuje na tk klasu

    def __init__(self):
        super().__init__()
        self.title('APLIKACIJA BOLNICA')
        self.geometry("450x300")

        meni_bar = Menu(self)

        datoteka_meni = Menu(meni_bar, tearoff=0)  # -----tearof iskljucuje mogucnost da ga izvucemo sa strane
        datoteka_meni.add_command(label="Izlaz", command=self.komanda_izlaz)  # -----u datoteka meni smo dodali komandu izlaz
        meni_bar.add_cascade(label="Datoteka", menu=datoteka_meni)  # -----dodajemo ga u glavni meni pod nazivom datot

        self.__elementi_meni = Menu(meni_bar, tearoff=0)
        self.__elementi_meni.add_command(label='Pacijenti', command= self.komanda_prozor_pacijent)
        self.__elementi_meni.add_command(label='Lekari', command=self.komanda_prozor_lekari)
        self.__elementi_meni.add_command(label='Recepti', command=self.komanda_prozor_recepti)
        self.__elementi_meni.add_command(label='Lekovi', command=self.komanda_prozor_lekovi)
        meni_bar.add_cascade(label="izbor", menu=self.__elementi_meni)

        self.config(menu=meni_bar)


class DodavanjeProzorpacijenti(Toplevel):

    def ocisti_labele(self):
        self.__jmbg_labela['text'] = ""
        self.__ime_labela['text'] = ''
        self.__prezime_labela['text'] = ''
        self.__datum_labela['text'] = ''

    def popuni_labele(self, pacijent):
        self.__jmbg_labela['text'] = pacijent.jmbg
        self.__ime_labela['text'] = pacijent.ime
        self.__prezime_labela['text'] = pacijent.prezime
        self.__datum_labela['text'] = pacijent.datum_rodjenja
        self.__lbo_labela['text'] = pacijent.lbo

    def popuni_pacijenti_listbox(self, pacijenti):
        self.__pacijenti_listbox.delete(0, END)  # obrisati sve unose iz Listbox-a
        for pacijent in pacijenti:  # za svaki proizvod iz liste
            self.__pacijenti_listbox.insert(END, pacijent.ime)

        self.ocisti_labele()  # Listbox će izgubiti prethodnu selekciju; ne želimo da labele prikazuju bilo šta ako ništa nije selektovano

    def prikazi_recept(self):
        pass

    def komanda_dodaj(self):
        pass

    def komanda_izmeni(self):
        pass

    def komanda_obrisi(self):
        pass


    def __init__(self, master):
        super().__init__(master)

        self.geometry("710x400")
        self.title('PACIJENTI')

        levi_frame = Frame(self, borderwidth=2, relief="ridge", padx=10, pady=10)
        levi_frame.pack(side=LEFT, fill=BOTH, expand=1)

        Label(levi_frame, text="LISTA PACIJENATA").grid(sticky=W)

        self.__pacijenti_listbox = Listbox(levi_frame, width=43, activestyle="none")
        self.__pacijenti_listbox.grid(pady=(5,5))

        desni_frame = Frame(self, borderwidth=2, relief="ridge", padx=10, pady=10)
        desni_frame.pack(side=RIGHT, fill=BOTH, expand=1)

        # -----------------------------

        red = 0
        Label(desni_frame, text="JMBG:").grid(row=red, sticky=E)  # sticky argument određuje horinzotalno poravnanje kolone (E, W), odnosno vertikalno poravnanje reda (N, S)
        red += 1
        Label(desni_frame, text="Ime:").grid(row=red, sticky=E)
        red += 1
        Label(desni_frame, text="Prezime:").grid(row=red, sticky=E)
        red += 1
        Label(desni_frame, text="Datum rodjenja:").grid(row=red, sticky=E)
        red += 1
        Label(desni_frame, text="lbo:").grid(row=red, sticky=E)

        self.__jmbg_labela = Label(desni_frame)
        self.__ime_labela = Label(desni_frame)
        self.__prezime_labela = Label(desni_frame)
        self.__datum_labela = Label(desni_frame)
        self.__lbo_labela = Label(desni_frame)

        red = 0
        kolona = 1
        self.__jmbg_labela.grid(row=red, column=kolona, sticky=W)
        red += 1
        self.__ime_labela.grid(row=red, column=kolona, sticky=W)
        red += 1
        self.__prezime_labela.grid(row=red, column=kolona, sticky=W)
        red += 1
        self.__datum_labela.grid(row=red, column=kolona, sticky=W)
        red += 1
        self.__lbo_labela.grid(row=red, column=kolona, sticky=W)

        red += 1
        Label(desni_frame, text="").grid(row=red)

        # --------------------------------

        self.__dodaj_button = Button(desni_frame, text="Dodaj", width=10, command=self.komanda_dodaj)
        self.__izmeni_button = Button(levi_frame, text="Izmeni",state=DISABLED , width=10, command=self.komanda_izmeni)
        self.__ukloni_button = Button(desni_frame, text="Obriši",state=DISABLED ,width=10, command=self.komanda_obrisi)
        self.__recepti_button = Button(desni_frame, text="Recept", state=DISABLED, width=10, command=self.prikazi_recept)


        red += 1
        self.__dodaj_button.grid(row=red, column=kolona, sticky=W)
        self.__izmeni_button.grid(row=2, column=0, sticky= W, pady=(5,5))
        self.__ukloni_button.grid(row=red, column=kolona, sticky=E)
        self.__recepti_button.grid(row=red, column=kolona)
        red += 1
        Label(desni_frame, text="").grid(row=red)

        # --------------------------------

        red = 8
        Label(desni_frame, text="JMBG:").grid(row=red, sticky=E)
        red += 1
        Label(desni_frame, text="Ime:").grid(row=red, sticky=E)
        red += 1
        Label(desni_frame, text="Prezime:").grid(row=red, sticky=E)
        red += 1
        Label(desni_frame, text="Datum rodjenja:").grid(row=red, sticky=E)
        red += 1
        Label(desni_frame, text="lbo:").grid(row=red, sticky=E)

        self.__jmbgTxt = StringVar(master)
        self.__imeTxt = StringVar(master)
        self.__prezimeTxt = StringVar(master)
        self.__datumTxt = StringVar(master)
        self.__lboTxt = StringVar(master)

        self.__jmbg_entry = Entry(desni_frame, width=50, textvariable=self.__jmbgTxt)
        self.__ime_entry = Entry(desni_frame, width=50, textvariable=self.__imeTxt)  # textvariable argument povezuje StringVar, IntVar i sl. objekte sa komponentom
        self.__prezime_entry = Entry(desni_frame, width=50, textvariable=self.__prezimeTxt)
        self.__datum_entry = Entry(desni_frame, width=50, textvariable=self.__datumTxt)
        self.__lbo_entry = Entry(desni_frame, width=50, textvariable=self.__lboTxt)

        red = 8
        kolona = 1
        self.__jmbg_entry.grid(row=red, column=kolona, sticky=W, pady=(5,5))
        red += 1
        self.__ime_entry.grid(row=red, column=kolona, sticky=W, pady=(5,5))
        red += 1
        self.__prezime_entry.grid(row=red, column=kolona, sticky=W, pady=(5,5))
        red += 1
        self.__datum_entry.grid(row=red, column=kolona, sticky=W, pady=(5,5))
        red += 1
        self.__lbo_entry.grid(row=red, column=kolona, sticky=W, pady=(5,5))

    # ----------------------
class DodavanjeProzorLekari(Toplevel):

    def prikazi_recept(self):
        pass

    def komanda_dodaj(self):
        pass

    def komanda_izmeni(self):
        pass

    def komanda_obrisi(self):
        pass


    def __init__(self, master):
        super().__init__(master)

        self.geometry("710x400")
        self.title('LEKARI')

        levi_frame = Frame(self, borderwidth=2, relief="ridge", padx=10, pady=10)
        levi_frame.pack(side=LEFT, fill=BOTH, expand=1)

        Label(levi_frame, text="LISTA LEKARA").grid(sticky=W)

        self.__pacijenti_listbox = Listbox(levi_frame, width=43, activestyle="none")
        self.__pacijenti_listbox.grid(pady=(5,5))

        desni_frame = Frame(self, borderwidth=2, relief="ridge", padx=10, pady=10)
        desni_frame.pack(side=RIGHT, fill=BOTH, expand=1)

        # ------------------------------

        red = 0
        Label(desni_frame, text="JMBG:").grid(row=red, sticky=E)  # sticky argument određuje horinzotalno poravnanje kolone (E, W), odnosno vertikalno poravnanje reda (N, S)
        red += 1
        Label(desni_frame, text="Ime:").grid(row=red, sticky=E)
        red += 1
        Label(desni_frame, text="Prezime:").grid(row=red, sticky=E)
        red += 1
        Label(desni_frame, text="Datum rodjenja:").grid(row=red, sticky=E)
        red += 1
        Label(desni_frame, text="Specijalizacija:").grid(row=red, sticky=E)

        self.__jmbg_labela = Label(desni_frame)
        self.__ime_labela = Label(desni_frame)
        self.__prezime_labela = Label(desni_frame)
        self.__datum_labela = Label(desni_frame)
        self.__spec_labela = Label(desni_frame)

        red = 0
        kolona = 1
        self.__jmbg_labela.grid(row=red, column=kolona, sticky=W)
        red += 1
        self.__ime_labela.grid(row=red, column=kolona, sticky=W)
        red += 1
        self.__prezime_labela.grid(row=red, column=kolona, sticky=W)
        red += 1
        self.__datum_labela.grid(row=red, column=kolona, sticky=W)
        red += 1
        self.__spec_labela.grid(row=red, column=kolona, sticky=W)

        red += 1
        Label(desni_frame, text="").grid(row=red)

        # ------------------------------

        self.__dodaj_button = Button(desni_frame, text="Dodaj", width=10, command=self.komanda_dodaj)
        self.__izmeni_button = Button(levi_frame, text="Izmeni", state=DISABLED, width=10, command=self.komanda_izmeni)
        self.__ukloni_button = Button(desni_frame, text="Obriši", state=DISABLED, width=10, command=self.komanda_obrisi)
        self.__recepti_button = Button(desni_frame, text="Recept", state=DISABLED, width=10, command=self.prikazi_recept)

        red += 1
        self.__dodaj_button.grid(row=red, column=kolona, sticky=W)
        self.__izmeni_button.grid(row=2, column=0, sticky=W, pady=(5, 5))
        self.__ukloni_button.grid(row=red, column=kolona, sticky=E)
        self.__recepti_button.grid(row=red, column=kolona)
        red += 1
        Label(desni_frame, text="").grid(row=red)

        # ------------------------------

        red = 8
        Label(desni_frame, text="JMBG:").grid(row=red, sticky=E)
        red += 1
        Label(desni_frame, text="Ime:").grid(row=red, sticky=E)
        red += 1
        Label(desni_frame, text="Prezime:").grid(row=red, sticky=E)
        red += 1
        Label(desni_frame, text="Datum rodjenja:").grid(row=red, sticky=E)
        red += 1
        Label(desni_frame, text="Specijalizacija:").grid(row=red, sticky=E)

        self.__jmbgTxt = StringVar(master)
        self.__imeTxt = StringVar(master)
        self.__prezimeTxt = StringVar(master)
        self.__datumTxt = StringVar(master)
        self.__specTxt = StringVar(master)

        self.__jmbg_entry = Entry(desni_frame, width=50, textvariable=self.__jmbgTxt)
        self.__ime_entry = Entry(desni_frame, width=50, textvariable=self.__imeTxt)  # textvariable argument povezuje StringVar, IntVar i sl. objekte sa komponentom
        self.__prezime_entry = Entry(desni_frame, width=50, textvariable=self.__prezimeTxt)
        self.__datum_entry = Entry(desni_frame, width=50, textvariable=self.__datumTxt)
        self.__spec_entry = Entry(desni_frame, width=50, textvariable=self.__specTxt)

        red = 8
        kolona = 1
        self.__jmbg_entry.grid(row=red, column=kolona, sticky=W, pady=(5,5))
        red += 1
        self.__ime_entry.grid(row=red, column=kolona, sticky=W, pady=(5,5))
        red += 1
        self.__prezime_entry.grid(row=red, column=kolona, sticky=W, pady=(5,5))
        red += 1
        self.__datum_entry.grid(row=red, column=kolona, sticky=W, pady=(5,5))
        red += 1
        self.__spec_entry.grid(row=red, column=kolona, sticky=W, pady=(5,5))

    # -------------------------------



def main():

    glavni_prozor = AppGui()


    glavni_prozor.mainloop()


main()

