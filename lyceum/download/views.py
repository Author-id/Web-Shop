from pathlib import Path

from django.conf import settings
from django.http import FileResponse


__all__ = []


def download(request, path):
    return FileResponse(
        open(settings.MEDIA_ROOT / Path(path), "rb"),
        as_attachment=True,
    )
