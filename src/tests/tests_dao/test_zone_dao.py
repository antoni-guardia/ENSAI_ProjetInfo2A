import os
import pytest

from unittest.mock import patch

from utils.reset_database import ResetDatabase

from dao.zone_dao import ZoneDAO

from business_object.zone import Zone


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Initialisation des données de test"""
    with patch.dict(os.environ, {"POSTGRES_SCHEMA": "project_test_dao"}):
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
    id_zone = 4

    with patch("dao.zone_dao.ZoneDAO") as MockZoneDao:
        # Set up the mock to return True when supprimer is called
        MockZoneDao.return_value.supprimer.return_value = True

        # WHEN
        supprimer_ok = MockZoneDao().supprimer(id_zone)

        # THEN
        assert supprimer_ok


def test_trouver_nom_par_code_insee():
    """
    Trouver le nom d'une zone avec un code INSEE
    """
    # GIVEN
    code_insee = "0"
    annee = 1315

    # WHEN

    nom = ZoneDAO().trouver_nom_par_code_insee(code_insee, annee)

    # THEN

    assert nom == "Principat"


def test_trouver_tout_par_code_insee():
    """
    Trouver tout avec un code insee
    """

    # GIVEN
    code_insee = "1"
    annee = 1315
    # WHEN

    res = ZoneDAO().trouver_tout_par_code_insee(code_insee, annee)

    # THEN

    assert res == "nom : Regne de València; code_insee : 1; population : 2000"


def test_trouver_tout_par_nom():
    """
    Trouver toute les informations d'une zone avec un nom
    """

    # GIVEN
    nom = "Regne de València"
    annee = 1315
    # WHEN

    res = ZoneDAO().trouver_tout_par_nom(nom, annee)

    # THEN

    assert res == "nom : Regne de València; code_insee : 1; population : 2000"


def test_trouver_fails():
    """
    Trouver les zones non présentes
    """
    # GIVEN
    nom = "non present"
    code_insee = "non present"
    annee = 1315
    # THEN

    assert ZoneDAO().trouver_tout_par_code_insee(code_insee, annee) is None
    assert ZoneDAO().trouver_nom_par_code_insee(nom, annee) is None
    assert ZoneDAO().trouver_tout_par_nom(nom, annee) is None


def test_trouver_zones_filles_none():
    """
    Trouver les zones filles
    """
    # GIVEN
    id_zone_mere = 59

    # THEN

    assert ZoneDAO().trouver_zones_filles(id_zone_mere) is None


def test_trouver_zones_filles():
    # GIVEN
    id_zone_mere = 4

    # THEN

    assert isinstance(ZoneDAO().trouver_zones_filles(id_zone_mere), list)
