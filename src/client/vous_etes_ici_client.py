import os
import requests

from typing import List


class VEIClient:
    """Make call to the pokemon endpoint"""

    def __init__(self) -> None:
        self.__host = os.environ["WEBSERVICE_HOST"]

    def get_zonnages_type(self) -> List[str]:
        """
        Returns list of pokemon types (fire, water, grass...)
        """

        # Appel du Web service
        req = requests.get(f"{self.__host}/type")

        # Création d'une liste puis parcours du json pour ajouter tous
        # les types de Pokemons à la liste
        pokemon_types = []
        if req.status_code == 200:
            raw_types = req.json()["results"]
            for t in raw_types:
                pokemon_types.append(t["name"])

        return sorted(pokemon_types)

    def get_all_pokemon_by_types(self, pokemon_type) -> List[str]:
        """
        Renvoie la liste des Pokemons du type indiqué en paramètre
        """
        # Appel du Web service
        req = requests.get(f"{self.__host}/type/{pokemon_type}")

        # Création d'une liste puis parcours du json pour ajouter tous
        # les Pokemons à la liste
        pokemons = []
        if req.status_code == 200:
            raw_pokemon = req.json()["pokemon"]
            for p in raw_pokemon:
                pokemons.append(p["pokemon"]["name"])

        return pokemons

#  Get
