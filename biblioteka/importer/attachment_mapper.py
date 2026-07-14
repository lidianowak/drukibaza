"""
attachment_mapper.py

Mapowanie kolumn arkusza Załączniki.
"""

ATTACHMENT_MAP = {
    "ID importu": "id_importu",
    "Sekcja": "sekcja",
    "Nazwa": "nazwa",
    "Opis": "opis",
    "Ścieżka pliku": "sciezka",
    "Kolejność": "kolejnosc",
    "Sygnatura egzemplarza": "sygnatura",
}


def map_attachment(record):

    mapped = {}

    for excel_name, value in record.items():

        internal_name = ATTACHMENT_MAP.get(excel_name)

        if internal_name:
            mapped[internal_name] = value

    return mapped