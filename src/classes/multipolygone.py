
class MultiPolygone:
    """
    Répresentation d'un multipolygone
    """
    def __init__(self,
                 contour: list[tuple],
                 exclaves: list["MultiPolygone"] | None):

        self.__contour = contour
        self.__exclaves = exclaves

    def est_dedans(point: tuple):
        pass
