"""
report.py

Tworzy raport z walidacji i importu.
"""


class ImportReport:

    def __init__(self):
        self.errors = []
        self.warnings = []
        self.created = {}
        self.updated = {}

    def add_error(self, message):
        self.errors.append(message)

    def add_warning(self, message):
        self.warnings.append(message)