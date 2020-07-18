import bottle 
import os
import random
import hashlib
from model import *

vadba = Vadba([], [], "tek.json", "pohod.json")
vadba.nalozi_tek()
vadba.nalozi_pohod()

uporabnik = {}
skrivnost = 'NEVIDNO'

for ime_datoteke in os.listdir('uporabnik' ):
    uporabnik = Uporabnik.nalozi_vadbe(os.path.join('uporabnik', ime_datoteke))
    uporabnik[uporabnik.uporabnisko_ime] = uporabnik

def poisci_tek(ime_polja):
    ime_tek = bottle.request.forms.getunicode(ime_polja)
    vadba = vadba_uporabnika()
    return vadba.poisci_tek(ime_tek)

def poisci_pohod(ime_polja):
    ime_pohod = bottle.request.forms.getunicode(ime_polja)
    vadba = vadba_uporabnika()
    return vadba.poisci_pohod(ime_pohod)

def trenutni_uporabnik():
    uporabnisko_ime = bottle.request.get_cookie('uporabnisko_ime', secret=skrivnost)
    if uporabnisko_ime is None:
        bottle.redirect('/prijava/' )
    return uporabniki[uporabnisko_ime]

def vadba_uporabnika():
    return trenutni_uporabnik().vadba_uporabnika

def shrani_trenutnega_uporabnika():
    uporabnik = trenutni_uporabnik()
    uporabnik.shrani_vadbe(os.path.join('uporabnik', f'{uporabnik.uporabnisko_ime}.json' ))

@bottle.get("/")
def zacetna_stran():
    bottle.redirect('/vadba/')

@bottle.get('vadba')
def nacrtovanje_vadbe():
    vadba = vadba_uporabnika()
    return bottle.template('vadba.html', vadba=vadba)

@bottle.get('/prijava/' )
def prijava_get():
    return bottle.template('prijava.html' )

@bottle.post('/prijava/')
def prijava_post():
    uporabnisko_ime = bottle.request.forms.getunicode('uporabnisko_ime' )
    geslo = bottle.request.forms.getunicode('geslo')
    h = hashlib.blake2b()
    h.update(geslo.encode(encoding = 'utf-8'))
    skrito_geslo = h.hexdigest()
    if 'nov_racun' in bottle.request.forms and uporabnisko_ime not in uporabnik:
        uporabnik = Uporabnik(
            uporabnisko_ime,
            skrito_geslo,
            Vadba()
        )
        uporabniki[uporabnisko_ime] = uporabnik
    else:
        uporabnik = uporabniki[uporabnisko_ime]
        uporabnik.preveri_geslo(skrito_geslo)
    bpttle.response.set_copkie('uporabnisko_ime', uporabnik.uporabnisko_ime, path='/', secret=skrivnost)
    bottle.redirect('/')

@bottle.post('/odjava/')
def odjava():
    bottle.response.delete_cookie('uporabnisko_ime', path='/')
    bottle.redirect('/')

@bottle.get('/')
def osnovna_stran():
    return bottle.template('osnovna.html')

@bottle.post('/nov_tek')
def nov_tek():
    return bottle.template('vnost_teka.html')

@bottle.post('/nov_tek/nov')
def pomozna1():
    ime = bottle.request.forms.get('ime')
    cas = bottle.request.forms.get('cas')
    razdalja = bottle.request.forms.get('razdalja')
    mesec = bottle.request.forms.get('mesec')
    tek = Tek(ime, cas, razdalja, mesec)
    vadba.nov_tek(tek)
    vadba.zapisi_tek()
    bottle.redirect('/')

 @bottle.post('/nov_pohod')
def nov_pohod():
    return bottle.template('vnost_pohoda.html')

@bottle.post('/nov_pohod/nov')
def pomozna1():
    ime = bottle.request.forms.get('ime')
    cas = bottle.request.forms.get('cas')
    visina = bottle.request.forms.get('visina')
    mesec = bottle.request.forms.get('mesec')
    pohod = Pohod(ime, cas, visina, mesec)
    vadba.nov_pohod(pohod)
    vadba.zapisi_pohod()
    bottle.redirect('/')  

@bottle.post('/izpisi_tek/') 
def izpisi_tek():
    return bottle.template('izpisi_tek.html')

@bottle.post('/izpisi_tek/vsi_tek')
def izpisi_tek():
    return vadba.izpisi_tek()

@bottle.post('/izpisi_tek/izpisi_tek_mesec')
def za_mesec1():
    mesec = bottle.request.forms.get('mesec')
    return vadba.izpisi_tek_meseci(mesec)

@bottle.post('/izpisi_pohod/') 
def izpisi_pohod():
    return bottle.template('izpisi_pohod.html')

@bottle.post('/izpisi_pohod/vsi_tek')
def izpisi_pohod():
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

bottle.run(debug=True, reloader=True)  