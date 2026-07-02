from django.contrib import admin
from .models import Jezyk, Format, Czcionka
from .models import Jezyk, Format, Czcionka, Osoba

admin.site.register(Jezyk)
admin.site.register(Format)
admin.site.register(Czcionka)

admin.site.register(Osoba)

