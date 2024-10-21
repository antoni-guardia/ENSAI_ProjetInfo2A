import pytest
from business_object.point import Point as P
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
        assert pytest.zonage_0.trouver_zone(points[i]) == zones[i], f"Erreur pour le point {points[i]} : zone attendue {zones[i]}"
