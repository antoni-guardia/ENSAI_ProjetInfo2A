import os
import requests
from typing import List, Tuple
import dotenv


###############################################################################
##################################### GET #####################################
###############################################################################

class VEIClient:
    """Make calls to the zonage web service."""

    def __init__(self) -> None:
        self.__host = os.environ["WEBSERVICE_HOST"]

    def get_zonages_type(self) -> List[str]:
        """
        Returns a list of all zonages types available.
        """
        req = requests.get(f"{self.__host}/type")
        zonage_types = []
        if req.status_code == 200:
            raw_types = req.json()["results"]
            for t in raw_types:
                zonage_types.append(t["name"])
        return sorted(zonage_types)

    def get_zonage_by_point(
        self, lat: float, lon: float, type_coord: str = "gps"
    ) -> str:
        """
        Returns the zonage name for a given point (latitude, longitude).
        """
        req = requests.get(
            f"{self.__host}/zonage/trouver-zone",
            params={"lat": lat, "lon": lon, "type_coord": type_coord},
        )
        if req.status_code == 200:
            zonage = req.json().get("zonage", None)
            return zonage if zonage else "No zonage found"
        return "Error: Unable to retrieve zonage"

    def get_zonages_by_points(
        self, points: List[Tuple[float, float]], type_coord: str = "gps"
    ) -> List[str]:
        """
        Returns the zonages for multiple points (list of lat, lon tuples).
        """
        points_param = ";".join([f"{lat},{lon}" for lat, lon in points])
        req = requests.get(
            f"{self.__host}/zonage/trouver-zones",
            params={"points": points_param, "type_coord": type_coord},
        )
        if req.status_code == 200:
            return req.json().get("zonages", [])
        return []

    def get_zone_path_for_point(
        self, lat: float, lon: float, type_coord: str = "gps"
    ) -> str:
        """
        Returns the zone path for a given point (latitude, longitude).
        """
        req = requests.get(
            f"{self.__host}/zonage/trouver-zone-chemin",
            params={"lat": lat, "lon": lon, "type_coord": type_coord},
        )
        if req.status_code == 200:
            zone_path = req.json().get("zone_path", "")
            return zone_path if zone_path else "No zone path found"
        return "Error: Unable to retrieve zone path"

    def get_zone_paths_for_points(
        self, points: List[Tuple[float, float]], type_coord: str = "gps"
    ) -> List[str]:
        """
        Returns the zone paths for multiple points (list of lat, lon tuples).
        """
        points_param = ";".join([f"{lat},{lon}" for lat, lon in points])
        req = requests.get(
            f"{self.__host}/zonage/trouver-zones-chemins",
            params={"points": points_param, "type_coord": type_coord},
        )
        if req.status_code == 200:
            return req.json().get("zone_paths", [])
        return []

    def get_zonage_nom(self) -> str:
        """
        Returns the name of the current zonage.
        """
        req = requests.get(f"{self.__host}/zonage/nom")
        if req.status_code == 200:
            return req.json().get("nom", "Unknown zonage")
        return "Error: Unable to retrieve zonage name"

    def get_all_zones(self) -> List[str]:
        """
        Returns the list of all zones in the current zonage.
        """
        req = requests.get(f"{self.__host}/zonage/zones")
        if req.status_code == 200:
            return req.json().get("zones", [])
        return []

###############################################################################
#################################### POST #####################################
###############################################################################

    def create_zonage(
        self, nom: str, zones: List[dict], zonage_mere_id: int = None
    ) -> str:
        """
        Create a new zonage with the given name, zones, and optional
        zonage_mere_id.
        """
        payload = {
            "nom": nom,
            "zones": zones,
            "zonage_mere_id": zonage_mere_id
        }
        req = requests.post(f"{self.__host}/zonages", json=payload)
        if req.status_code == 201:
            return "Zonage created successfully"
        return f"Error: Unable to create zonage, status code: {req.status_code}"

    def create_zone(
        self, zonage_id: int, nom: str, points: List[Tuple[float, float]]
    ) -> str:
        """
        Create a new zone in the specified zonage.
        """
        payload = {
            "nom": nom,
            "points": [{"lat": lat, "lon": lon} for lat, lon in points]
        }
        req = requests.post(
            f"{self.__host}/zonages/{zonage_id}/zones", json=payload
        )
        if req.status_code == 201:
            return "Zone created successfully"
        return f"Error: Unable to create zone, status code: {req.status_code}"

    def find_or_create_zone_for_point(
        self, zonage_id: int, point: Tuple[float, float], nom_zone: str
    ) -> str:
        """
        Finds the zone for a given point or creates a new zone if not found.
        """
        zonage = self.get_zonage_by_point(point[0], point[1])
        if zonage == "No zonage found":
            return self.create_zone(zonage_id, nom_zone, [point])
        return f"Zone found: {zonage}"

    def create_multiple_zones(
        self, zonage_id: int, zones: List[dict]
    ) -> str:
        """
        Create multiple zones in the specified zonage.
        """
        payload = {"zones": zones}
        req = requests.post(
            f"{self.__host}/zonages/{zonage_id}/zones/batch", json=payload
        )
        if req.status_code == 201:
            return "Zones created successfully"
        return f"Error: Unable to create zones, status code: {req.status_code}"

###############################################################################
################################## DELETE #####################################
###############################################################################

    def delete_zonage(self, zonage_id: int) -> str:
        """
        Deletes a zonage with the specified ID.
        """
        req = requests.delete(f"{self.__host}/zonages/{zonage_id}")
        if req.status_code == 204:
            return f"Zonage {zonage_id} deleted successfully"
        return f"Error: Unable to delete zonage {zonage_id}, status code: {req.status_code}"

    def delete_zone(self, zonage_id: int, zone_id: int) -> str:
        """
        Deletes a specific zone in a zonage.
        """
        req = requests.delete(f"{self.__host}/zonages/{zonage_id}/zones/{zone_id}")
        if req.status_code == 204:
            return f"Zone {zone_id} in zonage {zonage_id} deleted successfully"
        return f"Error: Unable to delete zone {zone_id}, status code: {req.status_code}"

    def delete_all_zones(self, zonage_id: int) -> str:
        """
        Deletes all zones in a zonage.
        """
        req = requests.delete(f"{self.__host}/zonages/{zonage_id}/zones")
        if req.status_code == 204:
            return f"All zones in zonage {zonage_id} deleted successfully"
        return f"Error: Unable to delete all zones in zonage {zonage_id}, status code: {req.status_code}"

###############################################################################
##################################### PUT #####################################
###############################################################################

    def update_zonage(
        self, zonage_id: int, nom: str = None, zones: List[dict] = None,
        zonage_mere_id: int = None
    ) -> str:
        """
        Updates an existing zonage with the provided information.
        """
        payload = {}
        if nom is not None:
            payload["nom"] = nom
        if zones is not None:
            payload["zones"] = zones
        if zonage_mere_id is not None:
            payload["zonage_mere_id"] = zonage_mere_id
        if not payload:
            return "Error: No data to update"
        req = requests.put(f"{self.__host}/zonages/{zonage_id}", json=payload)
        if req.status_code == 200:
            return f"Zonage {zonage_id} updated successfully"
        return f"Error: Unable to update zonage {zonage_id}, status code: {req.status_code}"

    def update_zone(
        self, zonage_id: int, zone_id: int, nom: str = None,
        points: List[Tuple[float, float]] = None
    ) -> str:
        """
        Updates a specific zone within a zonage.
        """
        payload = {}
        if nom is not None:
            payload["nom"] = nom
        if points is not None:
            payload["points"] = [{"lat": lat, "lon": lon} for lat, lon in points]
        if not payload:
            return "Error: No data to update"
        req = requests.put(
            f"{self.__host}/zonages/{zonage_id}/zones/{zone_id}", json=payload
        )
        if req.status_code == 200:
            return f"Zone {zone_id} updated successfully"
        return f"Error: Unable to update zone {zone_id}, status code: {req.status_code}"

###############################################################################
################################## MAIN #######################################
###############################################################################


if __name__ == "__main__":
    # Charger les variables d'environnement du fichier .env
    dotenv.load_dotenv(override=True)

    # Initialiser le client VEI
    vei_client = VEIClient()

    # Exemple d'appel d'une méthode : obtenir le zonage pour un point spécifique
    lat = 48.8566  # Coordonnée latitude (exemple : Paris)
    lon = 2.3522   # Coordonnée longitude
    zonage = vei_client.get_zonage_by_point(lat, lon)

    # Afficher le résultat
    print(f"Zonage for the point ({lat}, {lon}): {zonage}")
