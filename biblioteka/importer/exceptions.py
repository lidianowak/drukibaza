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
            "Import zawiera błędy walidacji."
        )