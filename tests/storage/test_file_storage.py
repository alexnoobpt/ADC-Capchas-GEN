"""Testes da gravação e do download (nunca escrevem na pasta Downloads real)."""

from pathlib import Path

from PIL import Image

from src.captcha.generator import generate_captcha
from src.storage import file_storage
from src.storage.file_storage import _safe_filename, download_image, save_image


def test_save_image_creates_png(tmp_path):
    image = Image.new("RGB", (10, 10), (255, 0, 0))
    path = save_image(image, output_dir=tmp_path / "out", filename="test.png")

    assert path.exists()
    with Image.open(path) as saved:
        assert saved.format == "PNG"
        assert saved.size == (10, 10)


def test_save_image_cria_png(tmp_path):
    path = save_image(generate_captcha("ABC"), tmp_path, "x.png")

    assert path == tmp_path / "x.png"
    with Image.open(path) as img:
        assert img.format == "PNG"


def test_save_image_substitui_por_defeito(tmp_path):
    save_image(generate_captcha("ABC"), tmp_path, "x.png")
    path = save_image(generate_captcha("ABC"), tmp_path, "x.png")

    assert path.name == "x.png"
    assert len(list(tmp_path.iterdir())) == 1


def test_save_image_sem_overwrite_numera(tmp_path):
    imagem = generate_captcha("ABC")
    nomes = [
        save_image(imagem, tmp_path, "x.png", overwrite=False).name for _ in range(3)
    ]

    assert nomes == ["x.png", "x_1.png", "x_2.png"]


def test_download_cria_png(tmp_path):
    path = download_image(generate_captcha("ABC"), "ABC", folder=tmp_path)

    assert path == tmp_path / "ABC.png"
    with Image.open(path) as img:
        assert img.format == "PNG"


def test_download_nao_sobrescreve(tmp_path):
    imagem = generate_captcha("ABC")
    nomes = [download_image(imagem, "ABC", folder=tmp_path).name for _ in range(3)]

    assert nomes == ["ABC.png", "ABC_1.png", "ABC_2.png"]


def test_download_cria_pasta(tmp_path):
    pasta = tmp_path / "novo" / "sub"
    path = download_image(generate_captcha("ABC"), folder=pasta)
    assert path.parent == pasta and path.exists()


def test_pasta_das_definicoes(tmp_path, monkeypatch):
    monkeypatch.setattr(file_storage, "DOWNLOADS_DIR", tmp_path)
    path = download_image(generate_captcha("ABC"))
    assert path.parent == tmp_path


def test_pasta_descoberta(tmp_path, monkeypatch):
    monkeypatch.setattr(file_storage, "DOWNLOADS_DIR", None)
    monkeypatch.setattr(file_storage, "_default_downloads_dir", lambda: tmp_path)
    path = download_image(generate_captcha("ABC"))
    assert path.parent == tmp_path


def test_import_e_pasta_sem_home(monkeypatch, tmp_path):
    def sem_home():
        raise RuntimeError("sem home")

    monkeypatch.setattr(Path, "home", sem_home)
    monkeypatch.chdir(tmp_path)
    assert file_storage._default_downloads_dir() == Path.cwd()


def test_pasta_xdg_traduzida(tmp_path, monkeypatch):
    (tmp_path / "user-dirs.dirs").write_text(
        'XDG_DOWNLOAD_DIR="$HOME/Transferências"\n', encoding="utf-8"
    )
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    home = Path("/home/aluno")
    assert file_storage._xdg_downloads_dir(home) == home / "Transferências"


def test_safe_filename_caracteres_invalidos():
    assert _safe_filename("a/b:c*d") == "a_b_c_d"


def test_safe_filename_vazio():
    assert _safe_filename("") == "captcha"
    assert _safe_filename("///") == "captcha"


def test_safe_filename_extensao_png():
    assert _safe_filename("meu.png") == "meu"
    assert _safe_filename("MEU.PNG") == "MEU"


def test_safe_filename_nomes_reservados():
    assert _safe_filename("CON") == "_CON"
    assert _safe_filename("nul") == "_nul"
    assert _safe_filename("COM1") == "_COM1"


def test_safe_filename_nome_longo(tmp_path):
    nome = _safe_filename("a" * 500)
    assert len(nome) <= file_storage.MAX_FILENAME_LENGTH
    path = download_image(generate_captcha("ABC"), "a" * 500, folder=tmp_path)
    assert path.exists()


def test_save_image_sem_overwrite_nao_deixa_ficheiro_vazio(tmp_path, monkeypatch):
    imagem = generate_captcha("ABC")

    def falha(*args, **kwargs):
        raise OSError("disco cheio")

    monkeypatch.setattr(imagem, "save", falha)
    try:
        save_image(imagem, tmp_path, "x.png", overwrite=False)
    except OSError:
        pass
    assert not (tmp_path / "x.png").exists()
