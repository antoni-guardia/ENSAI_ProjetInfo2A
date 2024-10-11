import pytest
from src.business_object.contour import Contour
from src.business_object.polygone import Polygone

class TestPolygone:

    def setup_method(self):
        # Configuration du polygone a tester
        self.points_contour = [(0, 0), (0, 5), (5, 5), (5, 0)]
        self.contour = Contour(self.points_contour)
        self.polygone = Polygone(self.contour)

    def test_est_dedans_true(self):
        """
        Teste si un point à l'intérieur du polygone retourne True.
        """
        assert self.polygone.est_dedans((2, 2)) is True  # Point à l'intérieur

    def test_est_dedans_false(self):
        """
        Teste si un point à l'extérieur du polygone retourne False.
        """
        assert self.polygone.est_dedans((6, 6)) is False  # Point à l'extérieur

    def test_recherche_point_extremum(self):
        """
        Teste la recherche des points extrêmes.
        """
        extremum = self.polygone.recherche_point_extremum()
        assert extremum['min_x'] == 0
        assert extremum['max_x'] == 5
        assert extremum['min_y'] == 0
        assert extremum['max_y'] == 5

    def test_point_dans_rectangle_true(self):
        """
        Teste si un point à l'intérieur du rectangle retourné par recherche_point_extremum est vrai.
        """
        assert self.polygone.point_dans_rectangle((3, 3)) is True  # Point à l'intérieur du rectangle

    def test_point_dans_rectangle_false(self):
        """
        Teste si un point à l'extérieur du rectangle retourné par recherche_point_extremum est faux.
        """
        assert self.polygone.point_dans_rectangle((6, 3)) is False  # Point à l'extérieur du rectangle
