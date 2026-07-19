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

from biblioteka.importer.template_validator import (
    validate_template_structure,
)

from collections import Counter

def validate_import(
    mapped_records,
    mapped_specimens,
    mapped_attachments,
    validator,
    result,
    import_ids,
):
    
    """
    Wykonuje pełną walidację danych przed rozpoczęciem importu.
    """

    # ---------- Rekordy ----------

    for row, mapped in enumerate(mapped_records, start=2):


        if not validator.validate_record(mapped, row):
            continue

        if not validator.validate_relations(
            mapped,
            import_ids,
            row,
        ):
            continue

    # ---------- Egzemplarze ----------

    for row, mapped in enumerate(mapped_specimens, start=2):

        
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

    for row, mapped in enumerate(mapped_attachments, start=2):

        
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

def execute_import(
    mapped_records,
    mapped_specimens,
    mapped_attachments,
    uzytkownik,
):
    """
    Tworzy obiekty w bazie po pomyślnej walidacji.
    """

    rekordy = {}

    # ---------- Rekordy ----------

    for mapped in mapped_records:

        rekord = create_record(
            mapped,
            uzytkownik,
        )

        rekordy[mapped["id_importu"]] = rekord

    # ---------- Relacje ----------

    for mapped in mapped_records:

        relacje = map_relations(mapped)

        rekord = rekordy[mapped["id_importu"]]

        create_relations(
            rekord,
            relacje,
            rekordy,
        )

    # ---------- Egzemplarze ----------

    for mapped in mapped_specimens:

        rekord = rekordy[mapped["id_importu"]]

        create_specimen(
            rekord,
            mapped,
        )

    # ---------- Załączniki ----------

    for mapped in mapped_attachments:

        rekord = rekordy[mapped["id_importu"]]

        create_attachment(
            rekord,
            mapped,
        )

    return rekordy



def run_import(
    workbook,
    uzytkownik,
    dry_run=False,
):
    """
    Wykonuje pełny import danych z formularza.
    """

    result = ImportResult()

    validator = ImportValidator(result)

    validate_template_structure(
        workbook,
        result,
    )

    if result.errors:
        raise ImportValidationError(result)

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
        
        mapped_records = [
            map_record(record)
            for record in records
        ]
        
        id_rows = {}

        for row, record in enumerate(mapped_records, start=2):

            import_id = record["id_importu"]

            id_rows.setdefault(
                import_id,
                [],
            ).append(row)

        for import_id, rows in id_rows.items():

            if len(rows) > 1:

                result.add_error(
                    message=(
                        f"Id importu '{import_id}' "
                        f"występuje wielokrotnie "
                        f"(wiersze: {', '.join(map(str, rows))})."
                    ),
                    sheet="Rekordy",
                    field="Id importu",
                    import_id=import_id,
                )

        import_ids = set(id_rows.keys())

        specimens = parse_sheet(
                workbook["Egzemplarze"],
                "Biblioteka",
            )
        
        mapped_specimens = [
            map_specimen(specimen)
            for specimen in specimens
        ]

        attachments = parse_sheet(
                workbook["Załączniki"],
                "Ścieżka pliku",
            )
        
        mapped_attachments = [
            map_attachment(attachment)
            for attachment in attachments
        ]

        print(f"Liczba rekordów: {len(records)}")
        print(f"Liczba egzemplarzy: {len(specimens)}")
        print(f"Liczba załączników: {len(attachments)}")

        result.records = len(records)
        result.specimens = len(specimens)
        result.attachments = len(attachments)

        validate_import(
            mapped_records,
            mapped_specimens,
            mapped_attachments,
            validator,
            result,
            import_ids,
        )

        if result.errors:
            raise ImportValidationError(result)
        
        if dry_run:
            return result
        
        execute_import(
            mapped_records,
            mapped_specimens,
            mapped_attachments,
            uzytkownik,
        )

        return result