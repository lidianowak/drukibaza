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

from datetime import datetime

from biblioteka.importer.loader import load_workbook
from biblioteka.importer.import_service import run_import


@staff_member_required
def index(request):

    if request.method == "POST":

        import_form = ImportForm(
            request.POST,
            request.FILES,
        )

        if import_form.is_valid():

            workbook = load_workbook(
                request.FILES["plik"],
            )

            try:

                run_import(
                    workbook=workbook,
                    uzytkownik=request.user,
                )

                messages.success(
                    request,
                    "Import zakończył się pomyślnie.",
                )

            except Exception as e:

                messages.error(
                    request,
                    str(e),
                )

            return redirect("import-index")

    
    return render(
        request,
        "importer/index.html",
        {
            "import_form": ImportForm(),
            "csv_form": CsvImportForm(),
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