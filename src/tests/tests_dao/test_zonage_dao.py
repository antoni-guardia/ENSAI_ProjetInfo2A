import os
import pytest

from unittest.mock import patch

from utils.reset_database import ResetDatabase

from dao.zonage_dao import ZonageDAO

from business_object.zonage import Zonage


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Initialisation des données de test"""
    with patch.dict(os.environ, {"SCHEMA": "project_test_dao"}):
        ResetDatabase().lancer(test_dao=True)
        yield


def test_trouver_par_id():
    """Recherche par id d'un contour existant"""

    # GIVEN
    id_zonage = 1

    # WHEN
    zone = ZonageDAO().trouver_par_id(id_zonage)

    # THEN

    assert isinstance(zone, Zonage)


def test_creer():
    """Création d'un contour avec des points"""

    # GIVEN
    zonage = pytest.zonage_0

    with patch("dao.zonage_dao.ZonageDAO") as MockZonageDao:

        MockZonageDao.return_value.creer.return_value = True
        # WHEN

        id_zone = MockZonageDao().creer(zonage)

        # THEN

        assert isinstance(id_zone, int)


def test_supprimer():
    """Suppression d'un contour par son id"""

    # GIVEN
    id_zonage = 1

    with patch("dao.zonage_dao.ZonageDAO") as MockZonageDao:
        # Set up the mock to return True when supprimer is called
        MockZonageDao.return_value.supprimer.return_value = True

        # WHEN
        supprimer_ok = MockZonageDao().supprimer(id_zonage)

        # THEN
        assert supprimer_ok


def test_trouver_id():
    # GIVEN
    zonage_to_find = Zonage(name="Zonage 1")
    # WHEN
    zonage_id = ZonageDAO().trouver_id(zonage_to_find)
    # THEN
    assert zonage_id == 1
