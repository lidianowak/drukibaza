from pathlib import Path

from biblioteka.importer.loader import load_workbook
from biblioteka.importer.parser import parse_sheet

wb = load_workbook(Path(r"C:\Users\user\Desktop\drukibaza\formularz importu_BiDO.xlsx"))

records = parse_sheet(wb["Rekordy"])

print(type(records))
print(type(records[0]))
print(records[0])