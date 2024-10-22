import re

class Coord:
    """
    Classe pour convertir des coordonnées données par l'utilisateur en format GPS (latitude, longitude).
    """

    def __init__(self, point):
        """
        Initialise les coordonnées fournies par l'utilisateur.
 
        Parameters
        ----------
        point : str, tuple, list, ou dict
            Les coordonnées à convertir. Peut être sous forme de tuple (lat, lon), 
            d'une chaîne de caractères ou d'autres formats.
        """
        self.point = point

    def verifier_format(self):
        """
        Vérifie si les coordonnées fournies sont dans un format valide.
 
        Returns
        -------
        bool
            True si le format est valide, sinon False.
        """
        if isinstance(self.point, (tuple, list)) and len(self.point) == 2:
            # Vérifie si c'est un tuple ou une liste avec deux éléments (latitude, longitude)
            return True
        elif isinstance(self.point, str):
            # Vérifie si c'est une chaîne de caractères avec un format GPS valide
            return bool(re.match(r"^-?\d+(\.\d+)?\s*,\s*-?\d+(\.\d+)?$", self.point))
        elif isinstance(self.point, dict) and 'lat' in self.point and 'lon' in self.point:
            # Vérifie si c'est un dictionnaire contenant 'lat' et 'lon'
            return True
        else:
            return False

    def convertir_en_gps(self):
        """
        Convertit les coordonnées en format GPS (latitude, longitude).
 
        Returns
        -------
        tuple
            Un tuple (latitude, longitude) en format GPS.

        Raises
        ------
        ValueError
            Si le format des coordonnées n'est pas valide.
        """
        if not self.verifier_format():
            raise ValueError("Le format des coordonnées est invalide.")

        if isinstance(self.point, (tuple, list)):
            # Les coordonnées sont déjà sous forme de tuple/liste (lat, lon)
            return float(self.point[0]), float(self.point[1])

        elif isinstance(self.point, str):
            # Convertir une chaîne de caractères au format "lat, lon" en tuple
            lat, lon = map(str.strip, self.point.split(","))
            return float(lat), float(lon)

        elif isinstance(self.point, dict):
            # Extraire latitude et longitude à partir d'un dictionnaire
            return float(self.point['lat']), float(self.point['lon'])

    def convertir_en_degres_minutes_secondes(self):
        """
        Convertit les coordonnées GPS en degrés, minutes et secondes (DMS).

        Returns
        -------
        tuple
            Un tuple contenant les coordonnées en DMS : ((deg, min, sec), (deg, min, sec)).
        """
        lat, lon = self.convertir_en_gps()

        def en_dms(coord):
            deg = int(coord)
            min = int((coord - deg) * 60)
            sec = (coord - deg - min / 60) * 3600
            return deg, min, sec

        return en_dms(lat), en_dms(lon)
