import pytest
from business_object.point import Point


def test_point_init_x_invalid():
    """
    Teste que l'initialisation échoue si x n'est pas un float ou int.
    """
    with pytest.raises(
        TypeError, match="Les coordonnées x et y doivent être des nombres flotants."
    ):
        Point("3", 4.2)


def test_point_init_y_invalid():
    """
    Teste que l'initialisation échoue si y n'est pas un float ou int.
    """
    with pytest.raises(
        TypeError, match="Les coordonnées x et y doivent être des nombres flotants."
    ):
        Point(3.3, "4")


def test_point_init_id_invalid():
    """
    Teste que l'initialisation échoue si l'id n'est pas un int ou None.
    """
    with pytest.raises(TypeError, match="id de type int ou None."):
        Point(3.3, 4.2, id="invalid")


def test_point_init_valid_floats():
    """
    Teste l'initialisation correcte d'un Point avec des coordonnées en float.
    """
    p = Point(3.5, 4.7)
    assert p.x == 3.5, "La coordonnée x est incorrecte."
    assert p.y == 4.7, "La coordonnée y est incorrecte."


def test_point_init_valid_ints():
    """
    Teste l'initialisation correcte d'un Point avec des coordonnées en int.
    """
    p = Point(3, 4)
    assert p.x == 3, "La coordonnée x est incorrecte."
    assert p.y == 4, "La coordonnée y est incorrecte."


def test_point_type_error_both_strings():
    """
    Teste que l'initialisation échoue si x et y sont des chaînes de caractères.
    """
    with pytest.raises(
        TypeError, match="Les coordonnées x et y doivent être des nombres flotants."
    ):
        Point("3", "4.5")  # x et y sont des chaînes de caractères


def test_point_type_error_non_numeric_strings():
    """
    Teste que l'initialisation échoue si x et y ne sont pas des nombres valides.
    """
    with pytest.raises(
        TypeError, match="Les coordonnées x et y doivent être des nombres flotants."
    ):
        Point("abc", "xyz")  # x et y sont des chaînes non numériques


def test_point_init_valid_with_id():
    """
    Teste l'initialisation correcte d'un Point avec un id valide.
    """
    p = Point(3.5, 4.7, id=1)
    assert p.x == 3.5, "La coordonnée x est incorrecte."
    assert p.y == 4.7, "La coordonnée y est incorrecte."
    assert p.id == 1, "L'ID est incorrect."


def test_point_init_id_none():
    """
    Teste l'initialisation correcte d'un Point avec id=None.
    """
    p = Point(3.5, 4.7, id=None)
    assert p.x == 3.5, "La coordonnée x est incorrecte."
    assert p.y == 4.7, "La coordonnée y est incorrecte."
    assert p.id is None, "L'ID devrait être None."
