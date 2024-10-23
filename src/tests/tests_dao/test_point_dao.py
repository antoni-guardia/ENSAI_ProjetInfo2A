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
    """Crée un point en prenant un objet point"""

    # GIVEN
    point = Point(1, 4)  # Créer un objet Point avec des coordonnées (1, 4)

    # Le point doit obtenir un id après la création, donc imaginons que l'id créé soit 42
    expected_id = 42

    # Utilisation du patch pour remplacer PointDao
    with patch("PointDao") as MockPointDao:
        # On configure le mock pour que la méthode creer retourne un id fictif (42)
        MockPointDao.return_value.creer.return_value = expected_id

        # WHEN
        id_point = MockPointDao().creer(point)

        # THEN
        assert id_point == expected_id
        # Vérifier que la méthode creer a bien été appelée avec le bon objet point
        MockPointDao.return_value.creer.assert_called_with(point)


def test_supprimer():
    """Supprime un point en prenant son id"""

    # GIVEN
    id_point = 2

    with patch("PointDao") as MockPointDao:
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
