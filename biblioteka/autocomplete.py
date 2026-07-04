from dal import autocomplete

from .models import Osoba


class OsobaAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Osoba.objects.all()

        if self.q:
            qs = qs.filter(
                nazwisko__icontains=self.q
            ) | Osoba.objects.filter(
                imiona__icontains=self.q
            )

        return qs
    
from .models import (
    Miejsce,
    Instytucja,
    Temat,
    Gatunek,
    Wydarzenie,
    Motyw,
    Rekord,
    Tag,
)


class MiejsceAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Miejsce.objects.all()

        if self.q:
            qs = qs.filter(nazwa__icontains=self.q)

        return qs


class InstytucjaAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Instytucja.objects.all()

        if self.q:
            qs = qs.filter(nazwa__icontains=self.q)

        return qs


class TematAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Temat.objects.all()

        if self.q:
            qs = qs.filter(nazwa__icontains=self.q)

        return qs


class GatunekAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Gatunek.objects.all()

        if self.q:
            qs = qs.filter(nazwa__icontains=self.q)

        return qs


class WydarzenieAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Wydarzenie.objects.all()

        if self.q:
            qs = qs.filter(nazwa__icontains=self.q)

        return qs


class MotywAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Motyw.objects.all()

        if self.q:
            qs = qs.filter(nazwa__icontains=self.q)

        return qs


class RekordAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Rekord.objects.all()

        if self.q:
            qs = qs.filter(
                tytul_skrocony__icontains=self.q
            ) | Rekord.objects.filter(
                identyfikator__icontains=self.q
            )

        return qs
    
class TagAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Tag.objects.all()

        if self.q:
            qs = qs.filter(nazwa__icontains=self.q)

        return qs