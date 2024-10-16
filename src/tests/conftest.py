from business_object.point import Point as P
from business_object.contour import Contour as C
from business_object.polygone import Polygone as Poly
from business_object.multipolygone import MultiPolygone
from business_object.zone import Zone
from business_object.zonage import Zonage
import pytest


# Point

@pytest.fixture
def point_sans_id():
    return {"x": 0,
            "y": 1
            }


@pytest.fixture
def point_avec_id():
    return {"x": 0.5,
            "y": -37.65,
            "id": 5
            }


# Contours

@pytest.fixture
def contour_sans_id():
    return {"points": [P(0, 0), P(0, 1), P(1, 1), P(1, 0)]
            }


@pytest.fixture
def contour_avec_id():
    return {"points": [P(2, 2), P(2, 2.5), P(2.5, 2.5), P(2.5, 2)],
            "id": 47
            }


# Polygones

@pytest.fixture
def polygone_sans_id():
    return {"contours": [C([P(0, 0), P(0, 1), P(1, 1), P(1, 0)]),
                         C([P(0.15, 0.15), P(0.15, 0.85), P(0.85, 0.85), P(0.85, 0.15)])
                         ],
            }


@pytest.fixture
def polygone_avec_id():
    return {"contours": [C([P(0, 0), P(0, 1), P(1, 1), P(1, 0)]),
                         C([P(0.15, 0.15), P(0.15, 0.85), P(0.85, 0.85), P(0.85, 0.15)])
                         ],
            "id": 123
            }


# Multipolygones

@pytest.fixture
def multipolygone_sans_id():
    return {"contour": [Poly([C([P(0, 0), P(0, 1), P(1, 1), P(1, 0)]),
                             C([P(0.15, 0.15), P(0.15, 0.85), P(0.85, 0.85), P(0.85, 0.15)])]),

                        Poly([C([P(2, 2), P(2, 2.5), P(2.5, 2.5), P(2.5, 2)]),
                             C([P(2.1, 2.1), P(2.1, 2.4), P(2.4, 2.4), P(2.4, 2.1)])]),

                        Poly([C([P(0.2, 0.2), P(0.2, 0.6), P(0.6, 0.6), P(0.6, 0.2)])])]
            }


@pytest.fixture
def multipolygone_avec_id():
    return {"contour": [Poly([C([P(0, 0), P(0, 1), P(2.18, 3.79), P(1.52, 0.61), P(2.84, -2.09),
                                 P(3.66, -2.57), P(6.8, 0.37), P(8.38, -1.31), P(5.22, -3.39),
                                 P(6.76, -6.23), P(0.58, -5.79), P(1.54, -1.19), P(-2.54, -3.73)]),
                              C([P(2.12, -3.83), P(2, -5), P(4.86, -4.57)])]),

                        Poly([C([P(2.54, -4.19), P(3.22, -4.37), P(2.82, -4.61)])]),

                        Poly([C([P(3.44, 1.69), P(2.48, 0.63), P(3.28, -1.01), P(4.8, 0.49)]),
                              C([P(3.24, 0.55), P(3.82, 0.37), P(3.44, 1.17)])]),

                        Poly([C([P(0.54, -2.63), P(-1.38, -3.95), P(0.38, -4.09)])])],
            "id": 77
            }


# Zones

@pytest.fixture
def zone_sans_id():
    return {
        "nom": "Zone sans id",
        "multipolygone": pytest.multipolygone_avec_id,
    }


@pytest.fixture
def zone_avec_id():
    return {
        "nom": "Zone avec id",
        "multipolygone": pytest.multipolygone_avec_id,
        "id": 45
    }


# Zonages

@pytest.fixture
def zonage_sans_id():
    return {
        "nom": "Zonage sans id",
        "zones": [pytest.zone_avec_id, pytest.zone_sans_id],
        "annee": 2024,
    }


def pytest_configure():

    # Multipolygones

    pytest.multipolygone_sans_id = MultiPolygone(
        polygones=[Poly([C([P(0, 0), P(0, 1), P(1, 1), P(1, 0)]),
                         C([P(0.15, 0.15), P(0.15, 0.85), P(0.85, 0.85), P(0.85, 0.15)])]),

                   Poly([C([P(2, 2), P(2, 2.5), P(2.5, 2.5), P(2.5, 2)]),
                         C([P(2.1, 2.1), P(2.1, 2.4), P(2.4, 2.4), P(2.4, 2.1)])]),

                   Poly([C([P(0.2, 0.2), P(0.2, 0.6), P(0.6, 0.6), P(0.6, 0.2)])])])

    pytest.multipolygone_avec_id = MultiPolygone(
        polygones=[Poly([C([P(0, 0), P(0, 1), P(2.18, 3.79), P(1.52, 0.61), P(2.84, -2.09),
                            P(3.66, -2.57), P(6.8, 0.37), P(8.38, -1.31), P(5.22, -3.39),
                            P(6.76, -6.23), P(0.58, -5.79), P(1.54, -1.19), P(-2.54, -3.73)]),
                         C([P(2.12, -3.83), P(2, -5), P(4.86, -4.57)])]),

                   Poly([C([P(2.54, -4.19), P(3.22, -4.37), P(2.82, -4.61)])]),

                   Poly([C([P(3.44, 1.69), P(2.48, 0.63), P(3.28, -1.01), P(4.8, 0.49)]),
                         C([P(3.24, 0.55), P(3.82, 0.37), P(3.44, 1.17)])]),

                   Poly([C([P(0.54, -2.63), P(-1.38, -3.95), P(0.38, -4.09)])])],
        id=77
    )

    pytest.m_0_0_1 = MultiPolygone(
       polygones=[Poly([C([P(0, 1), P(1, 1), P(1, 2), P(0, 2)])])]
                )

    pytest.m_0_0_2 = MultiPolygone(
       polygones=[Poly([C([P(1, 1), P(1, 2), P(2, 2), P(2, 1)])])]
                )

    pytest.m_0_0_3 = MultiPolygone(
       polygones=[Poly([C([P(0, 0), P(0, 1), P(1, 1), P(1, 0)])])]
                )

    pytest.m_0_0_4 = MultiPolygone(
       polygones=[Poly([C([P(1, 0), P(1, 1), P(2, 1), P(2, 0)])])]
                )

    pytest.m_0_1_1 = MultiPolygone(
       polygones=[Poly([C([P(1, 0), P(3, 0), P(1, -2)])])]
                )

    pytest.m_0_1_2 = MultiPolygone(
       polygones=[Poly([C([P(1, -2), P(3, 0), P(3, -2)])])]
                )

    pytest.m_1_0_1 = MultiPolygone(
       polygones=[Poly([C([P(0, 0), P(2, 0), P(2, 2), P(0, 2)])])]
                )

    pytest.m_1_1_1 = MultiPolygone(
       polygones=[Poly([C([P(1, 0), P(3, 0), P(3, -2), P(1, -2)])])]
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
