"""
parser.py

Zamienia tekst z arkusza Excel
na obiekty zgodne z modelem BiDO.
"""
HEADER_ROW = 14
EXAMPLE_ROW = 15
DATA_START_ROW = 16

def parse_sheet(worksheet):
    """
    Odczytuje jeden arkusz formularza importu
    i zwraca listę słowników.

    Nie interpretuje danych.
    """

    headers = [cell.value for cell in worksheet[HEADER_ROW]]

    records = []

    for row in worksheet.iter_rows(
        min_row=DATA_START_ROW,
        values_only=True,
    ):

        record = dict(zip(headers, row))

        # pomijamy niewypełnione wiersze formularza
        if not record["Tytuł skrócony (transkrypcja)"]:
            continue

        records.append(record)


    return records

def parse_person(text):
    """
    Parsuje zapis osoby.

    Przykład:

    Kochanowski [Cochanovius], Jan [Ioannes] (starszy)
    """
    raise NotImplementedError


def parse_place(text):
    raise NotImplementedError


def parse_institution(text):
    raise NotImplementedError


def parse_library(text):
    raise NotImplementedError

print("PARSER ZAŁADOWANY")