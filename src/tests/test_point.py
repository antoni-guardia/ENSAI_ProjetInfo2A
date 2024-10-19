import pytest
from business_object.point import Point

def test_point_init_x_invalid():
    """
    Teste que l'initialisation échoue si x n'est pas un float ou int.
    """
    with pytest.raises(TypeError, match="Les coordonnées x et y doivent être des nombres flotants."):  # Ensure the error message matches exactly
        Point('3', 4.2)  # Passing a string should raise a TypeError

def test_point_init_y_invalid():
    """
    Teste que l'initialisation échoue si y n'est pas un float ou int.    
    """
    with pytest.raises(TypeError, match="Les coordonnées x et y doivent être des nombres flotants."):
        Point(3.3, '4')  # Passing a string should raise a TypeError

def test_point_init_valid_floats():
    """
    Teste l'initialisation correcte d'un Point avec des coordonnées en float.
    """
    p = Point(3.5, 4.7)
    assert p.x == 3.5
    assert p.y == 4.7

def test_point_type_error1():
    """
    Teste que l'initialisation échoue si x ou y sont des chaînes de caractères.
    """
    with pytest.raises(TypeError, match="Les coordonnées x et y doivent être des nombres flotants."):
        Point('3', '4.5')  # Both values are strings, should raise TypeError

def test_point_type_error2():
    """
    Teste que l'initialisation échoue si x ou y ne sont pas des nombres valides.
    """
    with pytest.raises(TypeError, match="Les coordonnées x et y doivent être des nombres flotants."):
        Point('abc', 'xyz')  # Invalid non-numeric strings should raise TypeError
