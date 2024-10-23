import pytest
from unittest.mock import patch, MagicMock
from dao.zonage_dao import ZonageDAO
from business_object.zonage import Zonage

@pytest.fixture
def mock_zonage():
    """Fixture pour un objet Zonage fictif"""
    return Zonage(nom="Test Zonage", zones=[], zonage_mere=None)

@patch("dao.zonage_dao.ZonageDAO.requete")
def test_creer(mock_requete, mock_zonage):
    """Test de la méthode creer() de ZonageDAO"""

    # GIVEN
    zonage_dao = ZonageDAO()
    mock_requete.return_value = [{"id": 1}]

    # WHEN
    id_zonage = zonage_dao.creer(mock_zonage)

    # THEN
    mock_requete.assert_called()
    assert id_zonage == 1
    assert mock_zonage.id == 1


@patch("dao.zonage_dao.ZonageDAO.requete")
@patch("dao.zone_dao.ZoneDAO.trouver_par_id")
def test_get_zones(mock_trouver_par_id, mock_requete):
    """Test de la méthode get_zones()"""

    # GIVEN
    zonage_dao = ZonageDAO()
    mock_requete.return_value = [{"id": 1}, {"id": 2}]
    mock_trouver_par_id.side_effect = [MagicMock(id=1), MagicMock(id=2)]

    # WHEN
    zones = zonage_dao.get_zones(1)

    # THEN
    mock_requete.assert_called_once_with("SELECT id FROM Zone WHERE id_zonage=%(id_zonage)s;", {"id_zonage": 1})
    assert len(zones) == 2
    assert zones[0].id == 1
    assert zones[1].id == 2


@patch("dao.zonage_dao.ZonageDAO.requete")
@patch("dao.zonage_dao.ZonageDAO.get_zones")
@patch("dao.zone_dao.ZoneDAO.supprimer")
def test_supprimer(mock_supprimer_zone, mock_get_zones, mock_requete):
    """Test de la méthode supprimer()"""

    # GIVEN
    zonage_dao = ZonageDAO()
    mock_get_zones.return_value = [MagicMock(id=1), MagicMock(id=2)]
    mock_requete.return_value = 1

    # WHEN
    resultat = zonage_dao.supprimer(1)

    # THEN
    mock_get_zones.assert_called_once_with(1, filles=False)
    assert mock_supprimer_zone.call_count == 2
    assert resultat


@patch("dao.zonage_dao.ZonageDAO.requete")
@patch("dao.zonage_dao.ZonageDAO.get_zones")
def test_trouver_par_id(mock_get_zones, mock_requete):
    """Test de la méthode trouver_par_id()"""

    # GIVEN
    zonage_dao = ZonageDAO()
    mock_requete.side_effect = [[{"nom": "Zonage 1"}], None]
    mock_get_zones.return_value = []

    # WHEN
    zonage = zonage_dao.trouver_par_id(1)

    # THEN
    mock_requete.assert_any_call("SELECT nom FROM Zonage WHERE id=%(id_zonage)s;", {"id_zonage": 1})
    assert zonage.nom == "Zonage 1"
    assert zonage.id == 1
    assert zonage.zonage_mere is None


@patch("dao.zonage_dao.ZonageDAO.requete")
def test_trouver_id(mock_requete, mock_zonage):
    """Test de la méthode trouver_id()"""

    # GIVEN
    zonage_dao = ZonageDAO()
    mock_requete.return_value = [{"id": 1}]

    # WHEN
    id_zonage = zonage_dao.trouver_id(mock_zonage)

    # THEN
    mock_requete.assert_called_once_with("SELECT id FROM Zonage WHERE nom=%(nom)s", {"nom": mock_zonage.nom})
    assert id_zonage == 1
