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
