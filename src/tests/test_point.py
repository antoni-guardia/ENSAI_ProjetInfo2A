import pytest
#from src.business_object.point import Point
#import re


class TestPoint:

    def test_point_int(self):
        p = Point(3, 4)
        assert p.x == 3.0
        assert p.y == 4.0

    def test_point_floats(self):
        p = Point(3.5, 4.7)
        assert p.x == 3.5
        assert p.y == 4.7

    def test_point_strings(self):
        p = Point('3', '4.5')
        assert p.x == 3.0
        assert p.y == 4.5

    def test_point_value_error(self):
        with pytest.raises(ValueError):
           p = Point('abc', 'xyz')
