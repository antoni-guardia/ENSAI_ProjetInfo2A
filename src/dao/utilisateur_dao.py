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
        joueur : Joueur

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
                    "(%(pseudo)s, %(mdp)s, %(est_admin)s)  ;                              ",
                    {
                        "pseudo": utilisateur.pseudo,
                        "mdp": utilisateur.mdp,
                        "est_admin": utilisateur.est_admin,
                    },
                )
                res = cursor.rowcount

        created = False
        if res:
            created = True

        return created

    def trouver_par_pseudo(self, pseudo) -> Utilisateur:
        """trouver un joueur grace à son pseudo

        Parameters
        ----------
        id_joueur : int
            numéro id du joueur que l'on souhaite trouver

        Returns
        -------
        joueur : Joueur
            renvoie le joueur que l'on cherche par pseudo
        """

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT *                           "
                    "  FROM project.utilisateur                      "
                    " WHERE pseudo = %(pseudo)s;  ",
                    {"pseudo": pseudo},
                )
                res = cursor.fetchone()

        utilisateur = None
        if res:
            utilisateur = Utilisateur(
                pseudo=res["pseudo"], mdp=res["mdp"], est_admin=res["est_admin"]
            )

        return utilisateur

    def lister_tous(self) -> list[Utilisateur]:
        """lister tous les utliisateurs

        Parameters
        ----------
        None

        Returns
        -------
        liste_utlisateur: list[Utlisateur]
            renvoie la liste de tous les joueurs dans la base de données
        """

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT *                              "
                    "  FROM project.utilisateur;                        "
                )
                res = cursor.fetchall()
        liste = []
        if res:
            for row in res:
                user = Utilisateur(
                    pseudo=row["pseudo"],
                    mdp=row["mdp"],
                    est_admin=row["est_admin"],
                )

                liste.append(user)
        return liste

    def modifier_mdp(self, utlisateur: Utilisateur, new_mdp: str) -> bool:
        """Modification du mdp dans la base de données

        Parameters
        ----------
        utlisateur : Utlisateur

        Returns
        -------
        created : bool
            True si la modification est un succès
            False sinon
        """

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE project.utilisateur                   "
                    "   SET    mdp         = %(mdp)s              "
                    " WHERE pseudo = %(pseudo)s;                  ",
                    {
                        "pseudo": utlisateur.pseudo,
                        "mdp": new_mdp,
                    },
                )
                res = cursor.rowcount
        return res == 1

    def supprimer_utlisateur(self, utlisateur=Utilisateur):
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


if __name__ == "__main__":
    dao = UtilisateurDao()
    user = Utilisateur("3asba", "nayek")
    created = dao.supprimer_utlisateur(user)
    print(created)
