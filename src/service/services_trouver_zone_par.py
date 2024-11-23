from dao.zone_dao import ZoneDAO


class ServicesRechercheZone:

    def nom_par_code_insee(self, code_insee: str, annee: int):
        """
        Trouve le nom d'une zone à travers son code insee

        Parameters
        ----------
            code_insee : str
            annee : int

        Returns
        -------
            nom : str

        """

        nom = ZoneDAO().trouver_nom_par_code_insee(code_insee, annee)

        if not isinstance(nom, str):
            return None
        return nom

    def tout_par_nom(self, nom: str, annee: int):
        """
        Trouve l'ensemble des infos connues de la zone à travers le nom et année.

        Parameters
        ----------
            nom : str
            annee : int

        Returns
        -------
            infos : str
                infos de la zone associe au nom fourni sous la forme:
                    - `"nom`: ____; code_insee : ____; population : ___"

        """

        info = ZoneDAO().trouver_tout_par_nom(nom, annee)

        if not isinstance(info, str):
            return None
        return info

    def tout_par_code_insee(self, code_insee: str, annee: int):
        """
        Trouve l'ensemble des infos connues de la zone à travers le code insee et année.

        Parameters
        ----------
            code_insee : str
            annee : int

        Returns
        -------
            infos : str
                infos de la zone associe au nom fourni sous la forme:
                    - `"nom`: ____; code_insee : ____; population : ___"

        """

        info = ZoneDAO().trouver_tout_par_code_insee(code_insee, annee)

        if not isinstance(info, str):
            return None
        return info


if __name__ == "__main__":
    nom = ServicesRechercheZone().tout_par_code_insee("48", 2024)
    print(nom)
