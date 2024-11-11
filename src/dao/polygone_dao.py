from utils.log_decorator import log
from business_object.polygone import Polygone
from dao.contour_dao import ContourDao
from dao.abstract_dao import AbstractDao


class PolygoneDAO(AbstractDao):

    @log
    def cle_hash_dedans(self, cle_hash):
        cle_hash_count = self.requete(
            f"SELECT COUNT(*) AS count FROM Polygone WHERE cle_hash = {cle_hash};"
        )
        # Si le count est supérieur à 0, cela signifie que cle_hash existe
        return cle_hash_count[0]["count"] > 0

    @log
    def __inserer(self, cle_hash) -> int:
        res = self.requete(
            f"INSERT INTO Polygone (cle_hash) VALUES({cle_hash}) RETURNING id;",
        )

        if res:
            return res[0]["id"]
        return None

    @log
    def __CreerEstEnclave(self, id_contour: int, id_polygone: int, est_enclave: bool) -> bool:
        res = self.requete(
            "INSERT INTO OrdrePointContour (est_enclave, id_contour, id_polygone)"
            " VALUES (%(est_enclave)s, %(id_contour)s, %(id_polygone)s)"
            " RETURNING cardinal;",
            {
                "est_enclave": est_enclave,
                "id_contour": id_contour,
                "id_polygone": id_polygone,
            },
        )

        if res:
            return True
        return False

    @log
    def creer(self, polygone: Polygone) -> int:

        # on crée le polygone
        id_polygone = self.__inserer(hash(polygone))

        for index, contour in enumerate(polygone.contours):
            id_contour = ContourDao().trouver_id(contour)

            if id_contour is None:
                id_contour = ContourDao().creer(contour)

            self.__CreerEstEnclave(id_contour, id_polygone, bool(index))

        polygone.id = id_polygone
        return id_polygone

    @log
    def supprimer(self, id_polygone: int):

        self.requete(
            "DELETE FROM EstEnclave WHERE id_polygone=%(id_polygone)s;",
            {"id_polygone": id_polygone},
        )

        res = self.requete_row_count(
            "DELETE FROM Polygone WHERE id=%(id_polygone)s;",
            {"id_polygone": id_polygone},
        )

        return res > 0

    @log
    def trouver_par_id(self, id_polygone: int):

        res = self.requete(
            "SELECT id_contour FROM EstEnclave"
            " WHERE id_polygone=%(id_polygone)s"
            " ORDER BY est_enclave DESC;",
            {"id_polygone": id_polygone},
        )
        if res is None:
            return None

        liste_contours = []
        for id_contour in res:
            liste_contours.append(ContourDao().trouver_par_id(id_contour["id_contour"]))
        return Polygone(contours=liste_contours, id=id_polygone)

    @log
    def trouver_id(self, polygone: Polygone):

        cle_hash = hash(polygone)
        id_polygone = self.requete(f"SELECT id FROM Polygone WHERE cle_hash = {cle_hash}")

        if not id_polygone:
            return None

        return id_polygone[0]["id"]
