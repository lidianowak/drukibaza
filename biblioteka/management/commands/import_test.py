from pathlib import Path

from django.core.management.base import BaseCommand

from biblioteka.importer.loader import load_workbook
from biblioteka.importer.parser import parse_sheet
from biblioteka.importer.mapper import map_record

from biblioteka.importer.object_parser import (
    parse_persons,
    parse_places,
    parse_institutions,
)

from biblioteka.importer.builder import (
    get_or_create_person,
    get_or_create_place,
    get_or_create_institution,
)

from biblioteka.importer.record_builder import create_record

from biblioteka.importer.specimen_mapper import map_specimen
from biblioteka.importer.specimen_builder import create_specimen

from biblioteka.importer.attachment_mapper import map_attachment
from biblioteka.importer.attachment_builder import create_attachment

from biblioteka.importer.relation_mapper import map_relations
from biblioteka.importer.relation_builder import create_relations


class Command(BaseCommand):
    help = "Test importera BiDO"

    def handle(self, *args, **options):

        wb = load_workbook(
            Path(r"C:\Users\user\Desktop\drukibaza\formularz importu_BiDO.xlsx")
        )

        records = parse_sheet(
            wb["Rekordy"],
            "Tytuł skrócony (transkrypcja)",
        )

        specimens = parse_sheet(
            wb["Egzemplarze"],
            "Biblioteka",
        )

        attachments = parse_sheet(
            wb["Załączniki"],
            "Ścieżka pliku",
        )

        print(f"Liczba rekordów: {len(records)}")
        print(f"Liczba egzemplarzy: {len(specimens)}")
        print(f"Liczba załączników: {len(attachments)}")

        rekordy = {}
        
        for record in records:

            mapped = map_record(record)


            rekord = create_record(mapped)

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