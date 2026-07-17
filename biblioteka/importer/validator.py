from .result import ImportResult


class ImportValidator:

    def __init__(self, result: ImportResult):
        self.result = result

    def validate_record(self, record: dict, row: int) -> bool:
        """
        Waliduje pojedynczy rekord.
        Zwraca True, jeśli rekord może zostać utworzony.
        Zwraca False, jeśli zawiera błędy krytyczne.
        """

        valid = True

        # Tytuł skrócony jest polem obowiązkowym
        if not record.get("tytul_skrocony"):
            self.result.add_error(
                message="Brak tytułu skróconego.",
                sheet="Rekordy",
                row=row,
                field="Tytuł skrócony",
            )
            valid = False

        return valid

    def validate_specimen(self, specimen: dict, row: int) -> bool:

        valid = True

        if not specimen.get("biblioteka"):
            self.result.add_error(
                message="Brak biblioteki.",
                sheet="Egzemplarze",
                row=row,
                field="Biblioteka",
            )
            valid = False

        return valid

    def validate_attachment(self, attachment: dict, row: int) -> bool:

        valid = True

        if not attachment.get("sciezka"):
            self.result.add_error(
                message="Brak ścieżki pliku.",
                sheet="Załączniki",
                row=row,
                field="Ścieżka pliku",
            )
            valid = False

        return valid