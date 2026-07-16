from pathlib import Path

from django.core.management.base import BaseCommand

from biblioteka.importer.loader import load_workbook


from django.contrib.auth import get_user_model

from biblioteka.importer.import_service import run_import


class Command(BaseCommand):
    help = "Test importera BiDO"

    def add_arguments(self, parser):
        parser.add_argument(
            "--user",
            required=True,
            help="Nazwa użytkownika wykonującego import",
        )
    
    def handle(self, *args, **options):

        username = options["user"]
        User = get_user_model()

        uzytkownik = User.objects.get(
            username=username,
        )
        
        wb = load_workbook(
            Path(r"C:\Users\user\Desktop\drukibaza\formularz importu_BiDO.xlsx")
        )

        run_import(
            workbook=wb,
            uzytkownik=uzytkownik,
        )