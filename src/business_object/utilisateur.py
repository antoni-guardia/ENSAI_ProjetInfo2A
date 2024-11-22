import hashlib


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
        # Hash the password immediately when setting it
        self.mdp = self.hash_password(mdp)

    def __str__(self):
        """Permet d'afficher les informations du joueur"""
        return f"Joueur({self.pseudo}, {self.mdp})"

    def hash_password(self, password: str) -> str:
        """Hash the password using SHA-256"""
        sha256_hash = hashlib.sha256()
        sha256_hash.update(password.encode("utf-8"))
        return sha256_hash.hexdigest()

    def verify_password(self, password: str) -> bool:
        """Verify the provided password against the stored hash"""
        return self.mdp == self.hash_password(password)
