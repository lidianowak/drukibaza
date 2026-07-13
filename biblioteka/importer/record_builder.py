"""
record_builder.py

Tworzenie obiektu Rekord
na podstawie danych z formularza importu.
"""

from biblioteka.models import Rekord


def create_record(mapped):
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
        status_opracowania=mapped.get("status_opracowania") or "do_opracowania",
    )


    return rekord