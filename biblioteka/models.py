from django.db import models
from django.db.models import Max


class Slownik(models.Model):
    nazwa = models.CharField(max_length=100, unique=True)

    class Meta:
        abstract = True
        ordering = ["nazwa"]

    def __str__(self):
        return self.nazwa


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


class Obiekt(models.Model):
    opis = models.TextField(blank=True)
    czytaj_wiecej = models.TextField(blank=True)

    class Meta:
        abstract = True


class ObiektNazwany(Obiekt):
    nazwa = models.CharField(max_length=255, unique=True)

    class Meta:
        abstract = True
        ordering = ["nazwa"]

    def __str__(self):
        return self.nazwa


class Osoba(Obiekt):
    imiona = models.CharField(max_length=255)
    nazwisko = models.CharField(max_length=255)
    warianty = models.TextField(blank=True)

    rok_urodzenia = models.PositiveIntegerField(blank=True, null=True)
    rok_smierci = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        ordering = ["nazwisko", "imiona"]
        verbose_name = "Osoba"
        verbose_name_plural = "Osoby"

    def __str__(self):
        return f"{self.nazwisko}, {self.imiona}"

    @property
    def nazwa_wyswietlana(self):
        return f"{self.imiona} {self.nazwisko}"
    
    

class Miejsce(ObiektNazwany):
    

    class Meta:

        verbose_name = "Miejsce"
        verbose_name_plural = "Miejsca"




class Instytucja(ObiektNazwany):

    class Meta:

        verbose_name = "Instytucja"
        verbose_name_plural = "Instytucje"

  


class Biblioteka(ObiektNazwany):

    class Meta:
        verbose_name = "Biblioteka"
        verbose_name_plural = "Biblioteki"




class Wydarzenie(ObiektNazwany):

    class Meta:
        verbose_name = "Wydarzenie"
        verbose_name_plural = "Wydarzenia"



class Gatunek(ObiektNazwany):

    class Meta:
        verbose_name = "Gatunek"
        verbose_name_plural = "Gatunki"



class Motyw(ObiektNazwany):

    class Meta:
        verbose_name = "Motyw"
        verbose_name_plural = "Motywy"



class Temat(ObiektNazwany):

    class Meta:
        verbose_name = "Temat"
        verbose_name_plural = "Tematy"

class Rekord(models.Model):

    # ===== IDENTYFIKACJA REKORDU =====

 
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


    wersja_zdigitalizowana = models.URLField(
        verbose_name="Wersja zdigitalizowana",
        blank=True
    )

    # ===== OPIS FIZYCZNY =====

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

    # ===== POWIĄZANIA =====

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
        return f"{self.rekord.identyfikator} → {self.osoba} ({self.get_typ_display()})"

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
        return f"{self.rekord.identyfikator} → {self.miejsce} ({self.get_typ_display()})"   
    
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