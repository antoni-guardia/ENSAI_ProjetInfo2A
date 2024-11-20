from dao.zone_dao import ZoneDAO


class ServicesRechercheZone:

    def nom_par_code_insee(self, code_insee: str, annee: int):

        nom = ZoneDAO().trouver_nom_par_code_insee(code_insee, annee)

        if not isinstance(nom, str):
            return None
        return nom

    def tout_par_nom(self, nom: str, annee: int):

        info = ZoneDAO().trouver_tout_par_nom(nom, annee)

        if not isinstance(info, str):
            return None
        return info

    def tout_par_code_insee(self, code_insee: str, annee: int):

        info = ZoneDAO().trouver_tout_par_code_insee(code_insee, annee)

        if not isinstance(info, str):
            return None
        return info


if __name__ == "__main__":
    nom = ServicesRechercheZone().tout_par_code_insee("48", 2024)
    print(nom)
