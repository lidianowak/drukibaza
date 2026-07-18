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
                import_id=record.get("id_importu"),
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
                import_id=specimen.get("id_importu"),
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
                import_id=attachment.get("id_importu"),
            )
            valid = False

        if not attachment.get("sekcja"):
            self.result.add_error(
                message="Nie wybrano sekcji załącznika.",
                sheet="Załączniki",
                row=row,
                field="Sekcja",
                import_id=attachment.get("id_importu"),
            )
            valid = False

        return valid