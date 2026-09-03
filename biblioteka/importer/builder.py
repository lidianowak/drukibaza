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
    Jezyk,
    Format,
    Czcionka,
)

from biblioteka.importer.object_parser import (
    ParsedPerson,
    ParsedName,
)

import unicodedata

def normalize_for_comparison(text):
    """
    Przygotowuje tekst do porównania fuzzy.

    Ignoruje wielkość liter i nadmiarowe spacje.
    """

    return text.strip().lower()


def damerau_levenshtein_distance(text1, text2):
    """
    Oblicza odległość Damerau-Levenshteina.

    Uwzględnia:
    - dodanie znaku,
    - usunięcie znaku,
    - zamianę znaku,
    - przestawienie dwóch sąsiednich znaków.
    """

    if text1 == text2:
        return 0

    if not text1:
        return len(text2)

    if not text2:
        return len(text1)

    previous_previous = None
    previous = list(range(len(text2) + 1))

    for i, char1 in enumerate(text1, start=1):
        current = [i]

        for j, char2 in enumerate(text2, start=1):
            cost = 0 if char1 == char2 else 1

            value = min(
                current[j - 1] + 1,
                previous[j] + 1,
                previous[j - 1] + cost,
            )

            if (
                previous_previous is not None
                and i > 1
                and j > 1
                and char1 == text2[j - 2]
                and text1[i - 2] == char2
            ):
                value = min(
                    value,
                    previous_previous[j - 2] + 1,
                )

            current.append(value)

        previous_previous = previous
        previous = current

    return previous[-1]


def find_fuzzy_match(
    model,
    nazwa,
    related_name="warianty_nazw",
):
    """
    Szuka istniejącego obiektu o nazwie bardzo podobnej
    do podanej nazwy.

    Wykrywa przede wszystkim prawdopodobne literówki.
    """

    nazwa_porownawcza = normalize_for_comparison(nazwa)

    if len(nazwa_porownawcza) < 4:
        return None

    kandydaci = []

    for obj in model.objects.all():
        nazwy = [obj.nazwa]

        warianty = (
            getattr(obj, related_name, None)
            if related_name is not None
            else None
        )

        if warianty is not None:
            nazwy.extend(
                wariant.nazwa
                for wariant in warianty.all()
            )

        for kandydat in nazwy:
            kandydat_porownawczy = normalize_for_comparison(
                kandydat
            )

            if kandydat_porownawczy == nazwa_porownawcza:
                continue

            distance = damerau_levenshtein_distance(
                nazwa_porownawcza,
                kandydat_porownawczy,
            )

            max_distance = 1

            if len(nazwa_porownawcza) >= 10:
                max_distance = 2

            if distance <= max_distance:
                kandydaci.append(
                    (distance, obj, kandydat)
                )

    if not kandydaci:
        return None

    kandydaci.sort(
        key=lambda item: item[0]
    )

    najlepszy = kandydaci[0]

    return najlepszy[1], najlepszy[2]

def find_fuzzy_person_match(person):
    """
    Szuka istniejącej osoby o nazwie bardzo podobnej
    do podanej osoby.

    Dla osób klasycznych porównuje osobno nazwisko i imiona.
    Dla osób jednoczłonowych porównuje nazwę.
    Kwalifikator musi być zgodny dokładnie.
    """

    kandydaci = []

    for obj in Osoba.objects.all():

        kwalifikator = person.kwalifikator or ""

        if kwalifikator != obj.kwalifikator:
            continue

        if person.nazwa:
            if not obj.nazwisko:
                distance = damerau_levenshtein_distance(
                    normalize_for_comparison(person.nazwa),
                    normalize_for_comparison(obj.imiona),
                )

                if distance <= 1:
                    kandydaci.append(
                        (distance, obj, obj.imiona)
                    )

            continue

        if not obj.nazwisko:
            continue

        nazwisko_distance = damerau_levenshtein_distance(
            normalize_for_comparison(person.nazwisko),
            normalize_for_comparison(obj.nazwisko),
        )

        imiona_distance = damerau_levenshtein_distance(
            normalize_for_comparison(person.imiona),
            normalize_for_comparison(obj.imiona),
        )

        if (
            nazwisko_distance <= 1
            and imiona_distance == 0
        ):
            kandydaci.append(
                (
                    nazwisko_distance,
                    obj,
                    obj.nazwisko,
                    "nazwisku",
                )
            )

        elif (
            nazwisko_distance == 0
            and imiona_distance <= 1
        ):
            kandydaci.append(
                (
                    imiona_distance,
                    obj,
                    obj.imiona,
                    "imieniu",
                )
            )

        elif (
            nazwisko_distance <= 1
            and imiona_distance <= 1
            and nazwisko_distance + imiona_distance <= 2
        ):
            kandydaci.append(
                (
                    nazwisko_distance + imiona_distance,
                    obj,
                    f"{obj.nazwisko}, {obj.imiona}",
                    "osobie",
                )
            )

    if not kandydaci:
        return None

    kandydaci.sort(
        key=lambda item: item[0]
    )

    najlepszy = kandydaci[0]

    return najlepszy[1], najlepszy[2], najlepszy[3]

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


def find_named_object(
    model,
    place: ParsedName,
    related_name="warianty_nazw",
):
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
            o,
            p,
            WariantNazwyTematu,
            "temat",
        ),
    )


def create_genre(genre: ParsedName):
    return create_named_object(
        model=Gatunek,
        parsed=genre,
        add_variants=lambda o, p: add_named_object_variants(
            o,
            p,
            WariantNazwyGatunku,
            "gatunek",
        ),
    )


def create_motif(motif: ParsedName):
    return create_named_object(
        model=Motyw,
        parsed=motif,
        add_variants=lambda o, p: add_named_object_variants(
            o,
            p,
            WariantNazwyMotywu,
            "motyw",
        ),
    )


def create_event(event: ParsedName):
    return create_named_object(
        model=Wydarzenie,
        parsed=event,
        add_variants=lambda o, p: add_named_object_variants(
            o,
            p,
            WariantNazwyWydarzenia,
            "wydarzenie",
        ),
    )


def create_library(library: ParsedName):
    return create_named_object(
        model=Biblioteka,
        parsed=library,
        add_variants=lambda o, p: add_named_object_variants(
            o,
            p,
            WariantNazwyBiblioteki,
            "biblioteka",
        ),
    )


def get_or_create_institution(
    institution: ParsedName,
    result=None,
):
    return get_or_create_named_object(
        model=Instytucja,
        variant_model=WariantNazwyInstytucji,
        relation_field="instytucja",
        parsed=institution,
        result=result,
        object_type="Instytucje",
    )


def get_or_create_theme(
    theme: ParsedName,
    result=None,
):
    return get_or_create_named_object(
        model=Temat,
        variant_model=WariantNazwyTematu,
        relation_field="temat",
        parsed=theme,
        result=result,
        object_type="Tematy",
    )


def get_or_create_genre(
    genre: ParsedName,
    result=None,
):
    return get_or_create_named_object(
        model=Gatunek,
        variant_model=WariantNazwyGatunku,
        relation_field="gatunek",
        parsed=genre,
        result=result,
        object_type="Gatunki",
    )


def get_or_create_motif(
    motif: ParsedName,
    result=None,
):
    return get_or_create_named_object(
        model=Motyw,
        variant_model=WariantNazwyMotywu,
        relation_field="motyw",
        parsed=motif,
        result=result,
        object_type="Motywy",
    )


def get_or_create_event(
    event: ParsedName,
    result=None,
):
    return get_or_create_named_object(
        model=Wydarzenie,
        variant_model=WariantNazwyWydarzenia,
        relation_field="wydarzenie",
        parsed=event,
        result=result,
        object_type="Wydarzenia",
    )


def get_or_create_library(
    library: ParsedName,
    result=None,
):
    return get_or_create_named_object(
        model=Biblioteka,
        variant_model=WariantNazwyBiblioteki,
        relation_field="biblioteka",
        parsed=library,
        result=result,
        object_type="Biblioteki",
    )


def add_person_variants(
    osoba: Osoba,
    person: ParsedPerson,
):
    """
    Dodaje brakujące warianty nazw osoby.
    """

    istniejące = {
        wariant.nazwa
        for wariant in osoba.warianty_nazw.all()
    }

    kolejnosc = osoba.warianty_nazw.count() + 1

    warianty = []

    for nazwisko in [
        person.nazwisko,
        *person.warianty_nazwiska,
    ]:
        if nazwisko is None:
            continue

        for imiona in [
            person.imiona,
            *person.warianty_imion,
        ]:
            if imiona is None:
                continue

            warianty.append(
                f"{nazwisko}, {imiona}"
            )

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


def add_named_object_variants(
    obj,
    parsed,
    variant_model,
    relation_field,
):
    """
    Dodaje brakujące warianty nazw obiektu nazwanego.
    """

    istniejące = {
        wariant.nazwa
        for wariant in obj.warianty_nazw.all()
    }

    kolejnosc = obj.warianty_nazw.count() + 1

    for nazwa in [
        parsed.nazwa,
        *parsed.warianty,
    ]:

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


def add_place_variants(
    miejsce: Miejsce,
    place: ParsedName,
):
    """
    Dodaje brakujące warianty nazw miejsca.
    """

    add_named_object_variants(
        obj=miejsce,
        parsed=place,
        variant_model=WariantNazwyMiejsca,
        relation_field="miejsce",
    )


def create_named_object(
    model,
    parsed,
    add_variants,
):
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
    result=None,
    object_type=None,
):
    """
    Zwraca istniejący obiekt nazwany lub tworzy nowy.
    """

    matches = find_named_object(
        model,
        parsed,
    )

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

    fuzzy_match = find_fuzzy_match(
        model=model,
        nazwa=parsed.nazwa,
    )

    if fuzzy_match is not None and result is not None:
        podobny_obj, podobna_nazwa = fuzzy_match

        result.add_warning(
            message=(
                f"Możliwa literówka w nazwie: „{parsed.nazwa}”. "
                f"Istnieje podobny obiekt: „{podobna_nazwa}”. "
                "Sprawdź poprawność danych i usuń niepoprawne obiekty."
            ),
            field=object_type,
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

    if result is not None and object_type is not None:
        result.add_created_object(object_type)

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


def get_or_create_place(
    place: ParsedName,
    result=None,
):

    
    """
    Zwraca istniejące miejsce lub tworzy nowe.
    """

    matches = find_place(place)

    if matches.count() == 1:
        miejsce = matches.first()

        add_place_variants(
            miejsce,
            place,
        )

        return miejsce

    if matches.count() > 1:
        raise ValueError(
            f"Znaleziono więcej niż jedno miejsce: {place}"
        )



    miejsce = create_place(place)

    if result is not None:
        result.add_created_object("Miejsca")

    return miejsce


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

    add_person_variants(
        osoba,
        person,
    )

    return osoba


def get_or_create_person(
    person: ParsedPerson,
    result=None,
):
    """
    Zwraca istniejącą osobę lub tworzy nową.
    """

    matches = find_person(person)

    if matches.count() == 1:
        osoba = matches.first()

        add_person_variants(
            osoba,
            person,
        )

        return osoba

    if matches.count() > 1:
        raise ValueError(
            f"Znaleziono więcej niż jedną osobę: {person}"
        )



    osoba = create_person(person)

    if result is not None:
        result.add_created_object("Osoby")

    return osoba


def get_or_create_dictionary_object(
    model,
    parsed,
    result=None,
    object_type=None,
    fuzzy=False,
):
    """
    Zwraca obiekt słownikowy lub tworzy nowy.
    """


    obj, created = model.objects.get_or_create(
        nazwa=parsed.nazwa,
    )

    if created and result is not None and object_type is not None:
        result.add_created_object(object_type)

    return obj


def get_or_create_language(
    language,
    result=None,
):
    return get_or_create_dictionary_object(
        Jezyk,
        language,
        result=result,
        object_type="Języki",
        fuzzy=True,
    )


def get_or_create_format(
    format_,
    result=None,
):
    return get_or_create_dictionary_object(
        Format,
        format_,
        result=result,
        object_type="Formaty",
    )


def get_or_create_font(
    font,
    result=None,
):
    return get_or_create_dictionary_object(
        Czcionka,
        font,
        result=result,
        object_type="Czcionki",
    )
