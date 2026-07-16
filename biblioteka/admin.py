from django.contrib import admin
from django.forms.models import BaseInlineFormSet
from django.core.exceptions import ValidationError

from .models import (
    Jezyk,
    Format,
    Czcionka,

    Osoba,
    WariantNazwyOsoby,

    Miejsce,
    WariantNazwyMiejsca,

    Instytucja,
    WariantNazwyInstytucji,

    Biblioteka,
    WariantNazwyBiblioteki,

    Wydarzenie,
    WariantNazwyWydarzenia,

    Gatunek,
    WariantNazwyGatunku,

    Motyw,
    WariantNazwyMotywu,

    Temat,
    WariantNazwyTematu,

    Rekord,
    WersjaZdigitalizowana,

    RelacjaRekordu,
    RelacjaOsoby,
    RelacjaMiejsca,
    RelacjaInstytucji,
    RelacjaTematu,
    RelacjaGatunku,
    RelacjaWydarzenia,
    RelacjaMotywu,

    Egzemplarz,
    OpracowanieRekordu,
    Tag,
    Zalacznik,

    ImportDanych,
)

from .forms import RekordForm

from django import forms



# ==========================================================
# Rejestracja prostych słowników
# ==========================================================

MODELE = [
    Jezyk,
    Format,
    Czcionka,
]

for model in MODELE:
    admin.site.register(model)


# ==========================================================
# Inline
# ==========================================================

class WersjaZdigitalizowanaInline(admin.TabularInline):
    model = WersjaZdigitalizowana
    extra = 0


class EgzemplarzInline(admin.StackedInline):
    model = Egzemplarz
    extra = 0
    autocomplete_fields = ["biblioteka"]

class RekordZalacznikForm(forms.ModelForm):

    class Meta:
        model = Zalacznik
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["sekcja"].choices = [
            c
            for c in Zalacznik.SEKCJE
            if c[0] != "marginalia"
        ]


class EgzemplarzZalacznikForm(forms.ModelForm):

    class Meta:
        model = Zalacznik
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["sekcja"].choices = [
            ("marginalia", "Marginalia")
        ]

class ZalacznikInlineFormSet(BaseInlineFormSet):

    def clean(self):
        super().clean()

        for form in self.forms:

            if not hasattr(form, "cleaned_data"):
                continue

            if form.cleaned_data.get("DELETE"):
                continue

            sekcja = form.cleaned_data.get("sekcja")
            egzemplarz = form.cleaned_data.get("egzemplarz")

            if sekcja == "marginalia" and not egzemplarz:
                raise ValidationError(
                    "Załączniki do marginaliów wymagają wskazania egzemplarza."
                )

            if sekcja != "marginalia" and egzemplarz:
                raise ValidationError(
                    "Egzemplarz można wskazać wyłącznie dla załączników do marginaliów."
                )


class RekordZalacznikInline(admin.TabularInline):
    model = Zalacznik
    fk_name = "rekord"
    form = RekordZalacznikForm
    formset = ZalacznikInlineFormSet
    extra = 0

    fields = [
        "sekcja",
        "egzemplarz",
        "nazwa_wyswietlana",
        "opis",
        "plik",
        "kolejnosc",
    ]


class EgzemplarzZalacznikInline(admin.TabularInline):
    model = Zalacznik
    fk_name = "egzemplarz"
    form = EgzemplarzZalacznikForm
    formset = ZalacznikInlineFormSet
    extra = 0

    fields = [
        "sekcja",
        "nazwa_wyswietlana",
        "opis",
        "plik",
        "kolejnosc",
    ]


class OpracowanieRekorduInline(admin.StackedInline):
    model = OpracowanieRekordu
    extra = 0
    autocomplete_fields = ["uzytkownik"]


class WariantNazwyOsobyInline(admin.TabularInline):
    model = WariantNazwyOsoby
    extra = 0


class WariantNazwyMiejscaInline(admin.TabularInline):
    model = WariantNazwyMiejsca
    extra = 0


class WariantNazwyInstytucjiInline(admin.TabularInline):
    model = WariantNazwyInstytucji
    extra = 0


class WariantNazwyBibliotekiInline(admin.TabularInline):
    model = WariantNazwyBiblioteki
    extra = 0


class WariantNazwyWydarzeniaInline(admin.TabularInline):
    model = WariantNazwyWydarzenia
    extra = 0


class WariantNazwyGatunkuInline(admin.TabularInline):
    model = WariantNazwyGatunku
    extra = 0


class WariantNazwyMotywuInline(admin.TabularInline):
    model = WariantNazwyMotywu
    extra = 0


class WariantNazwyTematuInline(admin.TabularInline):
    model = WariantNazwyTematu
    extra = 0


# ==========================================================
# Admin słowników
# ==========================================================

# ==========================================================
# Admin słowników
# ==========================================================

@admin.register(Osoba)
class OsobaAdmin(admin.ModelAdmin):
    inlines = [WariantNazwyOsobyInline]

    search_fields = [
        "nazwisko",
        "imiona",
    ]


@admin.register(Miejsce)
class MiejsceAdmin(admin.ModelAdmin):
    inlines = [WariantNazwyMiejscaInline]

    search_fields = [
        "nazwa",
    ]


@admin.register(Instytucja)
class InstytucjaAdmin(admin.ModelAdmin):
    inlines = [WariantNazwyInstytucjiInline]

    search_fields = [
        "nazwa",
    ]


@admin.register(Biblioteka)
class BibliotekaAdmin(admin.ModelAdmin):
    inlines = [WariantNazwyBibliotekiInline]

    search_fields = [
        "nazwa",
    ]


@admin.register(Temat)
class TematAdmin(admin.ModelAdmin):
    inlines = [WariantNazwyTematuInline]

    search_fields = [
        "nazwa",
    ]


@admin.register(Gatunek)
class GatunekAdmin(admin.ModelAdmin):
    inlines = [WariantNazwyGatunkuInline]

    search_fields = [
        "nazwa",
    ]


@admin.register(Wydarzenie)
class WydarzenieAdmin(admin.ModelAdmin):
    inlines = [WariantNazwyWydarzeniaInline]

    search_fields = [
        "nazwa",
    ]


@admin.register(Motyw)
class MotywAdmin(admin.ModelAdmin):
    inlines = [WariantNazwyMotywuInline]

    search_fields = [
        "nazwa",
    ]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = [
        "nazwa",
    ]


# ==========================================================
# Rekord
# ==========================================================

@admin.register(Rekord)
class RekordAdmin(admin.ModelAdmin):
    form = RekordForm

    readonly_fields = [
        "identyfikator",
        "data_dodania",
        "data_ostatniej_modyfikacji",
    ]

    fieldsets = (
        ("Informacje podstawowe", {
            "fields": (
                "miniatura",
                "autor",
                "tytul_skrocony",
                "tytul_pelny",
                "rok_wydania",
                "miejsce_wydania",
                "drukarz",
                "jezyki",
            )
        }),
        ("Opis fizyczny", {
            "fields": (
                "format",
                "liczba_arkuszy",
                "liczba_kart",
                "kolacjonowanie",
                "czcionki",
                "ozdobniki",
                "ryciny",
                "uwagi",
            )
        }),
        ("Powiązania", {
            "fields": (
                "adresat_dedykacji",
                "powiazane_osoby",
                "instytucje",
                "powiazane_miejsca",
                "tematy",
                "gatunki",
                "wydarzenia",
                "warianty",
                "warianty_opis",

                "wznowienia",
                "wznowienia_opis",

                "pozostale_druki_powiazane",
                "literatura_przedmiotu",
                "bibliografie",
                "streszczenie",
                "motywy",
            )
        }),
        ("Metadane", {
            "fields": (
                "status_opracowania",
                "tagi",
                "data_dodania",
                "data_ostatniej_modyfikacji",
            )
        }),
    )

    inlines = [
        WersjaZdigitalizowanaInline,
        EgzemplarzInline,
        RekordZalacznikInline,
        OpracowanieRekorduInline,
    ]

    search_fields = [
        "identyfikator",
        "tytul_skrocony",
        "tytul_pelny",
    ]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        istnieje = OpracowanieRekordu.objects.filter(
            rekord=obj,
            uzytkownik=request.user
        ).exists()

        if not istnieje:
            ostatnia = OpracowanieRekordu.objects.filter(
                rekord=obj
            ).count()

            OpracowanieRekordu.objects.create(
                rekord=obj,
                uzytkownik=request.user,
                sposob_dodania="auto",
                kolejnosc=ostatnia + 1
            )


# ==========================================================
# Relacje
# ==========================================================

@admin.register(RelacjaRekordu)
class RelacjaRekorduAdmin(admin.ModelAdmin):
    autocomplete_fields = ["rekord", "rekord_powiazany"]


@admin.register(RelacjaOsoby)
class RelacjaOsobyAdmin(admin.ModelAdmin):
    autocomplete_fields = ["rekord", "osoba"]


@admin.register(RelacjaMiejsca)
class RelacjaMiejscaAdmin(admin.ModelAdmin):
    autocomplete_fields = ["rekord", "miejsce"]


@admin.register(RelacjaInstytucji)
class RelacjaInstytucjiAdmin(admin.ModelAdmin):
    autocomplete_fields = ["rekord", "instytucja"]


@admin.register(RelacjaTematu)
class RelacjaTematuAdmin(admin.ModelAdmin):
    autocomplete_fields = ["rekord", "temat"]


@admin.register(RelacjaGatunku)
class RelacjaGatunkuAdmin(admin.ModelAdmin):
    autocomplete_fields = ["rekord", "gatunek"]


@admin.register(RelacjaWydarzenia)
class RelacjaWydarzeniaAdmin(admin.ModelAdmin):
    autocomplete_fields = ["rekord", "wydarzenie"]


@admin.register(RelacjaMotywu)
class RelacjaMotywuAdmin(admin.ModelAdmin):
    autocomplete_fields = ["rekord", "motyw"]


# ==========================================================
# Pozostałe
# ==========================================================

@admin.register(Egzemplarz)
class EgzemplarzAdmin(admin.ModelAdmin):
    autocomplete_fields = ["rekord", "biblioteka"]

    inlines = [
        EgzemplarzZalacznikInline,
    ]

    search_fields = [
        "rekord__identyfikator",
        "sygnatura",
        "biblioteka__nazwa",
    ]


@admin.register(OpracowanieRekordu)
class OpracowanieRekorduAdmin(admin.ModelAdmin):
    autocomplete_fields = ["rekord", "uzytkownik"]

    search_fields = [
        "rekord__identyfikator",
        "uzytkownik__username",
        "uzytkownik__first_name",
        "uzytkownik__last_name",
        "imie_nazwisko",
    ]


@admin.register(WersjaZdigitalizowana)
class WersjaZdigitalizowanaAdmin(admin.ModelAdmin):
    autocomplete_fields = ["rekord"]

    search_fields = [
        "rekord__identyfikator",
        "link",
    ]

# ==========================================================
# IMPORT DANYCH
# ==========================================================

@admin.register(ImportDanych)
class ImportDanychAdmin(admin.ModelAdmin):

    list_display = (
        "data_rozpoczecia",
        "uzytkownik",
        "status",
        "liczba_rekordow",
        "liczba_egzemplarzy",
        "liczba_zalacznikow",
    )

    list_filter = (
        "status",
        "uzytkownik",
    )

    search_fields = (
        "uzytkownik__username",
    )

    readonly_fields = (
        "data_rozpoczecia",
        "data_zakonczenia",
        "czas_trwania",
    )

