from src import app
from src.app import main
from src.config.settings import OUTPUT_DIR, OUTPUT_FILENAME


def test_main_saves_captcha(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr("builtins.input", lambda prompt="": "n")

    main()

    assert (tmp_path / OUTPUT_DIR / OUTPUT_FILENAME).exists()
    assert "CAPTCHA guardado" in capsys.readouterr().out


def test_main_downloads_when_user_says_yes(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr("builtins.input", lambda prompt="": "s")
    downloads = tmp_path / "downloads"
    monkeypatch.setattr(app, "download_image", lambda image: _save(image, downloads))

    main()

    assert (downloads / "captcha.png").exists()
    assert "Download concluído" in capsys.readouterr().out


def _save(image, folder):
    folder.mkdir(parents=True)
    path = folder / "captcha.png"
    image.save(path, format="PNG")
    return path
