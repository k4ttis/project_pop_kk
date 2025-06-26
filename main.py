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

def pokaz_formularz(typ, obiekt=None):
    for widget in frame_formularz.winfo_children():
        widget.destroy()

    Label(frame_formularz, text="Nazwa").grid(row=0, column=0)
    global entry_name
    entry_name = Entry(frame_formularz)
    entry_name.grid(row=0, column=1)

    Label(frame_formularz, text="Miejscowość").grid(row=1, column=0)
    global entry_location
    entry_location = Entry(frame_formularz)
    entry_location.grid(row=1, column=1)

    global entry_extra
    entry_extra = None

    if typ != "zaklad":
        Label(frame_formularz, text="Zakład").grid(row=2, column=0)
        entry_extra = Entry(frame_formularz)
        entry_extra.grid(row=2, column=1)

    if obiekt:
        entry_name.insert(0, obiekt.nazwa)
        entry_location.insert(0, obiekt.miejscowosc)
        if entry_extra:
            entry_extra.insert(0, obiekt.zaklad)

        def update():
            obiekt.nazwa = entry_name.get()
            obiekt.miejscowosc = entry_location.get()
            if hasattr(obiekt, 'zaklad'):
                obiekt.zaklad = entry_extra.get()
            obiekt.coordinates = obiekt.get_coordinates()

            # Odswież listbox
            if typ == "zaklad":
                odswiez_listbox(listbox_zaklady, zaklady_fryzjerskie)
            elif typ == "pracownik":
                odswiez_listbox(listbox_pracownicy, pracownicy)
            elif typ == "klient":
                odswiez_listbox(listbox_klienci, klienci)

            clear_entries()
            pokaz_formularz(typ)

        Button(frame_formularz, text="Zapisz zmiany", command=update).grid(row=3, column=0, columnspan=2)
    else:
        if typ == "zaklad":
            Button(frame_formularz, text="Dodaj zakład", command=dodaj_zaklad).grid(row=3, column=0, columnspan=2)
        elif typ == "pracownik":
            Button(frame_formularz, text="Dodaj pracownika", command=dodaj_pracownika).grid(row=3, column=0, columnspan=2)
        elif typ == "klient":
            Button(frame_formularz, text="Dodaj klienta", command=dodaj_klienta).grid(row=3, column=0, columnspan=2)

def usun_wszystkie_markery():
    global wszystkie_markery
    for marker in wszystkie_markery:
        marker.delete()
    wszystkie_markery = []

def pokaz_wszystkie_zaklady():
    usun_wszystkie_markery()
    map_widget.set_zoom(6)
    for z in zaklady_fryzjerskie:
        z.marker = map_widget.set_marker(z.coordinates[0], z.coordinates[1], text=z.nazwa)
        wszystkie_markery.append(z.marker)

def pokaz_wszystkich_pracownikow():
    usun_wszystkie_markery()
    map_widget.set_zoom(6)
    for p in pracownicy:
        p.marker = map_widget.set_marker(p.coordinates[0], p.coordinates[1], text=f"{p.nazwa} - {p.zaklad}")
        wszystkie_markery.append(p.marker)

def pokaz_klientow_zakladu():
    usun_wszystkie_markery()
    nazwa_zakladu = entry_zaklad_klient.get()
    if nazwa_zakladu:
        for k in klienci:
            if k.zaklad == nazwa_zakladu:
                k.marker = map_widget.set_marker(k.coordinates[0], k.coordinates[1], text=f"{k.nazwa} - {k.zaklad}")
                wszystkie_markery.append(k.marker)

def pokaz_pracownikow_zakladu():
    usun_wszystkie_markery()
    nazwa_zakladu = entry_zaklad_pracownik.get()
    if nazwa_zakladu:
        for p in pracownicy:
            if p.zaklad == nazwa_zakladu:
                p.marker = map_widget.set_marker(p.coordinates[0], p.coordinates[1], text=f"{p.nazwa} - {p.zaklad}")
                wszystkie_markery.append(p.marker)

# === GUI ===

root = Tk()
root.geometry("1200x800")
root.title("Mapa Zakładów Fryzjerskich")

frame_left = Frame(root)
frame_left.grid(row=0, column=0, sticky=N)

