"""
exceptions.py

Wyjątki używane przez importer.
"""


class ImportError(Exception):
    """Błąd importu."""


class ValidationError(Exception):
    """Błąd walidacji."""