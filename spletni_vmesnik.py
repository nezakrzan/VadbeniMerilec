import bottle 
from bottle import route, run, static_file, template

import os
from os import path
import random
import hashlib
from datetime import datetime
from model import *

vadba = Vadba( [], [], "tek.json", "pohod.json")
vadba.nalozi_tek()
vadba.nalozi_pohod()

sessioni = {}

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

def preveri_avtorizacijo():
    uporabnik = trenutni_uporabnik()
    return uporabnik is not None

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

    h = hashlib.blake2b()
    h.update(geslo.encode(encoding = 'utf-8'))
    skrito_geslo = h.hexdigest()

    cas = str(datetime.now())
    h.update(cas.encode(encoding = 'utf-8')) 
    sessionID = h.hexdigest()

    if bottle.request.forms.get('nov_racun') is not None and not Uporabnik.obstaja(ime): 
        uporabnik = Uporabnik(
            ime,
            skrito_geslo,
            Vadba()
        )

        uporabnik.shrani()
        ustvari_sejo(sessionID, ime)
    else: 
        if Uporabnik.obstaja(ime): 
            uporabnik = Uporabnik.nalozi(ime)

            if uporabnik.preveri_geslo(skrito_geslo): 
                ustvari_sejo(sessionID, ime)

    bottle.redirect('/')

@bottle.post('/odjava')
def odjava():
    if not preveri_avtorizacijo():
        bottle.redirect('/prijava')

    sessionID = bottle.request.get_cookie('sessionID', secret=skrivnost)

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

    uporabnik = trenutni_uporabnik()
    uporabnik.vadba.nov_pohod(pohod)
    uporabnik.shrani()

    bottle.redirect('/')  

@bottle.get('/izpisi_tek') 
def izpisi_tek():
    return bottle.template('izpisi_tek.html')

@bottle.post('/izpisi_tek/vsi_tek')
def izpisi_tek_vse():
    return vadba.izpisi_tek()

@bottle.get('/izpisi_pohod') 
def izpisi_pohod():
    return bottle.template('izpisi_pohode.html')

@bottle.post('/izpisi_pohod/vsi_pohodi')
def izpisi_pohod_vse():
    return vadba.izpisi_pohod()

@bottle.get('/izpis_vadbe')
def izpisi_vadba():
    return bottle.template('izpis_vadb.html')

@bottle.post('/izpis_vadbe/celotna_vadba')
def celotno():
    return str(vadba.izpis_vadba())


if __name__ == '__main__':
    bottle.run(debug=True, reloader=True)  