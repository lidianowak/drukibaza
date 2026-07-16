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


def run_import(
    workbook,
    uzytkownik,
):
    """
    Wykonuje pełny import danych z formularza.
    """

    result = ImportResult()

    
    with transaction.atomic():

            

        records = parse_sheet(
                workbook["Rekordy"],
                "Tytuł skrócony (transkrypcja)",
            )

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

        rekordy = {}
        
        for record in records:

            mapped = map_record(record)


            rekord = create_record(
                mapped,
                uzytkownik,
            )

            rekordy[mapped["id_importu"]] = rekord

            
        print()
        print("=" * 60)
        print("IMPORT RELACJI")
        print("=" * 60)

        for record in records:

            mapped = map_record(record)

            print("MAPPED:")
            print(mapped)

            relacje = map_relations(mapped)

            print("RELACJE:")
            print(relacje)

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

        for specimen in specimens:

            mapped = map_specimen(specimen)

            rekord = rekordy.get(
                mapped["id_importu"]
            )

            if rekord is None:
                raise ValueError(
                    f"Nie znaleziono rekordu dla {mapped['id_importu']}"
                )

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

        for attachment in attachments:

            mapped = map_attachment(attachment)

            rekord = rekordy.get(
                mapped["id_importu"]
            )

            if rekord is None:

                result.success = False

                result.errors.append(
                    ImportErrorItem(
                        message=(
                            f"Nie znaleziono rekordu "
                            f"{mapped['id_importu']}"
                        ),
                        sheet="Egzemplarze",
                        field="Id importu",
                    )
                )

                raise ValueError(
                    f"Nie znaleziono rekordu dla {mapped['id_importu']}"
                )

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
                        