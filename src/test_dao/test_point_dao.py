import os
import pytest

from unittest.mock import patch

from utils.reset_database import ResetDatabase

from dao.point_dao import PointDao

from business_object.point import Point


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Initialisation des données de test"""
    with patch.dict(os.environ, {"SCHEMA": "projet_test_dao"}):
        ResetDatabase().lancer(test_dao=True)
        yield


def test_trouver_par_id_existant():
    """Recherche par id d'un joueur existant"""

    # GIVEN
    id_joueur = 998

    # WHEN
    joueur = JoueurDao().trouver_par_id(id_joueur)

    # THEN
    assert joueur is not None
