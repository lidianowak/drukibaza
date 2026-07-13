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
            places = parse_places(mapped["miejsce_wydania"])

            print("AUTORZY:")

            
            for person in persons:
                osoba = get_or_create_person(person)

                print(person)
                print(f"→ {osoba}")

            print("MIEJSCE WYDANIA:")

            for place in places:
                miejsce = get_or_create_place(place)

                print(place)
                print(f"→ {miejsce}")

    