"""
loader.py

Odpowiada wyłącznie za odczyt formularza importu BiDO (.xlsx)
i zamianę go na strukturę danych Pythona.

Nie wykonuje walidacji.
Nie tworzy modeli Django.
"""

from pathlib import Path
from openpyxl import load_workbook as openpyxl_load_workbook


REQUIRED_SHEETS = [
    "Rekordy",
    "Egzemplarze",
    "Karty tytułowe",
    "Załączniki",
]


def load_workbook(path: Path):
    """
    Otwiera formularz importu BiDO
    i sprawdza obecność wymaganych arkuszy.
    """

    workbook = openpyxl_load_workbook(path)

    missing = [
        sheet
        for sheet in REQUIRED_SHEETS
        if sheet not in workbook.sheetnames
    ]

    if missing:
        raise ValueError(
            f"Brakuje wymaganych arkuszy: {', '.join(missing)}"
        )

    return workbook
