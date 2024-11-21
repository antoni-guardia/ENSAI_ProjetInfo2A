class Utilisateur:
    """
    Classe représentant un Joueur

    Attributs
    ----------
    pseudo : str
        pseudo du joueur
    mdp : str
        le mot de passe du joueur
    """

    def __init__(self, pseudo, mdp):
        """Constructeur"""
        self.pseudo = pseudo
        self.mdp = mdp

    def __str__(self):
        """Permet d'afficher les informations du joueur"""
        return f"Joueur({self.pseudo}, {self.mdp})"

    def __hash__(self):
        """La clé qui hache le mdp"""
        return hash(self.mdp) * hash(self.pseudo[0])
