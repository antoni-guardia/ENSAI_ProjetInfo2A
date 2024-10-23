import os
import pytest

from unittest.mock import patch

from utils.reset_database import ResetDatabase

from dao.polygone_dao import PolygoneDAO

from business_object.polygone import Polygone



@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Initialisation des données de test"""
    with patch.dict(os.environ, {"SCHEMA": "project_test_dao"}):
        ResetDatabase().lancer(test_dao=True)
        yield


def test_trouver_par_id_existant():
    """Recherche par id d'un contour existant"""

    # GIVEN
    id_polygone = 1

    # WHEN
    polygone = PolygoneDAO().trouver_par_id(id_polygone)

    # THEN

    assert isinstance(polygone, Polygone)


def test_creer():
    """Création d'un contour avec des points"""

    # GIVEN
    polygone = pytest.polygone_1

    with patch("dao.polygone_dao.PolygoneDAO") as MockPolygoneDao:

        MockPolygoneDao.return_value.creer.return_value = True
        # WHEN

        id_polygone = MockPolygoneDao().creer(polygone)

        # THEN

        assert isinstance(id_polygone, int)


def test_supprimer():
    """Suppression d'un contour par son id"""

    # GIVEN
    id_polygone = 1

    with patch("dao.polygone_dao.PolygoneDAO") as MockPolygoneDao:
        # Set up the mock to return True when supprimer is called
        MockPolygoneDao.return_value.supprimer.return_value = True

        # WHEN
        supprimer_ok = MockPolygoneDao().supprimer(id_polygone)

        # THEN
        assert supprimer_ok


def test_trouver_id():
     """Recherche d'un id de polygone"""

    # GIVEN
    polygone_dao = PolygoneDAO()
    contours_id =[1]
    polygone = Polygone(contours=contour_id)
    id_polygone = polygone_dao.creer(polygone)
    
    # WHEN
    polygone_id =  polygone_dao.trouver_id(polygone)

    # THEN
    assert polygone_id == id_polygone

