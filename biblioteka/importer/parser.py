"""
parser.py

Zamienia tekst z arkusza Excel
na obiekty zgodne z modelem BiDO.
"""
HEADER_ROW = 14
EXAMPLE_ROW = 15
DATA_START_ROW = 16

def normalize_import_id(value):
    """
    Normalizuje identyfikator importu.

    R000001
    r000001
    R000001
    → R000001
    """
    if value is None:
        return None

    return str(value).strip().upper()

def parse_sheet(
    worksheet,
    required_column,
):
    """
    Odczytuje jeden arkusz formularza importu
    i zwraca listę słowników.

    Nie interpretuje danych.
    """

   

    headers = [cell.value for cell in worksheet[HEADER_ROW]]

    if required_column not in headers:
        raise ValueError(
            f'Arkusz nie zawiera wymaganej kolumny "{required_column}".'
        )

    records = []

    for row_number, row in enumerate(
        worksheet.iter_rows(
            min_row=DATA_START_ROW,
            values_only=True,
        ),
        start=DATA_START_ROW,
    ):

        record = dict(zip(headers, row))

        record["_excel_row"] = row_number

        # normalizacja identyfikatora importu
        if "ID importu" in record:
            record["ID importu"] = normalize_import_id(record["ID importu"])

        # pomijamy tylko całkowicie puste wiersze
        if all(
            value is None or str(value).strip() == ""
            for value in row
        ):
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