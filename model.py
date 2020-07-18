import json


meseci = ["januar", "februar", "marec", "april", "maj", "junij",
          "julij", "avgust", "september", "oktober", "november", "december"]


class Uporabnik:

    def __init__(self, uporabnisko_ime, skrito_geslo, vadba):
        self.uporabnisko_ime = uporabnisko_ime
        self.skrito_geslo = skrito_geslo
        self.vadba = vadba

    def preveri_geslo(self, skrito_geslo):
        if self.geslo != geslo:
            raise ValueError('Napačno geslo!' )

    def shrani_stanje(self, ime_datoteke):
        slovar_vadb = {
            'uporabnisko_ime': self.uporabnisko_ime,
            'geslo': self.skrito_geslo,
            'vadba': self.vadba.slovar_z_vadbami(),
        }
        with open(ime_datoteke, 'w') as datoteka:
            json.dump(slovar_vadb, datoteka, ensure_ascii=False, indent=4)
    
    @classmethod
    def nalozi_vadbe(cls, ime_datoteke):
        with open(ime_datoteke) as datoteka:
            slovar_vadb = json.load(datoteka)
        uporabnisko_ime = slovar_vadb['uporabnisko_ime' ]
        geslo = slovar_vadb['geslo' ]
        vadba = Vadba.nalozi_iz_vadb(slovar_vadb['vadba' ])
        return cls(uporabnisko_ime, geslo, vadba)


class Tek:

    def __init__(self,ime, cas, razdalja, mesec):
        self.ime = ime
        self.cas = cas
        self.razdalja = razdalja
        self.mesec = mesec

    def __str__(self):
        return "{}: {}, {}".format(self.ime, self.cas, self.razdalja, self.mesec)
    
    def __lt__(self, other):
        return (meseci.index(self.mesec) < meseci.index(other.mesec))



class Pohod:

    def __init__(self, ime, cas, visina, mesec):
        self.ime = ime
        self.cas = cas
        self.visina = visina
        self.mesec = mesec

    def __str__(self):
        return "{}: {}, {}".format(self.ime, self.cas, self.visina, self.mesec)
    
    def __lt__(self, other):
        return (meseci.index(self.mesec) < meseci.index(other.mesec))



class Vadba:

    def _init__(self, seznam_tek, seznam_pohodi, datoteka_tek, datoteka_pohod):
        self.seznam_tek = seznam_tek
        self.seznam_pohodi = seznam_pohodi
        self.datoteka_tek = datoteka_tek
        self.datoteka_pohod = datoteka_pohod
        self.tek_po_imenih = {}
        self.pohod_po_imenih = {}
    
    def nov_tek(self, tek):
        if tek in self.tek_po_imenih:
            raise ValueError('Tekaška vadba s tem imenom že obstaja!')
        nov = Tek(tek, self)
        self.seznam_tek.append(nov)
        self.tek_po_imenih[tek] = nov
        return nov
    
    def izpisi_tek(self):
        prikaz = ""
        self.seznam_tek.sort()
        for tek in self.seznam_tek:
            prikaz += ("<br>" + str(tek) + "</br>")
        return prikaz

    def izpisi_tek_meseci(self, mesec):
        prikaz = ""
        for tek in self.seznam_tek:
            if tek.mesec == mesec:
                prikaz += ("<br>" + str(tek) + "</br>")
        return prikaz
    
    def nov_pohod(self, pohod):
        if pohod in self.pohod_po_imenih:
            raise ValueError('Pohod s tem imenom že obstaja!')
        nov = Pohod(pohod, self)
        self.seznam_pohodi.append(nov)
        self.pohod_po_imenih[pohod] = nov
        return nov
    
    def izpisi_pohod(self):
        prikaz = ""
        self.seznam_pohodi.sort()
        for pohod in self.seznam_pohodi:
            prikaz += ("<br>" + str(pohod) + "</br>")
        return prikaz

    def izpisi_pohod_meseci(self, mesec):
        prikaz = ""
        for pohod in self.seznam_pohodi:
            if pohod.mesec == mesec:
                prikaz += ("<br>" + str(pohod) + "</br>")
        return prikaz

    def zapisi_tek(self):
        with open(self.datoteka_tek, "w") as f:
            vsi_tek = []
            for tek in self.seznam_tek:
                tek_dic = {"ime": tek.ime "čas": tek.cas, "razdalja": tek.razdalja, "mesec": tek.mesec}
                vsi_tek.append(tek_dic)
            json.dump(vsi_tek, f)
    
    def nalozi_tek(self):
        with open(self.datoteka_tek, "r") as f:
            tek_dat = json.load(f)
            for tek_dic in tek_dat:
                self.seznam_tek.append(Tek(tek_dic["ime"], tek_dic["čas"], tek_dic["razdalja"], tek_dic["mesec"]))
    
    def zapisi_pohod(self):
        with open(self.datoteka_pohod, "w") as f:
            vsi_pohod = []
            for pohod in self.seznam_pohodi:
                pohod_dic = {"ime": pohod.ime, "čas": pohod.cas, "vrh": pohod.visina, "mesec": pohod.mesec}
                vsi_pohod.append(pohod_dic)
            json.dump(vsi_pohod, f)
    
    def nalozi_pohod(self):
        with open(self.datoteka_pohod, "r") as f:
            pohod_dat = json.load(f)
            for pohod_dic in pohod_dat:
                self.seznam_pohodi.append(Pohod(pohod_dic["ime"], pohod_dic["čas"], pohod_dic["višina"], pohod_dic["mesec"]))
    
    def izpis_vadba(self):
        teki = 0
        pohodi = 0
        for tek in self.seznam_tek:
            teki += int(tek.ime)
        for pohod in self.seznam_pohodi:
            pohodi += int(pohod.ime)
        return teki + pohodi

     def izpis_vadba_mesec(self, mesec):
        teki = 0
        pohodi = 0
        for tek in self.seznam_tek:
            if tek.mesec == mesec:
                teki += int(tek.ime)
        for pohod in self.seznam_pohodi:
            if pohod.mesec == mesec:
                pohodi += int(pohod.ime)
        return teki + pohodi

    def slovar_z_vadbami(self):
        return {
            'tek': [{
                'ime': tek.ime,
                'datum': str(tek.datum)
            } for tek in self.tek],
            'pohod': [{
                'ime': pohod.ime,
                'datum': str(pohod.datum)
            } for pohod in self.pohod],
        }
    
    @classmethod
    def nalozi_iz_vadb(cls, slovar_z_vadbami):
        vadbe = cls()
        for tek in slovar_z_vadbami['tek' ]:
            nov_tek = vadba.nov_tek(tek['ime' ])
        for pohod in slovar_z_vadbami['pohod' ]:
            nov_pohod = vadba.nov_pohod(pohod['ime' ])
        return vadba 

    def shrani_vadbe(self, ime_datoteke):
        with open(ime_datoteke):
            json.dump(self.slovar_z_vadbami(), datoteka, ensure_ascii=False, indent=4)
    
    @classmethod
    def nalozi_vadbe(cls, ime-datoteke):
        with open(ime_datoteke) as datoteka:
            slovar_z_vadbami = json.load(datoteka)
        return cls.nalozi_iz_vadb(slovar_z_vadbami)