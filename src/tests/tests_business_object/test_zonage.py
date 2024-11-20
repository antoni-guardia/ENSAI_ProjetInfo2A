import pytest
from business_object.point import Point as P

# from business_object.zone import Zone
from business_object.zonage import Zonage


def test_zonage_initialisation():
    # Test avec des valeurs valides
    zones = [pytest.zone_1_0_1, pytest.zone_1_1_1]
    zonage = Zonage(nom="Zonage Test", zones=zones, id=1)

    assert zonage.nom == "Zonage Test"
    assert zonage.id == 1
    assert zonage.zonage_mere is None
    assert zonage.zones == zones

    # Test avec zonage_mere
    zonage_mere = Zonage(nom="Zonage Mère", zones=zones)
    zonage_fille = Zonage(nom="Zonage Fille", zones=zones, zonage_mere=zonage_mere)

    assert zonage_fille.zonage_mere == zonage_mere

    # Test avec une valeur de `id` non valide
    with pytest.raises(TypeError):
        Zonage(nom="Zonage Erreur", zones=zones, id="invalid_id")


# Tests methodes ------------------------------------------------------------


def test_zonage_trouver_zone_simple():
    """
    Teste la méthode trouver_zone pour un zonage simple sans zonage mère.
    """
    points = [P(100, 35), P(1, 1), P(1.25, 1.25), P(2, -1)]

    # Les zones attendues en fonction des points (à ajuster selon ta config)
    zones = [None, pytest.zone_1_0_1, pytest.zone_1_0_1, pytest.zone_1_1_1]

    for i, point in enumerate(points):
        assert (
            pytest.zonage_1.trouver_zone(point) == zones[i]
        ), f"Erreur pour le point {point} : zone attendue {zones[i]}"


# Tests des propriétés -------------------------------------------------------


def test_erreur_point():
    """
    Teste la méthode privée __erreur_point pour s'assurer qu'elle lève bien une exception
    si le point n'est pas du bon type.
    """
    with pytest.raises(TypeError):
        pytest.zonage_1.trouver_zone((1, 1))  # Passer un tuple au lieu d'un objet Point


def test_zonage_proprietes_accesseurs():
    """
    Teste les accesseurs des propriétés (nom, zonage_mere, zones).
    """
    zones = [pytest.zone_1_0_1, pytest.zone_1_1_1]
    zonage = Zonage(nom="Zonage Test", zones=zones)

    assert zonage.nom == "Zonage Test", "Erreur sur la propriété nom"
    assert zonage.zonage_mere is None, "Erreur sur la propriété zonage_mere"
    assert zonage.zones == zones, "Erreur sur la propriété zones"


def test_erreur_point_type():
    """
    Teste que la méthode __erreur_point lève une exception pour des points de type incorrect.
    """
    with pytest.raises(TypeError):
        pytest.zonage_1.trouver_zone("invalid_point")  # Passer une chaîne au lieu d'un objet Point
