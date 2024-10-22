import pytest
from business_object.point import Point as P
from business_object.zone import Zone
from business_object.zonage import Zonage


def test_zonage_initialisation():
    # Test avec des valeurs valides
    zones = [pytest.zone_1_0_1, pytest.zone_1_1_1]
    zonage = Zonage(nom="Zonage Test", zones=zones, annee=2023, id=1)

    assert zonage.nom == "Zonage Test"
    assert zonage.annee == 2023
    assert zonage.id == 1
    assert zonage.zonage_mere is None
    assert zonage.zones == zones

    # Test avec zonage_mere
    zonage_mere = Zonage(nom="Zonage Mère", zones=zones, annee=2022)
    zonage_fille = Zonage(nom="Zonage Fille", zones=zones, annee=2023, zonage_mere=zonage_mere)

    assert zonage_fille.zonage_mere == zonage_mere

    # Test avec une valeur de `id` non valide
    with pytest.raises(TypeError):
        Zonage(nom="Zonage Erreur", zones=zones, annee=2023, id="invalid_id")


# Tests methodes ------------------------------------------------------------

def test_zonage_trouver_zone_simple():
    """
    Teste la méthode trouver_zone pour un zonage simple sans zonage mère.
    """
    points = [P(100, 35), P(1, 1), P(1.25, 1.25), P(2, -1)]
    
    # Les zones attendues en fonction des points (à ajuster selon ta config)
    zones = [None,
             pytest.zone_1_0_1,
             pytest.zone_1_0_1,
             pytest.zone_1_1_1]

    for i, point in enumerate(points):
        assert pytest.zonage_1.trouver_zone(point) == zones[i], (
            f"Erreur pour le point {point} : zone attendue {zones[i]}"
        )


def test_zonage_trouver_zone_complexe():
    """
    Teste la méthode trouver_zone pour un zonage avec une zonage mère.
    """
    points = [P(100, 35), P(0.25, 0.25), P(1.25, 1.25), P(2, -1.25)]

    # Zones attendues pour les points (doivent correspondre à la configuration du zonage mère)
    zones = [None,
             pytest.zone_0_0_3,
             pytest.zone_0_0_2,
             pytest.zone_0_1_2]

    for i, point in enumerate(points):
        assert pytest.zonage_0.trouver_zone(point) == zones[i], (
            f"Erreur pour le point {point} : zone attendue {zones[i]}"
        )


def test_zonage_trouver_zones():
    """
    Teste la méthode trouver_zones qui trouve les zones pour une liste de points.
    """
    points = [P(100, 35), P(1, 1), P(1.25, 1.25), P(2, -1)]
    zones_attendues = [None, pytest.zone_1_0_1, pytest.zone_1_0_1, pytest.zone_1_1_1]

    resultat = pytest.zonage_1.trouver_zones(points)
    assert resultat == zones_attendues, f"Erreur : zones attendues {zones_attendues}, obtenu {resultat}"



def test_zonage_trouver_zones_chemins():
    """
    Teste la méthode trouver_zones_chemins qui renvoie le chemin des zones pour plusieurs points.
    """
    points = [P(1, 1), P(2, -1)]
    chemins_attendus = ["Zone mère 1/Zone 1.0.1", "Zone mère 1/Zone 1.1.1"]  

    chemins_obtenus = pytest.zonage_1.trouver_zones_chemins(points)
    assert chemins_obtenus == chemins_attendus, f"Erreur : chemins attendus {chemins_attendus}, obtenu {chemins_obtenus}"


def test_zonage_trouver_zone_avec_mere():
    """
    Teste la méthode trouver_zone avec une zonage mère.
    """
    point_dans_zone_fille = P(0.5, 0.5)
    point_hors_zone = P(100, 100)

    # Zonage mère et fille définis
    zone_fille = pytest.zone_1_0_1
    zonage_mere = Zonage(nom="Zonage Mère", zones=[pytest.zone_0_0_3], annee=2023)
    zonage_fille = Zonage(nom="Zonage Fille", zones=[zone_fille], annee=2023, zonage_mere=zonage_mere)

    # Point dans la zone fille
    assert zonage_fille.trouver_zone(point_dans_zone_fille) == zone_fille, "Erreur pour la recherche dans zone fille"

    # Point hors de toute zone
    assert zonage_fille.trouver_zone(point_hors_zone) is None, "Erreur pour la recherche hors zone"


def test_zonage_trouver_zone_chemin():
    """
    Teste la méthode trouver_zone_chemin pour un point dans une zone fille
    et un point hors de toute zone.
    """
    point_dans_zone_fille = P(0.5, 0.5)
    point_hors_zone = P(100, 100)

    # Zonage mère et fille définis
    zone_fille = pytest.zone_1_0_1
    zonage_mere = Zonage(nom="Zonage Mère", zones=[pytest.zone_0_0_3], annee=2023)
    zonage_fille = Zonage(nom="Zonage Fille", zones=[zone_fille], annee=2023, zonage_mere=zonage_mere)

    # Chemin pour le point dans la zone fille
    chemin_attendu = "Zonage Mère/Zone Fille"
    assert zonage_fille.trouver_zone_chemin(point_dans_zone_fille) == chemin_attendu, "Erreur sur le chemin attendu"

    # Chemin pour un point hors zone
    assert zonage_fille.trouver_zone_chemin(point_hors_zone) == "", "Erreur pour le chemin hors zone"


def test_zonage_trouver_zones_vide():
    """
    Teste la méthode trouver_zones avec une liste vide de points.
    """
    points = []
    zones_attendues = []

    resultat = pytest.zonage_1.trouver_zones(points)
    assert resultat == zones_attendues, "Erreur pour la liste vide"


def test_zonage_trouver_zones_chemins_vide():
    """
    Teste la méthode trouver_zones_chemins avec une liste vide de points.
    """
    points = []
    chemins_attendus = []

    resultat = pytest.zonage_1.trouver_zones_chemins(points)
    assert resultat == chemins_attendus, "Erreur pour la liste vide de chemins"

# Tests des propriétés -------------------------------------------------------


def test_zonage_proprietes():
    """
    Teste les propriétés de base de la classe Zonage.
    """
    assert pytest.zonage_1.nom == "Zonage 1", f"Erreur : nom attendu 'Zonage 1', obtenu {pytest.zonage_1.nom}"
    assert pytest.zonage_1.annee == 2023, f"Erreur : année attendue 2023, obtenu {pytest.zonage_1.annee}"
    assert pytest.zonage_1.zonage_mere is None, "Erreur : zonage_mere attendu None"
    assert isinstance(pytest.zonage_1.zones, list), "Erreur : zones attendu comme liste"


def test_erreur_point():
    """
    Teste la méthode privée __erreur_point pour s'assurer qu'elle lève bien une exception
    si le point n'est pas du bon type.
    """
    with pytest.raises(TypeError):
        pytest.zonage_1.trouver_zone((1, 1))  # Passer un tuple au lieu d'un objet Point


def test_trouver_zone_limites():
    points = [P(0, 0), P(1, 1), P(1.5, 1.5), P(3, -1)]  # points aux limites
    zones = [pytest.zone_1_0_1, pytest.zone_1_0_1, None, pytest.zone_1_1_1]
    for i in range(len(points)):
        assert pytest.zonage_1.trouver_zone(points[i]) == zones[i], f"Erreur pour le point limite {points[i]}"


def test_zonage_proprietes_accesseurs():
    """
    Teste les accesseurs des propriétés (nom, annee, zonage_mere, zones).
    """
    zones = [pytest.zone_1_0_1, pytest.zone_1_1_1]
    zonage = Zonage(nom="Zonage Test", zones=zones, annee=2023)

    assert zonage.nom == "Zonage Test", "Erreur sur la propriété nom"
    assert zonage.annee == 2023, "Erreur sur la propriété annee"
    assert zonage.zonage_mere is None, "Erreur sur la propriété zonage_mere"
    assert zonage.zones == zones, "Erreur sur la propriété zones"


def test_erreur_point_type():
    """
    Teste que la méthode __erreur_point lève une exception pour des points de type incorrect.
    """
    with pytest.raises(TypeError):
        pytest.zonage_1.trouver_zone("invalid_point")  # Passer une chaîne au lieu d'un objet Point



#######################################################################################################################################





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
