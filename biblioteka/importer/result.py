from dataclasses import dataclass, field

@dataclass
class ImportErrorItem:

    message: str

    sheet: str | None = None
    row: int | None = None
    field: str | None = None

@dataclass
class ImportResult:

    success: bool = True

    records: int = 0
    specimens: int = 0
    attachments: int = 0

    errors: list[ImportErrorItem] = field(default_factory=list)
    warnings: list = field(default_factory=list)