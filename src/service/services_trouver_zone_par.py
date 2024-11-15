from dao.zone_dao import ZoneDAO


class ServicesRecherchePoint:

    def nom_par_code_insee(self, code_insee: int, annee: int):

        nom = ZoneDAO().trouver_nom_par_code_insee(code_insee, annee)

        if not isinstance(nom, str):
            return None
        return nom

    def tout_par_nom(self, nom: str, annee: int):

        info = ZoneDAO().trouver_tout_par_nom(nom, annee)

        if not isinstance(info, str):
            return None
        return info

    def tout_par_code_insee(self, code_insee: int, annee: int):

        info = ZoneDAO().trouver_tout_par_code_insee(code_insee, annee)

        if not isinstance(info, str):
            return None
        return info
