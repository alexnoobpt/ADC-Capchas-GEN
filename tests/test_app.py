from src.app import main
from src.config.settings import OUTPUT_DIR, OUTPUT_FILENAME


def test_main_saves_captcha(tmp_path, monkeypatch, capsys):
    # Corre numa pasta temporária para não sujar o projeto
    monkeypatch.chdir(tmp_path)

    main()

    assert (tmp_path / OUTPUT_DIR / OUTPUT_FILENAME).exists()
    assert "CAPTCHA guardado" in capsys.readouterr().out
