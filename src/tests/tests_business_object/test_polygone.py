import pytest
from business_object.contour import Contour
from business_object.point import Point
from business_object.polygone import Polygone

# Setup fixture to initialize the objects


@pytest.fixture
def setup_polygone():
    # Configuration du polygone à tester avec des points de type Point
    points_contour = [Point(0, 0), Point(0, 5), Point(5, 5), Point(5, 0)]
    contour = Contour(points_contour)
    polygone = Polygone([contour])
    return polygone


def test_est_dedans_true(setup_polygone):
    """
    Teste si un point est à l'intérieur du polygone
    """
    assert setup_polygone.est_dedans(Point(2, 2)) is True


def test_est_dedans_false(setup_polygone):
    """
    Teste si un point est à l'extérieur du polygone
    """
    assert setup_polygone.est_dedans(Point(6, 6)) is False
