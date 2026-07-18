from io import BytesIO

from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import (
    redirect,
    render,
)

from django.contrib import messages

from .forms import (
    CsvImportForm,
    ImportForm,
)

from .template_generator import generate_template

from django.utils import timezone

from biblioteka.importer.loader import load_workbook
from biblioteka.importer.import_service import run_import

from biblioteka.models import ImportDanych

from django.http import HttpResponse

from django.core.files.base import ContentFile

from .report import build_report

from django.http import FileResponse
from django.http import Http404
from .exceptions import ImportValidationError

from zipfile import BadZipFile


@staff_member_required
def index(request):

    if request.method == "POST":

        import_form = ImportForm(
            request.POST,
            request.FILES,
        )

        if import_form.is_valid():

            import_danych = ImportDanych.objects.create(
                uzytkownik=request.user,
                plik=request.FILES["plik"],
            )

            try:

                workbook = load_workbook(
                    request.FILES["plik"],
                )

                result = run_import(
                    workbook=workbook,
                    uzytkownik=request.user,
                )

                import_danych.status = "zakonczony"

                import_danych.liczba_rekordow = result.records
                import_danych.liczba_egzemplarzy = result.specimens
                import_danych.liczba_zalacznikow = result.attachments

                import_danych.data_zakonczenia = timezone.now()

                import_danych.czas_trwania = (
                    import_danych.data_zakonczenia
                    - import_danych.data_rozpoczecia
                )

                report = build_report(
                    import_danych,
                    result,
                )

                filename = (
                    f"raport_importu_{import_danych.pk}.txt"
                )

                import_danych.raport.save(
                    filename,
                    ContentFile(report.encode("utf-8")),
                    save=False,
                )

                import_danych.save()

                request.session["ostatni_import"] = import_danych.pk

                messages.success(
                    request,
                    "Import zakończył się pomyślnie.",
                )

            except ImportValidationError as e:

                result = e.result

                import_danych.status = "blad"

                import_danych.data_zakonczenia = timezone.now()

                import_danych.czas_trwania = (
                    import_danych.data_zakonczenia
                    - import_danych.data_rozpoczecia
                )

                report = build_report(
                    import_danych,
                    result,
                )

                filename = (
                    f"raport_importu_{import_danych.pk}.txt"
                )

                import_danych.raport.save(
                    filename,
                    ContentFile(report.encode("utf-8")),
                    save=False,
                )

                import_danych.save()

                request.session["ostatni_import"] = import_danych.pk

                messages.error(
                    request,
                    str(e),
                )

            except BadZipFile:

                import_danych.status = "blad"

                import_danych.data_zakonczenia = timezone.now()

                import_danych.czas_trwania = (
                    import_danych.data_zakonczenia
                    - import_danych.data_rozpoczecia
                )

                import_danych.save()

                request.session["ostatni_import"] = import_danych.pk

                messages.error(
                    request,
                    "Wybrany plik nie jest poprawnym plikiem programu Excel (.xlsx).",
                )
            
            except Exception as e:

                import_danych.status = "blad"

                import_danych.data_zakonczenia = timezone.now()

                import_danych.czas_trwania = (
                    import_danych.data_zakonczenia
                    - import_danych.data_rozpoczecia
                )

                import_danych.save()

                request.session["ostatni_import"] = import_danych.pk

                messages.error(
                    request,
                    str(e),
                )       

            return redirect("import-index")

    historia_importow = (
        ImportDanych.objects
        .order_by("-data_rozpoczecia")[:30]
    )

    ostatni_import = request.session.pop(
        "ostatni_import",
        None,
    )

    if request.method != "POST":
        import_form = ImportForm()

    return render(
        request,
        "importer/index.html",
        {
            "import_form": import_form,
            "csv_form": CsvImportForm(),
            "historia_importow": historia_importow,
            "ostatni_import": ostatni_import,
        },
    )


@staff_member_required
def download_template(request):
    """
    Generuje aktualny formularz importu.
    """

    workbook = generate_template()

    output = BytesIO()

    workbook.save(output)

    output.seek(0)

    response = HttpResponse(
        output.read(),
        content_type=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        ),
    )

    timestamp = timezone.localtime().strftime("%Y-%m-%d_%H-%M")

    username = request.user.username

    filename = (
        f"formularz_importu_BiDO_"
        f"{timestamp}_"
        f"{username}.xlsx"
    )

    response["Content-Disposition"] = (
        f'attachment; filename="{filename}"'
    )

    return response


@staff_member_required
def report(request, pk):

    import_danych = ImportDanych.objects.get(pk=pk)

    report = ""

    if import_danych.raport:
        with import_danych.raport.open("rb") as f:
            report = f.read().decode("utf-8")

    return render(
        request,
        "importer/report.html",
        {
            "import_danych": import_danych,
            "report": report,
        },
    )


@staff_member_required
def download_report(request, pk):

    import_danych = ImportDanych.objects.get(
        pk=pk,
    )

    if not import_danych.raport:
        raise Http404("Raport nie istnieje.")

    response = FileResponse(
        import_danych.raport.open("rb"),
        content_type="text/plain",
    )

    response["Content-Disposition"] = (
        f'attachment; filename="{import_danych.raport.name.split("/")[-1]}"'
    )

    return response