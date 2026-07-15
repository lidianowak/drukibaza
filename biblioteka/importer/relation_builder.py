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

def create_relation(
    rekord,
    value,
    typ,
    rekordy,
):
    """
    Tworzy pojedynczą relację rekordu.

    Obsługuje:
    - R000001
    - 000123
    - {opis bibliograficzny}
    """

    value = value.strip()

    if value.startswith("{") and value.endswith("}"):

        RelacjaRekordu.objects.create(
            rekord=rekord,
            typ=typ,
            opis=value[1:-1].strip(),
        )

        return

    rekord_powiazany = find_record(
        value,
        rekordy,
    )

    RelacjaRekordu.objects.create(
        rekord=rekord,
        rekord_powiazany=rekord_powiazany,
        typ=typ,
    )

    RelacjaRekordu.objects.get_or_create(
        rekord=rekord_powiazany,
        rekord_powiazany=rekord,
        typ=typ,
    )


def find_record(value, rekordy):
    """
    Wyszukuje rekord.

    Obsługuje:
    - R000001 (rekord z importu)
    - 000123 (rekord istniejący)
    """

    print("SZUKAM:", repr(value), type(value))

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

        create_relation(
            rekord,
            value,
            "wariant",
            rekordy,
        )

    for value in split_values(mapped.get("wznowienia")):

        create_relation(
            rekord,
            value,
            "wznowienie",
            rekordy,
        )