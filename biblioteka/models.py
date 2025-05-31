from django.db import models

class Starodruk(models.Model):
    tytul_transkrypcja = models.CharField(max_length=255)
    tytul_transliteracja = models.CharField(max_length=255)
    autor = models.CharField(max_length=255, blank=True, null=True)
    miejsce_wydania = models.CharField(max_length=255, blank=True, null=True)
    data_wydania = models.CharField(max_length=100, blank=True, null=True)
    drukarnia = models.CharField(max_length=255, blank=True, null=True)
    format = models.TextField(blank=True, null=True)
    liczba_kart = models.CharField(max_length=50, blank=True, null=True)
    liczba_arkuszy = models.CharField(max_length=50, blank=True, null=True)
    jezyk = models.CharField(max_length=100, blank=True, null=True)
    gatunek = models.CharField(max_length=255, blank=True, null=True)
    adresat = models.CharField(max_length=255, blank=True, null=True)
    okolicznosci_powstania = models.TextField(blank=True, null=True)
    dodatkowe_informacje = models.TextField(blank=True, null=True)
    sygnatury = models.TextField(blank=True, null=True)
    link_do_wersji = models.URLField(blank=True, null=True)
    miniatura = models.ImageField(upload_to='miniatury/', blank=True, null=True)

    def __str__(self):
        return self.tytul_transkrypcja

# Create your models here.
