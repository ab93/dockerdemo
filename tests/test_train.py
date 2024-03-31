import os

import pytest
from PIL import Image
from src.constants import TESTS_DIR
from src.predict import classify_image


@pytest.fixture
def image():
    return Image.open(os.path.join(TESTS_DIR, "resources", "2.png"))


def test_classify_image(image):
    out = classify_image(image)
    assert out == 2
