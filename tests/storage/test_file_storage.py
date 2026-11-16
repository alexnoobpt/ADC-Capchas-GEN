from PIL import Image

from src.storage.file_storage import save_image


def test_save_image_creates_png(tmp_path):
    image = Image.new("RGB", (10, 10), (255, 0, 0))
    path = save_image(image, output_dir=tmp_path / "out", filename="test.png")

    assert path.exists()
    with Image.open(path) as saved:
        assert saved.format == "PNG"
        assert saved.size == (10, 10)
