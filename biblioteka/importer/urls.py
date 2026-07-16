from django.urls import path

from .views import (
    download_template,
    index,
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
]