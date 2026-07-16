from django import forms


class ImportForm(forms.Form):
    """
    Import gotowego formularza BiDO (.xlsx).
    """

    plik = forms.FileField(
        label="Formularz importu (.xlsx)",
    )


class CsvImportForm(forms.Form):
    """
    Konwersja pliku CSV do formularza BiDO.
    """

    plik = forms.FileField(
        label="Plik CSV",
    )