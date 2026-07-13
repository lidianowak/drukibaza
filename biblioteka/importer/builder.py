"""
builder.py

Buduje obiekty Django
na podstawie sparsowanych danych importera.
"""

from biblioteka.models import (
    Osoba,
    WariantNazwyOsoby,
    Miejsce,
    WariantNazwyMiejsca,
    Instytucja,
    WariantNazwyInstytucji,
    Temat,
    Gatunek,
    Motyw,
    Wydarzenie,
    Biblioteka,
    WariantNazwyInstytucji,
    WariantNazwyTematu,
    WariantNazwyGatunku,
    WariantNazwyMotywu,
    WariantNazwyWydarzenia,
    WariantNazwyBiblioteki,
)

from biblioteka.importer.object_parser import (
    ParsedPerson,
    ParsedName,
)

def find_person(person: ParsedPerson):
    """
    Szuka osoby najpierw po nazwie głównej,
    a następnie po wariantach nazw.
    """

    if person.nazwa:
        matches = Osoba.objects.filter(
            imiona=person.nazwa,
            nazwisko="",
        )

        if matches.exists():
            return matches

        return Osoba.objects.filter(
            warianty_nazw__nazwa=person.nazwa
        )

    full_name = f"{person.nazwisko}, {person.imiona}"

    matches = Osoba.objects.filter(
        nazwisko=person.nazwisko,
        imiona=person.imiona,
    )

    if matches.exists():
        return matches

    return Osoba.objects.filter(
        warianty_nazw__nazwa=full_name
    ).distinct()

def find_named_object(model, place: ParsedName, related_name="warianty_nazw"):
    """
    Szuka obiektu nazwanego po nazwie głównej i wszystkich wariantach.
    """

    nazwy = [place.nazwa, *place.warianty]

    znalezione = set()

    for nazwa in nazwy:

        matches = model.objects.filter(nazwa=nazwa)

        for obj in matches:
            znalezione.add(obj.pk)

        matches = model.objects.filter(
            **{f"{related_name}__nazwa": nazwa}
        )

        for obj in matches:
            znalezione.add(obj.pk)

    return model.objects.filter(pk__in=znalezione)

def find_place(place: ParsedName):
    """
    Szuka miejsca po wszystkich znanych nazwach.
    """

    return find_named_object(Miejsce, place)

def find_institution(institution: ParsedName):
    """
    Szuka instytucji po wszystkich znanych nazwach.
    """

    return find_named_object(
        Instytucja,
        institution,
    )

def find_theme(theme: ParsedName):
    return find_named_object(Temat, theme)


def find_genre(genre: ParsedName):
    return find_named_object(Gatunek, genre)


def find_motif(motif: ParsedName):
    return find_named_object(Motyw, motif)


def find_event(event: ParsedName):
    return find_named_object(Wydarzenie, event)


def find_library(library: ParsedName):
    return find_named_object(Biblioteka, library)

def add_institution_variants(
    instytucja: Instytucja,
    institution: ParsedName,
):
    """
    Dodaje brakujące warianty nazw instytucji.
    """

    add_named_object_variants(
        obj=instytucja,
        parsed=institution,
        variant_model=WariantNazwyInstytucji,
        relation_field="instytucja",
    )


def create_institution(institution: ParsedName):
    """
    Tworzy nową instytucję.
    """

    return create_named_object(
        model=Instytucja,
        parsed=institution,
        add_variants=add_institution_variants,
    )

def create_theme(theme: ParsedName):
    return create_named_object(
        model=Temat,
        parsed=theme,
        add_variants=lambda o, p: add_named_object_variants(
            o, p,
            WariantNazwyTematu,
            "temat",
        ),
    )


def create_genre(genre: ParsedName):
    return create_named_object(
        model=Gatunek,
        parsed=genre,
        add_variants=lambda o, p: add_named_object_variants(
            o, p,
            WariantNazwyGatunku,
            "gatunek",
        ),
    )


def create_motif(motif: ParsedName):
    return create_named_object(
        model=Motyw,
        parsed=motif,
        add_variants=lambda o, p: add_named_object_variants(
            o, p,
            WariantNazwyMotywu,
            "motyw",
        ),
    )


def create_event(event: ParsedName):
    return create_named_object(
        model=Wydarzenie,
        parsed=event,
        add_variants=lambda o, p: add_named_object_variants(
            o, p,
            WariantNazwyWydarzenia,
            "wydarzenie",
        ),
    )


def create_library(library: ParsedName):
    return create_named_object(
        model=Biblioteka,
        parsed=library,
        add_variants=lambda o, p: add_named_object_variants(
            o, p,
            WariantNazwyBiblioteki,
            "biblioteka",
        ),
    )


def get_or_create_institution(institution: ParsedName):
    return get_or_create_named_object(
        model=Instytucja,
        variant_model=WariantNazwyInstytucji,
        relation_field="instytucja",
        parsed=institution,
    )

def get_or_create_theme(theme: ParsedName):
    return get_or_create_named_object(
        model=Temat,
        variant_model=WariantNazwyTematu,
        relation_field="temat",
        parsed=theme,
    )


def get_or_create_genre(genre: ParsedName):
    return get_or_create_named_object(
        model=Gatunek,
        variant_model=WariantNazwyGatunku,
        relation_field="gatunek",
        parsed=genre,
    )


def get_or_create_motif(motif: ParsedName):
    return get_or_create_named_object(
        model=Motyw,
        variant_model=WariantNazwyMotywu,
        relation_field="motyw",
        parsed=motif,
    )


def get_or_create_event(event: ParsedName):
    return get_or_create_named_object(
        model=Wydarzenie,
        variant_model=WariantNazwyWydarzenia,
        relation_field="wydarzenie",
        parsed=event,
    )


def get_or_create_library(library: ParsedName):
    return get_or_create_named_object(
        model=Biblioteka,
        variant_model=WariantNazwyBiblioteki,
        relation_field="biblioteka",
        parsed=library,
    )


def add_person_variants(osoba: Osoba, person: ParsedPerson):
    """
    Dodaje brakujące warianty nazw osoby.
    """

    istniejące = {
        wariant.nazwa
        for wariant in osoba.warianty_nazw.all()
    }

    kolejnosc = osoba.warianty_nazw.count() + 1

    warianty = []

    for nazwisko in [person.nazwisko, *person.warianty_nazwiska]:
        if nazwisko is None:
            continue

        for imiona in [person.imiona, *person.warianty_imion]:
            if imiona is None:
                continue

            warianty.append(f"{nazwisko}, {imiona}")

    if person.nazwa:
        warianty.append(person.nazwa)

    for nazwa in warianty:

        if nazwa in istniejące:
            continue

        WariantNazwyOsoby.objects.create(
            osoba=osoba,
            nazwa=nazwa,
            kolejnosc=kolejnosc,
        )

        kolejnosc += 1

def add_named_object_variants(obj, parsed, variant_model, relation_field):
    """
    Dodaje brakujące warianty nazw obiektu nazwanego.
    """

    istniejące = {
        wariant.nazwa
        for wariant in obj.warianty_nazw.all()
    }

    kolejnosc = obj.warianty_nazw.count() + 1

    for nazwa in [parsed.nazwa, *parsed.warianty]:

        if nazwa in istniejące:
            continue

        variant_model.objects.create(
            **{
                relation_field: obj,
                "nazwa": nazwa,
                "kolejnosc": kolejnosc,
            }
        )

        kolejnosc += 1

def add_place_variants(miejsce: Miejsce, place: ParsedName):
    """
    Dodaje brakujące warianty nazw miejsca.
    """

    add_named_object_variants(
        obj=miejsce,
        parsed=place,
        variant_model=WariantNazwyMiejsca,
        relation_field="miejsce",
    )

def create_named_object(model, parsed, add_variants):
    """
    Tworzy nowy obiekt nazwany.
    """

    obj = model.objects.create(
        nazwa=parsed.nazwa,
    )

    add_variants(obj, parsed)

    return obj

def get_or_create_named_object(
    model,
    variant_model,
    relation_field,
    parsed,
):
    """
    Zwraca istniejący obiekt nazwany lub tworzy nowy.
    """

    matches = find_named_object(model, parsed)

    if matches.count() == 1:
        obj = matches.first()

        add_named_object_variants(
            obj=obj,
            parsed=parsed,
            variant_model=variant_model,
            relation_field=relation_field,
        )

        return obj

    if matches.count() > 1:
        raise ValueError(
            f"Znaleziono więcej niż jeden obiekt: {parsed.nazwa}"
        )

    obj = create_named_object(
        model=model,
        parsed=parsed,
        add_variants=lambda o, p: add_named_object_variants(
            obj=o,
            parsed=p,
            variant_model=variant_model,
            relation_field=relation_field,
        ),
    )

    return obj

def create_place(place: ParsedName):
    """
    Tworzy nowe miejsce.
    """

    return create_named_object(
        model=Miejsce,
        parsed=place,
        add_variants=add_place_variants,
    )

def get_or_create_place(place: ParsedName):
    """
    Zwraca istniejące miejsce lub tworzy nowe.
    """

    matches = find_place(place)

    if matches.count() == 1:
        miejsce = matches.first()

        add_place_variants(miejsce, place)

        return miejsce

    if matches.count() > 1:
        raise ValueError(
            f"Znaleziono więcej niż jedno miejsce: {place}"
        )

    return create_place(place)

def create_person(person: ParsedPerson):
    """
    Tworzy nowy obiekt Osoba.
    """

    if person.nazwa:
        osoba = Osoba.objects.create(
            imiona=person.nazwa,
            nazwisko="",
            kwalifikator=person.kwalifikator or "",
        )
    else:
        osoba = Osoba.objects.create(
            imiona=person.imiona,
            nazwisko=person.nazwisko,
            kwalifikator=person.kwalifikator or "",
        )

    add_person_variants(osoba, person)

    return osoba

def get_or_create_person(person: ParsedPerson):
    """
    Zwraca istniejącą osobę lub tworzy nową.
    """

    matches = find_person(person)

    if matches.count() == 1:
        osoba = matches.first()

        add_person_variants(osoba, person)

        return osoba

    if matches.count() > 1:
        raise ValueError(
            f"Znaleziono więcej niż jedną osobę: {person}"
        )

    return create_person(person)

