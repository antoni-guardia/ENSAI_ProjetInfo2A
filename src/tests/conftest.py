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

    pytest.multipolygone_cat = MultiPolygone(
        contour=[[[(.02, 1.37), (.42, .39), (1.06, 0.67), (1.5, .75), (1.68, 1.15),
                   (1.74, 1.67), (2.16, 2.31), (2.46, 2.65), (3, 3),
                   (3.84, 3.37), (4.68, 3.51), (5.4, 3.97), (6.14, 4.45), (6.96, 5.15),
                   (7.42, 5.71), (7.5, 6.67), (7.22, 7.19), (7.56, 7.59), (8.04, 7.85),
                   (7.8, 8.23), (7.16, 8.53), (6.42, 8.41), (4.9, 8.33), (3.86, 8.53),
                   (2.6, 8.57), (1.28, 8.79), (0, 9), (0.22, 8.11), (.48, 6.49),
                   (.58, 5.05), (.28, 3.71), (0, 2.59)]]]
    )

    pytest.multipolygone_tar = MultiPolygone(
        contour=[[[(.02, 1.37), (.42, .39), (1.06, 0.67), (1.5, .75), (1.68, 1.15),
                   (1.74, 1.67), (2.16, 2.31), (2.46, 2.65), (3, 3),
                   (3.84, 3.37), (3.66, 4.25), (3, 5), (2, 4), (1.22, 3.19),
                   (0, 2.59)]]]
    )

    pytest.multipolygone_lle = MultiPolygone(
        contour=[[[(3.86, 8.53),
                   (2.6, 8.57), (1.28, 8.79), (0, 9), (0.22, 8.11), (.48, 6.49),
                   (.58, 5.05), (.28, 3.71), (0, 2.59), (1.22, 3.19), (2, 4),
                   (3, 5), (3.22, 6.09), (3.68, 6.81), (4.2, 7.03)]]]
    )

    pytest.multipolygone_gir = MultiPolygone(
        contour=[[[(6.96, 5.15),
                   (7.42, 5.71), (7.5, 6.67), (7.22, 7.19), (7.56, 7.59), (8.04, 7.85),
                   (7.8, 8.23), (7.16, 8.53), (6.42, 8.41), (4.9, 8.33), (3.86, 8.53),
                   (4.2, 7.45), (4.74, 7.03), (4.74, 6.43), (5.64, 6.39), (5.66, 5.93),
                   (5.68, 5.37), (6.48, 5.51)]]]
        )

    pytest.multipolygone_bar = MultiPolygone(
        contour=[[[(4.2, 7.45), (4.74, 7.03), (4.74, 6.43), (5.64, 6.39), (5.66, 5.93),
                   (5.68, 5.37), (6.48, 5.51), (6.96, 5.15), (6.14, 4.45), (5.4, 3.97)
                   (4.68, 3.51), (3.84, 3.37), (3.66, 4.25), (3, 5),
                   (3.22, 6.09), (3.68, 6.81)]]]
        )

    # Zones

    pytest.zone_bcn = Zone(nom="Bcn",
                           mutipolygone=pytest.multipolygone_bar,
                           zone_fille=None
                           )

    pytest.zone_lle = Zone(nom="Lle",
                           mutipolygone=pytest.multipolygone_lle,
                           zone_fille=None
                           )

    pytest.zone_tar = Zone(nom="Tar",
                           mutipolygone=pytest.multipolygone_tar,
                           zone_fille=None
                           )

    pytest.zone_gir = Zone(nom="Gir",
                           mutipolygone=pytest.multipolygone_gir,
                           zone_fille=None
                           )

    pytest.zone_cat = Zone(nom="Cat",
                           mutipolygone=pytest.multipolygone_cat,
                           zone_fille=[pytest.zone_bcn,
                                       pytest.zone_lle,
                                       pytest.zone_tar,
                                       pytest.zone_gir]
                           )

    # Zonage

    pytest.zonage_reg = Zonage(nom="Région",
                               zones=[pytest.zone_lle,
                                      pytest.zone_bar,
                                      pytest.zone_tar,
                                      pytest.zone_gir
                                      ],
                               annee=2024)

    pytest.zonage_pays = Zonage(nom="Pays",
                                zones=[pytest.zone_cat],
                                annee=2024,
                                zonage_fille=pytest.zonage_reg
                                )
