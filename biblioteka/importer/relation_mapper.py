"""
relation_mapper.py

Mapowanie relacji między rekordami.
"""

def map_relations(mapped):
    """
    Zwraca dane potrzebne do utworzenia relacji.
    """

    return {
        "warianty": mapped.get("warianty"),
        "wznowienia": mapped.get("wznowienia"),
    }

