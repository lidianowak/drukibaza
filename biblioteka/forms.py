from django import forms

from dal import autocomplete

from .models import (
    Rekord,
    Osoba,
    Miejsce,
    Instytucja,
    Temat,
    Gatunek,
    Wydarzenie,
    Motyw,
    RelacjaOsoby,
    RelacjaMiejsca,
    RelacjaInstytucji,
    RelacjaTematu,
    RelacjaGatunku,
    RelacjaWydarzenia,
    RelacjaMotywu,
    RelacjaRekordu,
    Tag,
)


class RekordForm(forms.ModelForm):
    autor = forms.ModelMultipleChoiceField(
        queryset=Osoba.objects.all(),
        required=False,
        label="Autor",
        widget=autocomplete.ModelSelect2Multiple(
            url="osoba-autocomplete",
        ),
    )

    drukarz = forms.ModelMultipleChoiceField(
        queryset=Osoba.objects.all(),
        required=False,
        label="Drukarz",
        widget=autocomplete.ModelSelect2Multiple(
            url="osoba-autocomplete",
        ),
    )

    adresat_dedykacji = forms.ModelMultipleChoiceField(
        queryset=Osoba.objects.all(),
        required=False,
        label="Adresat dedykacji",
        widget=autocomplete.ModelSelect2Multiple(
            url="osoba-autocomplete",
        ),
    )

    powiazane_osoby = forms.ModelMultipleChoiceField(
        queryset=Osoba.objects.all(),
        required=False,
        label="Powiązane osoby",
        widget=autocomplete.ModelSelect2Multiple(
            url="osoba-autocomplete",
        ),
    )

    miejsce_wydania = forms.ModelMultipleChoiceField(
        queryset=Miejsce.objects.all(),
        required=False,
        label="Miejsce wydania",
        widget=autocomplete.ModelSelect2Multiple(
            url="miejsce-autocomplete",
        ),
    )

    powiazane_miejsca = forms.ModelMultipleChoiceField(
        queryset=Miejsce.objects.all(),
        required=False,
        label="Powiązane miejsca",
        widget=autocomplete.ModelSelect2Multiple(
            url="miejsce-autocomplete",
        ),
    )

    instytucje = forms.ModelMultipleChoiceField(
        queryset=Instytucja.objects.all(),
        required=False,
        label="Powiązane instytucje",
        widget=autocomplete.ModelSelect2Multiple(
            url="instytucja-autocomplete",
        ),
    )

    tematy = forms.ModelMultipleChoiceField(
        queryset=Temat.objects.all(),
        required=False,
        label="Temat",
        widget=autocomplete.ModelSelect2Multiple(
            url="temat-autocomplete",
        ),
    )

    gatunki = forms.ModelMultipleChoiceField(
        queryset=Gatunek.objects.all(),
        required=False,
        label="Gatunek",
        widget=autocomplete.ModelSelect2Multiple(
            url="gatunek-autocomplete",
        ),
    )

    wydarzenia = forms.ModelMultipleChoiceField(
        queryset=Wydarzenie.objects.all(),
        required=False,
        label="Powiązane wydarzenie",
        widget=autocomplete.ModelSelect2Multiple(
            url="wydarzenie-autocomplete",
        ),
    )

    motywy = forms.ModelMultipleChoiceField(
        queryset=Motyw.objects.all(),
        required=False,
        label="Motywy",
        widget=autocomplete.ModelSelect2Multiple(
            url="motyw-autocomplete",
        ),
    )

    tagi = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        label="Tagi",
        widget=autocomplete.ModelSelect2Multiple(
            url="tag-autocomplete",
        ),
    )

    warianty = forms.ModelMultipleChoiceField(
        queryset=Rekord.objects.all(),
        required=False,
        label="Warianty",
        widget=autocomplete.ModelSelect2Multiple(
            url="rekord-autocomplete",
        ),
    )

    wznowienia = forms.ModelMultipleChoiceField(
        queryset=Rekord.objects.all(),
        required=False,
        label="Wznowienia",
        widget=autocomplete.ModelSelect2Multiple(
            url="rekord-autocomplete",
        ),
    )


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    

        if self.instance.pk:

            autorzy = RelacjaOsoby.objects.filter(
                rekord=self.instance,
                typ="autor"
            )

            self.fields["autor"].initial = [
                r.osoba for r in autorzy
            ]

            drukarze = RelacjaOsoby.objects.filter(
                rekord=self.instance,
                typ="drukarz"
            )

            self.fields["drukarz"].initial = [
                r.osoba for r in drukarze
            ]

            adresaci = RelacjaOsoby.objects.filter(
                rekord=self.instance,
                typ="adresat"
            )

            self.fields["adresat_dedykacji"].initial = [
                r.osoba for r in adresaci
            ]

            powiazane = RelacjaOsoby.objects.filter(
                rekord=self.instance,
                typ="powiazana"
            )

            self.fields["powiazane_osoby"].initial = [
                r.osoba for r in powiazane
            ]

            miejsca_wydania = RelacjaMiejsca.objects.filter(
                rekord=self.instance,
                typ="wydania"
            )

            self.fields["miejsce_wydania"].initial = [
                r.miejsce for r in miejsca_wydania
            ]

            powiazane_miejsca = RelacjaMiejsca.objects.filter(
                rekord=self.instance,
                typ="powiazane"
            )

            self.fields["powiazane_miejsca"].initial = [
                r.miejsce for r in powiazane_miejsca
            ]

            instytucje = RelacjaInstytucji.objects.filter(
                rekord=self.instance
            )

            self.fields["instytucje"].initial = [
                r.instytucja for r in instytucje
            ]

            tematy = RelacjaTematu.objects.filter(
                rekord=self.instance
            )

            self.fields["tematy"].initial = [
                r.temat for r in tematy
            ]

            gatunki = RelacjaGatunku.objects.filter(
                rekord=self.instance
            )

            self.fields["gatunki"].initial = [
                r.gatunek for r in gatunki
            ]

            wydarzenia = RelacjaWydarzenia.objects.filter(
                rekord=self.instance
            )

            self.fields["wydarzenia"].initial = [
                r.wydarzenie for r in wydarzenia
            ]

            motywy = RelacjaMotywu.objects.filter(
                rekord=self.instance
            )

            self.fields["motywy"].initial = [
                r.motyw for r in motywy
            ]

            warianty = RelacjaRekordu.objects.filter(
                rekord=self.instance,
                typ="wariant"
            )

            self.fields["warianty"].initial = [
                r.rekord_powiazany for r in warianty
            ]

            wznowienia = RelacjaRekordu.objects.filter(
                rekord=self.instance,
                typ="wznowienie"
            )

            self.fields["wznowienia"].initial = [
                r.rekord_powiazany for r in wznowienia
            ]

    def save(self, commit=True):
        rekord = super().save(commit)

        # Usuwamy dotychczasowe relacje osób
        RelacjaOsoby.objects.filter(rekord=rekord).delete()

        # Autorzy
        for osoba in self.cleaned_data["autor"]:
            RelacjaOsoby.objects.create(
                rekord=rekord,
                osoba=osoba,
                typ="autor"
            )

        # Drukarze
        for osoba in self.cleaned_data["drukarz"]:
            RelacjaOsoby.objects.create(
                rekord=rekord,
                osoba=osoba,
                typ="drukarz"
            )

        # Adresaci dedykacji
        for osoba in self.cleaned_data["adresat_dedykacji"]:
            RelacjaOsoby.objects.create(
                rekord=rekord,
                osoba=osoba,
                typ="adresat"
            )

        # Powiązane osoby
        for osoba in self.cleaned_data["powiazane_osoby"]:
            RelacjaOsoby.objects.create(
                rekord=rekord,
                osoba=osoba,
                typ="powiazana"
            )

        # Usuwamy dotychczasowe relacje miejsc
        RelacjaMiejsca.objects.filter(rekord=rekord).delete()

        # Miejsca wydania
        for miejsce in self.cleaned_data["miejsce_wydania"]:
            RelacjaMiejsca.objects.create(
                rekord=rekord,
                miejsce=miejsce,
                typ="wydania"
            )

        # Powiązane miejsca
        for miejsce in self.cleaned_data["powiazane_miejsca"]:
            RelacjaMiejsca.objects.create(
                rekord=rekord,
                miejsce=miejsce,
                typ="powiazane"
            )  

                # Instytucje
        RelacjaInstytucji.objects.filter(rekord=rekord).delete()

        for instytucja in self.cleaned_data["instytucje"]:
            RelacjaInstytucji.objects.create(
                rekord=rekord,
                instytucja=instytucja
            )

        # Tematy
        RelacjaTematu.objects.filter(rekord=rekord).delete()

        for temat in self.cleaned_data["tematy"]:
            RelacjaTematu.objects.create(
                rekord=rekord,
                temat=temat
            )

        # Gatunki
        RelacjaGatunku.objects.filter(rekord=rekord).delete()

        for gatunek in self.cleaned_data["gatunki"]:
            RelacjaGatunku.objects.create(
                rekord=rekord,
                gatunek=gatunek
            )

        # Wydarzenia
        RelacjaWydarzenia.objects.filter(rekord=rekord).delete()

        for wydarzenie in self.cleaned_data["wydarzenia"]:
            RelacjaWydarzenia.objects.create(
                rekord=rekord,
                wydarzenie=wydarzenie
            )

        # Motywy
        RelacjaMotywu.objects.filter(rekord=rekord).delete()

        for motyw in self.cleaned_data["motywy"]:
            RelacjaMotywu.objects.create(
                rekord=rekord,
                motyw=motyw
            )  

                # Warianty i wznowienia
        RelacjaRekordu.objects.filter(rekord=rekord).delete()

        for rekord_powiazany in self.cleaned_data["warianty"]:
            RelacjaRekordu.objects.create(
                rekord=rekord,
                rekord_powiazany=rekord_powiazany,
                typ="wariant"
            )

        for rekord_powiazany in self.cleaned_data["wznowienia"]:
            RelacjaRekordu.objects.create(
                rekord=rekord,
                rekord_powiazany=rekord_powiazany,
                typ="wznowienie"
            )

        return rekord

    class Meta:
        model = Rekord
        fields = "__all__"