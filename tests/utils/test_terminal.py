import re

from PIL import Image

from src.utils.terminal import HALF_BLOCK, image_to_ansi, print_image


def _cells(text):
    return re.findall(r"38;2;(\d+;\d+;\d+)m\x1b\[48;2;(\d+;\d+;\d+)m" + HALF_BLOCK, text)


def test_each_cell_shows_top_and_bottom_pixel():
    image = Image.new("RGB", (1, 2))
    image.putpixel((0, 0), (255, 0, 0))
    image.putpixel((0, 1), (0, 0, 255))

    assert _cells(image_to_ansi(image, max_width=1)) == [("255;0;0", "0;0;255")]


def test_image_is_scaled_to_max_width():
    lines = image_to_ansi(Image.new("RGB", (200, 80)), max_width=50).splitlines()

    assert len(lines) == 10
    assert all(len(_cells(line)) == 50 for line in lines)


def test_print_image_reports_unsupported_terminal(monkeypatch):
    def fail(*args, **kwargs):
        raise UnicodeEncodeError("cp1252", HALF_BLOCK, 0, 1, "no")

    monkeypatch.setattr("builtins.print", fail)
    monkeypatch.setattr("os.system", lambda command: 0)

    assert print_image(Image.new("RGB", (2, 2))) is False
