from utils.log_decorator import log

from business_object.utilisateur import Utilisateur
from dao.utilisateur_dao import UtilisateurDao


class UtilisateurService:
    """Classe contenant les méthodes de service des Utilisateurs"""

    @log
    def creer(self, pseudo, mdp):
        """Création d'un utilisateur à partir de ses attributs"""
        if self.pseudo_deja_utilise(pseudo):
            return False

        nouveau_usr = Utilisateur(pseudo=pseudo, mdp=mdp)

        return nouveau_usr if UtilisateurDao().creer_utilisateur(nouveau_usr) else None

    @log
    def lister_tous(self) -> list[str]:
        """Lister tous les joueurs
        Si inclure_mdp=True, les mots de passe seront inclus
        Par défaut, tous les mdp des joueurs sont à None
        """
        usrs = UtilisateurDao().lister_tous()

        return usrs

    @log
    def modifier(self, pseudo, mdp, new_mdp):
        """Modification d'un utilisateur"""

        usr = Utilisateur(pseudo, mdp)

        UtilisateurDao().modifier_mdp(usr, new_mdp)

    @log
    def supprimer(self, pseudo, mdp) -> bool:
        """Supprimer le compte d'un joueur"""
        usr = Utilisateur(pseudo, mdp)

        return UtilisateurDao().supprimer(usr)

    @log
    def pseudo_deja_utilise(self, pseudo) -> bool:
        """Vérifie si le pseudo est déjà utilisé
        Retourne True si le pseudo existe déjà en BDD"""
        usrs = UtilisateurDao().lister_tous()
        return pseudo in usrs

    @log
    def connection_reussie(self, pseudo, mdp):
        usr = Utilisateur(pseudo, mdp)
        return UtilisateurDao().connection_reusie(usr)


if __name__ == "__main__":
    print(UtilisateurService().creer("toni", "123"))
    print(UtilisateurService().lister_tous())
