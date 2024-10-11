class Point:

    def __init__(self, x: float, y: float) -> None:
        """
        Initialise un point avec des coordonnées x et y.
        Les coordonnées doivent être des nombres flottants (float).

        :param x: La coordonnée x du point (doit être un float).
        :param y: La coordonnée y du point (doit être un float).
        :raises TypeError: Si x ou y n'est pas un float.
            """
        if not isinstance(x, float) or not isinstance(y, float):
            raise TypeError("Les coordonnées x et y doivent être des nombres flottants.")
        self._x = x
        self._y = y

    @property
    def x(self):
        """
        Retourne la coordonnée x du point.

        :return: La coordonnée x
        """
        return self._x

    @property
    def y(self):
        """
        Retourne la coordonnée y du point.

        :return: La coordonnée y
        """
        return self._y
