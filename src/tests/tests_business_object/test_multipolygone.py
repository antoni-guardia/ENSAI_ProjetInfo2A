import pytest
from business_object.multipolygone import MultiPolygone
from business_object.point import Point as P
import re


# Tests methodes


def test_multipolygone_est_dedans():
    """
    Teste si un point est dans multipolygone
    """
    multipolygone_sans_id = pytest.multipolygone_sans_id

    assert not multipolygone_sans_id.est_dedans(P(2.2, 2.2))
    assert multipolygone_sans_id.est_dedans(P(0.5, 0.5))
    assert multipolygone_sans_id.est_dedans(P(0.1, 0.1))
    assert not multipolygone_sans_id.est_dedans(P(0.8, 0.8))


def test_multipolygone_id_est_dedans():
    """
    Teste si l'id de multipolygone est dedans
    """
    multipolygone_avec_id = pytest.multipolygone_avec_id
    points_dedans = [
        P(-0.06, -3.53),
        P(-1.44, -2.51),
        P(3.36, -0.11),
        P(2.84, -4.38),
        P(6.74, -1.05),
        P(1.36, 1.81),
    ]
    points_dehors = [P(1, -2), P(3.76, -4.49), P(3.54, 0.63), P(4.38, -0.88)]

    for point in points_dedans:
        assert multipolygone_avec_id.est_dedans(point)

    for point in points_dehors:
        assert not multipolygone_avec_id.est_dedans(point)


def test_multipolygone_point_raises():
    """
    Teste si c'est le bon type
    """
    with pytest.raises(TypeError, match="point doit être de type Point"):
        pytest.multipolygone_sans_id.est_dedans("5")
        pytest.multipolygone_avec_id.est_dedans((5, 1))


def test_multipolygone_polygones_raises():
    """
    Teste si c'est le bon type
    """
    non_polygones = [
        5,
        [],
        [[]],
        [["1"]],
        [[dict()]],
        [[[dict(), (0, 1), (1, 1), (1, 0)]]],
        [[[[(0, 0), (0, 1), (1, 1), (1, 0)]]]],
        [
            [[P(0, 0), P(0, 1), P(1, 1), P(1, 0)]],
            [
                [
                    P(2, 2),
                    P(2, 2.5),
                    P(2.5, 2.5),
                ]
            ],
        ],
    ]

    for non_polygone in non_polygones:
        with pytest.raises(TypeError, match=re.escape("polygones est une liste de contour")):
            MultiPolygone(polygones=non_polygones)


def test_points_rectangle():

    assert pytest.m_0_0_3.coord_rectangle == [0, 0, 1, 1]

    assert pytest.multipolygone_avec_id.coord_rectangle == [-2.54, -6.23, 8.38, 3.79]
