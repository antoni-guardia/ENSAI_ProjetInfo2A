from utils.log_decorator import log
from business_object.zone import Zone
from dao.polygone_dao import PolygoneDAO
from dao.abstract_dao import AbstractDao
from business_object.multipolygone import MultiPolygone


class ZoneDAO(AbstractDao):

    @log
    def __inserer(
        self, id_zonage, nom, population, code_insee, annee, max_x, min_x, max_y, min_y, cle_hash
    ) -> int:
        res = self.requete(
            "INSERT INTO Zone(id_zonage, nom, population, code_insee, annee,max_x, min_x, max_y, "
            "min_y, cle_hash) VALUES"
            " (%(id_zonage)s, %(nom)s, %(population)s, %(code_insee)s, %(annee)s, %(max_x)s, "
            "%(min_x)s, %(max_y)s, %(min_y)s, %(cle_hash)s)"
            "  RETURNING id;",
            {
                "id_zonage": id_zonage,
                "nom": nom,
                "population": population,
                "code_insee": code_insee,
                "annee": annee,
                "max_x": max_x,
                "min_x": min_x,
                "max_y": max_y,
                "min_y": min_y,
                "cle_hash": cle_hash,
            },
        )

        if res:
            return res[0]["id"]
        return None

    @log
    def __CreerMultipolygone(self, id_zone: int, id_polygone: int) -> bool:
        res = self.requete(
            "INSERT INTO MultiPolygone (id_zone, id_polygone)"
            " VALUES (%(id_zone)s, %(id_polygone)s) RETURNING id_polygone;",
            {
                "id_zone": id_zone,
                "id_polygone": id_polygone,
            },
        )
        if res:
            return True
        return False

    @log
    def creer(self, zone: Zone, id_zonage, enregistrer_multipolygone=True) -> int:
        """Commencer à construire par les zones les plus petites"""
        if zone.multipolygone is None:
            min_x = min_y = max_x = max_y = None
        else:
            val_rect_multipolygone = zone.multipolygone.coord_rectangle

            min_x = val_rect_multipolygone[0]
            min_y = val_rect_multipolygone[1]
            max_x = val_rect_multipolygone[2]
            max_y = val_rect_multipolygone[3]

        # on crée la zone
        id_zone = self.__inserer(
            id_zonage,
            zone.nom,
            zone.population,
            zone.code_insee,
            zone.annee,
            max_x,
            min_x,
            max_y,
            min_y,
            hash(zone),
        )
        if zone.multipolygone is not None and enregistrer_multipolygone:
            for polygone in zone.multipolygone:
                id_polygone = PolygoneDAO().creer(polygone)

                self.__CreerMultipolygone(id_zone, id_polygone)
        else:
            id_polygone = None
        id_zone_mere = id_zone
        if zone.zones_fille is not None:
            for zone_fille in zone.zones_fille:

                if zone_fille.id is None:
                    id_zone_fille = self.trouver_id(zone_fille)

                else:
                    id_zone_fille = zone_fille.id
                self.requete_no_return(
                    "INSERT INTO ZoneFille (id_zone_mere, id_zone_fille)"
                    " VALUES (%(id_zone_mere)s, %(id_zone_fille)s);",
                    {"id_zone_mere": id_zone_mere, "id_zone_fille": id_zone_fille},
                )

        zone.id = id_zone
        return id_zone

    @log
    def supprimer(self, id_zone: int):

        self.requete_no_return(
            "DELETE FROM MultiPolygone WHERE id_zone=%(id_zone)s;",
            {"id_zone": id_zone},
        )

        self.requete_no_return(
            "DELETE FROM ZoneFille WHERE id_zone_mere=%(id_zone)s;",
            {"id_zone": id_zone},
        )

        self.requete_no_return(
            "DELETE FROM ZoneFille WHERE id_zone_fille=%(id_zone)s;",
            {"id_zone": id_zone},
        )

        res = self.requete_no_return(
            "DELETE FROM Zone WHERE id=%(id_zone)s;",
            {"id_zone": id_zone},
        )
        return res > 0

    @log
    def trouver_zones_filles(self, id_zone_mere):
        id_filles = self.requete(
            "SELECT id_zone_fille FROM ZoneFille WHERE id_zone_mere = %(id_zone_mere)s;",
            {"id_zone_mere": id_zone_mere},
        )

        if not id_filles:
            return None

        return [self.trouver_par_id(id_fille["id_zone_fille"]) for id_fille in id_filles]

    @log
    def trouver_par_id(self, id_zone: int, filles=True):

        res = self.requete(
            "SELECT id_polygone FROM MultiPolygone WHERE id_zone=%(id_zone)s;",
            {"id_zone": id_zone},
        )

        data_zone = self.requete(
            "SELECT nom, population, code_insee, annee FROM Zone WHERE id=%(id_zone)s;",
            {"id_zone": id_zone},
        )

        if res is None or data_zone is None:
            return None

        liste_polygones = []
        for id_polygone in res:
            liste_polygones.append(PolygoneDAO().trouver_par_id(id_polygone["id_polygone"]))

        multipolygone = MultiPolygone(liste_polygones)
        nom = data_zone[0]["nom"]
        population = data_zone[0]["population"]
        code_insee = data_zone[0]["code_insee"]
        annee = data_zone[0]["annee"]

        if filles:
            zones_fille = self.trouver_zones_filles(id_zone)

            return Zone(nom, multipolygone, population, code_insee, annee, zones_fille, id_zone)

        return Zone(nom, multipolygone, population, code_insee, annee, None, id_zone)

    @log
    def trouver_id_zones_par_rectangles(self, x, y, id_zonage):
        res = self.requete(
            "SELECT id FROM Zone WHERE "
            "id_zonage = %(id_zonage)s AND "
            "min_x < %(x)s AND %(x)s < max_x AND "
            "min_y < %(y)s AND %(y)s < max_y;",
            {"x": x, "y": y, "id_zonage": id_zonage},
        )

        return [i["id"] for i in res]

    @log
    def trouver_id(self, zone: Zone):
        res = self.requete(
            f"SELECT id FROM Zone WHERE cle_hash={hash(zone)}" f" AND annee={zone.annee};"
        )
        if res:
            zone.id = res[0]["id"]
            return res[0]["id"]

        return None

    @log
    def trouver_nom_par_code_insee(self, code_insee, annee):
        """
        Trouve le nom associe a un code insee particulier

        Parameters
        ----------
            code_insee: str
                code insee associé a la zone.

            annee: int
                année associé à la zone.

        Returns
        -------
            nom: str
                le nom de la zone associé au code insee fourni
        """

        res = self.requete(
            "SELECT nom FROM Zone WHERE annee=%(annee)s AND code_insee=%(code_insee)s;",
            {"annee": annee, "code_insee": code_insee},
        )

        if not res:
            return None

        return res[0]["nom"]

    @log
    def trouver_tout_par_code_insee(self, code_insee, annee):
        """
        Trouve le nom associe a un code insee particulier

        Parameters
        ----------
            code_insee: str
                Code Insee associé a la zone.

            annee: int
                année associé à la zone.

        Returns
        -------
            infos: str
                infos de la zone associe au code insee fourni sous la forme:
                "nom : ____; code_insee : ____; population : ___"
        """
        res = self.requete(
            "SELECT nom, population FROM Zone WHERE annee=%(annee)s AND code_insee=%(code_insee)s;",
            {"annee": annee, "code_insee": code_insee},
        )
        if not res:
            return None
        nom = res[0]["nom"]
        population = res[0]["population"]
        format_str = f"nom : {nom}; code_insee : {code_insee}; population : {population}"

        return format_str

    @log
    def trouver_tout_par_nom(self, nom, annee):
        """
        Trouve le nom associe a un code insee particulier

        Parameters
        ----------
            nom: str
                nom associé a la zone.

            annee: int
                année associé à la zone.

        Returns
        -------
            infos: str
                infos de la zone associe au nom fourni sous la forme:
                "nom : ____; code_insee : ____; population : ___"
        """
        res = self.requete(
            "SELECT population, code_insee FROM Zone WHERE annee=%(annee)s AND nom=%(nom)s;",
            {"annee": annee, "nom": nom},
        )
        if not res:
            return None
        code_insee = res[0]["code_insee"]
        population = res[0]["population"]
        format_str = f"nom : {nom}; code_insee : {code_insee}; population : {population}"

        return format_str

    @log
    def annees_disponibles(self):
        """
        Renvoie les années disponibles dans la base de données.
        Returns
        -------
            list[str] : liste de l'ensemble des années disponibles
        """
        res = self.requete("SELECT DISTINCT annee FROM Zone;")
        if res is None:
            return []
        return [int(i["annee"]) for i in res]

    @log
    def zonages_disponibles(self, annee):
        """
        Renvoie l'ensembles des zonages disponibles dans la bdd.
        Parameters
        ----------
        annee : int
            année dont on cherche les zonages disponibles.
        Returns
        -------
            list[str] : liste de l'ensemble des noms des zonages disponibles
        """
        if not isinstance(annee, int):
            return None

        res = self.requete(
            "SELECT DISTINCT Zonage.nom AS nom FROM Zonage"
            "JOIN Zone ON Zonage.id_Zonage = Zone.id_zonage "
            "WHERE Zone.annee = %(annee)s;",
            {"annee": annee},
        )
        if res is not None:
            return [i["nom"] for i in res]
        return []

    @log
    def trouver_id_mere(self, id_zone, id_zonage):
        """
        Trouve l' id_mere associe a un id_zone particulier

        Parameters
        ----------
            id_zone : int
                code insee associé a la zone.

        Returns
        -------
            id_zone_mere: int
                l'identifiant de la mère de la zone associé à id_zone
                None s'il n'existe pas.
            id_zonage: int
                id du zonage de la mere.
        """
        res = self.requete(
            "SELECT id_zone_mere FROM ZoneFille JOIN Zone ON Zone.id = ZoneFille.id_zone_mere"
            " WHERE id_zone_fille = %(id_zone_fille)s AND Zone.id_zonage = %(id_zonage)s;",
            {"id_zone_fille": id_zone, "id_zonage": id_zonage},
        )

        if res is None:
            return None

        return res[0]["id_zone_mere"]

    @log
    def trouver_nom_par_id(self, id_zone: int):
        """
        Trouve le nom associe a un id particulier

        Parameters
        ----------
            id_zone : int
                id associé a la zone.

        Returns
        -------
            nom: str
                le nom de la zone associé au code insee fourni
        """

        res = self.requete(
            "SELECT nom FROM Zone WHERE id=%(id_zone)s;",
            {"id_zone": id_zone},
        )

        if not res:
            return None

        return res[0]["nom"]


if __name__ == "__main__":
    id_mere = ZoneDAO().trouver_id_mere(35003, 1)
    nom = ZoneDAO().trouver_nom_par_id(id_mere)
    print(nom)
