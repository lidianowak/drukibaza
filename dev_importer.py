from pathlib import Path

from biblioteka.importer.loader import load_workbook
from biblioteka.importer.parser import parse_sheet
from biblioteka.importer.mapper import map_record

wb = load_workbook(
    Path(r"C:\Users\user\Desktop\drukibaza\formularz importu_BiDO.xlsx")
)

records = parse_sheet(wb["Rekordy"])

mapped = map_record(records[0])

print(mapped)

from biblioteka.importer.object_parser import split_variants

print()

print(split_variants("Kochanowski"))

print(split_variants("Kochanowski [Cochanovius]"))

print(split_variants("Kochanowski [Cochanovius|Cochanovsky]"))

from biblioteka.importer.object_parser import split_qualifier

print()

print(split_qualifier("Jan"))

print(split_qualifier("Jan (starszy)"))

print(split_qualifier("Jan Andrzej (opat)"))

from biblioteka.importer.object_parser import split_list

print()

print(split_list("Kochanowski, Jan"))

print(
    split_list(
        "Kochanowski, Jan; Piotrkowczyk, Andrzej"
    )
)

from biblioteka.importer.object_parser import split_name

print()

print(split_name("Kochanowski, Jan"))

print(split_name("Nowak-Kowalski, Jan Andrzej"))

print(split_name("de Bry, Theodor"))

from biblioteka.importer.object_parser import parse_persons

print()
print("TEST PARSE_PERSONS")

persons = parse_persons(
    "Kochanowski [Cochanovius], Jan Andrzej [Ioannes|Johannes] (starszy); "
    "Bartłomiej (z Wrześni); "
    "Piotrkowczyk, Andrzej"
)

print(persons)

for person in persons:
    print(person)

from biblioteka.importer.object_parser import parse_named_objects

print()
print("TEST PARSE_NAMED_OBJECTS")

objects = parse_named_objects(
    "Kraków [Cracovia|Cracov]; Wilno"
)

for obj in objects:
    print(obj)

