import pytest
from business_object.point import Point as P
from business_object.zone import Zone as Z

# import re


def test_init_zone():
    multipolygone = pytest.multipolygone_avec_id

    assert isinstance(Z("zone1", multipolygone, 1555, 4545, 95), Z)


def test_zone_erreur_nom():

    multipolygone = pytest.multipolygone_avec_id

    with pytest.raises(TypeError, match="id de type int ou None."):
        Z("test", multipolygone, id="t")


def test_hash_zone():
    zone = pytest.zone_0_0_1

    assert isinstance(hash(zone), int)


def test_zone_est_dedans():

    zone = pytest.zone_0_0_1

    assert not zone.point_dans_zone(P(0.5, 0.5))
    assert zone.point_dans_zone(P(0.5, 1.5))
