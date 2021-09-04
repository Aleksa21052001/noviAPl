import datetime
from GuiApp.guiApp import *

def main():
    glavni_prozor = AppGui()

    glavni_prozor.mainloop()

    #
    # p1 = Pacijent("2105001800456","Aleksa","Cosovic","21.05.2001.","12587532753",[])
    # p2 = Pacijent("2103998800776", "Stefan", "Markovic", "21.03.1999.", "97867452086", [])
    # p3 = Pacijent("2307970800998", "Ivan", "Orosic", "23.07.1970.", "63932517585", [])
    # p4 = Pacijent("0304965008055", "Milana", "Dobric", "03.04.1965.", "06847284751", [])
    # pacijenti = [p1, p2,p3,p4]
    # sacuvaj_pacijente(pacijenti)
    #
    #
    #
    # l1 = Lekar("1805989529172","Danilo","Cosovic","18.05.1989.", "Psihoterapeut",[])
    # l2 = Lekar("1804983636387", "Luka", "krtinic", "18.04.1983.",  "Psihijatar", [])
    # l3 = Lekar("1803985723423", "Milan", "Stankovic", "18.03.1985.", "Psiholog", [])
    # l4 = Lekar("2342342342341", "Ruza", "kamenkovic", "11.07.1999.", "Neurolog", [])
    # l5 = Lekar("1245436234235", "Dragana", "Orlovic", "15.03.1976.", "Pedijatar", [])
    #
    #
    # lekari = [l1,l2,l3,l4,l5]
    # sacuvaj_lekare(lekari)
    #
    # lek1 = Lek("2157101","Andol", "Galenika", "Antibiotik", [])
    # lek2 = Lek("1122460", "Brufen", "Pharmanova", "Analgetik", [])
    # lek3 = Lek("2342342", "Paracetanol", "Hemofarm", "Antiseptik", [])
    # lek4 = Lek("2343244", "norepinefrin", "Galenika", "Trankvilajzeri:", [])
    # lek5 = Lek("2342342", "venetoklaks", "Pharmanova", "Stabilizatori raspoloženja", [])
    # lek6 = Lek("2342342", "Andalektinibol", "Hemofarm", "Antipiretici", [])
    # lekovi= [lek1,lek2,lek3, lek4, lek5,lek6]
    # sacuvaj_lekovi(lekovi)
    #
    # r1 = Recept(p1, datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "stanje ide na bolje", l1, lek1, "12")
    # r2 = Recept(p2, datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "stanje je sve gore", l2, lek2, "4")
    # r3 = Recept(p3, datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "Za sada stabilno stanje",l2,lek3,"2")
    # r4 =  Recept(p1, datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "Pogorsava se", l3, lek3, "12")
    # recepti = [r1, r2,r3,r4]
    # sacuvaj_recepte(recepti)


main()