from dataclasses import dataclass, field


@dataclass
class ImportErrorItem:

    message: str

    sheet: str | None = None
    row: int | None = None
    field: str | None = None
    import_id: str | None = None


@dataclass
class ImportResult:

    success: bool = True

    records: int = 0
    specimens: int = 0
    attachments: int = 0

    errors: list[ImportErrorItem] = field(default_factory=list)
    warnings: list[ImportErrorItem] = field(default_factory=list)

    def add_error(
        self,
        message,
        sheet=None,
        row=None,
        field=None,
        import_id=None,
    ):
        self.errors.append(
            ImportErrorItem(
                message=message,
                sheet=sheet,
                row=row,
                field=field,
                import_id=import_id,
            )
        )
        self.success = False

    def add_warning(
        self,
        message,
        sheet=None,
        row=None,
        field=None,
        import_id=None,
    ):
        self.warnings.append(
            ImportErrorItem(
                message=message,
                sheet=sheet,
                row=row,
                field=field,
                import_id=import_id,
            )
        )