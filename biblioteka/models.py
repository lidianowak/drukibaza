from django.db import models
from django.db.models import Max
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


# ==========================================================
# KLASY BAZOWE
# ==========================================================

class Slownik(models.Model):
    nazwa = models.CharField(max_length=100, unique=True)

    class Meta:
        abstract = True
        ordering = ["nazwa"]

    def __str__(self):
        return self.nazwa


class Obiekt(models.Model):

    opis = models.TextField(blank=True)

    czytaj_wiecej = models.TextField(blank=True)

    ilustracja = models.ImageField(
        upload_to="obiekty/",
        blank=True,
        null=True,
        verbose_name="Ilustracja"
    )

    podpis_ilustracji = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Podpis ilustracji"
    )

    zrodlo_ilustracji = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Źródło ilustracji"
    )

    class Meta:
        abstract = True


class ObiektNazwany(Obiekt):
    nazwa = models.CharField(max_length=255, unique=True)

    class Meta:
        abstract = True
        ordering = ["nazwa"]

    def __str__(self):
        return self.nazwa


# ==========================================================
# SŁOWNIKI
# ==========================================================

class Jezyk(Slownik):

    class Meta:
        verbose_name = "Język"
        verbose_name_plural = "Języki"


class Format(Slownik):

    class Meta:
        verbose_name = "Format"
        verbose_name_plural = "Formaty"


class Czcionka(Slownik):

    class Meta:
        verbose_name = "Czcionka"
        verbose_name_plural = "Czcionki"


# ==========================================================
# OBIEKTY
# ==========================================================

class Osoba(Obiekt):

    imiona = models.CharField(max_length=255)
    nazwisko = models.CharField(max_length=255)
    kwalifikator = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Kwalifikator"
    )

    
    rok_urodzenia = models.PositiveIntegerField(
        blank=True,
        null=True
    )

    rok_smierci = models.PositiveIntegerField(
        blank=True,
        null=True
    )

    class Meta:
        ordering = ["nazwisko", "imiona"]
        verbose_name = "Osoba"
        verbose_name_plural = "Osoby"

    def __str__(self):
        return self.nazwa_glowna

    @property
    def nazwa_glowna(self):
        if self.kwalifikator:
            return f"{self.imiona} {self.nazwisko} ({self.kwalifikator})"
        
        return f"{self.imiona} {self.nazwisko}"

    
class WariantNazwyOsoby(models.Model):

        osoba = models.ForeignKey(
            Osoba,
            on_delete=models.CASCADE,
            related_name="warianty_nazw"
        )

        nazwa = models.CharField(
            max_length=255,
            verbose_name="Wariant nazwy"
        )

        kolejnosc = models.PositiveSmallIntegerField(
            default=1,
            verbose_name="Kolejność"
        )

        class Meta:
            ordering = ["kolejnosc", "id"]
            verbose_name = "Wariant nazwy osoby"
            verbose_name_plural = "Warianty nazw osób"

        def __str__(self):
            return self.nazwa    


class Miejsce(ObiektNazwany):

    class Meta:
        verbose_name = "Miejsce"
        verbose_name_plural = "Miejsca"

class WariantNazwyMiejsca(models.Model):

    miejsce = models.ForeignKey(
        Miejsce,
        on_delete=models.CASCADE,
        related_name="warianty_nazw"
    )

    nazwa = models.CharField(
        max_length=255,
        verbose_name="Wariant nazwy"
    )

    kolejnosc = models.PositiveSmallIntegerField(
        default=1,
        verbose_name="Kolejność"
    )

    class Meta:
        ordering = ["kolejnosc", "id"]
        verbose_name = "Wariant nazwy miejsca"
        verbose_name_plural = "Warianty nazw miejsc"

    def __str__(self):
        return self.nazwa


class Instytucja(ObiektNazwany):

    class Meta:
        verbose_name = "Instytucja"
        verbose_name_plural = "Instytucje"

class WariantNazwyInstytucji(models.Model):

    instytucja = models.ForeignKey(
        Instytucja,
        on_delete=models.CASCADE,
        related_name="warianty_nazw"
    )

    nazwa = models.CharField(
        max_length=255,
        verbose_name="Wariant nazwy"
    )

    kolejnosc = models.PositiveSmallIntegerField(
        default=1,
        verbose_name="Kolejność"
    )

    class Meta:
        ordering = ["kolejnosc", "id"]
        verbose_name = "Wariant nazwy instytucji"
        verbose_name_plural = "Warianty nazw instytucji"

    def __str__(self):
        return self.nazwa


class Biblioteka(ObiektNazwany):

    class Meta:
        verbose_name = "Biblioteka"
        verbose_name_plural = "Biblioteki"

class WariantNazwyBiblioteki(models.Model):

    biblioteka = models.ForeignKey(
        Biblioteka,
        on_delete=models.CASCADE,
        related_name="warianty_nazw"
    )

    nazwa = models.CharField(
        max_length=255,
        verbose_name="Wariant nazwy"
    )

    kolejnosc = models.PositiveSmallIntegerField(
        default=1,
        verbose_name="Kolejność"
    )

    class Meta:
        ordering = ["kolejnosc", "id"]
        verbose_name = "Wariant nazwy biblioteki"
        verbose_name_plural = "Warianty nazw bibliotek"

    def __str__(self):
        return self.nazwa


class Wydarzenie(ObiektNazwany):

    class Meta:
        verbose_name = "Wydarzenie"
        verbose_name_plural = "Wydarzenia"

class WariantNazwyWydarzenia(models.Model):

    wydarzenie = models.ForeignKey(
        Wydarzenie,
        on_delete=models.CASCADE,
        related_name="warianty_nazw"
    )

    nazwa = models.CharField(
        max_length=255,
        verbose_name="Wariant nazwy"
    )

    kolejnosc = models.PositiveSmallIntegerField(
        default=1,
        verbose_name="Kolejność"
    )

    class Meta:
        ordering = ["kolejnosc", "id"]
        verbose_name = "Wariant nazwy wydarzenia"
        verbose_name_plural = "Warianty nazw wydarzeń"

    def __str__(self):
        return self.nazwa


class Gatunek(ObiektNazwany):

    class Meta:
        verbose_name = "Gatunek"
        verbose_name_plural = "Gatunki"

class WariantNazwyGatunku(models.Model):

    gatunek = models.ForeignKey(
        Gatunek,
        on_delete=models.CASCADE,
        related_name="warianty_nazw"
    )

    nazwa = models.CharField(
        max_length=255,
        verbose_name="Wariant nazwy"
    )

    kolejnosc = models.PositiveSmallIntegerField(
        default=1,
        verbose_name="Kolejność"
    )

    class Meta:
        ordering = ["kolejnosc", "id"]
        verbose_name = "Wariant nazwy gatunku"
        verbose_name_plural = "Warianty nazw gatunków"

    def __str__(self):
        return self.nazwa


class Motyw(ObiektNazwany):

    class Meta:
        verbose_name = "Motyw"
        verbose_name_plural = "Motywy"

class WariantNazwyMotywu(models.Model):

    motyw = models.ForeignKey(
        Motyw,
        on_delete=models.CASCADE,
        related_name="warianty_nazw"
    )

    nazwa = models.CharField(
        max_length=255,
        verbose_name="Wariant nazwy"
    )

    kolejnosc = models.PositiveSmallIntegerField(
        default=1,
        verbose_name="Kolejność"
    )

    class Meta:
        ordering = ["kolejnosc", "id"]
        verbose_name = "Wariant nazwy motywu"
        verbose_name_plural = "Warianty nazw motywów"

    def __str__(self):
        return self.nazwa


class Temat(ObiektNazwany):

    class Meta:
        verbose_name = "Temat"
        verbose_name_plural = "Tematy"

class WariantNazwyTematu(models.Model):

    temat = models.ForeignKey(
        Temat,
        on_delete=models.CASCADE,
        related_name="warianty_nazw"
    )

    nazwa = models.CharField(
        max_length=255,
        verbose_name="Wariant nazwy"
    )

    kolejnosc = models.PositiveSmallIntegerField(
        default=1,
        verbose_name="Kolejność"
    )

    class Meta:
        ordering = ["kolejnosc", "id"]
        verbose_name = "Wariant nazwy tematu"
        verbose_name_plural = "Warianty nazw tematów"

    def __str__(self):
        return self.nazwa

# ==========================================================
# REKORD
# ==========================================================

class Rekord(models.Model):

    # ======================================================
    # IDENTYFIKACJA
    # ======================================================

    identyfikator = models.CharField(
        max_length=6,
        unique=True,
        editable=False,
        help_text="Automatycznie nadawany sześciocyfrowy identyfikator BiDO."
    )

    miniatura = models.ImageField(
        verbose_name="Miniatura",
        upload_to="miniatury/",
        blank=True,
        null=True,
        help_text="Miniatura wyświetlana na karcie rekordu i w wynikach wyszukiwania."
    )

    tytul_skrocony = models.TextField(
        verbose_name="Tytuł skrócony"
    )

    tytul_pelny = models.TextField(
        verbose_name="Tytuł pełny",
        blank=True
    )

    rok_wydania = models.PositiveSmallIntegerField(
        verbose_name="Data wydania",
        blank=True,
        null=True
    )

    jezyki = models.ManyToManyField(
        Jezyk,
        verbose_name="Języki",
        blank=True
    )


    # Wersje zdigitalizowane przechowywane są
    # w modelu WersjaZdigitalizowana.

    # ======================================================
    # OPIS FIZYCZNY
    # ======================================================

    format = models.ForeignKey(
        Format,
        verbose_name="Format",
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    liczba_arkuszy = models.DecimalField(
        verbose_name="Liczba arkuszy",
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True
    )

    liczba_kart = models.CharField(
        verbose_name="Liczba kart",
        max_length=100,
        blank=True
    )

    kolacjonowanie = models.TextField(
        verbose_name="Kolacjonowanie",
        blank=True
    )

    czcionki = models.ManyToManyField(
        Czcionka,
        verbose_name="Czcionki",
        blank=True
    )

    ozdobniki = models.TextField(
        verbose_name="Ozdobniki",
        blank=True
    )

    ryciny = models.TextField(
        verbose_name="Ryciny",
        blank=True,
        help_text="Pozostaw puste, jeśli druk nie zawiera rycin."
    )

    uwagi = models.TextField(
        verbose_name="Uwagi",
        blank=True
    )

    # ======================================================
    # POWIĄZANIA
    # ======================================================

    pozostale_druki_powiazane = models.TextField(
        verbose_name="Pozostałe druki powiązane",
        blank=True,
        help_text="Można wpisywać opisy bibliograficzne druków spoza bazy BiDO."
    )

    literatura_przedmiotu = models.TextField(
        verbose_name="Literatura przedmiotu, opracowania",
        blank=True
    )

    bibliografie = models.TextField(
        verbose_name="Bibliografie",
        blank=True
    )

    streszczenie = models.TextField(
        verbose_name="Streszczenie",
        blank=True
    )

    # ======================================================
    # METADANE
    # ======================================================
    tagi = models.ManyToManyField(
        "Tag",
        blank=True,
        verbose_name="Tagi"
    )


    status_opracowania = models.CharField(
        verbose_name="Status opracowania",
        max_length=30,
        choices=[
            ("do_opracowania", "Do opracowania"),
            ("czesciowo_opracowany", "Częściowo opracowany"),
            ("opracowany", "Opracowany"),
        ],
        default="do_opracowania",
    )

    data_dodania = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data dodania"
    )

    data_ostatniej_modyfikacji = models.DateTimeField(
        auto_now=True,
        verbose_name="Data ostatniej modyfikacji"
    )

    # ======================================================
    # METODY
    # ======================================================

    def __str__(self):
        return f"{self.identyfikator} — {self.tytul_skrocony}"

    def save(self, *args, **kwargs):

        if not self.identyfikator:

            ostatni = Rekord.objects.aggregate(
                Max("identyfikator")
            )["identyfikator__max"]

            if ostatni:
                nowy = int(ostatni) + 1
            else:
                nowy = 1

            self.identyfikator = f"{nowy:06d}"

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Rekord"
        verbose_name_plural = "Rekordy"

# ==========================================================
# WERSJE ZDIGITALIZOWANE
# ==========================================================

class WersjaZdigitalizowana(models.Model):

    rekord = models.ForeignKey(
        Rekord,
        on_delete=models.CASCADE,
        related_name="wersje_zdigitalizowane"
    )

    link = models.URLField(
        verbose_name="Link"
    )

    kolejnosc = models.PositiveSmallIntegerField(
        default=1,
        verbose_name="Kolejność"
    )

    class Meta:
        verbose_name = "Wersja zdigitalizowana"
        verbose_name_plural = "Wersje zdigitalizowane"
        ordering = ["kolejnosc", "id"]

    def __str__(self):
        return self.link


# ==========================================================
# RELACJE
# ==========================================================

class RelacjaRekordu(models.Model):

    TYPY_RELACJI = [
        ("wariant", "Wariant"),
        ("wznowienie", "Wznowienie"),
    ]

    rekord = models.ForeignKey(
        Rekord,
        on_delete=models.CASCADE,
        related_name="relacje"
    )

    rekord_powiazany = models.ForeignKey(
        Rekord,
        on_delete=models.CASCADE,
        related_name="powiazane_z"
    )

    typ = models.CharField(
        max_length=20,
        choices=TYPY_RELACJI
    )

    class Meta:
        verbose_name = "Relacja rekordu"
        verbose_name_plural = "Relacje rekordów"

    def __str__(self):
        return (
            f"{self.rekord.identyfikator} → "
            f"{self.rekord_powiazany.identyfikator} "
            f"({self.get_typ_display()})"
        )


class RelacjaOsoby(models.Model):

    TYPY_RELACJI = [
        ("autor", "Autor"),
        ("drukarz", "Drukarz"),
        ("adresat", "Adresat dedykacji"),
        ("powiazana", "Powiązana osoba"),
    ]

    rekord = models.ForeignKey(
        Rekord,
        on_delete=models.CASCADE,
        related_name="relacje_osob"
    )

    osoba = models.ForeignKey(
        Osoba,
        on_delete=models.CASCADE
    )

    typ = models.CharField(
        max_length=20,
        choices=TYPY_RELACJI
    )

    class Meta:
        verbose_name = "Relacja osoby"
        verbose_name_plural = "Relacje osób"

    def __str__(self):
        return (
            f"{self.rekord.identyfikator} → "
            f"{self.osoba} ({self.get_typ_display()})"
        )


class RelacjaMiejsca(models.Model):

    TYPY_RELACJI = [
        ("wydania", "Miejsce wydania"),
        ("powiazane", "Powiązane miejsce"),
    ]

    rekord = models.ForeignKey(
        Rekord,
        on_delete=models.CASCADE,
        related_name="relacje_miejsc"
    )

    miejsce = models.ForeignKey(
        Miejsce,
        on_delete=models.CASCADE
    )

    typ = models.CharField(
        max_length=20,
        choices=TYPY_RELACJI
    )

    class Meta:
        verbose_name = "Relacja miejsca"
        verbose_name_plural = "Relacje miejsc"

    def __str__(self):
        return (
            f"{self.rekord.identyfikator} → "
            f"{self.miejsce} ({self.get_typ_display()})"
        )


class RelacjaInstytucji(models.Model):

    rekord = models.ForeignKey(
        Rekord,
        on_delete=models.CASCADE,
        related_name="relacje_instytucji"
    )

    instytucja = models.ForeignKey(
        Instytucja,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Relacja instytucji"
        verbose_name_plural = "Relacje instytucji"

    def __str__(self):
        return f"{self.rekord.identyfikator} → {self.instytucja}"


class RelacjaTematu(models.Model):

    rekord = models.ForeignKey(
        Rekord,
        on_delete=models.CASCADE,
        related_name="relacje_tematow"
    )

    temat = models.ForeignKey(
        Temat,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Relacja tematu"
        verbose_name_plural = "Relacje tematów"

    def __str__(self):
        return f"{self.rekord.identyfikator} → {self.temat}"


class RelacjaGatunku(models.Model):

    rekord = models.ForeignKey(
        Rekord,
        on_delete=models.CASCADE,
        related_name="relacje_gatunkow"
    )

    gatunek = models.ForeignKey(
        Gatunek,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Relacja gatunku"
        verbose_name_plural = "Relacje gatunków"

    def __str__(self):
        return f"{self.rekord.identyfikator} → {self.gatunek}"


class RelacjaWydarzenia(models.Model):

    rekord = models.ForeignKey(
        Rekord,
        on_delete=models.CASCADE,
        related_name="relacje_wydarzen"
    )

    wydarzenie = models.ForeignKey(
        Wydarzenie,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Relacja wydarzenia"
        verbose_name_plural = "Relacje wydarzeń"

    def __str__(self):
        return f"{self.rekord.identyfikator} → {self.wydarzenie}"


class RelacjaMotywu(models.Model):

    rekord = models.ForeignKey(
        Rekord,
        on_delete=models.CASCADE,
        related_name="relacje_motywow"
    )

    motyw = models.ForeignKey(
        Motyw,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Relacja motywu"
        verbose_name_plural = "Relacje motywów"

    def __str__(self):
        return f"{self.rekord.identyfikator} → {self.motyw}"    
    
# ==========================================================
# EGZEMPLARZE
# ==========================================================

class Egzemplarz(models.Model):

    rekord = models.ForeignKey(
        Rekord,
        on_delete=models.CASCADE,
        related_name="egzemplarze"
    )

    biblioteka = models.ForeignKey(
        Biblioteka,
        on_delete=models.PROTECT,
        verbose_name="Biblioteka"
    )

    kolejnosc = models.PositiveSmallIntegerField(
        default=1,
        verbose_name="Kolejność"
    )

    sygnatura = models.TextField(
        verbose_name="Sygnatura",
        blank=True
    )

    
    katalog_biblioteczny = models.URLField(
        verbose_name="Katalog biblioteczny",
        blank=True
    )

    proweniencja = models.TextField(
        verbose_name="Proweniencja",
        blank=True
    )

    oprawa = models.TextField(
        verbose_name="Oprawa",
        blank=True
    )

    marginalia = models.TextField(
        verbose_name="Marginalia, ślady lektury",
        blank=True,
        help_text="Pozostaw puste, jeśli egzemplarz nie zawiera marginaliów ani śladów lektury."
    )

    class Meta:
        verbose_name = "Egzemplarz"
        verbose_name_plural = "Egzemplarze"
        ordering = ["kolejnosc", "id"]

    def __str__(self):
        return f"{self.rekord.identyfikator} – {self.biblioteka}"


# ======================================================
# ZAŁĄCZNIKI
# ======================================================

class Zalacznik(models.Model):

    SEKCJE = [
        ("ozdobniki", "Ozdobniki"),
        ("ryciny", "Ryciny"),
        ("uwagi", "Uwagi"),
        ("literatura_przedmiotu", "Literatura przedmiotu"),
        ("marginalia", "Marginalia"),
        ("inne", "Inne"),
    ]

    rekord = models.ForeignKey(
        Rekord,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="zalaczniki"
    )

    egzemplarz = models.ForeignKey(
        Egzemplarz,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="zalaczniki"
    )

    sekcja = models.CharField(
        max_length=30,
        choices=SEKCJE,
        default="inne",
        verbose_name="Sekcja"
    )

    plik = models.FileField(
        upload_to="zalaczniki/",
        verbose_name="Plik"
    )

    nazwa_wyswietlana = models.CharField(
        verbose_name="Nazwa wyświetlana",
        max_length=255,
        blank=True
    )

    opis = models.CharField(
        verbose_name="Opis",
        max_length=255,
        blank=True
    )

    kolejnosc = models.PositiveSmallIntegerField(
        verbose_name="Kolejność",
        default=1
    )

    class Meta:
        ordering = ["kolejnosc", "id"]
        verbose_name = "Załącznik"
        verbose_name_plural = "Załączniki"

    def __str__(self):
        return self.nazwa_wyswietlana or self.plik.name.split("/")[-1]
    
    def clean(self):
        super().clean()

        if self.sekcja == "marginalia" and not self.egzemplarz:
            raise ValidationError({
                "egzemplarz": (
                    "Dla załączników do marginaliów należy wskazać egzemplarz."
                )
            })

        if self.sekcja != "marginalia" and self.egzemplarz:
            raise ValidationError({
                "egzemplarz": (
                    "Egzemplarz można wskazać wyłącznie dla załączników do marginaliów."
                )
            })


# ==========================================================
# OPRACOWANIE REKORDU
# ==========================================================

class OpracowanieRekordu(models.Model):

    SPOSOBY_DODANIA = [
        ("auto", "Automatycznie"),
        ("recznie", "Ręcznie"),
    ]

    rekord = models.ForeignKey(
        Rekord,
        on_delete=models.CASCADE,
        related_name="opracowanie"
    )

    uzytkownik = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Użytkownik"
    )

    imie_nazwisko = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Imię i nazwisko"
    )

    sposob_dodania = models.CharField(
        max_length=20,
        choices=SPOSOBY_DODANIA,
        default="auto"
    )

    kolejnosc = models.PositiveSmallIntegerField(
        default=1,
        verbose_name="Kolejność"
    )

    class Meta:
        verbose_name = "Autor opracowania"
        verbose_name_plural = "Autorzy opracowania"
        ordering = ["kolejnosc", "id"]

    def __str__(self):

        if self.uzytkownik:

            pelna_nazwa = self.uzytkownik.get_full_name()

            if pelna_nazwa:
                autor = pelna_nazwa
            else:
                autor = self.uzytkownik.username

        else:
            autor = self.imie_nazwisko

        return f"{self.rekord.identyfikator} → {autor}"
    
# ==========================================================
# METADANE
# ==========================================================

class Tag(models.Model):

    nazwa = models.CharField(
        max_length=100,
        unique=True
    )

    class Meta:
        ordering = ["nazwa"]
        verbose_name = "Tag"
        verbose_name_plural = "Tagi"

    def __str__(self):
        return self.nazwa