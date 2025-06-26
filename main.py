from tkinter import *
import tkintermapview
import requests
from bs4 import BeautifulSoup

zaklady_fryzjerskie = []
pracownicy = []
klienci = []
wszystkie_markery = []

class ObiektMapy:
    def __init__(self, nazwa, miejscowosc):
        self.nazwa = nazwa
        self.miejscowosc = miejscowosc
        self.coordinates = self.get_coordinates()
        self.marker = None

    def get_coordinates(self):
        url = f"https://pl.wikipedia.org/wiki/{self.miejscowosc}"
        try:
            response = requests.get(url).text
            soup = BeautifulSoup(response, "html.parser")
            longitude = float(soup.select(".longitude")[1].text.replace(",", "."))
            latitude = float(soup.select(".latitude")[1].text.replace(",", "."))
            return [latitude, longitude]
        except:
            return [52.23, 21.0]  # domyślnie Warszawa

class ZakladFryzjerski(ObiektMapy):
    pass

class Pracownik(ObiektMapy):
    def __init__(self, nazwa, miejscowosc, zaklad):
        self.zaklad = zaklad
        super().__init__(nazwa, miejscowosc)

class Klient(ObiektMapy):
    def __init__(self, nazwa, miejscowosc, zaklad):
        self.zaklad = zaklad
        super().__init__(nazwa, miejscowosc)

def clear_entries():
    entry_name.delete(0, END)
    entry_location.delete(0, END)
    if entry_extra:
        entry_extra.delete(0, END)

def dodaj_zaklad():
    nazwa = entry_name.get()
    miejscowosc = entry_location.get()
    if nazwa and miejscowosc:
        zaklad = ZakladFryzjerski(nazwa, miejscowosc)
        zaklady_fryzjerskie.append(zaklad)
        odswiez_listbox(listbox_zaklady, zaklady_fryzjerskie)
    clear_entries()

def dodaj_pracownika():
    nazwa = entry_name.get()
    miejscowosc = entry_location.get()
    zaklad = entry_extra.get()
    if nazwa and miejscowosc and zaklad:
        pracownik = Pracownik(nazwa, miejscowosc, zaklad)
        pracownicy.append(pracownik)
        odswiez_listbox(listbox_pracownicy, pracownicy)
    clear_entries()

def dodaj_klienta():
    nazwa = entry_name.get()
    miejscowosc = entry_location.get()
    zaklad = entry_extra.get()
    if nazwa and miejscowosc and zaklad:
        klient = Klient(nazwa, miejscowosc, zaklad)
        klienci.append(klient)
        odswiez_listbox(listbox_klienci, klienci)
    clear_entries()

def odswiez_listbox(listbox, lista):
    listbox.delete(0, END)
    for o in lista:
        text = f"{o.nazwa} - {o.zaklad}" if hasattr(o, 'zaklad') else o.nazwa
        listbox.insert(END, text)

def usun_obiekt(lista, listbox, nazwa):
    index_to_remove = -1
    for i, obj in enumerate(lista):
        if obj.nazwa == nazwa:
            index_to_remove = i
            break
    if index_to_remove != -1:
        del lista[index_to_remove]
        odswiez_listbox(listbox, lista)
    entry_usun.delete(0, END)

def aktualizuj_obiekt(lista, nazwa, typ):
    for obj in lista:
        if obj.nazwa == nazwa:
            pokaz_formularz(typ, obj)
            break

