from  klase.ostakeklase import *
from klase.podaci import Podaci
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
from klase.pacijentIO import ucitaj_pacijente, sacuvaj_pacijente
from  klase.lekarIO import ucitaj_lekare, sacuvaj_lekare
from  klase.lekIIO import ucitaj_lekovi, sacuvaj_lekovi
from  klase.receptIO import ucitaj_recepte, sacuvaj_recepte





class AppGui(Tk): #glavni prozor

    def komanda_prozor_lekovi(self):
        prozor_lekovi = ProzorLekovi(self)
        self.wait_window(prozor_lekovi)

    def komanda_prozor_recepti(self):
        prozor_recepti = ProorRecepti(self)
        self.wait_window(prozor_recepti)
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
        meni_bar.add_cascade(label="Zatvori glavni prozor", menu=datoteka_meni)  # -----dodajemo ga u glavni meni pod nazivom datot

        self.__elementi_meni = Menu(meni_bar, tearoff=0)
        self.__elementi_meni.add_command(label='Pacijenti', command=self.komanda_prozor_pacijent)
        self.__elementi_meni.add_command(label='Lekari', command=self.komanda_prozor_lekari)
        self.__elementi_meni.add_command(label='Lekovi', command=self.komanda_prozor_lekovi)
        self.__elementi_meni.add_command(label='Recepti', command=self.komanda_prozor_recepti)

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
        self.__lbo_labela['text'] = ''

    def popuni_pacijente_listbox(self):
        self.__pacijenti_listbox.delete(0, END)  # obrisati sve unose iz Listbox-a

        for i in self.__pacijenti:
            self.__pacijenti_listbox.insert(END, i.prezime + " " + i.ime)
        self.ocisti_labele()  # Listbox će izgubiti prethodnu selekciju; ne želimo da labele prikazuju bilo šta ako ništa nije selektovano

    def promena_selekcije_u_listboxu(self, event = None): #popuni labele
        if not self.__pacijenti_listbox.curselection():
            self.ocisti_labele()

            self.__izmeni_button['state'] = DISABLED
            self.__ukloni_button['state'] = DISABLED
            return

        indeks = self.__pacijenti_listbox.curselection()[0]

        self.__izmeni_button['state'] = NORMAL
        self.__ukloni_button['state'] = NORMAL
        self.__prikazi_button['state'] = NORMAL
        self.__recepti_button['state'] = NORMAL
        self.ocisti_labele()

        print(indeks)
        return indeks

    #<--------RECEPTI---------->

    def prikazi_recept(self):
        if not self.__pacijenti_listbox.curselection():
            messagebox.showerror("greska","Morate da selektujete pacijenta")
            return None

        recepti = ucitaj_recepte()
        filtrirani_recepti = []
        indeks = self.promena_selekcije_u_listboxu()
        pacijent = self.__pacijenti[indeks]
        for recept in recepti:
            if pacijent.ime == recept.pacijent.ime and pacijent.prezime == recept.pacijent.prezime:
                filtrirani_recepti.append(recept)


        prikaz_recepata_pacijent = Toplevel(self.master)
        prikaz_recepata_pacijent.title("recepti")
        prikaz_recepata_pacijent.geometry("650x350")

        self.__filtrirani_reepti = filtrirani_recepti

        # ------------>FRAME<------------

        levi_frame = Frame(prikaz_recepata_pacijent, borderwidth=2, relief="ridge", padx=10, pady=10)
        levi_frame.pack(side=LEFT, fill=BOTH, expand=1)

        desni_frame = Frame(prikaz_recepata_pacijent, borderwidth=2, relief="ridge", padx=10, pady=10)
        desni_frame.pack(side=RIGHT, fill=BOTH, expand=1)

        # ------------>listbox<------------

        self.__recepti_listbox = Listbox(levi_frame, width=43, activestyle="none")
        self.__recepti_listbox.grid(row=2, column=0, pady=5, padx=5)
        self.__recepti_listbox.bind("<<ListboxSelect>>", self.promena_selekcije_listbox_recept)

        # ------------>LABELI<------------

        Label(levi_frame, text="LISTA RECEPATA").grid(row=1, column=0, sticky=W)

        red = 0
        Label(desni_frame, text="Pacijent:").grid(row=red,
                                                  sticky=E)  # sticky argument određuje horinzotalno poravnanje kolone (E, W), odnosno vertikalno poravnanje reda (N, S)
        red += 1
        Label(desni_frame, text="Datum i vreme:").grid(row=red, sticky=E)
        red += 1
        Label(desni_frame, text="Izvestaj:").grid(row=red, sticky=E)
        red += 1
        Label(desni_frame, text="lekar:").grid(row=red, sticky=E)
        red += 1
        Label(desni_frame, text="Lek:").grid(row=red, sticky=E)
        red += 1
        Label(desni_frame, text="Kolicina:").grid(row=red, sticky=E)

        self.__pacijent_labela = Label(desni_frame)
        self.__datum2_labela = Label(desni_frame)
        self.__izvestaj_labela = Label(desni_frame)
        self.__lekar_labela = Label(desni_frame)
        self.__lek_labela = Label(desni_frame)
        self.__kolicina_labela = Label(desni_frame)

        red = 0
        kolona = 1
        self.__pacijent_labela.grid(row=red, column=kolona, sticky=W)
        red += 1
        self.__datum2_labela.grid(row=red, column=kolona, sticky=W)
        red += 1
        self.__izvestaj_labela.grid(row=red, column=kolona, sticky=W)
        red += 1
        self.__lekar_labela.grid(row=red, column=kolona, sticky=W)
        red += 1
        self.__lek_labela.grid(row=red, column=kolona, sticky=W)
        red += 1
        self.__kolicina_labela.grid(row=red, column=kolona, sticky=W)

        red += 1
        Label(desni_frame, text="", width = 50).grid(row=red,column=1)

        # ------------>Button<------------

        self.__prikazi_recept_button = Button(levi_frame, text="Prikazi" ,state=DISABLED,width=10, command=self.on_prikazi_recept)
        self.__prikazi_recept_button.grid(row=3,column=0,padx=5,pady=5)
        self.__nazad_button = Button(desni_frame, text ='Nazad', command=prikaz_recepata_pacijent.destroy,width=10)
        self.__nazad_button.grid(row =red,column=0,padx=5,pady=5)

        self.recepti_pacijent_listbox(filtrirani_recepti)


    def recepti_pacijent_listbox(self, filtrirani_recepti):
        self.__recepti_listbox.delete(0, END)

        for recept in filtrirani_recepti:
            self.__recepti_listbox.insert(END, recept.pacijent.ime +" " + recept.pacijent.prezime + " "
                                          "|" + " "+ recept.lekar.ime + " " + recept.lekar.prezime)

    def ispisi_labele_recept(self, recept):
        self.__pacijent_labela['text'] = recept.pacijent.ime +" " + recept.pacijent.prezime
        self.__datum2_labela['text'] = recept.datum
        self.__izvestaj_labela['text'] = recept.izvestaj
        self.__lekar_labela['text'] = recept.lekar.ime + " " + recept.lekar.prezime
        self.__lek_labela['text'] = recept.lek.naziv
        self.__kolicina_labela['text'] = recept.kolicina

    def promena_selekcije_listbox_recept(self, evemt=None):
        if not self.__recepti_listbox.curselection():
            return
        indeks = self.__recepti_listbox.curselection()[0]
        self.__prikazi_recept_button['state'] = NORMAL
        return indeks

    def on_prikazi_recept(self):
        indeks = self.promena_selekcije_listbox_recept()
        filtrirani_recepti = self.__filtrirani_reepti
        recept_za_prikaz = filtrirani_recepti[indeks]
        self.ispisi_labele_recept(recept_za_prikaz)


    # <--------RECEPTI END---------->


    def on_dodaj(self):

        self.ocisti_labele()
        self.ocisti_entry()
        self.enable_entry()
        self.__sacuvajizmene_button['state'] = NORMAL

        self.__selektovani = None
        self.__jmbg_entry.focus()

        self.__PretragaTxt.set("")

    def on_sacuvaj(self):
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

            self.__pacijenti = pacijenti
            sacuvaj_pacijente(pacijenti)

            self.popuni_pacijente_listbox()

            self.__pacijenti_listbox.selection_set(END)
            indeks = self.promena_selekcije_u_listboxu()
            dodati_pacijent = self.__pacijenti[indeks]
            self.popuni_labele(dodati_pacijent)


            self.zakljucaj_dugmice()
            self.disable_entry()
            self.ocisti_entry()


        else: #izmena, pukne, nestane selekcija u listboxu
            indeks = self.promena_selekcije_u_listboxu()

            if indeks == -1:
                return

            p = self.__pacijenti[indeks] #izbacuje ove gresku ako ne bude ni jedan izabran<<<<<<<<<<
            jmbg = self.__jmbgTxt.get()
            ime = self.ime_validacija()
            if not ime:
                return
            prezime = self.prezime_validacija()
            if not prezime:
                return
            datum = self.__datumTxt.get()
            lbo = self.__lboTxt.get()
            pac = Pacijent(jmbg, ime, prezime, datum, lbo, p.recepti)
            print(pac)

            self.__pacijenti[indeks] = pac
            sacuvaj_pacijente(self.__pacijenti)

            # self.__pacijenti_listbox.selection_anchor(indeks)
            # indeks = self.promena_selekcije_u_listboxu()
            # izmenjeni_pacijent = self.__pacijenti[indeks]
            # self.popuni_labele(izmenjeni_pacijent)

            self.popuni_pacijente_listbox()
            self.zakljucaj_dugmice()
            self.disable_entry()
            self.ocisti_entry()

    def on_izmeni(self):
        self.ocisti_labele()
        self.enable_entry()
        self.__sacuvajizmene_button['state']= NORMAL

        self.__indeks = self.promena_selekcije_u_listboxu()
        indeks = self.__indeks
        if indeks == -1:
            return

        pacijent = self.__pacijenti[indeks]

        self.__jmbg_entry.configure(state="disabled")
        self.__lbo_entry.configure(state="disabled")

        self.__jmbgTxt.set(pacijent.jmbg)
        self.__imeTxt.set(pacijent.ime)
        self.__prezimeTxt.set(pacijent.prezime)
        self.__lboTxt.set(pacijent.lbo)
        self.__datumTxt.set(pacijent.datum_rodjenja)

        self.__selektovani = True

    def on_obrisi(self):
        if messagebox.askquestion("upozorenje", "Da li zelite da obrisete pacijenta, i njegove recepte?", icon="warning") == "no":
            return

        indeks = self.promena_selekcije_u_listboxu()
        if indeks >= 0:
            self.__pacijenti.pop(indeks)

        sacuvaj_pacijente(self.__pacijenti)

        self.popuni_pacijente_listbox()
        self.zakljucaj_dugmice()
        self.disable_entry()
        self.ocisti_entry()


    def on_prikazi(self):
        indeks = self.promena_selekcije_u_listboxu()
        pacijent = self.__pacijenti[indeks]
        # print(pacijent)
        self.popuni_labele(pacijent)

        self.__PretragaTxt.set("")

        # self.__izmeni_button['state'] = NORMAL
        # self.__ukloni_button['state'] = NORMAL

    def on_odustani(self):
        self.ocisti_labele()
        self.ocisti_entry()
        self.disable_entry()
        self.zakljucaj_dugmice()


    def filtriraj(self, event=None):
        self.__pacijenti = ucitaj_pacijente()
        pojam = self.__PretragaTxt.get().lower()
        rezultat_pretrage = []
        for p in self.__pacijenti:
            if pojam in p.ime.lower() or pojam in p.prezime.lower():
                rezultat_pretrage.append(p)
        self.__pacijenti = rezultat_pretrage
        self.popuni_pacijente_listbox()

    def proveri_jmbg(self, jmbg):
        pacijenti = self.__pacijenti
        for pacijent in pacijenti:
            if jmbg == pacijent.jmbg:
                return None
        return jmbg

    def jmbg_validacija(self):
        try:
            jmbg = self.__jmbgTxt.get()
            self.proveri_jmbg(jmbg)
            if len(str(jmbg)) != 13:
                messagebox.showerror("Greska", "Jmbg mora da sadrzi tacno 13 karaktera!" + "{:>2} {}".format(len(str(jmbg)), "karaktera"))
                return None
        except TclError:
            messagebox.showerror("Greška", "jmbg treba da bude sastavljen od brojeva")
            return None

        if self.proveri_jmbg(jmbg) is None:
            messagebox.showerror("Greska", "Pacijent sa unetim jmbg-om vec postoji!")
        else:
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

    def proveri_lbo(self, lbo):
        pacijenti = self.__pacijenti
        for pacijent in pacijenti:
            if lbo == pacijent.lbo:
                return None
        return lbo

    def lbo_validacija(self):
        try:
            lbo = self.__lboTxt.get()
            if len(str(lbo)) != 11:
                messagebox.showerror("Greska", "lbo mora da sadrzi tacno 11 karaktera!" + "{:>2} {}".format(len(str(lbo)), "karaktera"))
                return None
        except TclError:
            messagebox.showerror("Greška", "lbo treba da bude sastavljen od brojeva")
            return None

        if self.proveri_lbo(lbo) is None:
            messagebox.showerror("Greska", "Pacijent sa unetim lbo-om vec postoji!")
            return None
        else:
            return lbo




    def komanda_izlaz(self):
        self.destroy()

    def __init__(self, master):
        super().__init__(master)

        self.__pacijenti = ucitaj_pacijente()

        self.geometry("810x500")
        self.title('PACIJENTI')

        levi_frame = Frame(self, borderwidth=2, relief="ridge", padx=10, pady=10)
        levi_frame.pack(side=LEFT, fill=BOTH, expand=1)

        desni_frame = Frame(self, borderwidth=2, relief="ridge", padx=10, pady=10)
        desni_frame.pack(side=RIGHT, fill=BOTH, expand=1)

        self.__pacijenti_listbox = Listbox(levi_frame, width=43, activestyle="none")
        self.__pacijenti_listbox.grid(pady=(5,5))

        self.__pacijenti_listbox.bind("<<ListboxSelect>>",self.promena_selekcije_u_listboxu)


        # ------------>LABELI<------------

        Label(levi_frame, text="LISTA PACIJENATA").grid(sticky=W)

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
        self.__prikazi_button = Button(levi_frame, text="Prikazi" ,state=DISABLED,width=10, command=self.on_prikazi)
        self.__recepti_button = Button(desni_frame, text="Recept", state=DISABLED, width=10, command=self.prikazi_recept)
        self.__ukloni_button = Button(desni_frame, text="Obriši",state=DISABLED,  width=10, command=self.on_obrisi)
        self.__sacuvajizmene_button = Button(desni_frame, text="Sacuvaj", state=DISABLED, width=13, command=self.on_sacuvaj)
        #self.__filtriraj_button = Button(levi_frame, text="Pretraga", width=10, command=self.filtriraj)
        self.__povratak_button = Button(desni_frame, text='Odustani', width=10,command=self.on_odustani)



        red += 1
        self.__dodaj_button.grid(row=red, column=kolona, sticky=W, padx=9, pady=5)
        self.__izmeni_button.grid(row=red, column=kolona)
        self.__recepti_button.grid(row=red, column=kolona, sticky=E)
        self.__ukloni_button.grid(row=red, column=0, sticky=E, padx=9, pady=(5,5))
        self.__prikazi_button.grid(row=2, column=0, sticky= W, pady=(5,5))

        self.__sacuvajizmene_button.grid(row=13, column=1, sticky=W, pady=(5,5))
        self.__povratak_button.grid(row=13,column=1, sticky=E, padx=5, pady=5)
        #self.__filtriraj_button.grid(row=5, pady=(5,5))

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


        self.__jmbgTxt = StringVar(master)
        self.__imeTxt = StringVar(master)
        self.__prezimeTxt = StringVar(master)
        self.__datumTxt = StringVar(master)
        self.__lboTxt = StringVar(master)
        self.__PretragaTxt = StringVar(master)
        #self.__PretragaTxt.trace_add("write",self.filtriraj)

        dbkg = "#dfdfdf"  # siva boja za bekgraund
        self.__jmbg_entry = Entry(desni_frame, width=50, textvariable=self.__jmbgTxt, state='disabled',disabledbackground=dbkg)
        self.__ime_entry = Entry(desni_frame, width=50, textvariable=self.__imeTxt, state='disabled',disabledbackground=dbkg)  # textvariable argument povezuje StringVar, IntVar i sl. objekte sa komponentom
        self.__prezime_entry = Entry(desni_frame, width=50, textvariable=self.__prezimeTxt, state='disabled',disabledbackground=dbkg)
        self.__datum_entry = Entry(desni_frame, width=50, textvariable=self.__datumTxt, state='disabled',disabledbackground=dbkg)
        self.__lbo_entry = Entry(desni_frame, width=50, textvariable=self.__lboTxt, state='disabled',disabledbackground=dbkg)
        self.__pretraga_entry = Entry(levi_frame, width=50, textvariable=self.__PretragaTxt)
        self.__pretraga_entry.bind("<KeyRelease>", self.filtriraj)

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

    # ------------>meni<------------
        meni_bar = Menu(master)

        datoteka_meni = Menu(meni_bar, tearoff=0)
        datoteka_meni.add_command(label="Izlaz", command=self.komanda_izlaz)  # -----u datoteka meni smo dodali komandu izlaz
        meni_bar.add_cascade(label="Zatvori prozor", menu=datoteka_meni)  # -----dodajemo ga u glavni meni pod nazivom datot

        self.config(menu=meni_bar)
        # ------------><------------
        self.transient(master)  # ------prozor se ne pojavljuje se u taskbar-u(u task menageru), već samo njegov roditelj, namestamo da se ovaj prozor ne smatra novom aplikac vec kao deo prvog
        self.popuni_pacijente_listbox()
        self.focus_force()  # kad ga otvorimo da imamo fokus nad ekranom
        # self.grab_set()  #----- modalni

class DodavanjeProzorLekari(Toplevel):


    def on_prikazi_recept(self):
        pass

    def filtriraj(self, evnet=None):
        self.__lekari = ucitaj_lekare()
        karakter_pretrage = self.__PretragaTxt.get().lower()
        rezultat_pretrage = []
        for i in self.__lekari:
            if karakter_pretrage in i.ime.lower() or karakter_pretrage in i.prezime.lower():
                rezultat_pretrage.append(i)
        self.__lekari = rezultat_pretrage
        self.popuni_lekare_listbox( self.__lekari)

    def zakljucaj_dugmice(self):
        self.__izmeni_button1['state'] = DISABLED
        self.__ukloni_button['state'] = DISABLED
        self.__prikazi_button['state'] = DISABLED

    def on_obrisi(self):
        if messagebox.askquestion("UPOZORENJE", "Da li zelite da obrisete lekara, i njegove recepte?", icon="warning") == "no":
            DodajProzorLekar.focus_force(self)
            return

        indeks = self.promena_selekcije_u_listboxu()
        if indeks>=0:
            self.__lekari.pop(indeks)

        sacuvaj_lekare(self.__lekari)
        self.popuni_lekare_listbox( self.__lekari)
        self.zakljucaj_dugmice()
        DodajProzorLekar.focus_force(self)


    def popuni_labele(self, lekar):
        self.__jmbg_labela['text'] = lekar.jmbg
        self.__ime_labela['text'] = lekar.ime
        self.__prezime_labela['text'] = lekar.prezime
        self.__datum_labela['text'] = lekar.datum_rodjenja
        self.__spec_labela['text'] = lekar.specijalizacija

    def on_prikazi(self):
        indeks = self.promena_selekcije_u_listboxu()

        lekar = self.__lekari[indeks]
        print(lekar)

        self.popuni_labele(lekar)

        self.__PretragaTxt.set("")

    def ocisti_labele(self):
        self.__jmbg_labela["text"] = ''
        self.__ime_labela['text'] = ''
        self.__prezime_labela['text'] = ''
        self.__datum_labela['text'] = ''
        self.__spec_labela['text'] = ''

    def promena_selekcije_u_listboxu(self, event=None): #<------sta tacno znaci

        if not self.__lekari_listbox.curselection():
            self.ocisti_labele()
            self.zakljucaj_dugmice()
            return

        self.__izmeni_button1['state'] = NORMAL
        self.__ukloni_button['state'] = NORMAL
        self.__prikazi_button['state'] = NORMAL

        indeks = self.__lekari_listbox.curselection()[0]
        print(indeks)
        return indeks

    def popuni_lekare_listbox(self, lekari):
        self.__lekari_listbox.delete(0, END)

        for i in lekari:
            self.__lekari_listbox.insert(END, i.prezime + " " + i.ime)

        self.ocisti_labele()


    def on_dodaj(self):
        self.__PretragaTxt.set("")
        self.__lekari
        self.popuni_lekare_listbox( self.__lekari) #ne radi,

        # dodaj_prozor = DodajProzorLekar(self)
        # self.wait_window(dodaj_prozor)
        prozor_za_dodavanje_lekara = Toplevel(self.master) #sta znaci self master
        prozor_za_dodavanje_lekara.title("DODAJ LEKARA")
        prozor_za_dodavanje_lekara.geometry("480x230")

        red = 0
        Label(prozor_za_dodavanje_lekara, text="JMBG:").grid(row=red, sticky=E)
        red += 1
        Label(prozor_za_dodavanje_lekara, text="Ime:").grid(row=red, sticky=E)
        red += 1
        Label(prozor_za_dodavanje_lekara, text="Prezime:").grid(row=red, sticky=E)
        red += 1
        Label(prozor_za_dodavanje_lekara, text="Datum rodjenja:").grid(row=red, sticky=E)
        red += 1
        Label(prozor_za_dodavanje_lekara, text="Specijalizacija:").grid(row=red, sticky=E)

        # ------------>button<------------

        self.__dodaj_button = Button(prozor_za_dodavanje_lekara, text="Dodaj", width=10)
        self.__dodaj_button.grid(row=5, padx=5, pady=5)
        self.__povratak_button = Button(prozor_za_dodavanje_lekara, text='Odustani', width=10, command=prozor_za_dodavanje_lekara.destroy)
        self.__povratak_button.grid(row=5, column=1, padx=5, pady=5)
        # ------------>ENTRY<------------

        self.__jmbgTxt = StringVar(prozor_za_dodavanje_lekara)
        self.__imeTxt = StringVar(prozor_za_dodavanje_lekara)
        self.__prezimeTxt = StringVar(prozor_za_dodavanje_lekara)
        self.__datumTxt = StringVar(prozor_za_dodavanje_lekara)
        self.__specTxt = StringVar(prozor_za_dodavanje_lekara)

        self.__jmbg_entry = Entry(prozor_za_dodavanje_lekara, width=50, textvariable=self.__jmbgTxt)
        self.__ime_entry = Entry(prozor_za_dodavanje_lekara, width=50,textvariable=self.__imeTxt)  # textvariable argument povezuje StringVar, IntVar i sl. objekte sa komponentom
        self.__prezime_entry = Entry(prozor_za_dodavanje_lekara, width=50, textvariable=self.__prezimeTxt)
        self.__datum_entry = Entry(prozor_za_dodavanje_lekara, width=50, textvariable=self.__datumTxt)
        self.__spec_entry = Entry(prozor_za_dodavanje_lekara, width=50, textvariable=self.__specTxt)

        red = 0
        kolona = 1
        self.__jmbg_entry.grid(row=red, column=kolona, sticky=W, pady=5)
        red += 1
        self.__ime_entry.grid(row=red, column=kolona, sticky=W, pady=5)
        red += 1
        self.__prezime_entry.grid(row=red, column=kolona, sticky=W, pady=5)
        red += 1
        self.__datum_entry.grid(row=red, column=kolona, sticky=W, pady=5)
        red += 1
        self.__spec_entry.grid(row=red, column=kolona, sticky=W, pady=5)

        self.focus_force()

    def on_izmeni(self):
        self.__PretragaTxt.set("")
        # izmeni_prozor = IzmenaProzorLekar(self)
        # self.wait_window(izmeni_prozor)

        indeks = self.promena_selekcije_u_listboxu()
        lekar = self.__lekari[indeks]

        prozor_za_izmenu_lekara = Toplevel(self.master)

        prozor_za_izmenu_lekara.title("DODAJ LEKARA")
        prozor_za_izmenu_lekara.geometry("480x230")

        # ------------>LABELI<------------

        red = 0
        Label(prozor_za_izmenu_lekara, text="JMBG:").grid(row=red, sticky=E)
        red += 1
        Label(prozor_za_izmenu_lekara, text="Ime:").grid(row=red, sticky=E)
        red += 1
        Label(prozor_za_izmenu_lekara, text="Prezime:").grid(row=red, sticky=E)
        red += 1
        Label(prozor_za_izmenu_lekara, text="Datum rodjenja:").grid(row=red, sticky=E)
        red += 1
        Label(prozor_za_izmenu_lekara, text="Specijalizacija:").grid(row=red, sticky=E)

        # ------------>button<------------

        self.__dodaj_button = Button(prozor_za_izmenu_lekara, text="Izmeni", width=10, command=self.on_izmeni)
        self.__dodaj_button.grid(row=5, padx=5, pady=5)
        self.__povratak_button = Button(prozor_za_izmenu_lekara, text='Odustani', width=10,command=prozor_za_izmenu_lekara.destroy)
        self.__povratak_button.grid(row=5, column=1, padx=5, pady=5)
        # ------------>ENTRY<------------

        self.__jmbgTxt = StringVar(prozor_za_izmenu_lekara)
        self.__imeTxt = StringVar(prozor_za_izmenu_lekara)
        self.__prezimeTxt = StringVar(prozor_za_izmenu_lekara)
        self.__datumTxt = StringVar(prozor_za_izmenu_lekara)
        self.__specTxt = StringVar(prozor_za_izmenu_lekara)

        self.__jmbg_entry = Entry(prozor_za_izmenu_lekara, width=50, textvariable=self.__jmbgTxt, state='disabled')
        self.__ime_entry = Entry(prozor_za_izmenu_lekara, width=50,textvariable=self.__imeTxt)  # textvariable argument povezuje StringVar, IntVar i sl. objekte sa komponentom
        self.__prezime_entry = Entry(prozor_za_izmenu_lekara, width=50, textvariable=self.__prezimeTxt)
        self.__datum_entry = Entry(prozor_za_izmenu_lekara, width=50, textvariable=self.__datumTxt)
        self.__spec_entry = Entry(prozor_za_izmenu_lekara, width=50, textvariable=self.__specTxt)

        red = 0
        kolona = 1
        self.__jmbg_entry.grid(row=red, column=kolona, sticky=W, pady=5)
        red += 1
        self.__ime_entry.grid(row=red, column=kolona, sticky=W, pady=5)
        red += 1
        self.__prezime_entry.grid(row=red, column=kolona, sticky=W, pady=5)
        red += 1
        self.__datum_entry.grid(row=red, column=kolona, sticky=W, pady=5)
        red += 1
        self.__spec_entry.grid(row=red, column=kolona, sticky=W, pady=5)

        self.focus_force()


    def komanda_izlaz(self):
        odgovor = messagebox.askokcancel("Proizvodi", "Da li ste sigurni da želite da napustite aplikaciju?",icon="warning")
        if odgovor:
            self.destroy()  # self pokazuje na tk klasu


    def __init__(self, master):
        super().__init__(master)

        self.__lekari = ucitaj_lekare()

        self.geometry("800x400")
        self.title('LEKARI')

        levi_frame = Frame(self, borderwidth=2, relief="ridge", padx=10, pady=10)
        levi_frame.pack(side=LEFT, fill=BOTH, expand=1)

        Label(levi_frame, text="LISTA LEKARA").grid(sticky=W)

        self.__lekari_listbox = Listbox(levi_frame, width=43, activestyle="none")
        self.__lekari_listbox.grid(padx=9, pady=9)

        self.__lekari_listbox.bind("<<ListboxSelect>>",self.promena_selekcije_u_listboxu)

        desni_frame = Frame(self, borderwidth=2, relief="ridge", padx=10, pady=10)
        desni_frame.pack(side=RIGHT, fill=BOTH)

    # ------------>labele<------------

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

    # ------------>button<------------

        self.__dodaj_button = Button(desni_frame, text="Dodaj", width=10, command=self.on_dodaj)
        self.__izmeni_button1 = Button(desni_frame, text="Izmeni", state = DISABLED,  width=10, command=self.on_izmeni)
        self.__prikazi_button = Button(levi_frame, text="Prikazi", state=DISABLED, width=10, command = self.on_prikazi)
        self.__recepti_button = Button(desni_frame, text="Recept", state=DISABLED, width=10, command=self.on_prikazi_recept)
        self.__ukloni_button = Button(desni_frame, text="Obriši", state=DISABLED, width=10, command=self.on_obrisi)
        # self.__filtriraj_button = Button(levi_frame, text="Pretraga", width=10, command=self.filtriraj)

        # self.__sacuvajizmene_button = Button(desni_frame, text="Sacuvaj", state=DISABLED, width=13)
        # self.__povratak_button = Button(desni_frame, text='Odustani', width=10)

        red += 1
        self.__ukloni_button.grid(row=red, column=0, sticky=E, padx=9, pady=5)
        self.__dodaj_button.grid(row=red, column=kolona, padx=9, pady=5)
        self.__izmeni_button1.grid(row=red, column=2, sticky=W, padx=9, pady=5)  #sticky=W, column=1
        self.__recepti_button.grid(row=red, column=3, sticky=E, padx=9, pady=5)  #sticky=E, column=1
        self.__prikazi_button.grid(row=2, column=0, sticky=W, padx=9, pady=5)
        # self.__filtriraj_button.grid(row=5, pady=(5, 5))

        # self.__sacuvajizmene_button.grid(row=13, column=1, sticky=W, pady=(5, 5))
        # self.__povratak_button.grid(row=13, column=1, sticky=E, padx=5, pady=5)

        red += 1
        Label(desni_frame, text="").grid(row=red)

    # ------------>ENTRY<------------

        self.__PretragaTxt = StringVar(master)
        self.__pretraga_entry = Entry(levi_frame, width=50, textvariable=self.__PretragaTxt)
        self.__pretraga_entry.grid(row=4, column=0, sticky=W, pady=(5, 5))
        self.__pretraga_entry.bind("<KeyRelease>", self.filtriraj)





        # red = 8
        # Label(desni_frame, text="JMBG:").grid(row=red, sticky=E)
        # red += 1
        # Label(desni_frame, text="Ime:").grid(row=red, sticky=E)
        # red += 1
        # Label(desni_frame, text="Prezime:").grid(row=red, sticky=E)
        # red += 1
        # Label(desni_frame, text="Datum rodjenja:").grid(row=red, sticky=E)
        # red += 1
        # Label(desni_frame, text="Specijalizacija:").grid(row=red, sticky=E)
        #
        # self.__jmbgTxt = StringVar(master)
        # self.__imeTxt = StringVar(master)
        # self.__prezimeTxt = StringVar(master)
        # self.__datumTxt = StringVar(master)
        # self.__specTxt = StringVar(master)
        #
        # self.__jmbg_entry = Entry(desni_frame, width=50, textvariable=self.__jmbgTxt)
        # self.__ime_entry = Entry(desni_frame, width=50, textvariable=self.__imeTxt)  # textvariable argument povezuje StringVar, IntVar i sl. objekte sa komponentom
        # self.__prezime_entry = Entry(desni_frame, width=50, textvariable=self.__prezimeTxt)
        # self.__datum_entry = Entry(desni_frame, width=50, textvariable=self.__datumTxt)
        # self.__spec_entry = Entry(desni_frame, width=50, textvariable=self.__specTxt)
        #
        # red = 8
        # kolona = 1
        # self.__jmbg_entry.grid(row=red, column=kolona, sticky=W, pady=(5,5))
        # red += 1
        # self.__ime_entry.grid(row=red, column=kolona, sticky=W, pady=(5,5))
        # red += 1
        # self.__prezime_entry.grid(row=red, column=kolona, sticky=W, pady=(5,5))
        # red += 1
        # self.__datum_entry.grid(row=red, column=kolona, sticky=W, pady=(5,5))
        # red += 1
        # self.__spec_entry.grid(row=red, column=kolona, sticky=W, pady=(5,5))

        # ------------>meni<------------

        meni_bar = Menu(master)

        datoteka_meni = Menu(meni_bar, tearoff=0)
        datoteka_meni.add_command(label="Izlaz",command=self.komanda_izlaz)  # -----u datoteka meni smo dodali komandu izlaz
        meni_bar.add_cascade(label="Zatvori prozor",menu=datoteka_meni)  # -----dodajemo ga u glavni meni pod nazivom datot

        self.config(menu=meni_bar)

    # ------------><------------

        self.popuni_lekare_listbox( self.__lekari)
        self.transient(master)
        self.focus_force()


class DodajProzorLekar(Toplevel):

    def on_odustani(self):
        self.__jmbgTxt.set('')
        self.__imeTxt.set('')
        self.__prezimeTxt.set('')
        self.__datumTxt.set('')
        self.__specTxt.set('')

        self.destroy()

    def on_dodaj(self):
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
        spec = self.specijalizacija_validacija()
        if not spec:
            return

        l = Lekar(jmbg, ime, prezime, datum,spec,[])
        lekari = ucitaj_lekare()
        lekari.append(l)

        self.__lekari = lekari
        sacuvaj_lekare(self.__lekari)

        DodajProzorLekar.destroy(self)


    def jmbg_validacija(self):
        try:
            jmbg = self.__jmbgTxt.get()
            if len(str(jmbg)) != 13:
                messagebox.showerror("Greska", "Jmbg mora da sadrzi tacno 13 karaktera!" + "{:>2} {}".format(len(str(jmbg)), "karaktera"))
                return None
        except TclError:
            messagebox.showerror("Greška", "jmbg treba da bude sastavljen od brojeva")
            return None

        return jmbg

    def ime_validacija(self):
        ime = self.__imeTxt.get()

        if len(ime) < 1:
            messagebox.showerror("Greska", "ime mora da sadrzi bar 2 karaktera!")
            return None

        return  ime

    def prezime_validacija(self):
        prezime = self.__prezimeTxt.get()
        if len(prezime) < 2:
            messagebox.showerror("Greska", "Prezime mora da sadrzi bar 2 karaktera!")
            return None

        return prezime

    def specijalizacija_validacija(self):
        spec = self.__specTxt.get()
        if len(spec) < 2:
            messagebox.showerror("Greska", "Specijalizacija mora da sadrzi bar 2 karaktera!")
            return None

        return spec


    def __init__(self, master):
        super().__init__(master)

        # self.__lekari = ucitaj_lekare() #da li ovo moze ovako     <<<============================




        self.geometry("480x230")
        self.title('DODAVANJE')


    # ------------>LABELI<------------

        red = 0
        Label(self, text="JMBG:").grid(row=red, sticky=E)
        red += 1
        Label(self, text="Ime:").grid(row=red, sticky=E)
        red += 1
        Label(self, text="Prezime:").grid(row=red, sticky=E)
        red += 1
        Label(self, text="Datum rodjenja:").grid(row=red, sticky=E)
        red += 1
        Label(self, text="Specijalizacija:").grid(row=red, sticky=E)

    # ------------>button<------------

        self.__dodaj_button = Button(self, text="Dodaj", width=10, command=self.on_dodaj)
        self.__dodaj_button.grid(row=5, padx=5,pady=5)
        self.__povratak_button = Button(self, text='Odustani', width=10, command=self.on_odustani)
        self.__povratak_button.grid(row=5,column=1, padx=5,pady=5)


    # ------------>ENTRY<------------

        self.__jmbgTxt = StringVar(master)
        self.__imeTxt = StringVar(master)
        self.__prezimeTxt = StringVar(master)
        self.__datumTxt = StringVar(master)
        self.__specTxt = StringVar(master)

        self.__jmbg_entry = Entry(self, width=50, textvariable=self.__jmbgTxt)
        self.__ime_entry = Entry(self, width=50, textvariable=self.__imeTxt)  # textvariable argument povezuje StringVar, IntVar i sl. objekte sa komponentom
        self.__prezime_entry = Entry(self, width=50, textvariable=self.__prezimeTxt)
        self.__datum_entry = Entry(self, width=50, textvariable=self.__datumTxt)
        self.__spec_entry = Entry(self, width=50, textvariable=self.__specTxt)


        red = 0
        kolona = 1
        self.__jmbg_entry.grid(row=red, column=kolona, sticky=W, pady=5)
        red += 1
        self.__ime_entry.grid(row=red, column=kolona, sticky=W, pady=5)
        red += 1
        self.__prezime_entry.grid(row=red, column=kolona, sticky=W, pady=5)
        red += 1
        self.__datum_entry.grid(row=red, column=kolona, sticky=W, pady=5)
        red += 1
        self.__spec_entry.grid(row=red, column=kolona, sticky=W, pady=5)

        self.focus_force()


class IzmenaProzorLekar(Toplevel):

    def on_prikazi(self):
        pass
        # indeks = DodavanjeProzorLekari.indeks
        # lekari = ucitaj_lekare()
        # lekar = lekari[indeks]
        # self.__jmbgTxt.set(lekar.jmbg)
        # self.__imeTxt.set(lekar.ime)
        # self.__prezimeTxt.set(lekar.prezime)
        # self.__datumTxt.set(lekar.datum_rodjenja)
        # self.__specTxt.set(lekar.specijalizacija)



    def on_izmeni(self):
        pass
        # indeks = DodavanjeProzorLekari.indeks
        # if indeks == -1:
        #     return
        # self.__lekari = ucitaj_lekare()
        # l = self.__lekari[indeks]
        #
        # jmbg = self.__jmbgTxt.get()
        # if not jmbg:
        #     return
        # ime = self.ime_validacija()
        # if not ime:
        #     return
        # prezime = self.prezime_validacija()
        # if not prezime:
        #     return
        # datum = self.__datumTxt.get()
        # spec = self.specijalizacija_validacija()
        # if not spec:
        #     return
        # lekar = Lekar(jmbg, ime, prezime, datum,spec,[])
        # self.__lekari[indeks] = lekar
        # sacuvaj_lekare(self.__lekari)


    def ime_validacija(self):
        ime = self.__imeTxt.get()

        if len(ime) < 1:
            messagebox.showerror("Greska", "ime mora da sadrzi bar 2 karaktera!")
            return None

        return  ime

    def prezime_validacija(self):
        prezime = self.__prezimeTxt.get()
        if len(prezime) < 2:
            messagebox.showerror("Greska", "Prezime mora da sadrzi bar 2 karaktera!")
            return None

        return prezime

    def specijalizacija_validacija(self):
        spec = self.__specTxt.get()
        if len(spec) < 2:
            messagebox.showerror("Greska", "Specijalizacija mora da sadrzi bar 2 karaktera!")
            return None

        return spec

    def __init__(self, master):
        super().__init__(master)
        self.geometry("480x230")
        self.title('IZMENA')

        # ------------>LABELI<------------

        red = 0
        Label(self, text="JMBG:").grid(row=red, sticky=E)
        red += 1
        Label(self, text="Ime:").grid(row=red, sticky=E)
        red += 1
        Label(self, text="Prezime:").grid(row=red, sticky=E)
        red += 1
        Label(self, text="Datum rodjenja:").grid(row=red, sticky=E)
        red += 1
        Label(self, text="Specijalizacija:").grid(row=red, sticky=E)

        # ------------>button<------------

        self.__dodaj_button = Button(self, text="Izmeni", width=10, command=self.on_izmeni)
        self.__dodaj_button.grid(row=5, padx=5, pady=5)
        self.__prikazi_button= Button(self, text="Prikazi lekara za izmenu", width=20, command=self.on_prikazi)
        self.__prikazi_button.grid(row=5, padx=5, pady=5 , sticky=W)
        # ------------>ENTRY<------------

        self.__jmbgTxt = StringVar(master)
        self.__imeTxt = StringVar(master)
        self.__prezimeTxt = StringVar(master)
        self.__datumTxt = StringVar(master)
        self.__specTxt = StringVar(master)

        self.__jmbg_entry = Entry(self, width=50,  textvariable=self.__jmbgTxt, state='disabled')
        self.__ime_entry = Entry(self, width=50, textvariable=self.__imeTxt)  # textvariable argument povezuje StringVar, IntVar i sl. objekte sa komponentom
        self.__prezime_entry = Entry(self, width=50, textvariable=self.__prezimeTxt)
        self.__datum_entry = Entry(self, width=50, textvariable=self.__datumTxt)
        self.__spec_entry = Entry(self, width=50, textvariable=self.__specTxt)

        red = 0
        kolona = 1
        self.__jmbg_entry.grid(row=red, column=kolona, sticky=W, pady=5)
        red += 1
        self.__ime_entry.grid(row=red, column=kolona, sticky=W, pady=5)
        red += 1
        self.__prezime_entry.grid(row=red, column=kolona, sticky=W, pady=5)
        red += 1
        self.__datum_entry.grid(row=red, column=kolona, sticky=W, pady=5)
        red += 1
        self.__spec_entry.grid(row=red, column=kolona, sticky=W, pady=5)

        self.focus_force()





class ProzorLekovi(Toplevel):
    def on_odustani(self):
        self.ocisti_entry()
        self.disable_entry()
        self.zakljucaj_dugmice()


    def ocisti_entry(self):

        self.__jklTxt.set('')
        self.__nazivTxt.set('')
        self.__prpozvodjacTxt.set('')
        self.__tiplekaTxt.set('')

    def disable_entry(self):
        self.__jkl_entry.configure(state="disabled")
        self.__naziv_entry.configure(state="disabled")
        self.__proizvodjac_entry.configure(state="disabled")
        self.__tipleka_entry.configure(state="disabled")

    def enable_entry(self):
        self.__jkl_entry.configure(state="normal")
        self.__naziv_entry.configure(state="normal")
        self.__proizvodjac_entry.configure(state="normal")
        self.__tipleka_entry.configure(state="normal")

    def on_sacuvaj(self):
        if self.__selektovani is None:
            jkl = self.jkl_validacija()
            if not jkl:
                return
            naziv = self.naziv_validacija()
            if not naziv:
                return
            proiz = self.proiz_validacija()
            if not proiz:
                return
            tip = self.tip_leka_validacija()
            if not tip:
                return

            l = Lek(jkl,naziv,proiz,tip,[])
            lekovi = ucitaj_lekovi()
            lekovi.append(l)
            self.__lekovi = lekovi
            sacuvaj_lekovi(self.__lekovi)
            self.popuni_lekove_listbox()

            self.__lekovi_listbox.selection_set(END)
            indeks = self.prmena_selekcije_u_listboxu()
            dodati_lrk = self.__lekovi[indeks]
            self.popuni_labele(dodati_lrk)



            self.ocisti_entry()
            self.disable_entry()
            self.zakljucaj_dugmice()

        else: #izmena, pukne nekad program nzm zasto nekad nee wtffff <===================
            indeks = self.prmena_selekcije_u_listboxu()

            l = self.__lekovi[indeks]

            jkl = self.__jklTxt.get()
            naziv = self.naziv_validacija()
            if not naziv:
                return
            proiz = self.proiz_validacija()
            if not proiz:
                return
            tip = self.tip_leka_validacija()
            if not tip:
                return
            lek = Lek(jkl,naziv,proiz,tip, l.recepti)

            self.__lekovi[indeks] = lek
            sacuvaj_lekovi(self.__lekovi)
            self.popuni_lekove_listbox()


            self.ocisti_entry()
            self.disable_entry()
            self.zakljucaj_dugmice()

    def on_izmeni(self):
        self.ocisti_labele()
        self.enable_entry()
        self.__sacuvajizmene_button['state'] = NORMAL
        self.__odustani_button['state'] = NORMAL

        indeks = self.prmena_selekcije_u_listboxu()
        if indeks == -1:
            return

        lek = self.__lekovi[indeks]

        self.__jkl_entry.configure(state="disabled")

        self.__jklTxt.set(lek.jkl)
        self.__nazivTxt.set(lek.naziv)
        self.__prpozvodjacTxt.set(lek.proizvodjac)
        self.__tiplekaTxt.set(lek.tip_leka)

        self.__selektovani = True


    def on_dodaj(self):
        self.__sacuvajizmene_button['state'] = NORMAL
        self.ocisti_labele()
        self.ocisti_entry()
        self.enable_entry()
        self.__odustani_button['state'] = NORMAL

        self.__selektovani = None
        self.__jkl_entry.focus()

        self.__PretragaTxt.set("")
        # self.popuni_lekove_listbox()



    def filtriraj(self, event=None):
        self.__lekovi = ucitaj_lekovi()
        karakter_pretrage = self.__PretragaTxt.get().lower()
        rezultat_pretrage = []
        for i in self.__lekovi:
            if karakter_pretrage in i.naziv.lower():
                rezultat_pretrage.append(i)
        self.__lekovi = rezultat_pretrage
        self.popuni_lekove_listbox()


    def on_obrisi(self):
        if messagebox.askquestion("UPOZORENJE", "Da li zelite da obrisete lek, i njegove recepte?",icon="warning") == "no":
            return

        indeks = self.prmena_selekcije_u_listboxu()
        if indeks >= 0:
            self.__lekovi.pop(indeks)

        sacuvaj_lekovi(self.__lekovi)
        self.popuni_lekove_listbox()
        self.zakljucaj_dugmice()

    def popuni_labele(self, lek):
        self.__jkl_labela["text"] = lek.jkl
        self.__naziv_labela['text'] = lek.naziv
        self.__proizvodjac_labela['text'] = lek.proizvodjac
        self.__tip_leka_labela['text'] = lek.tip_leka

    def on_prikazi(self):
        indeks = self.prmena_selekcije_u_listboxu()
        lek = self.__lekovi[indeks]
        print(lek)
        self.popuni_labele(lek)

    def zakljucaj_dugmice(self):
        self.__izmeni_button['state'] = DISABLED
        self.__ukloni_button['state'] = DISABLED
        self.__dodaj_button['state'] = DISABLED
        self.__odustani_button['state'] = DISABLED

    def prmena_selekcije_u_listboxu(self, event = None):
        if not self.__lekovi_listbox.curselection():
            self.ocisti_labele()
            self.zakljucaj_dugmice()
            self.__dodaj_button['state'] = NORMAL
            return

        self.__izmeni_button['state'] = NORMAL
        self.__ukloni_button['state'] = NORMAL
        self.__prikazi_button['state'] = NORMAL
        self.ocisti_labele()


        indeks = self.__lekovi_listbox.curselection()[0]
        print(indeks)
        return indeks


    def ocisti_labele(self):
        self.__jkl_labela["text"] = ''
        self.__naziv_labela['text'] = ''
        self.__proizvodjac_labela['text'] = ''
        self.__tip_leka_labela['text'] = ''

    def popuni_lekove_listbox(self):
        self.__lekovi_listbox.delete(0, END)

        for i in self.__lekovi:
            self.__lekovi_listbox.insert(END, i.naziv)

        self.ocisti_labele()
    def komanda_izlaz(self):
        odgovor = messagebox.askokcancel("Proizvodi", "Da li ste sigurni da želite da napustite aplikaciju?",icon="warning")
        if odgovor:
            self.destroy()  # self pokazuje na tk klasu

    def proveri_jkl(self, jkl):
        lekovi = self.__lekovi
        for lek in lekovi:
            if jkl == lek.jkl:
                return None
        return jkl

    def jkl_validacija(self):
        try:
            jkl = self.__jklTxt.get()
            if len(str(jkl)) != 7:
                messagebox.showerror("Greska","JKL mora da sadrzi tacno 7 karaktera!" + "{:>2} {}".format(len(str(jkl)),"karaktera"))
                return None
        except TclError:
            messagebox.showerror("Greška", "JKL treba da bude sastavljen od brojeva")
            return None

        if self.proveri_jkl(jkl):

            return jkl
        else:
            messagebox.showerror("Greska", "Pacijent sa unetim JKL-om vec postoji")
            return None

    def naziv_validacija(self):
        naziv = self.__nazivTxt.get()

        if len(naziv) < 1:
            messagebox.showerror("Greska", "Naziv mora da sadrzi bar 2 karaktera!")
            return  None

        return naziv

    def proiz_validacija(self):
        proiz = self.__prpozvodjacTxt.get()

        if len(proiz) < 1:
            messagebox.showerror("Greska", "Proizvodjac mora da sadrzi bar 2 karaktera!")
            return  None

        return proiz

    def tip_leka_validacija(self):
        tip = self.__tiplekaTxt.get()

        if len(tip) < 1:
            messagebox.showerror("Greska", "Tip leka mora da sadrzi bar 2 karaktera!")
            return  None
        return tip

    def __init__(self, master):
        super().__init__(master)

        self.__lekovi = ucitaj_lekovi()

        self.geometry("810x500")
        self.title('LEKOVI')

    # ------------>FRAME<------------

        levi_frame = Frame(self, borderwidth=2, relief="ridge", padx=10, pady=10)
        levi_frame.pack(side=LEFT, fill=BOTH, expand=1)

        desni_frame = Frame(self, borderwidth=2, relief="ridge", padx=10, pady=10)
        desni_frame.pack(side=RIGHT, fill=BOTH, expand=1)


        self.__lekovi_listbox = Listbox(levi_frame, width=43, activestyle="none")
        self.__lekovi_listbox.grid(row =1,column=0, pady=(5, 5))
        self.__lekovi_listbox.bind("<<ListboxSelect>>",self.prmena_selekcije_u_listboxu)

    # ------------>LABELI<------------

        Label(levi_frame, text="LISTA LEKOVA").grid(row=0, column=0,sticky=W)

        red = 0
        Label(desni_frame, text="JKL:").grid(row=red, sticky=E)  # sticky argument određuje horinzotalno poravnanje kolone (E, W), odnosno vertikalno poravnanje reda (N, S)
        red += 1
        Label(desni_frame, text="Naziv:").grid(row=red, sticky=E)
        red += 1
        Label(desni_frame, text="Proizvodjac:").grid(row=red, sticky=E)
        red += 1
        Label(desni_frame, text="Tip Leka:").grid(row=red, sticky=E)


        self.__jkl_labela = Label(desni_frame)
        self.__naziv_labela = Label(desni_frame)
        self.__proizvodjac_labela = Label(desni_frame)
        self.__tip_leka_labela = Label(desni_frame)


        red = 0
        kolona = 1
        self.__jkl_labela.grid(row=red, column=kolona, sticky=W)
        red += 1
        self.__naziv_labela.grid(row=red, column=kolona, sticky=W)
        red += 1
        self.__proizvodjac_labela.grid(row=red, column=kolona, sticky=W)
        red += 1
        self.__tip_leka_labela.grid(row=red, column=kolona, sticky=W)

        red += 1
        Label(desni_frame, text="").grid(row=red)

        # ------------>button<------------

        self.__dodaj_button = Button(desni_frame, text="Dodaj", width=10, command=self.on_dodaj)
        self.__izmeni_button = Button(desni_frame, text="Izmeni", state=DISABLED, width=10,command=self.on_izmeni)
        self.__prikazi_button = Button(levi_frame, text="Prikazi", state=DISABLED, width=10, command=self.on_prikazi)
        self.__ukloni_button = Button(desni_frame, text="Obriši", state=DISABLED, width=10, command = self.on_obrisi)
        self.__sacuvajizmene_button = Button(desni_frame, text="Sacuvaj", state=DISABLED, width=13, command=self.on_sacuvaj)
        # self.__filtriraj_button = Button(levi_frame, text="Pretraga", width=10, command=self.filtriraj)
        self.__odustani_button = Button(desni_frame, state=DISABLED,text='Odustani', width=10, command=self.on_odustani)

        red += 1
        self.__dodaj_button.grid(row=red, column=kolona, sticky=W, padx=9, pady=5)
        self.__izmeni_button.grid(row=red, column=kolona)
        self.__ukloni_button.grid(row=red, column=0, sticky=E, padx=9, pady=(5, 5))
        self.__prikazi_button.grid(row=2, column=0, sticky=W, pady=(5, 5))

        self.__sacuvajizmene_button.grid(row=13, column=1, sticky=W, pady=(5, 5))
        self.__odustani_button.grid(row=13, column=1, sticky=E, padx=5, pady=5)
        # self.__filtriraj_button.grid(row=5, pady=(5, 5))

        red += 1
        Label(desni_frame, text="").grid(row=red)

        # ------------>ENTRY<------------

        red = 8
        Label(desni_frame, text="JKL:").grid(row=red, sticky=E)
        red += 1
        Label(desni_frame, text="Naziv:").grid(row=red, sticky=E)
        red += 1
        Label(desni_frame, text="Proizvodjac:").grid(row=red, sticky=E)
        red += 1
        Label(desni_frame, text="Tip leka:").grid(row=red, sticky=E)

        Label(levi_frame, text="Pretrazi:").grid(row=3, sticky=W)

        self.__jklTxt = StringVar(master)
        self.__nazivTxt = StringVar(master)
        self.__prpozvodjacTxt = StringVar(master)
        self.__tiplekaTxt = StringVar(master)

        self.__PretragaTxt = StringVar(master)

        dbkg = "#dfdfdf"  # siva boja za bekgraund
        self.__jkl_entry = Entry(desni_frame, width=50, textvariable=self.__jklTxt, state='disabled', disabledbackground=dbkg)
        self.__naziv_entry = Entry(desni_frame, width=50, textvariable=self.__nazivTxt, state='disabled', disabledbackground=dbkg)  # textvariable argument povezuje StringVar, IntVar i sl. objekte sa komponentom
        self.__proizvodjac_entry = Entry(desni_frame, width=50, textvariable=self.__prpozvodjacTxt, state='disabled', disabledbackground=dbkg)
        self.__tipleka_entry = Entry(desni_frame, width=50, textvariable=self.__tiplekaTxt, state='disabled',disabledbackground=dbkg)
        self.__pretraga_entry = Entry(levi_frame, width=50, textvariable=self.__PretragaTxt)
        self.__pretraga_entry.bind("<KeyRelease>", self.filtriraj)

        red = 8
        kolona = 1
        self.__jkl_entry.grid(row=red, column=kolona, sticky=W, pady=(5, 5))
        red += 1
        self.__naziv_entry.grid(row=red, column=kolona, sticky=W, pady=(5, 5))
        red += 1
        self.__proizvodjac_entry.grid(row=red, column=kolona, sticky=W, pady=(5, 5))
        red += 1
        self.__tipleka_entry.grid(row=red, column=kolona, sticky=W, pady=(5, 5))


        self.__pretraga_entry.grid(row=4, column=0, sticky=W, pady=(5, 5))


        # ------------>meni<------------
        meni_bar = Menu(master)

        datoteka_meni = Menu(meni_bar, tearoff=0)
        datoteka_meni.add_command(label="Izlaz", command=self.komanda_izlaz)  # -----u datoteka meni smo dodali komandu izlaz
        meni_bar.add_cascade(label="Zatvori prozor", menu=datoteka_meni)  # -----dodajemo ga u glavni meni pod nazivom datot

        self.config(menu=meni_bar)
        # ------------><------------
        self.popuni_lekove_listbox()
        self.transient(master)  # ------prozor se ne pojavljuje se u taskbar-u(u task menageru), već samo njegov roditelj, namestamo da se ovaj prozor ne smatra novom aplikac vec kao deo prvog
        self.focus_force()  # kad ga otvorimo da imamo fokus nad ekranom
        # self.grab_set()  #----- modalni



class ProorRecepti(Toplevel):
    def on_obrisi(self):
        pass

    def on_dodaj(self):
        pass
    def on_izmeni(self):
        pass

    def __init__(self, master):
        super().__init__(master)

        self.geometry("810x500")
        self.title('LEKOVI')

        self.__recepti =ucitaj_recepte()
        self.__pacijenti = ucitaj_pacijente()

        # ------------>FRAME<------------

        levi_frame = Frame(self, borderwidth=2, relief="ridge", padx=10, pady=10)
        levi_frame.pack(side=LEFT, fill=BOTH, expand=1)

        desni_frame = Frame(self, borderwidth=2, relief="ridge", padx=10, pady=10)
        desni_frame.pack(side=RIGHT, fill=BOTH, expand=1)

        # ------------>COMBOBOX<------------

        pacijenti = []
        for pacijent in self.__pacijenti:
            pacijenti.append(pacijent.ime + " " + pacijent.prezime)
        print(pacijenti)

        self.__pacijent_combobox = Combobox(levi_frame, width=25, state="readonly", values=pacijenti)

        self.__pacijent_combobox.grid(row=0)

        # ------------>listbox<------------

        self.__recepti_listbox = Listbox(levi_frame, width=43, activestyle="none")
        self.__recepti_listbox.grid(row=2, column=0, pady=5, padx=5)
        # self.__recepti_listbox.bind("<<ListboxSelect>>", self.prmena_selekcije_u_listboxu)

        # ------------>LABELI<------------

        Label(levi_frame, text="LISTA RECEPATA").grid(row=1, column=0,sticky=W)

        red = 0
        Label(desni_frame, text="Pacijent:").grid(row=red,sticky=E)  # sticky argument određuje horinzotalno poravnanje kolone (E, W), odnosno vertikalno poravnanje reda (N, S)
        red += 1
        Label(desni_frame, text="Datum i vreme:").grid(row=red, sticky=E)
        red += 1
        Label(desni_frame, text="Izvestaj:").grid(row=red, sticky=E)
        red += 1
        Label(desni_frame, text="lekar:").grid(row=red, sticky=E)
        red += 1
        Label(desni_frame,text="Lek:").grid(row=red, sticky=E)
        red += 1
        Label(desni_frame, text="Kolicina:").grid(row=red, sticky=E)



        self.__pacijent_labela = Label(desni_frame)
        self.__datum_labela = Label(desni_frame)
        self.__izvestaj_labela = Label(desni_frame)
        self.__lekar_labela = Label(desni_frame)
        self.__lek_labela = Label(desni_frame)
        self.__kolicina_labela = Label(desni_frame)

        red = 0
        kolona = 1
        self.__pacijent_labela.grid(row=red, column=kolona, sticky=W)
        red += 1
        self.__datum_labela.grid(row=red, column=kolona, sticky=W)
        red += 1
        self.__izvestaj_labela.grid(row=red, column=kolona, sticky=W)
        red += 1
        self.__lekar_labela.grid(row=red, column=kolona, sticky=W)
        red += 1
        self.__lek_labela.grid(row=red, column=kolona, sticky=W)
        red += 1
        self.__kolicina_labela.grid(row=red, column=kolona, sticky=W)

        red += 1
        Label(desni_frame, text="").grid(row=red)

        # ------------>button<------------

        self.__dodaj_button = Button(desni_frame, text="Dodaj", width=10, command=self.on_dodaj)
        self.__izmeni_button = Button(desni_frame, text="Izmeni", state=DISABLED, width=10, command=self.on_izmeni)
        self.__ukloni_button = Button(desni_frame, text="Obriši", state=DISABLED, width=10, command=self.on_obrisi)

        red += 1
        self.__ukloni_button.grid(row=red, column=0, sticky=E, padx=9, pady=(5, 5))
        self.__dodaj_button.grid(row=red, column=1, sticky=W, padx=9, pady=5)
        self.__izmeni_button.grid(row=red, column=2,sticky=E, padx=9, pady=5)

def main():
    glavni_prozor = AppGui()

    glavni_prozor.mainloop()

    # p1 = Pacijent("1231231231231","milos","obilic","01.01.2001","1234567",[])
    # p2 = Pacijent("1231231231231", "zoran", "obilic", "01.01.2002", "1234561", [])
    # p3 = Pacijent("1231231231231", "marko", "obilic", "01.01.2003", "1234562", [])
    # p4 = Pacijent("1231231231231", "milan", "obilic", "01.01.2004", "1234563", [])
    # pacijenti = [p1, p2]
    # sacuvaj_pacijente(pacijenti)
    #
    #
    #
    # l1 = Lekar("1231231231231","milos","obilic","01.01.2001", "Ginekolog",[])
    # l2 = Lekar("1231231231231", "zoran", "obilic", "01.01.2002",  "Dermatolog", [])
    # l3 = Lekar("1231231231231", "milan", "obilic", "01.01.2004", "neuro hirurgija", [])
    #
    # lekari =[l1,l2,l3]
    # sacuvaj_lekare(lekari)
    #
    #
    # lek1 = Lek("11111111","andol", "galenika", "antibiotik", [])
    # lek2 = Lek("22222222", "brufen", "galenika", "antibiotik", [])
    # lek3 = Lek("33333333", "paracetanol", "sinofarm", "antibiotik", [])
    #
    # lekovi = [lek1, lek2, lek3]
    # sacuvaj_lekovi(lekovi)
    #
    # p1 = Pacijent("1231231231231", "milos", "obilic", "01.01.2001", "1234567", [])
    # p2 = Pacijent("1231231231231", "zoran", "obilic", "01.01.2002", "1234561", [])
    # l1 = Lekar("1231231231231", "milos", "obilic", "01.01.2001", "Ginekolog", [])
    # l2 = Lekar("1231231231231", "zoran", "obilic", "01.01.2002", "Dermatolog", [])
    # lek1 = Lek("11111111", "andol", "galenika", "antibiotik", [])
    # lek2 = Lek("22222222", "brufen", "galenika", "antibiotik", [])
    #
    # r1 = Recept(p1, "21.05.2001", "stanje bolje", l1,lek1, "12")
    # r2 = Recept(p2, "21.05.2001", "stanje gore", l2, lek2, "4")
    # recepti = [r1, r2]
    # sacuvaj_recepte(recepti)

main()

