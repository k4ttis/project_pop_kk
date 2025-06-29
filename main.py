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

Button(frame_left, text="Formularz: Zakład", command=lambda: pokaz_formularz("zaklad")).grid(row=0, column=0, columnspan=2)
Button(frame_left, text="Formularz: Pracownik", command=lambda: pokaz_formularz("pracownik")).grid(row=1, column=0, columnspan=2)
Button(frame_left, text="Formularz: Klient", command=lambda: pokaz_formularz("klient")).grid(row=2, column=0, columnspan=2)

frame_formularz = Frame(frame_left)
frame_formularz.grid(row=3, column=0, columnspan=2, pady=10)

Button(frame_left, text="Pokaż wszystkie zakłady", command=pokaz_wszystkie_zaklady).grid(row=4, column=0, columnspan=2)
Button(frame_left, text="Pokaż wszystkich pracowników", command=pokaz_wszystkich_pracownikow).grid(row=5, column=0, columnspan=2)

Label(frame_left, text="Nazwa zakładu klientów:").grid(row=6, column=0, columnspan=2)
entry_zaklad_klient = Entry(frame_left)
entry_zaklad_klient.grid(row=7, column=0, columnspan=2)
Button(frame_left, text="Pokaż klientów zakładu", command=pokaz_klientow_zakladu).grid(row=8, column=0, columnspan=2)

Label(frame_left, text="Nazwa zakładu pracowników:").grid(row=9, column=0, columnspan=2)
entry_zaklad_pracownik = Entry(frame_left)
entry_zaklad_pracownik.grid(row=10, column=0, columnspan=2)
Button(frame_left, text="Pokaż pracowników zakładu", command=pokaz_pracownikow_zakladu).grid(row=11, column=0, columnspan=2)

Label(frame_left, text="Usuń/Aktualizuj - wpisz nazwę").grid(row=12, column=0, columnspan=2)
entry_usun = Entry(frame_left)
entry_usun.grid(row=13, column=0, columnspan=2)

Button(frame_left, text="Usuń zakład", command=lambda: usun_obiekt(zaklady_fryzjerskie, listbox_zaklady, entry_usun.get())).grid(row=14, column=0)
Button(frame_left, text="Aktualizuj zakład", command=lambda: aktualizuj_obiekt(zaklady_fryzjerskie, entry_usun.get(), "zaklad")).grid(row=14, column=1)

Button(frame_left, text="Usuń pracownika", command=lambda: usun_obiekt(pracownicy, listbox_pracownicy, entry_usun.get())).grid(row=15, column=0)
Button(frame_left, text="Aktualizuj pracownika", command=lambda: aktualizuj_obiekt(pracownicy, entry_usun.get(), "pracownik")).grid(row=15, column=1)

Button(frame_left, text="Usuń klienta", command=lambda: usun_obiekt(klienci, listbox_klienci, entry_usun.get())).grid(row=16, column=0)
Button(frame_left, text="Aktualizuj klienta", command=lambda: aktualizuj_obiekt(klienci, entry_usun.get(), "klient")).grid(row=16, column=1)

Label(frame_left, text="Zakłady").grid(row=17, column=0)
listbox_zaklady = Listbox(frame_left, height=5)
listbox_zaklady.grid(row=18, column=0, columnspan=2)

Label(frame_left, text="Pracownicy").grid(row=19, column=0)
listbox_pracownicy = Listbox(frame_left, height=5)
listbox_pracownicy.grid(row=20, column=0, columnspan=2)

Label(frame_left, text="Klienci").grid(row=21, column=0)
listbox_klienci = Listbox(frame_left, height=5)
listbox_klienci.grid(row=22, column=0, columnspan=2)

map_widget = tkintermapview.TkinterMapView(root, width=900, height=700, corner_radius=0)
map_widget.grid(row=0, column=1)
map_widget.set_position(52.23, 21.0)
map_widget.set_zoom(6)

root.mainloop()