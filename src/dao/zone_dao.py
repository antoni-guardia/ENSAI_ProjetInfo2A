from utils.log_decorator import log
from src.business_object.zone import Zone
from src.dao.polygone_dao import PolygoneDAO
from src.dao.abstract_dao import AbstractDao
from business_object.multipolygone import MultiPolygone


class ZoneDAO(AbstractDao):

    @log
    def __inserer(self, id_zonage, nom, population, code_insee, annee) -> int:
        res = self.__requete(
            "INSERT INTO ZONE(id_zonage, nom, population, code_insee, annee) VALUES"
            " (%(id_zonage)s, %(nom)s, %(population)s, %(code_insee)s, %(annee)s)  RETURNING id;",
        )

        if res:
            return res["id"]
        return None

    @log
    def __CreerMultipolygone(self, id_zone: int, id_polygone: int) -> bool:
        res = self.__requete(
            "INSERT INTO MultiPolygone (id_zone, id_polygone)"
            " VALUES (%(id_zone)s, %(id_polygone)s)"
            "RETURNING cardinal;",
            {
                "id_zone": id_zone,
                "id_polygone": id_polygone,
            },
        )

        if res:
            res["est_enclave"]
            return True
        return False

    @log
    def creer(self, zone: Zone, id_zonage) -> int:

        # on crée le polygone
        id_zone = self.__inserer(id_zonage,
                                 zone.nom,
                                 zone.population,
                                 zone.code_insee,
                                 zone.annee)

        for polygone in zone.multipolygone:
            id_polygone = PolygoneDAO().trouver_id(polygone)

            if id_polygone is None:
                id_polygone = PolygoneDAO().creer(polygone)

            self.__CreerMultipolygone(id_zone, id_polygone)

        zone.id = id_zone
        return id_zone

    @log
    def supprimer(self, id_zone: int):

        res1 = self.__requete(
            "DELETE FROM Zone WHERE id=%(id_zone)s ",
            {"id_zone": id_zone},
        )

        res2 = self.__requete(
            "DELETE FROM MultiPolygone WHERE id_zone=%(id_zone)s ",
            {"id_zone": id_zone},
        )

        return res1 > 0 and res2 > 0

    @log
    def trouver_par_id(self, id_zone: int):

        res = self.__requete(
            "SELECT id_polygone FROM MultiPolygone "
            "WHERE id_zone=%(id_zone)s ",
            {"id_zone": id_zone},
        )

        data_zone = self.__requete(
            "SELECT nom, popuation, code_insee, annee FROM Zone "
            "WHERE id_zone=%(id_zone)s ",
            {"id_zone": id_zone},
        )

        if res is None or data_zone is None:
            return None

        liste_polygones = []
        for id_polygone in res:
            liste_polygones.append(PolygoneDAO().trouver_par_id(id_polygone))

        multipolygone = MultiPolygone(liste_polygones)
        nom = data_zone[0][0]
        population = data_zone[0][1]
        code_insee = data_zone[0][2]
        annee = data_zone[0][3]

        zone_fille = None

        return Zone(nom, multipolygone, population, code_insee, annee, zone_fille, id_zone)

    @log
    def trouver_id(self, polygone: Polygone):

        id_contours = []

        for contour in polygone.contours:
            id_contours.append(ContourDao().trouver_id(contour))

        para_set = self.__polygones_contenant_contour(id_contours.pop())

        while len(para_set) > 1 and id_contours != []:
            para_set -= self.__polygones_contenant_contour(id_contours.pop())

        return para_set.pop()

    @log
    def __polygones_contenant_contour(self, id_contour):

        res = self.__requete(
            "SELECT id_polygone FROM EstEnclave WHERE id_contour = %(id_contour)s",
            {"id_contour": id_contour},
        )

        return {row[0] for row in res} if res else set()
