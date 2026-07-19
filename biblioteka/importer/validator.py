from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

from biblioteka.models import Rekord

from .result import ImportResult


class ImportValidator:

    def __init__(self, result: ImportResult):
        self.result = result
        self.url_validator = URLValidator()

    def validate_record(self, record: dict, row: int) -> bool:
        """
        Waliduje pojedynczy rekord.
        """

        valid = True

        # ---------- Pola obowiązkowe ----------

        if not record.get("tytul_skrocony"):
            self.result.add_error(
                message="Brak tytułu skróconego.",
                sheet="Rekordy",
                row=row,
                field="Tytuł skrócony",
                import_id=record.get("id_importu"),
            )
            valid = False

        # ---------- Linki do digitalizacji ----------

        urls = record.get("linki_digitalizacji")

        if urls:

            for url in urls.split(";"):

                url = url.strip()

                if not url:
                    continue

                try:
                    self.url_validator(url)

                except ValidationError:

                    self.result.add_error(
                        message=f"Niepoprawny adres URL: {url}",
                        sheet="Rekordy",
                        row=row,
                        field="Linki do digitalizacji",
                        import_id=record.get("id_importu"),
                    )

                    valid = False

        return valid

    def validate_specimen(self, specimen: dict, row: int) -> bool:

        valid = True

        # ---------- Pola obowiązkowe ----------

        if not specimen.get("biblioteka"):
            self.result.add_error(
                message="Brak biblioteki.",
                sheet="Egzemplarze",
                row=row,
                field="Biblioteka",
                import_id=specimen.get("id_importu"),
            )
            valid = False

        # ---------- Link do katalogu ----------

        katalog = specimen.get("katalog_biblioteczny")

        if katalog:

            try:
                self.url_validator(katalog)

            except ValidationError:

                self.result.add_error(
                    message=f"Niepoprawny adres URL: {katalog}",
                    sheet="Egzemplarze",
                    row=row,
                    field="Link do katalogu",
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
                message=(
                    "Załącznik w sekcji „marginalia” "
                    "wymaga wskazania sygnatury egzemplarza."
                ),
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