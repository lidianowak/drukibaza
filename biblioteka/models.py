from django.db import models


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
