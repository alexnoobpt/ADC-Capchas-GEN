from src.user.passwords import hash_password, verify_password


def test_correct_password_is_accepted():
    assert verify_password("segredo1", hash_password("segredo1"))


def test_wrong_password_is_rejected():
    assert not verify_password("errada", hash_password("segredo1"))


def test_same_password_gets_different_salt():
    assert hash_password("segredo1") != hash_password("segredo1")


def test_corrupted_hash_is_rejected():
    for stored in ["", "lixo", "zz:zz", None]:
        assert not verify_password("segredo1", stored)
