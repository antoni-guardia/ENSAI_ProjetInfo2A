import os
import pytest

from unittest.mock import patch

from utils.reset_database import ResetDatabase

from dao.zone_dao import ZoneDAO

from business_object.zone import Zone


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Initialisation des données de test"""
    with patch.dict(os.environ, {"SCHEMA": "project_test_dao"}):
        ResetDatabase().lancer(test_dao=True)
        yield


def test_trouver_par_id_existant_sans_filles():
    """Recherche par id d'un contour existant"""

    # GIVEN
    id_zone = 2

    # WHEN
    zone = ZoneDAO().trouver_par_id(id_zone, filles=False)

    # THEN

    assert isinstance(zone, Zone)


def test_trouver_par_id_existant_avec_filles():
    """Recherche par id d'un contour existant"""

    # GIVEN
    id_zone = 1

    # WHEN
    zone = ZoneDAO().trouver_par_id(id_zone, filles=True)

    # THEN

    assert isinstance(zone, Zone)


def test_creer():
    """Création d'un contour avec des points"""

    # GIVEN
    zone = pytest.zone_0_0_1

    with patch("dao.zone_dao.ZoneDAO") as MockZoneDao:

        MockZoneDao.return_value.creer.return_value = True
        # WHEN

        id_zone = MockZoneDao().creer(zone)

        # THEN

        assert isinstance(id_zone, int)


def test_supprimer():
    """Suppression d'un contour par son id"""

    # GIVEN
    id_zone = 1

    with patch("dao.zone_dao.ZoneDAO") as MockZoneDao:
        # Set up the mock to return True when supprimer is called
        MockZoneDao.return_value.supprimer.return_value = True

        # WHEN
        supprimer_ok = MockZoneDao().supprimer(id_zone)

        # THEN
        assert supprimer_ok


def test_trouver_id():
    """Trouver id d'une zone"""

    #GIVEN
    polygone_dao = PolygoneDAO()
    zone_dao = ZoneDAO()

    polygone = Polygone(contours=[1])
    id_polygone = polygone_dao.crer(polygone)

    multipolygone = multipolygone(polygone=[polygone])

    zone = Zone(1, 'Zone A', 1500, '12345', 2023)

    id_zone = zone_dao.creer(zone, id_zonage=1)

    #WHEN
    zone_id = zone_dao.trouver_id(zone)

    #THEN
    assert zone_id == id_zone
