import pytest

from src import main as main_module
from src.storage import db
from src.user import accounts, login, passwords


@pytest.fixture
def run(tmp_path, monkeypatch):
    """Corre o menu com as respostas dadas e devolve as opções do menu principal usadas."""
    path = tmp_path / "test.sqlite"
    monkeypatch.setattr(passwords, "ITERATIONS", 1_000)
    login._dummy_hash.cache_clear()
    monkeypatch.setattr(main_module, "init_db", lambda: db.init_db(path))
    monkeypatch.setattr(accounts, "get_connection", lambda: db.get_connection(path))
    monkeypatch.setattr(login, "get_connection", lambda: db.get_connection(path))

    called = []
    monkeypatch.setattr(main_module, "menu_imagem", lambda: called.append("imagem"))
    monkeypatch.setattr(main_module.captchas, "main", lambda: called.append("captchas"))

    def feed(*values):
        it = iter(values)
        monkeypatch.setattr("builtins.input", lambda prompt="": next(it))
        monkeypatch.setattr(accounts, "getpass", lambda prompt="": next(it))
        monkeypatch.setattr(login, "getpass", lambda prompt="": next(it))
        main_module.main()
        return called

    return feed


REGISTAR = ("2", "ana", "ana@x.pt", "segredo1")


def test_exit_without_login(run):
    assert run("3") == []


def test_wrong_password_does_not_open_main_menu(run, capsys):
    assert run(*REGISTAR, "1", "ana", "errada", "3") == []
    assert "Menu principal" not in capsys.readouterr().out


def test_login_opens_main_menu_options(run):
    assert run(*REGISTAR, "1", "ana", "segredo1", "1", "2", "4") == ["imagem", "captchas"]


def test_logout_goes_back_to_login(run, capsys):
    run(*REGISTAR, "1", "ana", "segredo1", "3", "3")
    out = capsys.readouterr().out
    assert "Sessão terminada." in out
    assert out.rstrip().endswith("Exiting...")
