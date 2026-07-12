from pathlib import Path

from django.core.management.base import BaseCommand

from biblioteka.importer.loader import load_workbook
from biblioteka.importer.parser import parse_sheet
from biblioteka.importer.mapper import map_record
from biblioteka.importer.object_parser import parse_persons
from biblioteka.importer.builder import get_or_create_person


class Command(BaseCommand):
    help = "Test importera BiDO"

    def handle(self, *args, **options):

        wb = load_workbook(
            Path(r"C:\Users\user\Desktop\drukibaza\formularz importu_BiDO.xlsx")
        )

        records = parse_sheet(wb["Rekordy"])
        print(f"Liczba rekordów: {len(records)}")

        for record in records:

            mapped = map_record(record)

            print()
            print("=" * 60)
            print(mapped["id_importu"])

            persons = parse_persons(mapped["autorzy"])

            print("AUTORZY:")

            from biblioteka.importer.builder import get_or_create_person

            for person in persons:
                osoba = get_or_create_person(person)

                print(person)
                print(f"→ {osoba}")

    