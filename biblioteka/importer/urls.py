from django.urls import path

from .views import (
    confirm_import,
    download_report,
    download_template,
    index,
    report,
)

urlpatterns = [
    path(
        "",
        index,
        name="import-index",
    ),

    path(
        "download/",
        download_template,
        name="download-template",
    ),

    path(
        "report/<int:pk>/",
        report,
        name="import-report",
    ),

    path(
        "report/<int:pk>/download/",
        download_report,
        name="download-report",
    ),

    path(
        "confirm/<int:pk>/",
        confirm_import,
        name="confirm-import",
    ),
]