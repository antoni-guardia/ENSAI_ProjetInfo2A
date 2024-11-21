from utils.log_decorator import log

from business_object.utilisateur import Utilisateur
from dao.utilisateur_dao import UtilisateurDao

from utils.reset_bdd_usr import ResetDatabaseUSR


class UtilisateurService:
    """Classe contenant les méthodes de service des Utilisateurs"""

    @log
    def __init__(self):
        ResetDatabaseUSR().lancer

    @log
    def creer(self, pseudo, mdp):
        """Création d'un utilisateur à partir de ses attributs"""
        if self.pseudo_deja_utilise(pseudo):
            return False

        nouveau_usr = Utilisateur(pseudo=pseudo, mdp=mdp)

        return nouveau_usr if UtilisateurDao().creer(nouveau_usr) else None

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
        return pseudo in [j.pseudo for j in usrs]
