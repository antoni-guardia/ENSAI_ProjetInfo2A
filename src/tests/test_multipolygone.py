import pytest
from src.classes.multipolygone import MultiPolygone


# Tests de typage
def test_multipolygone_init_raise_error(multipolygone_simple):

    a = MultiPolygone(multipolygone_simple["contour"])
    # Escriu un test que faci alguna cosa amb el multipolygone
    assert isinstance(a, MultiPolygone)


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


def test_multipolygone_est_dedans_complexe():

    multipolygone_complexe = pytest.multipolygone_complexe

    assert not multipolygone_complexe._est_dedans((2.2, 2.2))
    assert multipolygone_complexe._est_dedans((0.5, 0.5))
    assert multipolygone_complexe._est_dedans((0.1, 0.1))
    assert not multipolygone_complexe._est_dedans((0.8, 0.8))


def test_multipolygone_est_dedans_forme_etrange():

    multipolygone_etrange = pytest.multipolygone_forme_etrange
    points_dedans = [(-0.06, -3.53), (-1.44, -2.51), (3.36, -0.11), (2.84, -4.38),
                     (6.74, -1.05), (1.36, 1.81)]
    points_dehors = [(1, -2), (3.76, -4.49), (3.54, 0.63), (4.38, -0.88)]

    for point in points_dedans:
        assert multipolygone_etrange._est_dedans(point)

    for point in points_dehors:
        assert not multipolygone_etrange._est_dedans(point)
