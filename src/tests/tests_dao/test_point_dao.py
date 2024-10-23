import os
import pytest

from unittest.mock import patch

from utils.reset_database import ResetDatabase

from dao.point_dao import PointDao

from business_object.point import Point


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Initialisation des données de test"""
    with patch.dict(os.environ, {"SCHEMA": "project_test_dao"}):
        ResetDatabase().lancer(test_dao=True)
        yield


def test_trouver_par_id_existant():
    """Recherche par id d'un point existant"""

    # GIVEN
    id_point = 1

    # WHEN
    point = PointDao().trouver_par_id(id_point)

    # THEN
    assert isinstance(point, Point)


def test_creer():
    """Cree un point en prenant un objet point"""

    # GIVEN
    point = Point(1, 4)

    # WHEN
    id_point = PointDao().creer(point)

    # THEN

    assert point.id == id_point


def test_supprimer():
    """Supprime un point en prenant son id"""

    # GIVEN
    id_point = 2

    with patch("dao.point_dao.PointDao") as MockPointDao:
        # Set up the mock to return True when supprimer is called
        MockPointDao.return_value.supprimer.return_value = True

        # WHEN
        supprimer_ok = MockPointDao().supprimer(id_point)

        # THEN
        assert supprimer_ok


def test_trouver_par_id():
    """Trouver un point grace a son id"""

    # GIVEN
    id_point = 1

    # WHEN
    point = PointDao().trouver_par_id(id_point)

    # THEN

    assert point == Point(1.5, 2.5)
