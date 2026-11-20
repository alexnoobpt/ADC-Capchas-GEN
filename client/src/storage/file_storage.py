"""Gravação das imagens no disco e download para a pasta do utilizador."""

import itertools
import os
import re
import sys
from pathlib import Path

from PIL import Image

from src.config.settings import DOWNLOADS_DIR, OUTPUT_DIR, OUTPUT_FILENAME

MAX_FILENAME_LENGTH = 100

WINDOWS_RESERVED_NAMES = {
    "CON", "PRN", "AUX", "NUL",
    *(f"COM{i}" for i in range(1, 10)),
    *(f"LPT{i}" for i in range(1, 10)),
}


def save_image(
    image: Image.Image,
    output_dir: Path = OUTPUT_DIR,
    filename: str = OUTPUT_FILENAME,
    overwrite: bool = True,
) -> Path:
    """Guarda a imagem em PNG dentro de `output_dir` e devolve o caminho do ficheiro.

    Por defeito, um ficheiro com o mesmo nome é substituído. Com
    `overwrite=False`, é acrescentado um número ao nome (`captcha_1.png`,
    `captcha_2.png`, ...) em vez de o sobrescrever.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / filename

    if overwrite:
        image.save(path, format="PNG")
        return path

    for number in itertools.count():
        candidate = path if number == 0 else path.with_name(f"{path.stem}_{number}{path.suffix}")
        try:
            # O modo "xb" falha se o ficheiro já existir, por isso nunca
            # sobrescreve, mesmo com dois downloads ao mesmo tempo
            with open(candidate, "xb") as file:
                image.save(file, format="PNG")
        except FileExistsError:
            continue
        except Exception:
            candidate.unlink(missing_ok=True)
            raise
        return candidate


def download_image(
    image: Image.Image,
    filename: str = "captcha",
    folder: Path | str | None = None,
) -> Path:
    """Guarda a imagem como PNG na pasta de downloads e devolve o caminho.

    Se `folder` não for indicado, é usada a `DOWNLOADS_DIR` das definições ou,
    se for None, a pasta Downloads do utilizador (descoberta só no momento da
    chamada). Nunca sobrescreve ficheiros existentes.
    """
    if folder is None:
        folder = DOWNLOADS_DIR or _default_downloads_dir()
    return save_image(image, Path(folder), f"{_safe_filename(filename)}.png", overwrite=False)


def _windows_downloads_dir() -> Path | None:
    """Lê do registo do Windows onde está a pasta Downloads (pode estar no OneDrive)."""
    import winreg

    key_path = r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders"
    downloads_guid = "{374DE290-123F-4565-9164-39C4925E467B}"
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path) as key:
            value, _ = winreg.QueryValueEx(key, downloads_guid)
    except OSError:
        return None
    return Path(os.path.expandvars(value))


def _xdg_downloads_dir(home: Path) -> Path | None:
    """Lê do `user-dirs.dirs` onde está a pasta de downloads (ex.: ~/Transferências)."""
    config_home = Path(os.environ.get("XDG_CONFIG_HOME") or home / ".config")
    try:
        text = (config_home / "user-dirs.dirs").read_text(encoding="utf-8")
    except OSError:
        return None

    match = re.search(r'^XDG_DOWNLOAD_DIR="(.+)"', text, re.MULTILINE)
    if not match:
        return None
    return Path(match.group(1).replace("$HOME", str(home)))


def _default_downloads_dir() -> Path:
    """Descobre a pasta de downloads do utilizador.

    Respeita pastas movidas (Windows/OneDrive) ou traduzidas (Linux). Se não
    for possível descobrir, usa `~/Downloads`; se nem existir diretório home
    (ex.: alguns CI ou containers), usa a pasta atual.
    """
    try:
        home = Path.home()
    except RuntimeError:
        return Path.cwd()

    if sys.platform == "win32":
        found = _windows_downloads_dir()
    else:
        found = _xdg_downloads_dir(home)
    return found or home / "Downloads"


def _safe_filename(name: str) -> str:
    """Limpa o nome para ser usado como nome de ficheiro.

    Remove uma extensão `.png` no fim, substitui os caracteres que não sejam
    letras, números, `_` ou `-` por `_`, limita o tamanho e evita os nomes
    reservados do Windows (CON, NUL, ...). Se o resultado ficar vazio,
    devolve "captcha".
    """
    name = re.sub(r"\.png$", "", name.strip(), flags=re.IGNORECASE)

    cleaned = re.sub(r"[^\w\-]", "_", name)[:MAX_FILENAME_LENGTH].strip("_")
    if not cleaned:
        return "captcha"
    if cleaned.upper() in WINDOWS_RESERVED_NAMES:
        return f"_{cleaned}"
    return cleaned
