"""
record_builder.py

Tworzenie obiektu Rekord
na podstawie danych z formularza importu.
"""

from biblioteka.models import (
    Rekord,
    RelacjaOsoby,
    RelacjaMiejsca,
    RelacjaInstytucji,
    RelacjaTematu,
    RelacjaGatunku,
    RelacjaMotywu,
    RelacjaWydarzenia,
    WersjaZdigitalizowana,
    OpracowanieRekordu,
)

from biblioteka.importer.object_parser import (
    parse_persons,
    parse_places,
    parse_institutions,
    parse_named_objects,
)

from biblioteka.importer.builder import (
    get_or_create_person,
    get_or_create_place,
    get_or_create_institution,
    get_or_create_theme,
    get_or_create_genre,
    get_or_create_motif,
    get_or_create_event,
    get_or_create_language,
    get_or_create_format,
    get_or_create_font,
)

from pathlib import Path

from django.core.files import File

STATUS_MAP = {
    None: "do_opracowania",
    "": "do_opracowania",

    "nieopracowany": "do_opracowania",
    "do opracowania": "do_opracowania",

    "częściowo opracowany": "czesciowo_opracowany",

    "opracowany": "opracowany",
}


def import_relations(
    rekord,
    text,
    relation_type,
    parser,
    builder,
    relation_model,
    relation_field,
    result=None,
):
    """
    Uniwersalny importer relacji.
    """

    for parsed in parser(text):

        obj = builder(
            parsed,
            result=result,
        )

        kwargs = {
            "rekord": rekord,
            relation_field: obj,
        }

        if relation_type is not None:
            kwargs["typ"] = relation_type

        relation_model.objects.create(**kwargs)


def import_dictionary_objects(
    rekord,
    text,
    parser,
    builder,
    setter,
    result=None,
):
    """
    Importuje słowniki przypisane bezpośrednio do rekordu.
    """

    for parsed in parser(text):

        obj = builder(
            parsed,
            result=result,
        )

        setter(rekord, obj)


def import_person_relations(
    rekord,
    text,
    relation_type,
    result=None,
):
    """
    Importuje relacje osób do rekordu.
    """

    import_relations(
        rekord=rekord,
        text=text,
        relation_type=relation_type,
        parser=parse_persons,
        builder=get_or_create_person,
        relation_model=RelacjaOsoby,
        relation_field="osoba",
        result=result,
    )


def import_place_relations(
    rekord,
    text,
    relation_type,
    result=None,
):
    """
    Importuje relacje miejsc do rekordu.
    """

    import_relations(
        rekord=rekord,
        text=text,
        relation_type=relation_type,
        parser=parse_places,
        builder=get_or_create_place,
        relation_model=RelacjaMiejsca,
        relation_field="miejsce",
        result=result,
    )


def import_institution_relations(
    rekord,
    text,
    result=None,
):
    import_relations(
        rekord=rekord,
        text=text,
        relation_type=None,
        parser=parse_institutions,
        builder=get_or_create_institution,
        relation_model=RelacjaInstytucji,
        relation_field="instytucja",
        result=result,
    )


def import_theme_relations(
    rekord,
    text,
    result=None,
):
    import_relations(
        rekord=rekord,
        text=text,
        relation_type=None,
        parser=parse_named_objects,
        builder=get_or_create_theme,
        relation_model=RelacjaTematu,
        relation_field="temat",
        result=result,
    )


def import_genre_relations(
    rekord,
    text,
    result=None,
):
    import_relations(
        rekord=rekord,
        text=text,
        relation_type=None,
        parser=parse_named_objects,
        builder=get_or_create_genre,
        relation_model=RelacjaGatunku,
        relation_field="gatunek",
        result=result,
    )


def import_motif_relations(
    rekord,
    text,
    result=None,
):
    import_relations(
        rekord=rekord,
        text=text,
        relation_type=None,
        parser=parse_named_objects,
        builder=get_or_create_motif,
        relation_model=RelacjaMotywu,
        relation_field="motyw",
        result=result,
    )


def import_event_relations(
    rekord,
    text,
    result=None,
):
    import_relations(
        rekord=rekord,
        text=text,
        relation_type=None,
        parser=parse_named_objects,
        builder=get_or_create_event,
        relation_model=RelacjaWydarzenia,
        relation_field="wydarzenie",
        result=result,
    )


def import_languages(
    rekord,
    text,
    result=None,
):
    import_dictionary_objects(
        rekord=rekord,
        text=text,
        parser=parse_named_objects,
        builder=get_or_create_language,
        setter=lambda rekord, obj: rekord.jezyki.add(obj),
        result=result,
    )


def import_fonts(
    rekord,
    text,
    result=None,
):
    import_dictionary_objects(
        rekord=rekord,
        text=text,
        parser=parse_named_objects,
        builder=get_or_create_font,
        setter=lambda rekord, obj: rekord.czcionki.add(obj),
        result=result,
    )


def import_format(
    rekord,
    value,
    result=None,
):
    """
    Importuje format rekordu.
    """

    if value in (None, ""):
        return

    parsed = parse_named_objects(f"{value}°")

    rekord.format = get_or_create_format(
        parsed[0],
        result=result,
    )

    rekord.save(update_fields=["format"])


def import_digitalizations(
    rekord,
    text,
):
    """
    Importuje wersje zdigitalizowane rekordu.
    """

    if not text:
        return

    links = [
        link.strip()
        for link in text.split(";")
        if link.strip()
    ]

    for i, link in enumerate(links, start=1):

        WersjaZdigitalizowana.objects.create(
            rekord=rekord,
            link=link,
            kolejnosc=i,
        )


def import_thumbnail(
    rekord,
    path,
):
    """
    Importuje miniaturę rekordu.
    """

    if not path:
        return

    path = Path(path)

    if not path.exists():
        print(f"Brak pliku: {path}")
        return

    with path.open("rb") as f:

        rekord.miniatura.save(
            path.name,
            File(f),
            save=True,
        )


def create_record(
    mapped,
    uzytkownik,
    result=None,
):
    """
    Tworzy podstawowy obiekt Rekord.

    Na tym etapie bez relacji.
    """

    rekord = Rekord.objects.create(
        tytul_skrocony=mapped.get("tytul_skrocony") or "",
        tytul_pelny=mapped.get("tytul_pelny") or "",
        rok_wydania=mapped.get("rok_wydania") or None,
        liczba_arkuszy=mapped.get("liczba_arkuszy") or None,
        liczba_kart=mapped.get("liczba_kart") or "",
        kolacjonowanie=mapped.get("kolacjonowanie") or "",
        ozdobniki=mapped.get("ozdobniki") or "",
        ryciny=mapped.get("ryciny") or "",
        uwagi=mapped.get("uwagi_opis_fizyczny") or "",
        literatura_przedmiotu=mapped.get("literatura_przedmiotu") or "",
        bibliografie=mapped.get("bibliografie") or "",
        status_opracowania=STATUS_MAP.get(
            mapped.get("status_opracowania"),
            "do_opracowania",
        ),
    )

    OpracowanieRekordu.objects.create(
        rekord=rekord,
        uzytkownik=uzytkownik,
        sposob_dodania="import",
        kolejnosc=1,
    )

    import_person_relations(
        rekord,
        mapped.get("autorzy"),
        "autor",
        result=result,
    )

    import_person_relations(
        rekord,
        mapped.get("drukarze"),
        "drukarz",
        result=result,
    )

    import_person_relations(
        rekord,
        mapped.get("adresaci_dedykacji"),
        "adresat",
        result=result,
    )

    import_person_relations(
        rekord,
        mapped.get("powiazane_osoby"),
        "powiazana",
        result=result,
    )

    import_place_relations(
        rekord,
        mapped.get("miejsce_wydania"),
        "wydania",
        result=result,
    )

    import_place_relations(
        rekord,
        mapped.get("powiazane_miejsca"),
        "powiazane",
        result=result,
    )

    import_institution_relations(
        rekord,
        mapped.get("powiazane_instytucje"),
        result=result,
    )

    import_theme_relations(
        rekord,
        mapped.get("tematy"),
        result=result,
    )

    import_genre_relations(
        rekord,
        mapped.get("gatunki"),
        result=result,
    )

    import_motif_relations(
        rekord,
        mapped.get("motywy"),
        result=result,
    )

    import_event_relations(
        rekord,
        mapped.get("wydarzenia"),
        result=result,
    )

    import_languages(
        rekord,
        mapped.get("jezyki"),
        result=result,
    )

    import_fonts(
        rekord,
        mapped.get("czcionki"),
        result=result,
    )

    import_format(
        rekord,
        mapped.get("format"),
        result=result,
    )

    import_digitalizations(
        rekord,
        mapped.get("linki_digitalizacji"),
    )

    import_thumbnail(
        rekord,
        mapped.get("miniatura"),
    )

    return rekord