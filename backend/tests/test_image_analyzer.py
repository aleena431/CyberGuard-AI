from io import BytesIO

import pytest
from PIL import Image

from backend.app.vision.image_analyzer import (
    ImageValidationError,
    analyze_image,
)


def create_test_png():
    buffer = BytesIO()
    Image.new("RGB", (320, 200), "white").save(
        buffer, format="PNG"
    )
    return buffer.getvalue()


def test_valid_png():
    result = analyze_image(create_test_png())

    assert result["valid"] is True
    assert result["format"] == "PNG"
    assert result["width"] == 320
    assert result["height"] == 200


def test_empty_image_is_rejected():
    with pytest.raises(ImageValidationError):
        analyze_image(b"")


def test_invalid_image_is_rejected():
    with pytest.raises(ImageValidationError):
        analyze_image(b"This is not an image")


def test_oversized_upload_is_rejected():
    oversized_data = b"x" * (10 * 1024 * 1024 + 1)

    with pytest.raises(ImageValidationError):
        analyze_image(oversized_data)