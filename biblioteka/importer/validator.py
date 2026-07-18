from .result import ImportResult
from biblioteka.models import Rekord


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

        if (
            attachment.get("sekcja") == "marginalia"
            and not attachment.get("sygnatura")
        ):
            self.result.add_error(
                message="Załącznik w sekcji „marginalia” wymaga wskazania sygnatury egzemplarza.",
                sheet="Załączniki",
                row=row,
                field="Sygnatura egzemplarza",
                import_id=attachment.get("id_importu"),
            )
            valid = False

        return valid
    
    def validate_relations(
        self,
        record: dict,
        import_ids: set,
        row: int,
    ) -> bool:
        
        """
        Sprawdza, czy wszystkie rekordy wskazane
        w wariantach i wznowieniach istnieją.
        """

        valid = True

        for field, label in (
            ("warianty", "Warianty"),
            ("wznowienia", "Wznowienia"),
        ):

            values = record.get(field)

            if not values:
                continue

            for value in values.split(";"):

                value = value.strip()

                if not value:
                    continue

                # Opis bibliograficzny pomijamy
                if value.startswith("{") and value.endswith("}"):
                    continue

                # Rekord importowany w tym samym pliku
                if value.startswith("R"):

                    if value not in import_ids:

                        self.result.add_error(
                            message=f"Nie znaleziono rekordu {value}.",
                            sheet="Rekordy",
                            row=row,
                            field=label,
                            import_id=record.get("id_importu"),
                        )

                        valid = False

                else:

                    if not Rekord.objects.filter(
                        identyfikator=value
                    ).exists():

                        self.result.add_error(
                            message=f"Nie znaleziono rekordu {value}.",
                            sheet="Rekordy",
                            row=row,
                            field=label,
                            import_id=record.get("id_importu"),
                        )

                        valid = False

        return valid