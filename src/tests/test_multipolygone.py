import pytest
from src.classes.multipolygone import MultiPolygone


# Test que utilitza la fixture multipolygone_simple
def test_multipolygone_simple_fixture(multipolygone_simple):
    multipolygone = multipolygone_simple["contour"]
    # Escriu un test que faci alguna cosa amb el multipolygone
    assert len(multipolygone[0]) == 1  # Comprova que no hi ha inclaus


# Test que utilitza pytest.multipolygone_simple
def test_multipolygone_global():
    # Accedeix al multipolygone creat en pytest_configure
    multipolygone = pytest.multipolygone_simple
    assert isinstance(multipolygone, MultiPolygone)

    # Verifica la propietat contour
    assert len(multipolygone.contour) == 1
    assert len(multipolygone.contour[0]) == 1  # Assegura't que hi ha només el polygone principal
