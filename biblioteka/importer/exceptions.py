"""
exceptions.py

Wyjątki używane przez importer.
"""


class ImportError(Exception):
    """Błąd importu."""


class ValidationError(Exception):
    """Błąd walidacji."""

class ImportValidationError(Exception):

    def __init__(self, result):
        self.result = result

        super().__init__(
            "Import nie powiódł się z powodu krytycznych błędów walidacji! Sprawdź raport, popraw arkusz i załaduj go ponownie."
        )