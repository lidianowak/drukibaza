"""
builder.py

Buduje obiekty Django
na podstawie sparsowanych danych importera.
"""

from biblioteka.models import (
    Osoba,
    WariantNazwyOsoby,
)

from biblioteka.importer.object_parser import ParsedPerson

def find_person(person: ParsedPerson):
    """
    Szuka osoby w bazie.
    Zwraca QuerySet.
    """

    if person.nazwa:
        return Osoba.objects.filter(
            imiona=person.nazwa,
            nazwisko="",
        )

    return Osoba.objects.filter(
        nazwisko=person.nazwisko,
        imiona=person.imiona,
    )

def add_person_variants(osoba: Osoba, person: ParsedPerson):
    """
    Dodaje brakujące warianty nazw osoby.
    """

    istniejące = {
        wariant.nazwa
        for wariant in osoba.warianty_nazw.all()
    }

    kolejnosc = osoba.warianty_nazw.count() + 1

    warianty = []

    for nazwisko in [person.nazwisko, *person.warianty_nazwiska]:
        if nazwisko is None:
            continue

        for imiona in [person.imiona, *person.warianty_imion]:
            if imiona is None:
                continue

            warianty.append(f"{nazwisko}, {imiona}")

    if person.nazwa:
        warianty.append(person.nazwa)

    for nazwa in warianty:

        if nazwa in istniejące:
            continue

        WariantNazwyOsoby.objects.create(
            osoba=osoba,
            nazwa=nazwa,
            kolejnosc=kolejnosc,
        )

        kolejnosc += 1


def create_person(person: ParsedPerson):
    """
    Tworzy nowy obiekt Osoba.
    """

    if person.nazwa:
        osoba = Osoba.objects.create(
            imiona=person.nazwa,
            nazwisko="",
            kwalifikator=person.kwalifikator or "",
        )
    else:
        osoba = Osoba.objects.create(
            imiona=person.imiona,
            nazwisko=person.nazwisko,
            kwalifikator=person.kwalifikator or "",
        )

    add_person_variants(osoba, person)

    return osoba

def get_or_create_person(person: ParsedPerson):
    """
    Zwraca istniejącą osobę lub tworzy nową.
    """

    matches = find_person(person)

    if matches.count() == 1:
        osoba = matches.first()

        add_person_variants(osoba, person)

        return osoba

    if matches.count() > 1:
        raise ValueError(
            f"Znaleziono więcej niż jedną osobę: {person}"
        )

    return create_person(person)

    return Osoba.objects.create(
        imiona=person.imiona,
        nazwisko=person.nazwisko,
        kwalifikator=person.kwalifikator or "",
    )