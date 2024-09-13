class zonage:
    """
    Répresentation d'un découpage géographique
    """

    # -------------------------------------------------------------------------
    # Constructor
    # -------------------------------------------------------------------------

    def __init__(self,
                 nom,
                 type_coord,
                 zones,
                 annee,
                 zonage_mere=None,
                 zonage_fille=None):
        # -----------------------------
        # Attributes
        # -----------------------------
        self._nom: str = nom
        self._type_coord: str = type_coord
        self._zones = zones
        self._annee = annee
        self._zonage_mere = zonage_mere
        self._zonage_fille = zonage_fille

    # -------------------------------------------------------------------------
    # Methods
    # -------------------------------------------------------------------------
    def trouver_zone(self, point):
        pass

    @property
    def nom(self):
        return self._nom

    @property
    def type_coord(self):
        return self._type_coord

    @property
    def zones(self):
        return self.zones

    @property
    def annee(self):
        return self.annee

    @property
    def zonage_mere(self):
        return self.zonage_mere

    @property
    def zonage_fille(self):
        return self.zonage_fille
