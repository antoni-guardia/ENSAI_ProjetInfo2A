import pytest
from business_object.point import Point as P
# import re


# Tests methodes
def test_zone_est_dedans():

    zone = pytest.zone_0_0_1

    assert not zone.point_dans_zone(P(0.5, 0.5))
    assert zone.point_dans_zone(P(0.5, 1.5))
