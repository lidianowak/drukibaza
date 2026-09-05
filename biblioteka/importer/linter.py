"""
linter.py

Kontrola jakości danych w formularzu importu BiDO.
"""

import re


def normalize_spaces(text):
    """
    Usuwa spacje z początku i końca tekstu
    oraz redukuje wielokrotne spacje do jednej.
    """

    if not isinstance(text, str):
        return text

    return re.sub(r"\s+", " ", text.strip())


def check_brackets(text, opening, closing):
    """
    Sprawdza, czy nawiasy są sparowane i występują
    we właściwej kolejności.
    """

    if not text:
        return None

    depth = 0

    for char in text:

        if char == opening:
            depth += 1

        elif char == closing:

            if depth == 0:
                return (
                    f"Nieprawidłowa kolejność nawiasów "
                    f"„{opening}{closing}”."
                )

            depth -= 1

    if depth > 0:
        return (
            f"Niesparowany nawias "
            f"„{opening}{closing}”."
        )

    return None


def check_list_separators(text):
    """
    Sprawdza, czy lista rozdzielana średnikami
    nie zawiera pustych elementów.
    """

    if not text:
        return None

    parts = text.split(";")

    if len(parts) > 1 and any(not part.strip() for part in parts):
        return (
            "Pusty element listy rozdzielanej "
            "średnikiem „;”."
        )

    return None


def check_variant_separators(text):
    """
    Sprawdza, czy zapis wariantów rozdzielanych średnikiem
    wewnątrz [] nie zawiera pustych elementów.
    """

    if not text:
        return None

    matches = re.findall(r"\[(.*?)\]", text)

    for content in matches:

        variants = content.split(";")

        if len(variants) > 1 and any(
            not variant.strip()
            for variant in variants
        ):
            return (
                "Pusty element wśród wariantów "
                "rozdzielanych średnikiem „;”."
            )

    return None

def check_person_commas(text):
    """
    Sprawdza, czy w polu osób nie użyto przecinka
    jako potencjalnego separatora kolejnej osoby.

    Poprawny zapis wielu osób:
    "Nowak, Jan; Domański, Juliusz"

    Podejrzany zapis:
    "Nowak, Jan, Domański, Juliusz"
    """

    if not text:
        return None

    people = text.split(";")

    for person in people:

        if person.count(",") > 1:
            return (
                "Podejrzany zapis osoby: "
                "więcej niż jeden przecinek. "
                "Jeśli chodzi o kolejną osobę, użyj średnika „;”."
            )

    return None


def check_person_completeness(person):
    """
    Sprawdza, czy osoba może mieć niepełne dane.

    Osoby zapisane w formacie "Nazwisko, Imię" są uznawane
    za kompletne tylko wtedy, gdy obie części są podane.
    Osoby jednoczłonowe otrzymują ostrzeżenie, chyba że
    mają jawnie podany kwalifikator.
    """

    if person.nazwisko is not None:

        if not person.nazwisko or not person.imiona:
            return "Możliwie niepełne dane osoby."

        return None

    if person.nazwa is not None:

        if person.kwalifikator:
            return None

        return (
            f"Możliwie niepełne dane osoby: "
            f"„{person.nazwa}”."
        )

    return None


def check_year(year):
    """
    Sprawdza, czy rok wydania ma cztery cyfry.
    """

    if year is None or year == "":
        return None

    try:
        value = int(year)

    except (TypeError, ValueError):
        return None

    if value < 1000 or value > 9999:
        return "Rok wydania nie jest zapisany jako liczba czterocyfrowa."

    return None


PERSON_FIELDS = {
    "autorzy",
    "drukarze",
    "adresaci_dedykacji",
    "powiazane_osoby",
}


OBJECT_FIELDS = {
    "miejsce_wydania",
    "powiazane_instytucje",
    "powiazane_miejsca",
    "tematy",
    "gatunki",
    "motywy",
    "wydarzenia",
}


def lint_record(mapped):
    """
    Wykonuje linting jednego zmapowanego rekordu.

    Zwraca listę ostrzeżeń.
    """

    warnings = []

    # ---------- Pola obiektowe ----------

    for field_name in OBJECT_FIELDS:

        text = mapped.get(field_name)

        if not text:
            continue

        warning = check_brackets(text, "[", "]")

        if warning:
            warnings.append(
                (field_name, warning)
            )

        warning = check_brackets(text, "(", ")")

        if warning:
            warnings.append(
                (field_name, warning)
            )

        warning = check_variant_separators(text)

        if warning:
            warnings.append(
                (field_name, warning)
            )

        warning = check_list_separators(text)

        if warning:
            warnings.append(
                (field_name, warning)
            )

    # ---------- Osoby ----------

    for field_name in PERSON_FIELDS:

        text = mapped.get(field_name)

        if not text:
            continue

        warning = check_person_commas(text)

        if warning:
            warnings.append(
                (field_name, warning)
            )

        warning = check_list_separators(text)

        if warning:
            warnings.append(
                (field_name, warning)
            )

        warning = check_variant_separators(text)

        if warning:
            warnings.append(
                (field_name, warning)
            )

        warning = check_brackets(text, "[", "]")

        if warning:
            warnings.append(
                (field_name, warning)
            )

        warning = check_brackets(text, "(", ")")

        if warning:
            warnings.append(
                (field_name, warning)
            )

        from biblioteka.importer.object_parser import parse_persons

        persons = parse_persons(text)

        for person in persons:

            warning = check_person_completeness(person)

            if warning:
                warnings.append(
                    (field_name, warning)
                )

    # ---------- Pozostałe listy słownikowe ----------

    for field_name in {
        "jezyki",
        "czcionki",
    }:

        text = mapped.get(field_name)

        if not text:
            continue

        warning = check_list_separators(text)

        if warning:
            warnings.append(
                (field_name, warning)
            )

    # ---------- Rok wydania ----------

    warning = check_year(
        mapped.get("rok_wydania")
    )

    if warning:
        warnings.append(
            ("rok_wydania", warning)
        )

    return warnings