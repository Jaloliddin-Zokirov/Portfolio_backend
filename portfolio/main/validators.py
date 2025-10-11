from __future__ import annotations

import os
from typing import Any

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from PIL import Image, UnidentifiedImageError


ALLOWED_IMAGE_EXTENSIONS = {".gif", ".jpg", ".jpeg", ".png", ".svg", ".webp"}


def _get_file_descriptor(upload: Any):
    descriptor = getattr(upload, "file", upload)
    if not hasattr(descriptor, "read"):
        raise ValidationError(_("Unsupported file object."))
    return descriptor


def _is_svg(upload: Any) -> bool:
    """
    Return True if file-like object contains an SVG document.

    The function inspects the first chunk of the file instead of reading
    the whole stream to avoid loading large files into memory.
    """

    descriptor = _get_file_descriptor(upload)
    pos = descriptor.tell()
    try:
        header = descriptor.read(1024)
    finally:
        descriptor.seek(pos)

    snippet = header.decode("utf-8", errors="ignore").lower()
    return "<svg" in snippet


def validate_image_or_svg(upload: Any) -> None:
    """
    Allow standard raster images as well as SVGs.

    For raster images we rely on Pillow to verify the content.
    For SVGs we simply check extension/content markers because Pillow
    does not support vector formats.
    """

    name = getattr(upload, "name", "")
    extension = os.path.splitext(name)[1].lower()
    if extension not in ALLOWED_IMAGE_EXTENSIONS:
        raise ValidationError(
            _("Unsupported file extension. Allowed extensions: %(ext)s"),
            params={"ext": ", ".join(sorted(ALLOWED_IMAGE_EXTENSIONS))},
        )

    content_type = getattr(upload, "content_type", "") or ""
    if extension == ".svg" or content_type == "image/svg+xml":
        if not _is_svg(upload):
            raise ValidationError(_("Upload a valid SVG file."))
        return

    # For non-SVG files, defer to Pillow for verification.
    descriptor = _get_file_descriptor(upload)
    try:
        img = Image.open(descriptor)
        img.verify()
    except (UnidentifiedImageError, AttributeError, OSError) as exc:
        raise ValidationError(_("Upload a valid image file.")) from exc
    finally:
        descriptor.seek(0)
