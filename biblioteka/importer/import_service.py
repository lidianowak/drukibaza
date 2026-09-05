"""
import_service.py

Główna logika importu danych.
"""

from biblioteka.importer.parser import parse_sheet
from biblioteka.importer.mapper import map_record
from biblioteka.importer.object_parser import parse_persons

from biblioteka.importer.record_builder import create_record

from biblioteka.importer.specimen_mapper import map_specimen
from biblioteka.importer.specimen_builder import create_specimen

from biblioteka.importer.attachment_mapper import map_attachment
from biblioteka.importer.attachment_builder import create_attachment

from biblioteka.importer.relation_mapper import map_relations
from biblioteka.importer.relation_builder import create_relations
from biblioteka.importer.linter import lint_record, normalize_spaces

from biblioteka.models import (
    Rekord,
    RelacjaOsoby,
)

from biblioteka.importer.builder import find_person

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


def check_duplicate_records(mapped_records, result):
    """
    Sprawdza, czy wśród rekordów przeznaczonych do importu
    znajdują się rekordy o takim samym autorze, drukarzu
    i roku wydania.
    """

    keys = {}

    for mapped in mapped_records:

        row = mapped["_excel_row"]

        authors = parse_persons(
            mapped.get("autorzy") or ""
        )

        printers = parse_persons(
            mapped.get("drukarze") or ""
        )

        if not authors or not printers or not mapped.get("rok_wydania"):
            continue

        def person_key(person):

            if person.nazwa:
                return (
                    "nazwa",
                    person.nazwa,
                    person.kwalifikator or "",
                )

            return (
                "osoba",
                person.nazwisko or "",
                person.imiona or "",
                person.kwalifikator or "",
            )

        author_key = tuple(
            sorted(
                person_key(person)
                for person in authors
            )
        )

        printer_key = tuple(
            sorted(
                person_key(person)
                for person in printers
            )
        )

        year = mapped.get("rok_wydania")

        key = (
            author_key,
            printer_key,
            year,
        )

        keys.setdefault(
            key,
            [],
        ).append(row)

    for key, rows in keys.items():

        if len(rows) > 1:

            for row in rows:

                result.add_warning(
                    message=(
                        "Możliwy duplikat rekordu: "
                        "inny rekord w pliku ma tego samego "
                        "autora, drukarza i rok wydania."
                    ),
                    sheet="Rekordy",
                    row=row,
                    field="Autor(y), Drukarz, Rok wydania",
                )


def check_existing_duplicate_records(mapped_records, result):
    """
    Sprawdza, czy w bazie istnieją już rekordy o takim samym
    autorze, drukarzu i roku wydania jak rekordy przeznaczone
    do importu.
    """

    for mapped in mapped_records:

        row = mapped["_excel_row"]

        authors = parse_persons(
            mapped.get("autorzy") or ""
        )

        printers = parse_persons(
            mapped.get("drukarze") or ""
        )

        year = mapped.get("rok_wydania")

        if not authors or not printers or not year:
            continue

        # ---------- Autorzy ----------

        author_objects = []

        for person in authors:

            matches = find_person(person)

            if matches.count() != 1:
                author_objects = []
                break

            author_objects.append(
                matches.first()
            )

        if not author_objects:
            continue

        # ---------- Drukarze ----------

        printer_objects = []

        for person in printers:

            matches = find_person(person)

            if matches.count() != 1:
                printer_objects = []
                break

            printer_objects.append(
                matches.first()
            )

        if not printer_objects:
            continue

        imported_author_ids = {
            osoba.pk
            for osoba in author_objects
        }

        imported_printer_ids = {
            osoba.pk
            for osoba in printer_objects
        }

        # ---------- Istniejące rekordy ----------

        existing_records = Rekord.objects.filter(
            rok_wydania=year,
        )

        for existing in existing_records:

            existing_author_ids = set(
                RelacjaOsoby.objects.filter(
                    rekord=existing,
                    typ="autor",
                ).values_list(
                    "osoba_id",
                    flat=True,
                )
            )

            existing_printer_ids = set(
                RelacjaOsoby.objects.filter(
                    rekord=existing,
                    typ="drukarz",
                ).values_list(
                    "osoba_id",
                    flat=True,
                )
            )

            if (
                existing_author_ids == imported_author_ids
                and
                existing_printer_ids == imported_printer_ids
            ):

                result.add_warning(
                    message=(
                        "Możliwy duplikat rekordu: "
                        "w bazie istnieje już rekord "
                        "o tym samym autorze, drukarzu "
                        "i roku wydania."
                    ),
                    sheet="Rekordy",
                    row=row,
                    field="Autor(y), Drukarz, Rok wydania",
                )

def check_fuzzy_matches(mapped_records, result):
    """
    Sprawdza, czy wartości z importu nie są prawdopodobnymi
    literówkami istniejących obiektów w bazie.
    Nie modyfikuje bazy danych.
    """

    from biblioteka.importer.builder import (
        find_fuzzy_match,
        find_fuzzy_person_match,
    )

    from biblioteka.importer.object_parser import (
        parse_persons,
        parse_places,
        parse_institutions,
        parse_themes,
        parse_genres,
        parse_motifs,
        parse_events,
        parse_named_objects,
    )

    from biblioteka.models import (
        Miejsce,
        Instytucja,
        Temat,
        Gatunek,
        Motyw,
        Wydarzenie,
        Jezyk,
    )

    for mapped in mapped_records:

        row = mapped["_excel_row"]

        # ---------- Osoby ----------

        person_fields = {
            "autorzy": "Autor(y)",
            "drukarze": "Drukarz",
            "adresaci_dedykacji": "Adresat dedykacji",
            "powiazane_osoby": "Powiązane osoby",
        }

        for field_name, field_label in person_fields.items():

            persons = parse_persons(
                mapped.get(field_name) or ""
            )

            for person in persons:

                fuzzy_match = find_fuzzy_person_match(person)

                if fuzzy_match is None:
                    continue

                osoba, podobna_nazwa, rodzaj = fuzzy_match

                if person.nazwa:
                    wprowadzona_nazwa = person.nazwa
                else:
                    wprowadzona_nazwa = (
                        f"{person.nazwisko}, {person.imiona}"
                    )

                result.add_warning(
                    message=(
                        f"Możliwa literówka w danych osoby: "
                        f"„{podobna_nazwa}”. "
                        f"Wprowadzono: „{wprowadzona_nazwa}”."
                    ),
                    sheet="Rekordy",
                    row=row,
                    field=field_label,
                )

        # ---------- Miejsca ----------

        place_fields = {
            "miejsce_wydania": "Miejsce wydania",
            "powiazane_miejsca": "Powiązane miejsca",
        }

        for field_name, field_label in place_fields.items():

            places = parse_places(
                mapped.get(field_name) or ""
            )

            for place in places:

                fuzzy_match = find_fuzzy_match(
                    Miejsce,
                    place.nazwa,
                )

                if fuzzy_match is None:
                    continue

                _, podobna_nazwa = fuzzy_match

                result.add_warning(
                    message=(
                        f"Możliwa literówka w nazwie miejsca: "
                        f"„{place.nazwa}”. "
                        f"Istnieje podobne miejsce: "
                        f"„{podobna_nazwa}”."
                    ),
                    sheet="Rekordy",
                    row=row,
                    field=field_label,
                )

        # ---------- Pozostałe obiekty nazwane ----------

        named_object_fields = {
            "powiazane_instytucje": (
                parse_institutions,
                Instytucja,
                "Powiązane instytucje",
            ),
            "tematy": (
                parse_themes,
                Temat,
                "Tematy",
            ),
            "gatunki": (
                parse_genres,
                Gatunek,
                "Gatunki",
            ),
            "motywy": (
                parse_motifs,
                Motyw,
                "Motywy",
            ),
            "wydarzenia": (
                parse_events,
                Wydarzenie,
                "Wydarzenia",
            ),
        }

        for field_name, (
            parser,
            model,
            field_label,
        ) in named_object_fields.items():

            objects = parser(
                mapped.get(field_name) or ""
            )

            for parsed in objects:

                fuzzy_match = find_fuzzy_match(
                    model,
                    parsed.nazwa,
                )

                if fuzzy_match is None:
                    continue

                _, podobna_nazwa = fuzzy_match

                result.add_warning(
                    message=(
                        f"Możliwa literówka w nazwie: "
                        f"„{parsed.nazwa}”. "
                        f"Istnieje podobny obiekt: "
                        f"„{podobna_nazwa}”."
                    ),
                    sheet="Rekordy",
                    row=row,
                    field=field_label,
                )

        # ---------- Język ----------

        languages = parse_named_objects(
            mapped.get("jezyki") or ""
        )

        for language in languages:

            fuzzy_match = find_fuzzy_match(
                Jezyk,
                language.nazwa,
                related_name=None,
            )

            if fuzzy_match is None:
                continue

            _, podobna_nazwa = fuzzy_match

            result.add_warning(
                message=(
                    f"Możliwa literówka w nazwie języka: "
                    f"„{language.nazwa}”. "
                    f"Istnieje podobny język: "
                    f"„{podobna_nazwa}”."
                ),
                sheet="Rekordy",
                row=row,
                field="Język",
            )

def check_fuzzy_specimens(mapped_specimens, result):
    """
    Sprawdza, czy biblioteki podane w arkuszu Egzemplarze
    nie są prawdopodobnymi literówkami istniejących bibliotek.
    Nie modyfikuje bazy danych.
    """

    from biblioteka.importer.builder import find_fuzzy_match
    from biblioteka.importer.object_parser import parse_named_objects
    from biblioteka.models import Biblioteka

    for mapped in mapped_specimens:

        row = mapped["_excel_row"]

        libraries = parse_named_objects(
            mapped.get("biblioteka") or ""
        )

        for library in libraries:

            fuzzy_match = find_fuzzy_match(
                Biblioteka,
                library.nazwa,
            )

            if fuzzy_match is None:
                continue

            _, podobna_nazwa = fuzzy_match

            result.add_warning(
                message=(
                    f"Możliwa literówka w nazwie biblioteki: "
                    f"„{library.nazwa}”. "
                    f"Istnieje podobna biblioteka: "
                    f"„{podobna_nazwa}”."
                ),
                sheet="Egzemplarze",
                row=row,
                field="Biblioteka",
            )

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

    for mapped in mapped_records:

        row = mapped["_excel_row"]

        if not validator.validate_record(mapped, row):
            continue

        if not validator.validate_relations(
            mapped,
            import_ids,
            row,
        ):
            continue

    # ---------- Egzemplarze ----------

    for mapped in mapped_specimens:

        row = mapped["_excel_row"]

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

    for mapped in mapped_attachments:

        row = mapped["_excel_row"]

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
    result=None,
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
            result=result,
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

        for mapped in mapped_records:

            for field_name, value in mapped.items():

                if field_name == "_excel_row":
                    continue

                mapped[field_name] = normalize_spaces(value)

        for mapped in mapped_records:

            warnings = lint_record(mapped)

            for field_name, message in warnings:

                result.add_warning(
                    message=message,
                    sheet="Rekordy",
                    row=mapped["_excel_row"],
                    field=field_name,
                )

        check_duplicate_records(
            mapped_records,
            result,
        )

        check_existing_duplicate_records(
            mapped_records,
            result,
        )

        id_rows = {}

        for record in mapped_records:

            row = record["_excel_row"]

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

        check_fuzzy_matches(
            mapped_records,
            result,
        )

        check_fuzzy_specimens(
            mapped_specimens,
            result,
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
            result=result,
        )

        return result