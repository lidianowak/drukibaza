"""
specimen_mapper.py

Mapowanie arkusza Egzemplarze.
"""

SPECIMEN_MAP = {

    "ID importu": "id_importu",

    "Biblioteka": "biblioteka",
    "Sygnatura": "sygnatura",
    "Link do katalogu": "katalog_biblioteczny",

    "Proweniencja": "proweniencja",
    "Oprawa": "oprawa",
    "Marginalia": "marginalia",
}


def map_specimen(record):

    mapped = {}

    for excel_name, value in record.items():

        if excel_name == "_excel_row":
            mapped["_excel_row"] = value
            continue

        internal_name = SPECIMEN_MAP.get(excel_name)

        if internal_name:
            mapped[internal_name] = value

    return mapped