from datetime import date
from model import *

vadba = Vadba([], [], "tek.json", "pohod.json")
vadba.nalozi_tek()
vadba.nalozi_pohod()

def glavni_meni():
    print('Pozdravljeni v programu VADBENI DNEVNIK')

def pogovor_z_uporabnikom():
    while True:
        moznost = int(input(
            "Kaj želiš: \n 1. DODAJ TEKAŠKO VADBO \n 2. DODAJ POHOD \n 3. PRIKAŽI TEKAŠKE VADBE"
            + " \n 4. PRIKAŽI POHODE \n 5. IZPIS VADB \n 6. IZPIS VADB ZA MESEC"
            + "\n 7. IZHOD \n VPIŠI ŠTEVILKO"))
        if (moznost == 1):
            cas = input("ČAS")
            razdalja = input("RAZDALJA")
            mesec = input("MESEC")
            tek = Tek(cas, razdalja, mesec)
            vadba.nov_tek(tek)
            vadba.zapisi_tek()

        if (moznost == 2):
            cas = input("ČAS")
            visina = input("VIŠINA")
            mesec = input("MESEC")
            pohod = Pohod(cas, visina, mesec)
            vadba.nov_pohod(pohod)
            vadba.zapisi_pohod()
        
        if (moznost == 3):
            x = int(input(
                "Kaj želiš: \n 1. Izpis vseh tekaških vadb \n 2. Izpis tekaških vadb po mesecih"
                + "\n vpiši številko" ))
            if x == 1:
                vadba.izpisi_tek()
            if x == 2:
                mesec = input("Kateri mesec: ")
                vadba.izpisi_tek_meseci(mesec)
        
        if (moznost == 4):
           x = int(input(
                "Kaj želiš: \n 1. Izpis vseh pohodov \n 2. Izpis pohodov po mesecih"
                + "\n vpiši številko" ))
            if x == 1:
                vadba.izpisi_pohod()
            if x == 2:
                mesec = input("Kateri mesec: ")
                vadba.izpisi_pohod_meseci(mesec) 
        
        if (moznost == 5):
             print(vadba.izpis_vadba())

        if (moznost == 6):
            mesec = input("Kateri mesec:" )
            print(vadba.izpis_vadba_mesec(mesec))

        if (moznost == 7):
            break
