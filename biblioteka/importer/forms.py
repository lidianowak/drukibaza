from django import forms


class ImportForm(forms.Form):
    """
    Import gotowego formularza BiDO (.xlsx).
    """

    plik = forms.FileField(
        label="Formularz importu (.xlsx)",
        widget=forms.ClearableFileInput(
            attrs={
                "accept": ".xlsx",
            }
        ),
    )

    def clean_plik(self):

        plik = self.cleaned_data["plik"]

        if not plik.name.lower().endswith(".xlsx"):
            raise forms.ValidationError(
                "Wybierz plik programu Excel (*.xlsx)."
            )

        return plik


class CsvImportForm(forms.Form):
    """
    Konwersja pliku CSV do formularza BiDO.
    """

    plik = forms.FileField(
        label="Plik CSV",
    )