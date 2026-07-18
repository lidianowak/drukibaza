"""
import_service.py

Główna logika importu danych.
"""

from biblioteka.importer.parser import parse_sheet
from biblioteka.importer.mapper import map_record

from biblioteka.importer.record_builder import create_record

from biblioteka.importer.specimen_mapper import map_specimen
from biblioteka.importer.specimen_builder import create_specimen

from biblioteka.importer.attachment_mapper import map_attachment
from biblioteka.importer.attachment_builder import create_attachment

from biblioteka.importer.relation_mapper import map_relations
from biblioteka.importer.relation_builder import create_relations

from django.db import transaction

from biblioteka.importer.result import (
    ImportResult,
    ImportErrorItem,
)

from .validator import ImportValidator
from .exceptions import ImportValidationError

def validate_import(
    records,
    specimens,
    attachments,
    validator,
    result,
    import_ids,
):
    """
    Wykonuje pełną walidację danych przed rozpoczęciem importu.
    """

    # ---------- Rekordy ----------

    for row, record in enumerate(records, start=2):

        mapped = map_record(record)

        if not validator.validate_record(mapped, row):
            continue

        if not validator.validate_relations(
            mapped,
            import_ids,
            row,
        ):
            continue

    # ---------- Egzemplarze ----------

    for row, specimen in enumerate(specimens, start=2):

        mapped = map_specimen(specimen)

        validator.validate_specimen(
            mapped,
            row,
        )

        if mapped["id_importu"] not in import_ids:

            result.add_error(
                message=f"Nie znaleziono rekordu {mapped['id_importu']}.",
                sheet="Egzemplarze",
                row=row,
                field="Id importu",
                import_id=mapped["id_importu"],
            )

    # ---------- Załączniki ----------

    for row, attachment in enumerate(attachments, start=2):

        mapped = map_attachment(attachment)

        validator.validate_attachment(
            mapped,
            row,
        )

        if mapped["id_importu"] not in import_ids:

            result.add_error(
                message=f"Nie znaleziono rekordu {mapped['id_importu']}.",
                sheet="Załączniki",
                row=row,
                field="Id importu",
                import_id=mapped["id_importu"],
            )

def run_import(
    workbook,
    uzytkownik,
):
    """
    Wykonuje pełny import danych z formularza.
    """

    result = ImportResult()

    validator = ImportValidator(result)

    REQUIRED_SHEETS = [
        "Rekordy",
        "Egzemplarze",
        "Załączniki",
    ]

    missing = [
        sheet
        for sheet in REQUIRED_SHEETS
        if sheet not in workbook.sheetnames
    ]

    if missing:

        result.add_error(
            message=f"Brakuje wymaganych arkuszy: {', '.join(missing)}.",
            sheet="Plik",
        )

        raise ImportValidationError(result)

    
    with transaction.atomic():

            

        records = parse_sheet(
                workbook["Rekordy"],
                "Tytuł skrócony (transkrypcja)",
            )
        
        import_ids = {
            map_record(record)["id_importu"]
            for record in records
        }

        specimens = parse_sheet(
                workbook["Egzemplarze"],
                "Biblioteka",
            )

        attachments = parse_sheet(
                workbook["Załączniki"],
                "Ścieżka pliku",
            )

        print(f"Liczba rekordów: {len(records)}")
        print(f"Liczba egzemplarzy: {len(specimens)}")
        print(f"Liczba załączników: {len(attachments)}")

        result.records = len(records)
        result.specimens = len(specimens)
        result.attachments = len(attachments)

        validate_import(
            records,
            specimens,
            attachments,
            validator,
            result,
            import_ids,
        )

        if result.errors:
            raise ImportValidationError(result)
        
        rekordy = {}
        
        for row, record in enumerate(records, start=2):

            mapped = map_record(record)

            if not validator.validate_record(mapped, row):
                continue

            rekord = create_record(
                mapped,
                uzytkownik,
            )

            rekordy[mapped["id_importu"]] = rekord

        if result.errors:
            raise ImportValidationError(result)

            
        print()
        print("=" * 60)
        print("IMPORT RELACJI")
        print("=" * 60)

        for row, record in enumerate(records, start=2):

            mapped = map_record(record)

            if not validator.validate_relations(
                mapped,
                import_ids,
                row,
            ):
                raise ImportValidationError(result)

            relacje = map_relations(mapped)

            rekord = rekordy[mapped["id_importu"]]

            create_relations(
                rekord,
                relacje,
                rekordy,
            )

            print(mapped["id_importu"])

        print()
        print("=" * 60)
        print("IMPORT EGZEMPLARZY")
        print("=" * 60)

        for row, specimen in enumerate(specimens, start=2):

            mapped = map_specimen(specimen)

            if not validator.validate_specimen(mapped, row):
                raise ImportValidationError(result)

            rekord = rekordy.get(
                mapped["id_importu"]
            )

            if rekord is None:

                result.add_error(
                    message=f"Nie znaleziono rekordu {mapped['id_importu']}.",
                    sheet="Egzemplarze",
                    row=row,
                    field="Id importu",
                    import_id=mapped["id_importu"],
                )

                raise ImportValidationError(result)

            create_specimen(
                rekord,
                mapped,
            )

            print(
                f"{mapped['id_importu']} → "
                f"{mapped.get('biblioteka')}"
            )

        print()
        print("=" * 60)
        print("IMPORT ZAŁĄCZNIKÓW")
        print("=" * 60)

        for row, attachment in enumerate(attachments, start=2):

            mapped = map_attachment(attachment)

            if not validator.validate_attachment(mapped, row):
                raise ImportValidationError(result)

            rekord = rekordy.get(
                mapped["id_importu"]
            )

            if rekord is None:

                result.add_error(
                    message=f"Nie znaleziono rekordu {mapped['id_importu']}.",
                    sheet="Załączniki",
                    row=row,
                    field="Id importu",
                    import_id=mapped["id_importu"],
                )

                raise ImportValidationError(result)

            create_attachment(
                rekord,
                mapped,
            )

            print(
                rekord.identyfikator,
                "→",
                mapped["sekcja"],
            )

        return result
                        