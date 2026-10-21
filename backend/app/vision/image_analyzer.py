from io import BytesIO

from PIL import Image, UnidentifiedImageError

MAX_IMAGE_BYTES = 10 * 1024 * 1024  # 10 MB
MAX_IMAGE_PIXELS = 20_000_000  # 20 megapixels
SUPPORTED_FORMATS = {"PNG", "JPEG", "WEBP"}


class ImageValidationError(ValueError):
    """Raised when an uploaded image is invalid or unsupported."""


def analyze_image(image_bytes: bytes) -> dict:
    """Validate an image and return basic metadata without saving it."""

    if not image_bytes:
        raise ImageValidationError("The uploaded image is empty.")

    if len(image_bytes) > MAX_IMAGE_BYTES:
        raise ImageValidationError("Image exceeds the 10 MB size limit.")

    try:
        with Image.open(BytesIO(image_bytes)) as image:
            image_format = image.format
            width, height = image.size

            if image_format not in SUPPORTED_FORMATS:
                raise ImageValidationError(
                    "Unsupported image format. Use PNG, JPEG, or WEBP."
                )

            if width <= 0 or height <= 0:
                raise ImageValidationError("Invalid image dimensions.")

            if width * height > MAX_IMAGE_PIXELS:
                raise ImageValidationError(
                    "Image exceeds the 20-megapixel limit."
                )

            image.verify()

        return {
            "valid": True,
            "format": image_format,
            "width": width,
            "height": height,
            "size_bytes": len(image_bytes),
        }

    except UnidentifiedImageError as exc:
        raise ImageValidationError(
            "The uploaded file is not a valid image."
        ) from exc
    except OSError as exc:
        raise ImageValidationError(
            "The image is corrupted or cannot be read."
        ) from exc
