"""
relation_builder.py

Tworzenie relacji między rekordami.
"""

from biblioteka.models import (
    Rekord,
    RelacjaRekordu,
)


def split_values(text):
    """
    Zamienia tekst na listę wartości.
    """

    if not text:
        return []

    return [
        value.strip()
        for value in text.split(";")
        if value.strip()
    ]


def find_record(value, rekordy):
    """
    Wyszukuje rekord.

    Obsługuje:
    - R000001 (rekord z importu)
    - 000123 (rekord istniejący)
    """

    if value.startswith("R"):
        return rekordy.get(value)

    return Rekord.objects.get(
        identyfikator=value,
    )


def create_relations(
    rekord,
    mapped,
    rekordy,
):
    """
    Tworzy relacje rekordu.
    """

    for value in split_values(mapped.get("warianty")):

        rekord_powiazany = find_record(
            value,
            rekordy,
        )

        RelacjaRekordu.objects.create(
            rekord=rekord,
            rekord_powiazany=rekord_powiazany,
            typ="wariant",
        )

    for value in split_values(mapped.get("wznowienia")):

        rekord_powiazany = find_record(
            value,
            rekordy,
        )

        RelacjaRekordu.objects.create(
            rekord=rekord,
            rekord_powiazany=rekord_powiazany,
            typ="wznowienie",
        )