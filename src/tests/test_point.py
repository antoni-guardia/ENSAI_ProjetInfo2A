import pytest
from src.business_object.point import Point

class TestPoint:

    def test_point_init_x_invalid(self):
        """
        Teste que l'initialisation échoue si x n'est pas un float.
        """
        with pytest.raises(TypeError, match="Les coordonnées x et y doivent être des nombres flottants."):
            Point(3, 4.2)
  
    def test_point_init_y_invalid(self):
        """
        Teste que l'initialisation échoue si y n'est pas un float.
        """
        with pytest.raises(TypeError, match="Les coordonnées x et y doivent être des nombres flottants."):
            Point(3.3, 4)

    def test_point_init_valid_floats(self):
        """
        Teste l'initialisation correcte d'un Point avec des coordonnées en float.
        """
        p = Point(3.5, 4.7)
        assert p.x == 3.5
        assert p.y == 4.7

    def test_point_type_error1(self):
        """
        Teste que l'initialisation échoue si x ou y sont des chaînes de caractères.
        """
        with pytest.raises(TypeError, match="Les coordonnées x et y doivent être des nombres flottants."):
            Point('3', '4.5')

    def test_point_type_error2(self):
        """
        Teste que l'initialisation échoue si x ou y ne sont pas des nombres valides.
        """
        with pytest.raises(TypeError, match="Les coordonnées x et y doivent être des nombres flottants."):
            Point('abc', 'xyz')
