import os
import requests
from typing import List, Tuple


class VEIClient:
    """Make calls to the zonage web service"""

    def __init__(self) -> None:
        self.__host = os.environ["WEBSERVICE_HOST"]

    def get_zonages_type(self) -> List[str]:
        """
        Returns list of all zonages types available
        """

        # Call to the Web service
        req = requests.get(f"{self.__host}/type")

        # Creating a list and adding all zonage types from the response
        zonage_types = []
        if req.status_code == 200:
            raw_types = req.json()["results"]
            for t in raw_types:
                zonage_types.append(t["name"])

        return sorted(zonage_types)

    def get_zonage_by_point(self, lat: float, lon: float, type_coord: str = "gps") -> str:
        """
        Returns the zonage name for a given point (latitude, longitude)
        """
        # Call to the Web service
        req = requests.get(f"{self.__host}/zonage/trouver-zone",
                           params={"lat": lat, "lon": lon, "type_coord": type_coord})

        if req.status_code == 200:
            zonage = req.json().get("zonage", None)
            return zonage if zonage else "No zonage found"

        return "Error: Unable to retrieve zonage"

    def get_zonages_by_points(self, points: List[Tuple[float, float]], type_coord: str = "gps") -> List[str]:
        """
        Returns the zonages for multiple points (list of lat, lon tuples)
        """
        points_param = ";".join([f"{lat},{lon}" for lat, lon in points])
        req = requests.get(f"{self.__host}/zonage/trouver-zones", params={"points": points_param, "type_coord": type_coord})

        if req.status_code == 200:
            zonages = req.json().get("zonages", [])
            return zonages

        return []

    def get_zone_path_for_point(self, lat: float, lon: float, type_coord: str = "gps") -> str:
        """
        Returns the zone path for a given point (latitude, longitude)
        """
        req = requests.get(f"{self.__host}/zonage/trouver-zone-chemin", params={"lat": lat, "lon": lon, "type_coord": type_coord})

        if req.status_code == 200:
            zone_path = req.json().get("zone_path", "")
            return zone_path if zone_path else "No zone path found"

        return "Error: Unable to retrieve zone path"

    def get_zone_paths_for_points(self, points: List[Tuple[float, float]], type_coord: str = "gps") -> List[str]:
        """
        Returns the zone paths for multiple points (list of lat, lon tuples)
        """
        points_param = ";".join([f"{lat},{lon}" for lat, lon in points])
        req = requests.get(f"{self.__host}/zonage/trouver-zones-chemins", params={"points": points_param, "type_coord": type_coord})

        if req.status_code == 200:
            zone_paths = req.json().get("zone_paths", [])
            return zone_paths

        return []

    def get_zonage_nom(self) -> str:
        """
        Returns the name of the current zonage
        """
        req = requests.get(f"{self.__host}/zonage/nom")

        if req.status_code == 200:
            return req.json().get("nom", "Unknown zonage")

        return "Error: Unable to retrieve zonage name"

    def get_all_zones(self) -> List[str]:
        """
        Returns the list of all zones in the current zonage
        """
        req = requests.get(f"{self.__host}/zonage/zones")

        if req.status_code == 200:
            return req.json().get("zones", [])

        return []
