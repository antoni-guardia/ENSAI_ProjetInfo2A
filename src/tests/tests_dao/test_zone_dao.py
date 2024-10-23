import pytest
from unittest.mock import patch, MagicMock
from dao.zone_dao import ZoneDAO

@patch("dao.zone_dao.ZoneDAO.requete")
def test_inserer(mock_requete):
    """Test de la méthode __inserer() de ZoneDAO"""

    # GIVEN
    zone_dao = ZoneDAO()
    mock_requete.return_value = [{"id": 1}]

    # WHEN
    id_zone = zone_dao._ZoneDAO__inserer(1, "Zone Test", 1000, "12345", 2020)

    # THEN
    mock_requete.assert_called_once_with(
        "INSERT INTO Zone(id_zonage, nom, population, code_insee, annee) VALUES"
        " (%(id_zonage)s, %(nom)s, %(population)s, %(code_insee)s, %(annee)s)  RETURNING id;"
    )
    assert id_zone == 1

@log
def __CreerMultipolygone(self, id_zone: int, id_polygone: int) -> bool:
    res = self.requete(
        "INSERT INTO MultiPolygone (id_zone, id_polygone)"
        " VALUES (%(id_zone)s, %(id_polygone)s) RETURNING cardinal;",
        {
            "id_zone": id_zone,
            "id_polygone": id_polygone,
        },
    )
    if res:
        return True
    return False



@patch("dao.zone_dao.ZoneDAO._ZoneDAO__inserer")
@patch("dao.zone_dao.ZoneDAO._ZoneDAO__CreerMultipolygone")
@patch("dao.polygone_dao.PolygoneDAO.trouver_id")
@patch("dao.polygone_dao.PolygoneDAO.creer")
def test_creer(mock_creer_polygone, mock_trouver_id, mock_creer_multipolygone, mock_inserer):
    """Test de la méthode creer() de ZoneDAO"""

    # GIVEN
    zone_dao = ZoneDAO()
    mock_inserer.return_value = 1  # ID de la zone créée
    mock_trouver_id.side_effect = [None, 2]  # Le polygone n'existe pas donc on le crée
    mock_creer_polygone.return_value = 3  # ID du polygone créé
    mock_creer_multipolygone.return_value = True

    # Création d'une fausse zone avec un multipolygone
    zone = MagicMock()
    zone.nom = "Zone Test"
    zone.population = 1000
    zone.code_insee = "12345"
    zone.annee = 2020
    zone.multipolygone.polygones = [MagicMock()]

    # WHEN
    id_zone = zone_dao.creer(zone, 1)

    # THEN
    mock_inserer.assert_called_once()
    mock_creer_polygone.assert_called_once()
    assert id_zone == 1


@patch("dao.zone_dao.ZoneDAO.requete")
def test_supprimer(mock_requete):
    """Test de la méthode supprimer() de ZoneDAO"""

    # GIVEN
    zone_dao = ZoneDAO()
    mock_requete.return_value = 1

    # WHEN
    resultat = zone_dao.supprimer(1)

    # THEN
    mock_requete.assert_any_call("DELETE FROM MultiPolygone WHERE id_zone=%(id_zone)s;", {"id_zone": 1})
    mock_requete.assert_any_call("DELETE FROM Zone WHERE id=%(id_zone)s;", {"id_zone": 1})
    assert resultat is True


@patch("dao.zone_dao.ZoneDAO.requete")
@patch("dao.zone_dao.ZoneDAO.trouver_par_id")
def test_trouver_zones_filles(mock_trouver_par_id, mock_requete):
    """Test de la méthode trouver_zones_filles() de ZoneDAO"""

    # GIVEN
    zone_dao = ZoneDAO()
    mock_requete.return_value = [{"id_zone_fille": 1}, {"id_zone_fille": 2}]
    mock_trouver_par_id.side_effect = [MagicMock(id=1), MagicMock(id=2)]

    # WHEN
    zones_filles = zone_dao.trouver_zones_filles(1)

    # THEN
    assert len(zones_filles) == 2
    assert zones_filles[0].id == 1
    assert zones_filles[1].id == 2


@patch("dao.zone_dao.ZoneDAO.requete")
@patch("dao.zone_dao.ZoneDAO.trouver_zones_filles")
@patch("dao.polygone_dao.PolygoneDAO.trouver_par_id")
def test_trouver_par_id(mock_trouver_par_id, mock_trouver_zones_filles, mock_requete):
    """Test de la méthode trouver_par_id()"""

    # GIVEN
    zone_dao = ZoneDAO()
    
    # Simuler la requête pour les polygones
    mock_requete.side_effect = [
        [{"id_polygone": 1}],  # La liste des polygones de la zone
        [{"nom": "Zone 1", "population": 1000, "code_insee": "12345", "annee": 2020}]  # Données de la zone
    ]
    
    # Simuler la recherche des polygones
    mock_trouver_par_id.return_value = MagicMock(id=1, contours=[[(0, 0), (1, 1), (0, 1)]])
    
    # Simuler la recherche des zones filles
    mock_trouver_zones_filles.return_value = []

    # WHEN
    zone = zone_dao.trouver_par_id(1)

    # THEN
    assert zone.nom == "Zone 1"
    assert zone.population == 1000
    assert zone.code_insee == "12345"
    assert zone.annee == 2020
    assert isinstance(zone.multipolygone.polygones, list)



@patch("dao.zone_dao.ZoneDAO.requete")
@patch("dao.polygone_dao.PolygoneDAO.trouver_id")
def test_trouver_id(mock_trouver_id, mock_requete):
    """Test de la méthode trouver_id()"""

    # GIVEN
    zone_dao = ZoneDAO()
    
    # Simuler la recherche des polygones
    mock_trouver_id.return_value = 1  # ID d'un polygone
    
    # Simuler la recherche des zones contenant les polygones
    mock_requete.return_value = [{"id_zone": 1}, {"id_zone": 2}]

    # Création d'une fausse zone avec un multipolygone
    zone = MagicMock()
    zone.id = None
    zone.multipolygone.polygones = [MagicMock()]

    # WHEN
    id_zone = zone_dao.trouver_id(zone)

    # THEN
    mock_trouver_id.assert_called_once()
    assert id_zone == 1


@patch("dao.zone_dao.ZoneDAO.requete")
def test_zones_contenant_polygone(mock_requete):
    """Test de la méthode __zones_contenant_polygone()"""

    # GIVEN
    zone_dao = ZoneDAO()
    mock_requete.return_value = [{"id_zone": 1}, {"id_zone": 2}]

    # WHEN
    zones = zone_dao._ZoneDAO__zones_contenant_polygone(1)

    # THEN
    assert zones == {1, 2}
