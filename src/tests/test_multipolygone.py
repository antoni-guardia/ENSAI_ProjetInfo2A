import pytest
from business_object.multipolygone import MultiPolygone
import re


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
    points_dedans = {(-0.06, -3.53), (-1.44, -2.51), (3.36, -0.11), (2.84, -4.38),
                     (6.74, -1.05), (1.36, 1.81)}
    points_dehors = {(1, -2), (3.76, -4.49), (3.54, 0.63), (4.38, -0.88)}

    for point in points_dedans:
        assert multipolygone_etrange._est_dedans(point)

    for point in points_dehors:
        assert not multipolygone_etrange._est_dedans(point)


def test_multipolygone_point_raises():

    with pytest.raises(TypeError, match="Point est de type tuple."):
        pytest.multipolygone_simple._est_dedans("5")
        pytest.multipolygone_simple._est_dedans(("5", 1))


def test_multipolygone_contour_raises():

    non_contours = [5, [], [[]], [["1"]], [[dict()]],

                    [[[dict(), (0, 1), (1, 1), (1, 0)]]],

                    [[[[(0, 0), (0, 1), (1, 1), (1, 0)]]]],

                    [[[(0, 0), (0, 1), (1, 1), (1, 0)]],
                     [[(2, 2), (2, 2.5), (2.5, 2.5), []]]]
                    ]

    for non_contour in non_contours:
        with pytest.raises(TypeError,
                           match=re.escape("Contour est de type list[list[list[tuple]]].")):
            MultiPolygone(contour=non_contour)


def test_multipolygone_contour(multipolygone_simple_param,
                               multipolygone_forme_etrange_param):

    assert pytest.multipolygone_simple.contour == multipolygone_simple_param["contour"]

    poly_test = pytest.multipolygone_forme_etrange
    poly_test._est_dedans((4.5, 3.7))

    assert poly_test.contour == multipolygone_forme_etrange_param["contour"]


def test_points_rectangle():

    assert pytest.multipolygone_simple.points_rectangle == [0, 0, 1, 1]

    assert pytest.multipolygone_forme_etrange.points_rectangle == [-2.54, -6.23, 8.38, 3.79]
