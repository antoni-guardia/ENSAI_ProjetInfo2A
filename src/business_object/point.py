class Point:

    """
    Classe définissant un point.
    """

    def __init__(self, x: float, y: float, id: int = None) -> None:
        """
        Initialise un point avec des coordonnées x et y.
        Les coordonnées doivent être des nombres flottants (float).

        Parameters
        ----------

        x: float
            La coordonnée x du point (doit être un float).

        y: float
            La coordonnée y du point (doit être un float).

        Raises
        ------
        TypeError si x ou y n'est pas un float.
        TypeError si id n'est pas de type int ou None.
            """

        # if not isinstance(x, float) or not isinstance(y, float):
        #    raise TypeError("Les coordonnées x et y doivent être des nombres flottants.")

        #if not isinstance(id, int) or id is not None:
        #    raise TypeError("Les coordonnées x et y doivent être des nombres flottants.")

        self._x = x
        self._y = y
        self.id = id

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
