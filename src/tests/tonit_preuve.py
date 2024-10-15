from business_object.point import Point as P
from business_object.contour import Contour as C
from business_object.polygone import Polygone as Poly
from business_object.multipolygone import MultiPolygone

a= MultiPolygone(
        polygones=[Poly([C([P(0, 0), P(0, 1), P(2.18, 3.79), P(1.52, 0.61), P(2.84, -2.09),
                          P(3.66, -2.57), P(6.8, 0.37), P(8.38, -1.31), P(5.22, -3.39),
                          P(6.76, -6.23), P(0.58, -5.79), P(1.54, -1.19), P(-2.54, -3.73)]),
                       C([P(2.12, -3.83), P(2, -5), P(4.86, -4.57)])]),

                 Poly([C([P(2.54, -4.19), P(3.22, -4.37), P(2.82, -4.61)])]),

                 Poly([C([P(3.44, 1.69), P(2.48, 0.63), P(3.28, -1.01), P(4.8, 0.49)]),
                       C([P(3.24, 0.55), P(3.82, 0.37), P(3.44, 1.17)])]),

                 Poly([C([P(0.54, -2.63), P(-1.38, -3.95), P(0.38, -4.09)])])]
    )

points_dedans = {P(-0.06, -3.53), P(-1.44, -2.51), P(3.36, -0.11), P(2.84, -4.38),
                     P(6.74, -1.05), P(1.36, 1.81)}
points_dehors = {P(1, -2), P(3.76, -4.49), P(3.54, 0.63), P(4.38, -0.88)}

for point in points_dedans:
    assert a.est_dedans(point)

for point in points_dehors:
    assert not a.est_dedans(point)
print("all ok")