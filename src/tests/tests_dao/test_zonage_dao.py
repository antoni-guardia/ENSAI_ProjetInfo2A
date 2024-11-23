import os
import pytest

from unittest.mock import patch

from utils.reset_database import ResetDatabase

from dao.zonage_dao import ZonageDAO

from business_object.zonage import Zonage


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Initialisation des données de test"""
    with patch.dict(os.environ, {"POSTGRES_SCHEMA": "project_test_dao"}):
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
    """
    Trouver un zonage par id
    """
    # GIVEN
    zonage = ZonageDAO().trouver_par_id(1)
    zonage.id = None
    # WHEN
    zonage_id = ZonageDAO().trouver_id(zonage)
    # THEN
    assert zonage_id == 1


def test_trouver_id_par_nom_annee():
    """
    Trouver l'id d'un zonage par son nom et son année
    """
    # GIVEN
    nom = "Corona d Aragò"
    # WHEN
    id_z = ZonageDAO().trouver_id_par_nom_annee(nom)
    # THEN
    assert isinstance(id_z, int)


if __name__ == "__main__":
    test_trouver_id_par_nom_annee()
