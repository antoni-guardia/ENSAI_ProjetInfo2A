import os
import pytest

from unittest.mock import patch

from utils.reset_database import ResetDatabase

from dao.contour_dao import ContourDao

from business_object.contour import Contour

from business_object.point import Point


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Initialisation des données de test"""
    with patch.dict(os.environ, {"POSTGRES_SCHEMA": "project_test_dao"}):
        ResetDatabase().lancer(test_dao=True)
        yield


def test_trouver_par_id_existant():
    """Recherche par id d'un contour existant"""

    # GIVEN
    id_contour = 2

    # WHEN
    contour = ContourDao().trouver_par_id(id_contour)

    # THEN
    # print(contour.points)
    assert isinstance(contour, Contour)


def test_creer():
    """Création d'un contour avec des points"""

    # GIVEN
    points = [Point(1.5, 2.5), Point(3.0, 4.0), Point(5.0, 6.0)]
    contour = Contour(points=points)

    with patch("dao.contour_dao.ContourDao") as MockContourDao:

        MockContourDao.return_value.creer.return_value = True
        # WHEN

        id_contour = MockContourDao().creer(contour)

        # THEN

        assert isinstance(id_contour, int)


def test_supprimer():
    """Suppression d'un contour par son id"""

    # GIVEN
    id_contour = 2

    with patch("dao.contour_dao.ContourDao") as MockContourDao:
        # Set up the mock to return True when supprimer is called
        MockContourDao.return_value.supprimer.return_value = True

        # WHEN
        supprimer_ok = MockContourDao().supprimer(id_contour)

        # THEN
        assert supprimer_ok


def test_trouver_par_id_point():
    """Recherche d'un point existant dans un contour"""

    # GIVEN
    id_contour = 1

    # WHEN
    contour = ContourDao().trouver_par_id(id_contour)

    # THEN
    assert contour.points[0] == Point(8.77, 4.09)
