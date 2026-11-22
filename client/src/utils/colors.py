import random

from src.config.settings import BACKGROUND_MAX, BACKGROUND_MIN, Color


def random_color(
    minimum: int = BACKGROUND_MIN,
    maximum: int = BACKGROUND_MAX,
    rng: random.Random | None = None,
) -> Color:
    """Devolve uma cor RGB aleatória com cada canal entre `minimum` e `maximum`."""
    if not 0 <= minimum <= maximum <= 255:
        raise ValueError("É preciso 0 <= minimum <= maximum <= 255")

    rng = rng or random
    return (
        rng.randint(minimum, maximum),
        rng.randint(minimum, maximum),
        rng.randint(minimum, maximum),
    )
