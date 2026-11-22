import pytest

from src.captchas import desafios
from src.captchas.desafios import EMOJI, MATEMATICO, TEXTO, gerar, resolver


@pytest.fixture
def answers(monkeypatch):
    def feed(*values):
        it = iter(values)
        monkeypatch.setattr("builtins.input", lambda prompt="": next(it))

    return feed


@pytest.mark.parametrize("dificuldade, tamanho", [("1", 6), ("2", 12), ("3", 18)])
def test_text_code_length_follows_difficulty(dificuldade, tamanho):
    desafio, solucao = gerar(TEXTO, dificuldade)
    assert len(desafio["codigo"]) == tamanho
    assert solucao == desafio["codigo"]
    assert not set(solucao) & set("£§")


def test_emoji_challenge_contains_the_solution():
    desafio, solucao = gerar(EMOJI, "2")
    assert desafio["categoria"] == "Comida"
    assert len(desafio["opcoes"]) == desafios.TOTAL_OPCOES_EMOJI
    assert len(solucao) == desafio["quantidade"] == 5
    opcoes = {desafios._sem_variacao(o) for o in desafio["opcoes"]}
    assert set(solucao) <= opcoes


def test_math_solution_matches_operation():
    for _ in range(50):
        desafio, solucao = gerar(MATEMATICO, "3")
        a, op, b = desafio["num1"], desafio["operador"], desafio["num2"]
        esperado = {"+": a + b, "-": a - b, "*": a * b, "/": round(a / b, 2)}[op]
        assert solucao == esperado


def test_text_answer(answers, monkeypatch):
    monkeypatch.setattr(desafios.random, "choice", lambda perguntas: perguntas[-1])
    answers("2")
    assert resolver(TEXTO, {"codigo": "ab!#C1"}, "ab!#C1")


def test_emoji_answer_without_spaces_and_selector(answers):
    desafio = {"categoria": "Comida", "quantidade": 2, "opcoes": ["🌶️", "🍕", "🐺"]}
    answers("🍕🌶")
    assert resolver(EMOJI, desafio, sorted(["🌶", "🍕"]))


def test_math_division_accepts_rounded_answer_with_comma(answers):
    answers("1,333")
    assert resolver(MATEMATICO, {"num1": 100, "operador": "/", "num2": 75}, 1.33)


def test_invalid_number_is_wrong(answers):
    answers("abc")
    assert not resolver(MATEMATICO, {"num1": 1, "operador": "+", "num2": 1}, 2)
