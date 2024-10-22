import os
import pytest

from unittest.mock import patch

from utils.reset_database import ResetDatabase

from dao.contour_dao import ContourDao

from business_object.contour import Contour


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Initialisation des données de test"""
    with patch.dict(os.environ, {"SCHEMA": "project_test_dao"}):
        ResetDatabase().lancer(test_dao=True)
        yield


def test_trouver_par_id_existant():
    """Recherche par id d'un point existant"""

    # GIVEN
    id_contour = 1

    # WHEN
    contour = ContourDao().trouver_par_id(id_contour)

    # THEN
    assert isinstance(contour, Contour)


"""
def test_creer():

    # GIVEN
    point = Point(1, 4)

    # WHEN
    id_point = PointDao().creer(point)

    # THEN

    assert point.id == id_point


def test_supprimer():

    # GIVEN
    id_point = 2

    # WHEN
    supprimer_ok = PointDao().supprimer(id_point)

    # THEN

    assert supprimer_ok


def test_trouver_par_id():

    # GIVEN
    id_point = 1

    # WHEN
    point = PointDao().trouver_par_id(id_point)

    # THEN

    assert point == Point(1.5, 2.5)
"""
