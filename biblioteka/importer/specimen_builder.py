"""
specimen_builder.py

Tworzenie obiektów Egzemplarz.
"""

from biblioteka.models import Egzemplarz
from biblioteka.importer.object_parser import parse_named_objects
from biblioteka.importer.builder import get_or_create_library


def create_specimen(
    rekord,
    mapped,
):
    """
    Tworzy egzemplarz rekordu.
    """

    biblioteki = parse_named_objects(
        mapped.get("biblioteka")
    )

    if not biblioteki:
        return

    biblioteka = get_or_create_library(
        biblioteki[0]
    )

    kolejnosc = rekord.egzemplarze.count() + 1

    Egzemplarz.objects.create(
        rekord=rekord,
        biblioteka=biblioteka,
        kolejnosc=kolejnosc,
        sygnatura=mapped.get("sygnatura") or "",
        katalog_biblioteczny=mapped.get("katalog_biblioteczny") or "",
        proweniencja=mapped.get("proweniencja") or "",
        oprawa=mapped.get("oprawa") or "",
        marginalia=mapped.get("marginalia") or "",
    )