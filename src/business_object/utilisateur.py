class Utilisateur:
    """
    Classe représentant un Joueur

    Attributs
    ----------
    id_joueur : int
        identifiant
    pseudo : str
        pseudo du joueur
    mdp : str
        le mot de passe du joueur
    age : int
        age du joueur
    mail : str
        mail du joueur
    """

    def __init__(self, pseudo, mdp, est_admin: bool):
        """Constructeur"""
        self.pseudo = pseudo
        self.mdp = mdp
        self.est_admin = est_admin

    def __str__(self):
        """Permet d'afficher les informations du joueur"""
        return f"Joueur({self.pseudo}, {self.mdp},{self.est_admin})"
