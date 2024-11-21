# import logging

# from utils.log_decorator import log

from dao.bdd_connection import DBConnection

from business_object.utilisateur import Utilisateur


class UtilisateurDao:
    """Classe contenant les méthodes pour accéder aux Joueurs de la base de données"""

    def creer_utlisateur(self, utilisateur: Utilisateur) -> bool:
        """Creation d'un joueur dans la base de données

        Parameters
        ----------
        utlisateur : utilisateur

        Returns
        -------
        created : bool
            True si la création est un succès
            False sinon
        """

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO project.utilisateur(pseudo, mdp,est_admin) VALUES        "
                    "(%(pseudo)s, %(mdp)s)  ;                              ",
                    {"pseudo": utilisateur.pseudo, "mdp": hash(utilisateur)},
                )
                res = cursor.rowcount

        created = False
        if res:
            created = True

        return created

    def lister_tous(self) -> list[str]:
        """lister tous les utliisateurs

        Parameters
        ----------
        None

        Returns
        -------
        liste_utlisateur: list[str]
            renvoie la liste des noms de tous les utilisateurs
        """

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT pseudo" " FROM project.utilisateur;")
                res = cursor.fetchall()
        liste = []
        if res:
            return [i["pseudo"] for i in res]
        return liste

    def modifier_mdp(self, utilisateur: Utilisateur, new_mdp: str) -> bool:
        """Modification du mdp dans la base de données

        Parameters
        ----------
        utilisateur : Utlisateur

        Returns
        -------
        created : bool
            True si la modification est un succès
            False sinon
        """
        if self.connection_reusie(utilisateur):
            utilisateur.mdp = new_mdp

            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "UPDATE project.utilisateur                   "
                        "   SET    mdp         = %(mdp)s              "
                        " WHERE pseudo = %(pseudo)s;                  ",
                        {
                            "pseudo": utilisateur.pseudo,
                            "mdp": hash(utilisateur),
                        },
                    )
                    res = cursor.rowcount
            return res == 1
        return False

    def supprimer_utlisateur(self, utlisateur=Utilisateur):
        if self.connection_reusie(utlisateur):
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM project.utilisateur                  "
                        " WHERE pseudo = %(pseudo)s; ",
                        {
                            "pseudo": utlisateur.pseudo,
                        },
                    )
                    res = cursor.rowcount
            return res == -1
        return False

    def connection_reusie(self, utilisateur: Utilisateur):
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT pseudo FROM project.utilisateur"
                    " WHERE pseudo = %(pseudo)s AND mdp = %(mdp)s; ",
                    {"pseudo": utilisateur.pseudo, "mdp": hash(utilisateur)},
                )
                res = cursor.rowcount
        return bool(res)
