"""
attachment_builder.py

Tworzenie załączników.
"""

from pathlib import Path

from django.core.files import File

from biblioteka.models import (
    Zalacznik,
    Egzemplarz,
)

def find_specimen(
    rekord,
    sygnatura,
):
    """
    Zwraca egzemplarz o podanej sygnaturze.
    """

    if not sygnatura:
        return None

    return Egzemplarz.objects.get(
        rekord=rekord,
        sygnatura=sygnatura,
    )


def create_attachment(
    rekord,
    mapped,
):
    """
    Tworzy jeden załącznik.
    """

    print("SEKCJA:", repr(mapped["sekcja"]))
    print("SYGNATURA:", repr(mapped.get("sygnatura")))

    path = Path(mapped["sciezka"])

    if not path.exists():
        print(f"Brak pliku: {path}")
        return

    egzemplarz = None

    if mapped["sekcja"] == "marginalia":
        egzemplarz = find_specimen(
            rekord,
            mapped.get("sygnatura"),
        )

        print("EGZEMPLARZ:", egzemplarz)

    with path.open("rb") as f:

        zalacznik = Zalacznik(
            rekord=rekord if egzemplarz is None else None,
            egzemplarz=egzemplarz,
            sekcja=mapped["sekcja"],
            nazwa_wyswietlana=mapped.get("nazwa") or "",
            opis=mapped.get("opis") or "",
            kolejnosc=mapped.get("kolejnosc") or 1,
        )

        zalacznik.plik.save(
            path.name,
            File(f),
            save=False,
        )

        zalacznik.save()

        print("ZAPISANO:", zalacznik.id)