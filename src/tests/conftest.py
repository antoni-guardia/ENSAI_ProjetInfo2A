from src.classes.multipolygone import MultiPolygone
from src.classes.zone import Zone
from src.classes.zonage import Zonage
import pytest


# Multipolygones

@pytest.fixture
def multipolygone_simple_param():
    return {"contour": [[[(0, 0), (0, 1), (1, 1), (1, 0)]]]
            }


@pytest.fixture
def multipolygone_exclave_param():
    return {"contour": [[[(0, 0), (0, 1), (1, 1), (1, 0)]],
                        [[(2, 2), (2, 2.5), (2.5, 2.5), (2.5, 2)]]]
            }


@pytest.fixture
def multipolygone_inclave_param():
    return {"contour": [[[(0, 0), (0, 1), (1, 1), (1, 0)],
                         [(0.15, 0.15), (0.15, 0.85), (0.85, 0.85), (0.85, 0.15)]
                         ]]
            }


@pytest.fixture
def multipolygone_inclave_exclave_param():
    return {"contour": [[[(0, 0), (0, 1), (1, 1), (1, 0)],
                         [(0.15, 0.15), (0.15, 0.85), (0.85, 0.85), (0.85, 0.15)]],
                        [[(2, 2), (2, 2.5), (2.5, 2.5), (2.5, 2)]]]
            }


@pytest.fixture
def multipolygone_complexe_param():
    return {"contour": [[[(0, 0), (0, 1), (1, 1), (1, 0)],
                         [(0.15, 0.15), (0.15, 0.85), (0.85, 0.85), (0.85, 0.15)]],

                        [[(2, 2), (2, 2.5), (2.5, 2.5), (2.5, 2)],
                         [(2.1, 2.1), (2.1, 2.4), (2.4, 2.4), (2.4, 2.1)]],

                        [[(0.2, 0.2), (0.2, 0.6), (0.6, 0.6), (0.6, 0.2)]]]
            }


@pytest.fixture
def multipolygone_forme_etrange_param():
    return {"contour": [[[(0, 0), (0, 1), (2.18, 3.79), (1.52, 0.61), (2.84, -2.09), (3.66, -2.57),
                          (6.8, 0.37), (8.38, -1.31), (5.22, -3.39), (6.76, -6.23), (0.58, -5.79),
                          (1.54, -1.19), (-2.54, -3.73)],
                         [(2.12, -3.83), (2, -5), (4.86, -4.57)]],

                        [[(2.54, -4.19), (3.22, -4.37), (2.82, -4.61)]],

                        [[(3.44, 1.69), (2.48, 0.63), (3.28, -1.01), (4.8, 0.49)],
                         [(3.24, 0.55), (3.82, 0.37), (3.44, 1.17)]],

                        [[(0.54, -2.63), (-1.38, -3.95), (0.38, -4.09)]]]
            }

# Zones


@pytest.fixture
def zone_simple_param():
    return {
        "nom": "Zone simple",
        "multipolygone": pytest.multipolygone_inclave_exclave,
    }


def pytest_configure():

    # Multipolygones
    pytest.multipolygone_simple = MultiPolygone(contour=[[[(0, 0), (0, 1), (1, 1), (1, 0)]]])

    pytest.multipolygone_exclave = MultiPolygone(contour=[[[(0, 0), (0, 1), (1, 1), (1, 0)]],
                                                          [[(2, 2), (2, 2.5), (2.5, 2.5), (2.5, 2)]]
                                                          ])

    pytest.multipolygone_inclave = MultiPolygone(contour=[[[(0, 0), (0, 1), (1, 1), (1, 0)],
                                                           [(0.15, 0.15), (0.15, 0.85),
                                                            (0.85, 0.85), (0.85, 0.15)]
                                                           ]])

    pytest.multipolygone_inclave_exclave = MultiPolygone(
        contour=[[[(0, 0), (0, 1), (1, 1), (1, 0)],
                  [(0.15, 0.15), (0.15, 0.85), (0.85, 0.85), (0.85, 0.15)]],
                 [[(2, 2), (2, 2.5), (2.5, 2.5), (2.5, 2)]]]
    )

    pytest.multipolygone_complexe = MultiPolygone(
        contour=[
                 [[(0, 0), (0, 1), (1, 1), (1, 0)],
                  [(0.15, 0.15), (0.15, 0.85), (0.85, 0.85), (0.85, 0.15)]],

                 [[(2, 2), (2, 2.5), (2.5, 2.5), (2.5, 2)],
                  [(2.1, 2.1), (2.1, 2.4), (2.4, 2.4), (2.4, 2.1)]],

                 [[(0.2, 0.2), (0.2, 0.6), (0.6, 0.6), (0.6, 0.2)]]
                 ])

    pytest.multipolygone_forme_etrange = MultiPolygone(
        contour=[[[(0, 0), (0, 1), (2.18, 3.79), (1.52, 0.61), (2.84, -2.09), (3.66, -2.57),
                   (6.8, 0.37), (8.38, -1.31), (5.22, -3.39), (6.76, -6.23), (0.58, -5.79),
                   (1.54, -1.19), (-2.54, -3.73)],
                  [(2.12, -3.83), (2, -5), (4.86, -4.57)]],

                 [[(2.54, -4.19), (3.22, -4.37), (2.82, -4.61)]],

                 [[(3.44, 1.69), (2.48, 0.63), (3.28, -1.01), (4.8, 0.49)],
                  [(3.24, 0.55), (3.82, 0.37), (3.44, 1.17)]],

                 [[(0.54, -2.63), (-1.38, -3.95), (0.38, -4.09)]]]
    )

    pytest.m_0_0_1 = MultiPolygone(
       contour=[[[(0, 1), (1, 1), (1, 2), (0, 2)]]]
                )

    pytest.m_0_0_2 = MultiPolygone(
       contour=[[[(1, 1), (1, 2), (2, 2), (2, 1)]]]
                )

    pytest.m_0_0_3 = MultiPolygone(
       contour=[[[(0, 0), (0, 1), (1, 1), (1, 0)]]]
                )

    pytest.m_0_0_4 = MultiPolygone(
       contour=[[[(1, 0), (1, 1), (2, 1), (2, 0)]]]
                )

    pytest.m_0_1_1 = MultiPolygone(
       contour=[[[(1, 0), (3, 0), (1, -2)]]]
                )

    pytest.m_0_1_2 = MultiPolygone(
       contour=[[[(1, -2), (3, 0), (3, -2)]]]
                )

    pytest.m_1_0_1 = MultiPolygone(
       contour=[[[(0, 0), (2, 0), (2, 2), (0, 2)]]]
                )

    pytest.m_1_1_1 = MultiPolygone(
       contour=[[[(1, 0), (3, 0), (3, -2), (1, -2)]]]
                )

    # Zones

    pytest.zone_0_0_1 = Zone(nom="0_0_1",
                             mutipolygone=pytest.m_0_0_1,
                             zone_fille=None)

    pytest.zone_0_0_2 = Zone(nom="0_0_2",
                             mutipolygone=pytest.m_0_0_2,
                             zone_fille=None)

    pytest.zone_0_0_3 = Zone(nom="0_0_3",
                             mutipolygone=pytest.m_0_0_3)

    pytest.zone_0_0_4 = Zone(nom="0_0_4",
                             mutipolygone=pytest.m_0_0_4)

    pytest.zone_0_1_1 = Zone(nom="0_1_1",
                             mutipolygone=pytest.m_0_1_1)

    pytest.zone_0_1_2 = Zone(nom="0_1_2",
                             mutipolygone=pytest.m_0_1_2)

    pytest.zone_1_0_1 = Zone(nom="1_0_1",
                             mutipolygone=pytest.m_1_0_1,
                             zone_fille=[pytest.zone_0_0_1,
                                         pytest.zone_0_0_2,
                                         pytest.zone_0_0_3,
                                         pytest.zone_0_0_4])

    pytest.zone_1_1_1 = Zone(nom="1_1_1",
                             mutipolygone=pytest.m_1_1_1,
                             zone_fille=[pytest.zone_0_1_1,
                                         pytest.zone_0_1_2
                                         ])

    # Zonage

    pytest.zonage_1 = Zonage(nom="Niveau 1",
                             zones=[pytest.zone_1_0_1,
                                    pytest.zone_1_1_1],
                             annee=2024,
                             zonage_mere=None)

    pytest.zonage_0 = Zonage(nom="Niveau 0",
                             zones=[pytest.zone_0_0_1,
                                    pytest.zone_0_0_2,
                                    pytest.zone_0_0_3,
                                    pytest.zone_0_0_4,
                                    pytest.zone_0_1_1,
                                    pytest.zone_0_1_2],
                             annee=2024,
                             zonage_mere=pytest.zonage_1)
