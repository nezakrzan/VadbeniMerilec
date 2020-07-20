import bottle 
from bottle import route, run, static_file, template

import os
import random
import hashlib
from datetime import datetime
from model import *


# Tukaj noter bodo shranjeni sessioni (torej kdo je uspesno prijavljen na strani)
# Podatki so shranjeni kot {sessionID: razred Uporabniki}
sessioni = {}

# Skrivnost za kriptiranje podatkov v piskotih
skrivnost = 'NEVIDNO'

def poisci_tek(ime_polja):
    ime_tek = bottle.request.forms.getunicode(ime_polja)
    vadba = vadba_uporabnika()
    return vadba.poisci_tek(ime_tek)

def poisci_pohod(ime_polja):
    ime_pohod = bottle.request.forms.getunicode(ime_polja)
    vadba = vadba_uporabnika()
    return vadba.poisci_pohod(ime_pohod)


def vadba_uporabnika():
    return trenutni_uporabnik().vadba_uporabnika

def shrani_trenutnega_uporabnika():
    uporabnik = trenutni_uporabnik()
    uporabnik.shrani_vadbe(os.path.join('uporabnik', f'{uporabnik.uporabnisko_ime}.json' ))

def trenutni_uporabnik():
    sessionID = bottle.request.get_cookie('sessionID', secret=skrivnost)
    return sessioni.get(sessionID)

# Preveri, ce ima uporabnik shranjen sessionID ali ne
def preveri_avtorizacijo():
    # Ko je uporabnik prijavljen, je v programu shranjen njegov session
    # ter njegovi podatki. Ce tega ni, uporabnik ni prijavljen in nima
    # avtorizacije.
    uporabnik = trenutni_uporabnik()
    return uporabnik is not None

# Pomozna funkcija, ki pomaga pri prijavi/registraciji uporabnika
# tako, da shrani piskotke in nalozi/ustvari datoteko uporabnika
def ustvari_sejo(sessionID, ime):
    bottle.response.set_cookie('sessionID', sessionID, secret=skrivnost)

    uporabnik = Uporabnik.nalozi(ime)
    sessioni[sessionID]= uporabnik



# ==============
#     GET
# ==============
@bottle.route('/')
def osnovna_stran(): 
    if not preveri_avtorizacijo():
        bottle.redirect('/prijava')
    
    return bottle.template("views/osnova.html")

@bottle.route('/prijava')
def prijava_get():
    return bottle.template('views/prijava.html' )

@bottle.route('/vadba')
def nacrtovanje_vadbe():
    if not preveri_avtorizacijo():
        bottle.redirect('/prijava')

    vadba = vadba_uporabnika()
    return bottle.template('views/vadba.html', vadba=vadba)

@bottle.route('/nov_tek')
def nov_tek():
    if not preveri_avtorizacijo():
        bottle.redirect('/prijava')

    return bottle.template('vnos_teka.html')

@bottle.route('/nov_pohod')
def nov_pohod():
    if not preveri_avtorizacijo():
        bottle.redirect('/prijava')

    return bottle.template('vnos_pohoda.html')

# ==============
#     POST
# ==============
@bottle.post('/prijava')
def prijava_post():
    ime = bottle.request.forms.get('uporabnisko_ime')
    geslo = bottle.request.forms.get('geslo')

    # Zahasha geslo
    h = hashlib.blake2b()
    h.update(geslo.encode(encoding = 'utf-8'))
    skrito_geslo = h.hexdigest()

    # Ustvari sessionID - torej random hash glede 
    # na trenutni cas (da je res skoz random)
    cas = str(datetime.now())
    h.update(cas.encode(encoding = 'utf-8')) 
    sessionID = h.hexdigest()

    # Preveri ce je prijava ali registracija
    if bottle.request.forms.get('nov_racun') is not None and not Uporabnik.obstaja(ime): # Registracija
        uporabnik = Uporabnik(
            ime,
            skrito_geslo,
            Vadba()
        )

        uporabnik.shrani()
        ustvari_sejo(sessionID, ime)
    else: # Prijava
        # Preveri ce uporabnik sploh obstaja
        if Uporabnik.obstaja(ime): 
            uporabnik = Uporabnik.nalozi(ime)

            # Preveri geslo
            if uporabnik.preveri_geslo(skrito_geslo): 
                ustvari_sejo(sessionID, ime)


    bottle.redirect('/')

@bottle.post('/odjava')
def odjava():
    # Uporabnik je ze odavljen
    if not preveri_avtorizacijo():
        bottle.redirect('/prijava')

    sessionID = bottle.request.get_cookie('sessionID', secret=skrivnost)

    # Shrani vse ustvarjene podatke o odjavljenem uporabniku
    uporabnik = sessioni.pop(sessionID)
    uporabnik.shrani()

    bottle.response.delete_cookie('sessionID', path='/')


    bottle.redirect('/')

@bottle.post('/nov_tek')
def nov_tek_post():
    if not preveri_avtorizacijo():
        bottle.redirect('/prijava')

    ime = bottle.request.forms.get('ime')
    cas = bottle.request.forms.get('cas')
    razdalja = bottle.request.forms.get('razdalja')
    mesec = bottle.request.forms.get('mesec')

    tek = Tek(ime, cas, razdalja, mesec)

    # Shrani novo ustvarjeni tek v vadbo trenutnega uporabnika.
    # Potem pa posodobi informacije uporabnika v datoteko
    uporabnik = trenutni_uporabnik()
    uporabnik.vadba.nov_tek(tek)
    uporabnik.shrani()

    bottle.redirect('/')


@bottle.post('/nov_pohod')
def nov_pohod_post():
    if not preveri_avtorizacijo():
        bottle.redirect('/prijava')

    ime = bottle.request.forms.get('ime')
    cas = bottle.request.forms.get('cas')
    visina = bottle.request.forms.get('visina')
    mesec = bottle.request.forms.get('mesec')

    pohod = Pohod(ime, cas, visina, mesec)

    # Shrani novo ustvarjeni pohod v vadbo trenutnega uporabnika.
    # Potem pa posodobi informacije uporabnika v datoteko
    uporabnik = trenutni_uporabnik()
    uporabnik.vadba.nov_pohod(pohod)
    uporabnik.shrani()

    bottle.redirect('/')  

@bottle.post('/izpisi_tek/') 
def izpisi_tek():
    return bottle.template('izpisi_tek.html')

@bottle.post('/izpisi_tek/vsi_tek')
def izpisi_tek_vse():
    return vadba.izpisi_tek()

@bottle.post('/izpisi_tek/izpisi_tek_mesec')
def za_mesec1():
    mesec = bottle.request.forms.get('mesec')
    return vadba.izpisi_tek_meseci(mesec)

@bottle.post('/izpisi_pohod/') 
def izpisi_pohod():
    return bottle.template('izpisi_pohod.html')

@bottle.post('/izpisi_pohod/vsi_tek')
def izpisi_pohod_vse():
    return vadba.izpisi_pohod()

@bottle.post('/izpisi_pohod/izpisi_tek_mesec')
def za_mesec1():
    mesec = bottle.request.forms.get('mesec')
    return vadba.izpisi_pohod_meseci(mesec)

@bottle.post('/izpis_vadba')
def vadba():
    return bottle.template('izpis_vadba.html')

@bottle.post('/izpis_vadba/celotna_vadba')
def celotno():
    return str(vadba.izpis_vadba())

@bottle.post('/izpis_vadba/izpis_vadba_mesec')
def vadba_mesec():
    mesec = bottle.request.forms.get('mesec')
    return str(vadba.izpis_vadba_mesec(mesec)) 

# Server se zažene če je ta datoteka zagnana kot program
if __name__ == '__main__':
    bottle.run(debug=True, reloader=True)  