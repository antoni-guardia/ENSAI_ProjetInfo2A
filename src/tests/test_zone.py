import pytest
# from src.classes.multipolygone import MultiPolygone
# import re


# Tests methodes
def test_multipolygone_est_dedans_simple():

    multipolygone = pytest.multipolygone_simple

    assert multipolygone._est_dedans((0.5, 0.5))
    assert not multipolygone._est_dedans((1.5, 0.5))


def test_multipolygone_est_dedans_inclaves_exclaves():

    multipolygone_inclave = pytest.multipolygone_inclave
    multipolygone_exclave = pytest.multipolygone_exclave
    multipolygone_exclave_inclave = pytest.multipolygone_inclave_exclave

    # Multipolygone avec inclave
    assert not multipolygone_inclave._est_dedans((0.5, 0.5))

    # Multipolygone avec Exclave
    assert multipolygone_exclave._est_dedans((2.1, 2.1))

    # Multipolygone exclave et inclave
    assert multipolygone_exclave_inclave._est_dedans((2.1, 2.1))
    assert not multipolygone_exclave_inclave._est_dedans((0.5, 0.5))
