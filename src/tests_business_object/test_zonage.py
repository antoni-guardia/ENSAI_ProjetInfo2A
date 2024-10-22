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

    for i in range(len(points)):
        assert pytest.zonage_1.trouver_zone(points[i]) == zones[i], f"Erreur pour le point {points[i]} : zone attendue {zones[i]}"


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


def test_zonage_initialization():
    """
    Test if the Zonage class initializes correctly with valid inputs.
    """
    zones = [[],[]]  # Creating a list of zones
    zonage = Zonage(nom="Zonage Test", zones=zones, annee=2024)

    assert zonage._nom == "Zonage Test"
    assert zonage._zones == zones
    assert zonage._annee == 2024
    assert zonage._zonage_mere is None
    assert zonage.id is None


def test_zonage_with_zonage_mere():
    """
    Test Zonage initialization when a parent zonage (zonage_mere) is provided.
    """
    zones = [[]]
    zonage_mere = Zonage(nom="Parent Zonage", zones=zones, annee=2020)
    zonage = Zonage(nom="Child Zonage", zones=zones, annee=2024, zonage_mere=zonage_mere)

    assert zonage._nom == "Child Zonage"
    assert zonage._zonage_mere == zonage_mere


def test_zonage_with_id():
    """
    Test Zonage initialization when an ID is provided.
    """
    zones = [[],[]]
    zonage = Zonage(nom="Zonage with ID", zones=zones, annee=2024, id=101)

    assert zonage._nom == "Zonage with ID"
    assert zonage.id == 101


def test_zonage_invalid_id():
    """
    Test if the Zonage class raises a TypeError when id is not an int or None.
    """
    zones = [[]]
    with pytest.raises(TypeError):
        Zonage(nom="Invalid ID Zonage", zones=zones,
               annee=2024, id="invalid_id")


def test_zonage_no_zones():
    """
    Test if Zonage initializes correctly with an empty list of zones.
    """
    zonage = Zonage(nom="Empty Zones Zonage", zones=[], annee=2024)

    assert zonage._zones == []
