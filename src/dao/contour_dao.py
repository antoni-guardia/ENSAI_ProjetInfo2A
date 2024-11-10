from utils.log_decorator import log
from business_object.contour import Contour
from dao.point_dao import PointDao
from dao.abstract_dao import AbstractDao


class ContourDao(AbstractDao):
    """
    Classe contenant les méthodes pour accéder aux Contours de la base de données
    """

    @log
    def calculer_hash(self, contour: Contour):
        sum_x = 0
        sum_y = 0
        for point in contour.points:
            sum_x += round(point.x * 100)
            sum_y += round(point.y * 100)

        return (sum_x * 37 - sum_y * 73) % 10**5 + 3

    @log
    def cle_hash_dedans(self, cle_hash):
        cle_hash_count = self.requete("SELECT cle_hash FROM CONTOUR;")
        print(cle_hash_count)
        # Si le count est supérieur à 0, cela signifie que cle_hash existe
        return cle_hash_count[0]["count"] > 0

    @log
    def __inserer(self, cle_hash):

        res = self.requete("INSERT INTO Contour(cle_hash) " f"VALUES({cle_hash}) RETURNING id;")

        if res:
            return res[0]["id"]
        return None

    @log
    def __CreerOrdrePointContour(self, id_point: int, id_contour: int, cardinal: int):
        res = self.requete(
            "INSERT INTO OrdrePointContour (cardinal, id_point, id_contour)"
            " VALUES (%(cardinal)s, %(id_point)s, %(id_contour)s)"
            " RETURNING cardinal;",
            {"cardinal": cardinal, "id_point": id_point, "id_contour": id_contour},
        )

        if res is not None:
            return True

        return False

    @log
    def trouver_par_id(self, id_contour: int):
        res = self.requete(
            "SELECT id_point FROM OrdrePointContour"
            " WHERE id_contour=%(id_contour)s"
            " ORDER BY cardinal;",
            {"id_contour": id_contour},
        )

        if res is None:
            return None
        liste_points = []
        res = [i["id_point"] for i in res]
        for id_point in res:
            liste_points.append(PointDao().trouver_par_id(id_point))
        return Contour(points=liste_points, id=id_contour)

    @log
    def creer(self, contour: Contour):

        # on crée le contour
        cle_hash = self.calculer_hash(contour)
        if self.cle_hash_dedans(cle_hash):
            # alors le contour existe deja
            return self.trouver_id(contour)

        # le contour n'existe pas
        id_contour = self.__inserer(cle_hash)

        for cardinal, point in enumerate(contour.points):
            if PointDao().trouver_id(point) is None:
                id_point = PointDao().creer(point)

            self.__CreerOrdrePointContour(id_point, id_contour, cardinal)

        contour.id = id_contour
        return id_contour

    @log
    def trouver_id(self, contour: Contour):

        cle_hash = self.calculer_hash(contour)
        if not self.cle_hash_dedans(cle_hash):
            # le contour n'est pas dans la bdd
            return None

        res = self.requete(
            "SELECT id_contour FROM Contour WHERE cle_hash = %(cle_hash)s;",
            {"cle_hash": cle_hash},
        )
        id_contour = res[0]["id_contour"]
        return id_contour

    @log
    def supprimer(self, id_contour):

        self.requete(
            "DELETE FROM OrdrePointContour WHERE id_contour=%(id_contour)s;",
            {"id_contour": id_contour},
        )

        res = self.requete_row_count(
            "DELETE FROM Contour WHERE id=%(id_contour)s;",
            {"id_contour": id_contour},
        )

        return res > 0
