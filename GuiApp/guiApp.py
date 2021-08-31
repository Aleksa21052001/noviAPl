from  klase.ostakeklase import *
from klase.podaci import Podaci
from tkinter import *
from tkinter import messagebox
from klase.pacijentIO import ucitaj_pacijente, sacuvaj_pacijente





class AppGui(Tk): #glavni prozor

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


    #------------>MENI<------------

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

    def zakljucaj_dugmice(self):
        self.__izmeni_button["state"] = DISABLED
        self.__ukloni_button["state"] = DISABLED
        self.__sacuvajizmene_button["state"] = DISABLED


    def ocisti_entry(self):
        self.__jmbgTxt.set('')
        self.__imeTxt.set('')
        self.__prezimeTxt.set('')
        self.__datumTxt.set('')
        self.__lboTxt.set('')

    def enable_entry(self):
        self.__jmbg_entry.configure(state="normal")
        self.__ime_entry.configure(state="normal")
        self.__prezime_entry.configure(state="normal")
        self.__datum_entry.configure(state="normal")
        self.__lbo_entry.configure(state="normal")

    def disable_entry(self):
        self.__jmbg_entry.configure(state="disabled")
        self.__ime_entry.configure(state="disabled")
        self.__prezime_entry.configure(state="disabled")
        self.__datum_entry.configure(state="disabled")
        self.__lbo_entry.configure(state="disabled")

    def popuni_labele(self, pacijent): #namesti da pristupas preko propertia
        #for item in self.__pacijenti_listbox.curselection():

        self.__jmbg_labela['text'] = pacijent.jmbg
        self.__ime_labela['text'] = pacijent.ime
        self.__prezime_labela['text'] = pacijent.prezime
        self.__datum_labela['text'] = pacijent.datum_rodjenja
        self.__lbo_labela['text'] = pacijent.lbo


    def ocisti_labele(self):
        self.__jmbg_labela['text'] = ""
        self.__ime_labela['text'] = ''
        self.__prezime_labela['text'] = ''
        self.__datum_labela['text'] = ''


    def popuni_pacijente_listbox(self):
        self.__pacijenti_listbox.delete(0, END)  # obrisati sve unose iz Listbox-a

        for i in self.__pacijenti:
            self.__pacijenti_listbox.insert(END, i.prezime + " " + i.ime)
        self.ocisti_labele()  # Listbox će izgubiti prethodnu selekciju; ne želimo da labele prikazuju bilo šta ako ništa nije selektovano


    def promena_selekcije_u_listboxu(self, eventt = None): #popuni labele
        if not self.__pacijenti_listbox.curselection():
            self.ocisti_labele()
            return -1


        indeks = self.__pacijenti_listbox.curselection()[0]
        print(indeks)
        return indeks


    def prikazi_recept(self):
        pass

    def on_dodaj(self):

        self.ocisti_entry()
        self.enable_entry()
        self.__sacuvajizmene_button['state'] = NORMAL
        self.__selektovani = None
        self.__jmbg_entry.focus()

    def on_sacuvaj(self): #ne radi nekad, nekad radi ne kontam i nece da mi popuni poske dodavanjja pacijente
        if self.__selektovani is None: #dodavanje novog pacijenta
            # jmbg = self.__jmbgTxt.get()

            jmbg = self.jmbg_validacija()
            if not jmbg:
                return
            ime = self.ime_validacija()
            if not ime:
                return
            prezime = self.prezime_validacija()
            if not prezime:
                return
            datum = self.__datumTxt.get()
            lbo = self.lbo_validacija()
            if not lbo:
                return

            p = Pacijent(jmbg, ime, prezime, datum, lbo, [])
            pacijenti = ucitaj_pacijente()
            pacijenti.append(p)
            sacuvaj_pacijente(pacijenti)

            self.popuni_pacijente_listbox()
            self.zakljucaj_dugmice()
            self.disable_entry()
            self.ocisti_entry()


        else: #izmena
            indeks = self.promena_selekcije_u_listboxu()
            if indeks == -1:
                return
            p = self.__pacijenti[indeks]

            jmbg = self.__jmbgTxt.get()
            ime = self.ime_validacija()
            prezime = self.prezime_validacija()
            datum = self.__datumTxt.get()
            lbo = self.__lboTxt.get()
            pac = Pacijent(jmbg, ime, prezime, datum, lbo, p.recepti)
            print(pac)
            self.__pacijenti[indeks] = pac
            sacuvaj_pacijente(self.__pacijenti)

            self.popuni_pacijente_listbox()
            self.zakljucaj_dugmice()
            self.disable_entry()
            self.ocisti_entry()

    def on_izmeni(self):
        self.ocisti_labele()
        self.enable_entry()
        self.__sacuvajizmene_button['state']= NORMAL

        indeks = self.promena_selekcije_u_listboxu()
        if indeks == -1:
            return

        self.__jmbg_entry.configure(state="disabled")
        self.__lbo_entry.configure(state="disabled")

        pacijent = self.__pacijenti[indeks]
        self.__jmbgTxt.set(pacijent.jmbg)
        self.__imeTxt.set(pacijent.ime)
        self.__prezimeTxt.set(pacijent.prezime)
        self.__lboTxt.set(pacijent.lbo)
        self.__datumTxt.set(pacijent.datum_rodjenja)


        self.__selektovani = True

    def on_obrisi(self):
        if messagebox.askquestion("upozorenje", "Da li zelite da obrisete pacijenta?", icon="warning") == "no":
            return

        indeks = self.promena_selekcije_u_listboxu()
        if indeks >= 0:
            self.__pacijenti.pop(indeks)

        sacuvaj_pacijente(self.__pacijenti)
        #self.komanda_prikazi()
        self.popuni_pacijente_listbox()
        self.zakljucaj_dugmice()
        self.disable_entry()
        self.ocisti_entry()


    def on_prikazi(self):
        indeks = self.promena_selekcije_u_listboxu()
        pacijent = self.__pacijenti[indeks]
        # print(pacijent)
        self.popuni_labele(pacijent)

        self.__izmeni_button['state'] = NORMAL
        self.__ukloni_button['state'] = NORMAL


    def filtriraj(self):
        self.__pacijenti = ucitaj_pacijente()
        pojam = self.__PretragaTxt.get().lower()
        rezultat_pretrage = []
        for p in self.__pacijenti:
            if pojam in p.ime.lower() or pojam in p.prezime.lower():
                rezultat_pretrage.append(p)
        self.__pacijenti = rezultat_pretrage
        self.popuni_pacijente_listbox()

    def jmbg_validacija(self):
        try:
            jmbg = self.__jmbgTxt.get()
            if len(jmbg) != 13:
                messagebox.showerror("Greska", "Jmbg mora da sadrzi tacno 13 karaktera!" + "{:>2} {}".format(str(len(jmbg)), "karaktera"))
                return None
        except TclError:
            messagebox.showerror("Greška", "jmbg treba da bude sastavljen od brojeva")
            return None

        return jmbg

    def ime_validacija(self):
        ime = self.__imeTxt.get()

        if len(ime) < 1:
            messagebox.showerror("Greska", "ime mora da sadrzi bar 2 karaktera!")
            return  None

        return  ime

    def prezime_validacija(self):
        prezime = self.__prezimeTxt.get()
        if len(prezime) < 2:
            messagebox.showerror("Greska", "Prezime mora da sadrzi bar 2 karaktera!")
            return None

        return prezime

    def lbo_validacija(self):
        try:
            lbo = self.__lboTxt.get()
            if len(lbo) != 11:
                messagebox.showerror("Greska", "lbo mora da sadrzi tacno 11 karaktera!" + "{:>2} {}".format(str(len(lbo)), "karaktera"))
                return None
        except TclError:
            messagebox.showerror("Greška", "lbo treba da bude sastavljen od brojeva")
            return None

        return lbo

    def __init__(self, master):
        super().__init__(master)

        self.__pacijenti = ucitaj_pacijente()

        self.geometry("810x500")
        self.title('PACIJENTI')

        levi_frame = Frame(self, borderwidth=2, relief="ridge", padx=10, pady=10)
        levi_frame.pack(side=LEFT, fill=BOTH, expand=1)

        Label(levi_frame, text="LISTA PACIJENATA").grid(sticky=W)

        self.__pacijenti_listbox = Listbox(levi_frame, width=43, activestyle="none")
        self.__pacijenti_listbox.grid(pady=(5,5))



        desni_frame = Frame(self, borderwidth=2, relief="ridge", padx=10, pady=10)
        desni_frame.pack(side=RIGHT, fill=BOTH, expand=1)

        # ------------>LABELI<------------

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

    # ------------>button<------------

        self.__dodaj_button = Button(desni_frame, text="Dodaj", width=10, command=self.on_dodaj)
        self.__izmeni_button = Button(desni_frame, text="Izmeni" ,state=DISABLED, width=10, command=self.on_izmeni)
        self.__prikazi_button = Button(levi_frame, text="Prikazi" ,width=10, command=self.on_prikazi)
        self.__recepti_button = Button(desni_frame, text="Recept", state=DISABLED, width=10, command=self.prikazi_recept)
        self.__ukloni_button = Button(desni_frame, text="Obriši",state=DISABLED,  width=10, command=self.on_obrisi)
        self.__sacuvajizmene_button = Button(desni_frame, text="Sacuvaj", state=DISABLED, width=13, command=self.on_sacuvaj)
        self.__filtriraj_button = Button(levi_frame, text="Pretraga", width=10, command=self.filtriraj)




        red += 1
        self.__dodaj_button.grid(row=red, column=kolona, sticky=W, padx=9, pady=5)
        self.__izmeni_button.grid(row=red, column=kolona)
        self.__recepti_button.grid(row=red, column=kolona, sticky=E)
        self.__ukloni_button.grid(row=red, column=0, sticky=E, padx=9, pady=(5,5))
        self.__prikazi_button.grid(row=2, column=0, sticky= W, pady=(5,5))


        self.__sacuvajizmene_button.grid(row=13, column=1, sticky=W, pady=(5,5))
        self.__filtriraj_button.grid(row=5, pady=(5,5))

        red += 1
        Label(desni_frame, text="").grid(row=red)

        # ------------>ENTRY<------------

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

        Label(levi_frame, text="Pretrazi:").grid(row=3, sticky=W)


        self.__jmbgTxt = IntVar(master)
        self.__imeTxt = StringVar(master)
        self.__prezimeTxt = StringVar(master)
        self.__datumTxt = StringVar(master)
        self.__lboTxt = IntVar(master)
        self.__PretragaTxt = StringVar(master)
        #self.__PretragaTxt.trace_add("write",self.filtriraj)

        dbkg = "#dfdfdf"  # siva boja za bekgraund
        self.__jmbg_entry = Entry(desni_frame, width=50, textvariable=self.__jmbgTxt, state='disabled',disabledbackground=dbkg)
        self.__ime_entry = Entry(desni_frame, width=50, textvariable=self.__imeTxt, state='disabled',disabledbackground=dbkg)  # textvariable argument povezuje StringVar, IntVar i sl. objekte sa komponentom
        self.__prezime_entry = Entry(desni_frame, width=50, textvariable=self.__prezimeTxt, state='disabled',disabledbackground=dbkg)
        self.__datum_entry = Entry(desni_frame, width=50, textvariable=self.__datumTxt, state='disabled',disabledbackground=dbkg)
        self.__lbo_entry = Entry(desni_frame, width=50, textvariable=self.__lboTxt, state='disabled',disabledbackground=dbkg)
        self.__pretraga_entry = Entry(levi_frame, width=50, textvariable=self.__PretragaTxt)

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

        self.__pretraga_entry.grid(row=4, column=0, sticky=W, pady=(5,5))


    # ----------------------

        self.popuni_pacijente_listbox()

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
    # p1 = Pacijent("1231231231231","milos","obilic","01.01.2001","1234567",[])
    # p2 = Pacijent("1231231231231", "zoran", "obilic", "01.01.2002", "1234561", [])
    # p3 = Pacijent("1231231231231", "marko", "obilic", "01.01.2003", "1234562", [])
    # p4 = Pacijent("1231231231231", "milan", "obilic", "01.01.2004", "1234563", [])
    # pacijenti = [p1,p2,p3,p4]
    # sacuvaj_pacijente(pacijenti)


    glavni_prozor = AppGui()


    glavni_prozor.mainloop()


main()

