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

            workbook = load_workbook(
                request.FILES["plik"],
            )

            try:

                result = run_import(
                    workbook=workbook,
                    uzytkownik=request.user,
                )

                import_danych.liczba_rekordow = result.records
                import_danych.liczba_egzemplarzy = result.specimens
                import_danych.liczba_zalacznikow = result.attachments

                import_danych.status = "zakonczony"

                import_danych.data_zakonczenia = timezone.now()

                import_danych.czas_trwania = (
                    import_danych.data_zakonczenia
                    - import_danych.data_rozpoczecia
                )

                import_danych.save()

                request.session["ostatni_import"] = import_danych.pk

                messages.success(
                    request,
                    "Import zakończył się pomyślnie.",
                )

            except Exception as e:

                import_danych.status = "blad"

                import_danych.data_zakonczenia = timezone.now()

                import_danych.czas_trwania = (
                    import_danych.data_zakonczenia
                    - import_danych.data_rozpoczecia
                )

                import_danych.save()

                messages.error(
                    request,
                    str(e),
                )

            return redirect("import-index")

    historia_importow = (
        ImportDanych.objects
        .order_by("-data_rozpoczecia")[:10]
    )

    ostatni_import = request.session.pop(
        "ostatni_import",
        None,
    )

    return render(
        request,
        "importer/index.html",
        {
            "import_form": ImportForm(),
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

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")

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

    import_danych = ImportDanych.objects.get(
        pk=pk,
    )

    return render(
        request,
        "importer/report.html",
        {
            "import_danych": import_danych,
        },
    )


@staff_member_required
def download_report(request, pk):

    import_danych = ImportDanych.objects.get(
        pk=pk,
    )

    lines = [
        "RAPORT IMPORTU",
        "",
        f"Status: {import_danych.get_status_display()}",
        f"Data: {import_danych.data_rozpoczecia}",
        f"Użytkownik: {import_danych.uzytkownik}",
        "",
        "ZAIMPORTOWANO",
        f"Rekordy: {import_danych.liczba_rekordow}",
        f"Egzemplarze: {import_danych.liczba_egzemplarzy}",
        f"Załączniki: {import_danych.liczba_zalacznikow}",
    ]

    response = HttpResponse(
        "\n".join(lines),
        content_type="text/plain",
    )

    timestamp = import_danych.data_rozpoczecia.strftime(
    "%Y-%m-%d_%H-%M-%S"
    )

    filename = (
        f"raport_importu_"
        f"{timestamp}.txt"
    )

    response["Content-Disposition"] = (
        f'attachment; filename="{filename}"'
    )

    return response