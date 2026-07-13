"""
object_parser.py

Parsowanie obiektów zapisanych
w formularzu importu BiDO.
"""

import re

from dataclasses import dataclass, field

@dataclass
class ParsedName:

    nazwa: str

    warianty: list[str] = field(default_factory=list)

@dataclass
class ParsedPerson:

    nazwisko: str | None = None
    imiona: str | None = None

    # dla osób typu "Bartłomiej (z Wrześni)"
    nazwa: str | None = None

    warianty_nazwiska: list[str] = field(default_factory=list)
    warianty_imion: list[str] = field(default_factory=list)
    warianty_nazwy: list[str] = field(default_factory=list)

    kwalifikator: str | None = None


def split_variants(text):
    """
    Rozdziela nazwę główną i warianty.

    Przykład:

    Kochanowski [Cochanovius|Cochanovsky]

    →

    (
        "Kochanowski",
        ["Cochanovius", "Cochanovsky"]
    )
    """

    if not text:
        return "", []

    match = re.match(r"^(.*?)\s*\[(.*?)\]\s*$", text)

    if not match:
        return text.strip(), []

    main_name = match.group(1).strip()

    variants = [
        v.strip()
        for v in match.group(2).split("|")
        if v.strip()
    ]

    return main_name, variants

def split_qualifier(text):
    """
    Rozdziela nazwę i kwalifikator.

    Przykład:

    Jan (starszy)

    →

    ("Jan", "starszy")
    """

    if not text:
        return "", None

    match = re.match(r"^(.*?)\s*\((.*?)\)\s*$", text)

    if not match:
        return text.strip(), None

    value = match.group(1).strip()
    qualifier = match.group(2).strip()

    return value, qualifier

def split_list(text):
    """
    Rozdziela zapis wielu osób.

    Separator: średnik.
    """

    if not text:
        return []

    return [
        person.strip()
        for person in text.split(";")
        if person.strip()
    ]

def split_name(text):
    """
    Rozpoznaje dwa zapisy:

    Nazwisko, Imię

    lub

    Nazwa
    """

    if not text:
        return None, None, ""

    parts = text.split(",", 1)

    if len(parts) == 2:
        return (
            parts[0].strip(),
            parts[1].strip(),
            None,
        )

    return (
        None,
        None,
        text.strip(),
    )

def parse_named_objects(text):
    """
    Parsuje obiekty zapisane jako:

    Nazwa [wariant1|wariant2];
    Nazwa2
    """

    if not text:
        return []

    objects = []

    for item in split_list(text):

        name, variants = split_variants(item)

        objects.append(
            ParsedName(
                nazwa=name,
                warianty=variants,
            )
        )

    return objects

def parse_persons(text):
    """
    Parsuje zapis osób z formularza BiDO.

    Zwraca listę ParsedPerson.
    """

    if not text:
        return []

    people = []

    for person_text in split_list(text):

        surname_part, given_part, single_name = split_name(person_text)

        # ----------------------------
        # Osoba jednoczłonowa
        # np. "Bartłomiej (z Wrześni)"
        # ----------------------------
        if single_name is not None:

            single_name, qualifier = split_qualifier(single_name)

            name, variants = split_variants(single_name)

            people.append(
                ParsedPerson(
                    nazwa=name,
                    warianty_nazwy=variants,
                    kwalifikator=qualifier,
                )
            )

            continue

        # ----------------------------
        # Klasyczny zapis:
        # Nazwisko, Imię
        # ----------------------------

        surname, surname_variants = split_variants(surname_part)

        given_part, qualifier = split_qualifier(given_part)

        given_names, given_variants = split_variants(given_part)

        people.append(
            ParsedPerson(
                nazwisko=surname,
                imiona=given_names,
                warianty_nazwiska=surname_variants,
                warianty_imion=given_variants,
                kwalifikator=qualifier,
            )
        )

    return people

def parse_places(text):
    """
    Parsuje zapis miejsc z formularza BiDO.

    Zwraca listę ParsedPlace.
    """

    if not text:
        return []

    places = []

    for place_text in split_list(text):

        nazwa, warianty = split_variants(place_text)

        places.append(
            ParsedName(
                nazwa=nazwa,
                warianty=warianty,
            )
        )

    return places


def parse_institutions(text):
    """
    Parsuje zapis instytucji z formularza BiDO.
    """

    return parse_named_objects(text)

def parse_themes(text):
    """
    Parsuje zapis tematów z formularza BiDO.
    """
    return parse_named_objects(text)


def parse_genres(text):
    """
    Parsuje zapis gatunków z formularza BiDO.
    """
    return parse_named_objects(text)


def parse_motifs(text):
    """
    Parsuje zapis motywów z formularza BiDO.
    """
    return parse_named_objects(text)


def parse_events(text):
    """
    Parsuje zapis wydarzeń z formularza BiDO.
    """
    return parse_named_objects(text)


def parse_libraries(text):
    """
    Parsuje zapis bibliotek z formularza BiDO.
    """
    return parse_named_objects(text)