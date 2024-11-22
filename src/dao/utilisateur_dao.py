from business_object.utilisateur import Utilisateur
from dao.bdd_connection import DBConnection  # Assuming you have this connection logic defined


class UtilisateurDao:
    """Classe contenant les méthodes pour accéder aux Joueurs de la base de données"""

    def creer_utilisateur(self, utilisateur: Utilisateur) -> bool:
        """Creation d'un joueur dans la base de données"""
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO utlisateur_bdd.donnees_utilisateur(pseudo, mdp) VALUES"
                    "(%(pseudo)s, %(mdp)s);",
                    {"pseudo": utilisateur.pseudo, "mdp": utilisateur.mdp},
                )
                res = cursor.rowcount

        return res > 0

    def lister_tous(self) -> list:
        """Lister tous les utilisateurs"""
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT pseudo FROM utlisateur_bdd.donnees_utilisateur;")
                res = cursor.fetchall()

        return [i["pseudo"] for i in res] if res else []

    def modifier_mdp(self, utilisateur: Utilisateur, new_mdp: str) -> bool:
        """Modification du mot de passe dans la base de données"""
        if self.connection_reusie(utilisateur):
            utilisateur.mdp = utilisateur.hash_password(new_mdp)

            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "UPDATE utlisateur_bdd.donnees_utilisateur SET mdp = %(mdp)s "
                        "WHERE pseudo = %(pseudo)s;",
                        {"pseudo": utilisateur.pseudo, "mdp": utilisateur.mdp},
                    )
                    res = cursor.rowcount

            return res == 1

        return False

    def supprimer_utilisateur(self, utilisateur: Utilisateur) -> bool:
        """Suppression d'un utilisateur"""
        if self.connection_reusie(utilisateur):
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM utlisateur_bdd.donnees_utilisateur WHERE pseudo = %(pseudo)s;",
                        {"pseudo": utilisateur.pseudo},
                    )
                    res = cursor.rowcount

            return res > 0

        return False

    def connection_reusie(self, utilisateur: Utilisateur) -> bool:
        """Vérifie la validité de la connexion avec le pseudo et le mot de passe"""
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT pseudo, mdp FROM utlisateur_bdd.donnees_utilisateur "
                    "WHERE pseudo = %(pseudo)s;",
                    {"pseudo": utilisateur.pseudo},
                )
                res = cursor.fetchone()

        if res:
            # Compare the stored password hash with the one provided
            stored_password_hash = res["mdp"]
            return stored_password_hash == utilisateur.mdp

        return False
