class Joueur:
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

    def __init__(self, pseudo, mdp=None):
        """Constructeur"""
        self.pseudo = pseudo
        self.mdp = mdp

    def __str__(self):
        """Permet d'afficher les informations du joueur"""
        return f"Joueur({self.pseudo}, {self.age} ans)"

    def as_list(self) -> list[str]:
        """Retourne les attributs du joueur dans une liste"""
        return [self.pseudo, self.age, self.mail, self.fan_pokemon]
