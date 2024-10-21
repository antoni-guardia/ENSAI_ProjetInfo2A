import pytest
from business_object.point import Point as P
from business_object.zonage import Zonage
# import re


# Tests methodes
def test_zonage_trouver_zone_simple():

    points = [P(100, 35), P(1, 1), P(1.25, 1.25), P(2, -1)]

    zones = [None,
             pytest.zone_1_0_1,
             pytest.zone_1_0_1,
             pytest.zone_1_1_1]

    for i in range(len(points)):
        print(pytest.zonage_1.trouver_zone(points[i]))

    assert pytest.zonage_1.trouver_zone(points[i]) == zones[i]


def test_zonage_trouver_zone_complexe():
    points = [P(100, 35), P(.25, .25), P(1.25, 1.25), P(2, -1.25)]

    zones = [None,
             pytest.zone_0_0_3,
             pytest.zone_0_0_2,
             pytest.zone_0_1_2]

    for i in range(len(points)):
        assert pytest.zonage_0.trouver_zone(points[i]) == zones[i]


def test_zonage_init_type_error():
    nom = "Test Zonage"
    zones = [[], []]  # Create a list of Zone instances
    annee = 2024

    with pytest.raises(TypeError, match="id de type int ou None."):
        # Pass an invalid id type (e.g., a string)
        Zonage(nom=nom, zones=zones, annee=annee, id="invalid_id")

    with pytest.raises(TypeError, match="id de type int ou None."):
        # Pass an invalid id type (e.g., a float)
        Zonage(nom=nom, zones=zones, annee=annee, id=3.14)

    with pytest.raises(TypeError, match="id de type int ou None."):
        # Pass an invalid id type (e.g., a list)
        Zonage(nom=nom, zones=zones, annee=annee, id=[1, 2, 3])
