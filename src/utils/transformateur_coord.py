from pyproj import Transformer


class TransformerCoordonnees:
    def __init__(self):
        self.transformers = {
            "LAMB93": Transformer.from_crs("EPSG:2154", "EPSG:4326", always_xy=True),
            "RGAF09UTM20": Transformer.from_crs("EPSG:5490", "EPSG:4326", always_xy=True),
            "UTM22RGFG95": Transformer.from_crs("EPSG:2972", "EPSG:4326", always_xy=True),
            "RGR92UTM40S": Transformer.from_crs("EPSG:2975", "EPSG:4326", always_xy=True),
            "RGM04UTM38S": Transformer.from_crs("EPSG:4471", "EPSG:4326", always_xy=True),
        }

    def transformer(self, x, y, type_coord=None):
        """
        Transforme des coordonnées x, y au systeme WGS84G

        Parameters
        ----------

        x : float
            la premiere coordonnée.

        y : float
            la deuxieme coordonneée.

        type_coord : str
            Le systeme de coordonnes de x,y.

        Returns
        -------
            tuple
                resultat en coordonnées WGS84G
        """
        if type_coord is None:
            return x, y

        if type_coord not in self.transformers:
            raise ValueError(f"Type de coordonnées Non defni : {type_coord}")

        transformer = self.transformers[type_coord]
        lon, lat = transformer.transform(x, y)
        return lon, lat
