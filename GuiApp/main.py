
from GuiApp.guiApp import *

def main():
    glavni_prozor = AppGui()

    glavni_prozor.mainloop()
    #
    p1 = Pacijent("2105001800456","Aleksa","Cosovic","21.05.2001.","12587532753",[])
    p2 = Pacijent("2103998800776", "Stefan", "Markovic", "21.03.1999.", "97867452086", [])
    p3 = Pacijent("2307970800998", "Ivan", "Orosic", "23.07.1970.", "63932517585", [])
    p4 = Pacijent("0304965008055", "Milana", "Dobric", "03.04.1965.", "06847284751", [])
    pacijenti = [p1, p2,p3,p4]
    sacuvaj_pacijente(pacijenti)



    l1 = Lekar("1805989529172","Danilo","Cosovic","18.05.1989.", "Psihoterapeut",[])
    l2 = Lekar("1804983636387", "Luka", "krtinic", "18.04.1983.",  "Dermatolog", [])
    l3 = Lekar("1803985727362", "Ana", "Prokic", "18.03.1985.", "Psiholog", [])

    lekari = [l1,l2,l3]
    sacuvaj_lekare(lekari)


    lek1 = Lek("2157101","Andol", "Galenika", "Antibiotik", [])
    lek2 = Lek("1122460", "Brufen", "Pharmanova", "Analgetik", [])
    lek3 = Lek("1122846", "Paracetanol", "Hemofarm", "Antiseptik", [])
    lekovi= [lek1,lek2,lek3]
    # sacuvaj_lekovi(lekovi)
    #
    # r1 = Recept(p1, "21.05.2021", "stanje bolje", l1, lek1, "12")
    # r2 = Recept(p2, "11.07.2013", "stanje gore", l2, lek2, "4")
    # r3 = Recept(p3, "07.04.2019", "stabilno stanje)",l2,lek3,"2")
    # r4 =  Recept(p1, "21.06.2021", "stanje moze proci", l3, lek3, "12")
    # recepti = [r1, r2,r3,r4]
    # sacuvaj_recepte(recepti)
    # #

main()