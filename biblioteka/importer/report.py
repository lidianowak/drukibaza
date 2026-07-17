"""
report.py

Tworzy raport z walidacji i importu.
"""


from io import StringIO


from io import StringIO


def build_report(import_danych, result=None):
    """
    Buduje tekstowy raport importu.
    """

    output = StringIO()

    output.write("RAPORT IMPORTU\n\n")

    output.write(
        f"Status: {import_danych.get_status_display()}\n"
    )

    output.write(
        f"Data: {import_danych.data_rozpoczecia}\n"
    )

    output.write(
        f"Użytkownik: {import_danych.uzytkownik}\n\n"
    )

    output.write("ZAIMPORTOWANO\n")

    output.write(
        f"Rekordy: {import_danych.liczba_rekordow}\n"
    )

    output.write(
        f"Egzemplarze: {import_danych.liczba_egzemplarzy}\n"
    )

    output.write(
        f"Załączniki: {import_danych.liczba_zalacznikow}\n"
    )

    if result is not None:

        output.write("\n")
        output.write("WALIDACJA\n")

        if result.errors:

            output.write("\nBŁĘDY:\n")

            for error in result.errors:

                output.write(f"- {error.message}")

                if error.sheet:
                    output.write(f" | arkusz: {error.sheet}")

                if error.import_id:
                    output.write(f" | id importu: {error.import_id}")

                if error.row:
                    output.write(f" | wiersz: {error.row}")

                if error.field:
                    output.write(f" | pole: {error.field}")

                output.write("\n")

        if result.warnings:

            output.write("\nOSTRZEŻENIA:\n")

            for warning in result.warnings:

                output.write(f"- {warning.message}")

                if warning.sheet:
                    output.write(f" | arkusz: {warning.sheet}")

                if warning.import_id:
                    output.write(f" | id importu: {warning.import_id}")

                if warning.row:
                    output.write(f" | wiersz: {warning.row}")

                if warning.field:
                    output.write(f" | pole: {warning.field}")

                output.write("\n")

    return output.getvalue()