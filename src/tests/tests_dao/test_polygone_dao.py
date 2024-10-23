import pytest
from unittest.mock import MagicMock
from src.dao.polygone_dao import PolygoneDAO
from src.business_object.polygone import Polygone
from src.dao.contour_dao import ContourDao

@pytest.fixture
def polygone_dao(mocker):
    """Fixture to create an instance of PolygoneDAO with mocked dependencies."""
    dao = PolygoneDAO()
    # Mock the required methods
    mocker.patch.object(dao, 'requete', return_value=[{"id": 1}])  # Mocking the requete method for insertion
    return dao

def test_inserer(polygone_dao):
    """Test the __inserer method."""
    result = polygone_dao._PolygoneDAO__inserer()
    assert result == 1

def test_supprimer(polygone_dao, mocker):
    """Test the supprimer method."""
    mocker.patch.object(polygone_dao, 'requete_row_count', return_value=1)  # Mock the row count check

    result = polygone_dao.supprimer(1)

    assert result is True
    polygone_dao.requete.assert_any_call("DELETE FROM EstEnclave WHERE id_polygone=%(id_polygone)s;", {"id_polygone": 1})
    polygone_dao.requete.assert_any_call("DELETE FROM Polygone WHERE id=%(id_polygone)s;", {"id_polygone": 1})

def test_creer(polygone_dao, mocker):
    """Test the creer method."""
    mocker.patch('src.dao.contour_dao.ContourDao.trouver_id', side_effect=[None, 2])  # Mock the contour finding
    mocker.patch('src.dao.contour_dao.ContourDao.creer', return_value=2)  # Mock creating a new contour

    polygone = Polygone(contours=['contour1', 'contour2'])  # Example polygon

    result = polygone_dao.creer(polygone)

    assert result == 1
    polygone_dao.requete.assert_called_with(
        "INSERT INTO OrdrePointContour (est_enclave, id_contour, id_polygone) "
        "VALUES (%(est_enclave)s, %(id_contour)s, %(id_polygone)s) "
        "RETURNING cardinal;",
        {'est_enclave': False, 'id_contour': 2, 'id_polygone': 1}
    )

def test_trouver_par_id(polygone_dao, mocker):
    """Test the trouver_par_id method."""
    mocker.patch.object(polygone_dao, 'requete', return_value=[{'id_contour': 1}, {'id_contour': 2}])
    mocker.patch('src.dao.contour_dao.ContourDao.trouver_par_id', side_effect=[MagicMock(), MagicMock()])

    result = polygone_dao.trouver_par_id(1)

    assert isinstance(result, Polygone)
    assert result.id == 1
    assert len(result.contours) == 2

def test_trouver_id(polygone_dao, mocker):
    """Test the trouver_id method."""
    mocker.patch('src.dao.contour_dao.ContourDao.trouver_id', return_value=1)  # Simulate finding a contour ID
    mocker.patch.object(polygone_dao, '__polygones_contenant_contour', return_value={1, 2})  # Mock existing polygons

    polygone = Polygone(contours=['contour1'])  # Example polygon

    result = polygone_dao.trouver_id(polygone)

    assert result == 1
    polygone_dao.trouver_id.assert_called_once_with('contour1')
