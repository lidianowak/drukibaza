"""
mapper.py

Mapowanie nazw kolumn formularza importu
na wewnętrzne nazwy używane przez importer BiDO.
"""

REKORD_MAP = {

    "ID importu": "id_importu",

    "Autor(y)": "autorzy",
    "Tytuł skrócony (transkrypcja)": "tytul_skrocony",
    "Tytuł pełny (transliteracja)": "tytul_pelny",

    "Rok wydania": "rok_wydania",
    "Miejsce wydania": "miejsce_wydania",
    "Drukarz": "drukarze",

    "Język": "jezyki",
    "Format": "format",

    "Liczba arkuszy": "liczba_arkuszy",
    "Liczba kart": "liczba_kart",
    "Kolacjonowanie": "kolacjonowanie",

    "Czcionki": "czcionki",
    "Ozdobniki": "ozdobniki",
    "Ryciny": "ryciny",

    "Uwagi (opis fizyczny)": "uwagi_opis_fizyczny",

    "Adresat dedykacji": "adresaci_dedykacji",
    "Powiązane osoby": "powiazane_osoby",
    "Powiązane instytucje": "powiazane_instytucje",
    "Powiązane miejsca": "powiazane_miejsca",

    "Tematy": "tematy",
    "Gatunki": "gatunki",
    "Motywy": "motywy",
    "Wydarzenia": "wydarzenia",

    "Bibliografie": "bibliografie",
    "Literatura przedmiotu": "literatura_przedmiotu",
    "Linki do digitalizacji": "linki_digitalizacji",

    "Warianty": "warianty",
    "Wznowione / wznowienia": "wznowienia",
    "Pozostałe druki powiązane": "pozostale_druki_powiazane",

    "Tagi": "tagi",
    "Status opracowania": "status_opracowania",

    "Uwagi z importu": "uwagi_importu",
    
    "Miniatura karty tytułowej (ścieżka)": "miniatura",
}

def map_record(record):

    mapped = {}

    for excel_name, value in record.items():

        internal_name = REKORD_MAP.get(excel_name)

        if internal_name:
            mapped[internal_name] = value

    return mapped