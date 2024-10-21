import pytest
from business_object.point import Point
from business_object.contour import Contour


def test_initialisation_valide():
    """
    Teste l'initialisation valide d'un Contour.
    """
    points = [Point(0, 0), Point(0, 4), Point(4, 4), Point(4, 0)]
    contour = Contour(points)

    assert contour.points == points, "La liste de points du contour doit correspondre à celle fournie."
    assert contour.coord_rectangle == [0, 0, 4, 4], "Le rectangle englobant est incorrect."


def test_initialisation_invalide():
    """
    Teste les cas d'initialisation invalide d'un Contour.
    """
    with pytest.raises(TypeError):
        Contour("not_a_list")  # Le paramètre doit être une liste de points
    with pytest.raises(TypeError):
        Contour([Point(0, 0), "not_a_point"])  # Tous les éléments doivent être des instances de Point
    with pytest.raises(TypeError):
        Contour([Point(0, 0), Point(4, 4)], "not_an_int")  # L'ID doit être un int ou None


def test_est_dedans():
    """
    Teste la méthode est_dedans du Contour.
    """
    points = [Point(0, 0), Point(0, 4), Point(4, 4), Point(4, 0)]
    contour = Contour(points)

    # Point à l'intérieur du contour
    point_dedans = Point(2, 2)
    assert contour.est_dedans(point_dedans) is True, "Le point devrait être à l'intérieur du contour."

    # Point à l'extérieur du contour
    point_dehors = Point(5, 5)
    assert contour.est_dedans(point_dehors) is False, "Le point devrait être à l'extérieur du contour."

    # Point sur le bord du contour
    point_bord = Point(0, 2)
    assert contour.est_dedans(point_bord) is True, "Le point sur le bord devrait être considéré à l'intérieur."


def test_point_dans_rectangle():
    """
    Teste la méthode privée __point_dans_rectangle du Contour.
    """
    points = [Point(0, 0), Point(0, 4), Point(4, 4), Point(4, 0)]
    contour = Contour(points)

    # Point dans le rectangle mais pas forcément dans le contour
    point_dans_rectangle = Point(3, 3)
    assert contour._Contour__point_dans_rectangle(point_dans_rectangle) is True, "Le point doit être dans le rectangle."

    # Point en dehors du rectangle
    point_dehors_rectangle = Point(5, 5)
    assert contour._Contour__point_dans_rectangle(point_dehors_rectangle) is False, "Le point ne doit pas être dans le rectangle."


def test_coord_rectangle():
    """
    Teste que les coordonnées du plus petit rectangle englobant sont correctes.
    """
    points = [Point(1, 1), Point(1, 5), Point(5, 5), Point(5, 1)]
    contour = Contour(points)

    assert contour.coord_rectangle == [1, 1, 5, 5], "Les coordonnées du rectangle sont incorrectes."
