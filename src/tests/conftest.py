from src.classes.multipolygone import MultiPolygone
import pytest


# Multipolygones

@pytest.fixture
def multipolygone_simple():
    return {"contour": [[[(0, 0), (0, 1), (1, 1), (1, 0)]]]
            }


def pytest_configure():

    # Multipolygones
    pytest.multipolygone_simple = MultiPolygone(contour=[[[(0, 0), (0, 1), (1, 1), (1, 0)]]])
