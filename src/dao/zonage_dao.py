from utils.log_decorator import log
from business_object.zonage import Zonage
from dao.zone_dao import ZoneDAO
from dao.abstract_dao import AbstractDao


class ZonageDAO(AbstractDao):

    @log
    def creer(self, zonage: Zonage) -> int:
        """Rentrer le zonage le plus petit possible"""

        # on crée le zonage
        id_zonage = self.requete(
            "INSERT INTO Zonage(nom) VALUES" " (%(nom)s)  RETURNING id;",
        )

        # si le zonage vient d'être ajouté
        if id_zonage is not None:
            id_zonage = id_zonage[0]["id"]
            zonage.id = id_zonage

            # on regarde par rapport a la table ZonageMere
            if zonage.zonage_mere is not None:
                id_zonage_mere = self.trouver_id(zonage)
                if id_zonage_mere is None:
                    id_zonage_mere = self.creer()

                self.requete(
                    "INSERT INTO ZonageMere(id_zonage_mere, id_zonage_fille) VALUES"
                    " (%(id_zonage_mere)s, %(id_zonage_fille)s)  RETURNING id;",
                    {"id_zonage_mere": id_zonage_mere, "id_zonage_fille": id_zonage},
                )

            return id_zonage

        return None

    @log
    def get_zones(self, id_zonage: int, filles=True):
        """Renvoie les zones associés a un zonage en particulier"""
        id_zones = self.requete(
            "SELECT id FROM Zone WHERE id_zonage=%(id_zonage)s;", {"id_zonage": id_zonage}
        )
        if id_zones is None:
            return None
        id_zones = [id_zone["id"] for id_zone in id_zones]

        zones = [ZoneDAO().trouver_par_id(id_zone, filles) for id_zone in id_zones]

        return zones

    @log
    def supprimer(self, id_zonage: int):

        zones = self.get_zones(id_zonage, filles=False)
        for zone in zones:
            if zone.id is not None:
                ZoneDAO().supprimer(zone.id)

        self.requete(
            "DELETE FROM ZonageMere WHERE id_zone_mere=%(id_zonage)s"
            " OR id_zone_fille=%(id_zonage)s",
            {"id_zonage": id_zonage},
        )

        res = self.requete(
            "DELETE FROM Zonage WHERE id=%(id_zonage)s ",
            {"id": id_zonage},
        )

        return res > 0

    @log
    def trouver_par_id(self, id_zonage: int):

        zones = self.get_zones(id_zonage)

        nom = self.requete(
            "SELECT nom FROM Zonage WHERE id=%(id_zonage)s;",
            {"id_zonage": id_zonage},
        )
        if nom is not None:
            nom = nom[0]["nom"]

        id_zonage_mere = self.requete(
            "SELECT id_zonage_mere WHERE id_zonage_fille=%(id_zonage)s;", {"id_zonage": id_zonage}
        )

        if id_zonage_mere is not None:
            zonage_mere = self.trouver_par_id(id_zonage_mere[0]["id_zonage_mere"])

            return Zonage(nom, zones, zonage_mere, id_zonage)

        return Zonage(nom, zones, None, id_zonage)

    @log
    def trouver_id(self, zonage: Zonage):

        id_possibles = self.requete("SELECT id FROM Zonage WHERE nom=%(nom)s;", {"nom": zonage.nom})
        if id_possibles is None:
            return None
        if len(id_possibles) == 1:
            return id_possibles[0]["id"]

        id_possibles = [ids["id"] for ids in id_possibles]

        zone_test = zonage.zones[0]
        id_zone = zone_test.id
        id_zonage = self.requete(
            "SELECT id_zonage FROM Zone WHERE id=%(id_zone)s", {"id_zone": id_zone}
        )
        return id_zonage[0]["id_zonage"]
