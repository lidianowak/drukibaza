from django import forms

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
)


class RekordForm(forms.ModelForm):
    autor = forms.ModelMultipleChoiceField(
        queryset=Osoba.objects.all(),
        required=False,
        label="Autor"
    )

    drukarz = forms.ModelMultipleChoiceField(
        queryset=Osoba.objects.all(),
        required=False,
        label="Drukarz"
    )

    adresat_dedykacji = forms.ModelMultipleChoiceField(
        queryset=Osoba.objects.all(),
        required=False,
        label="Adresat dedykacji"
    )

    powiazane_osoby = forms.ModelMultipleChoiceField(
        queryset=Osoba.objects.all(),
        required=False,
        label="Powiązane osoby"
    )

    miejsce_wydania = forms.ModelMultipleChoiceField(
        queryset=Miejsce.objects.all(),
        required=False,
        label="Miejsce wydania"
    )

    powiazane_miejsca = forms.ModelMultipleChoiceField(
        queryset=Miejsce.objects.all(),
        required=False,
        label="Powiązane miejsca"
    )

    instytucje = forms.ModelMultipleChoiceField(
        queryset=Instytucja.objects.all(),
        required=False,
        label="Powiązane instytucje"
    )

    tematy = forms.ModelMultipleChoiceField(
        queryset=Temat.objects.all(),
        required=False,
        label="Temat"
    )

    gatunki = forms.ModelMultipleChoiceField(
        queryset=Gatunek.objects.all(),
        required=False,
        label="Gatunek"
    )

    wydarzenia = forms.ModelMultipleChoiceField(
        queryset=Wydarzenie.objects.all(),
        required=False,
        label="Powiązane wydarzenie"
    )

    motywy = forms.ModelMultipleChoiceField(
        queryset=Motyw.objects.all(),
        required=False,
        label="Motywy"
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

        return rekord

    class Meta:
        model = Rekord
        fields = "__all__"