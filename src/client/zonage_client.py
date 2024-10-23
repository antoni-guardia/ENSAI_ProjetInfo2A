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

    def get_zonage_by_point(self, lat: float, lon: float, type_coord: str = "gps") -> str:
        """
        Returns the zonage name for a given point (latitude, longitude).
        """
        # Call to the Web service
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

    def get_zone_path_for_point(self, lat: float, lon: float, type_coord: str = "gps") -> str:
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

    def create_zonage(self, nom: str, zones: List[dict], zonage_mere_id: int = None) -> str:
        """
        Create a new zonage with the given name, zones, and optional
        zonage_mere_id.
        """
        payload = {"nom": nom, "zones": zones, "zonage_mere_id": zonage_mere_id}

        req = requests.post(f"{self.__host}/zonages", json=payload)
        if req.status_code == 201:
            return "Zonage created successfully"
        return f"Error: Unable to create zonage, status code: {req.status_code}"

    def create_zone(self, zonage_id: int, nom: str, points: List[Tuple[float, float]]) -> str:
        """
        Create a new zone in the specified zonage.
        """
        payload = {"nom": nom, "points": [{"lat": lat, "lon": lon} for lat, lon in points]}

        req = requests.post(f"{self.__host}/zonages/{zonage_id}/zones", json=payload)

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

    def create_multiple_zones(self, zonage_id: int, zones: List[dict]) -> str:
        """
        Create multiple zones in the specified zonage.

        Parameters
        ----------
        zonage_id : int
            The ID of the zonage where the zones will be created.
        zones : List[dict]
            A list of zones, each represented by a dictionary
            with 'nom' and 'points'.

        Returns
        -------
        str
            The result of the operation (success or failure message).
        """
        payload = {"zones": zones}

        req = requests.post(f"{self.__host}/zonages/{zonage_id}/zones/batch", json=payload)

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
    Supprime toutes les zones d'un zonage.

    Parameters
    ----------
    zonage_id : int
        L'ID du zonage dont toutes les zones doivent être supprimées.

    Returns
    -------
    str
        Message indiquant si la suppression a réussi ou échoué.
    """
    req = requests.delete(f"{self.__host}/zonages/{zonage_id}/zones")

    if req.status_code == 204:
        return f"All zones in zonage {zonage_id} deleted successfully"

    return (
        f"Error: Unable to delete all zones in zonage {zonage_id}, status code: {req.status_code}"
    )


###############################################################################
##################################### PUT #####################################
###############################################################################


def update_zonage(
    self, zonage_id: int, nom: str = None, zones: List[dict] = None, zonage_mere_id: int = None
) -> str:
    """
    Met à jour un zonage existant avec les informations fournies.

    Parameters
    ----------
    zonage_id : int
        L'ID du zonage à mettre à jour.
    nom : str, optional
        Le nouveau nom du zonage (si nécessaire).
    zones : List[dict], optional
        La liste des zones à mettre à jour (chaque zone est un dictionnaire
        contenant 'nom' et 'points').
    zonage_mere_id : int, optional
        L'ID du zonage mère (si nécessaire).

    Returns
    -------
    str
        Message indiquant si la mise à jour a réussi ou échoué.
    """
    payload = {}

    # Ajouter les champs mis à jour au payload seulement s'ils sont fournis
    if nom is not None:
        payload["nom"] = nom
    if zones is not None:
        payload["zones"] = zones
    if zonage_mere_id is not None:
        payload["zonage_mere_id"] = zonage_mere_id

    # Vérification pour ne pas envoyer un payload vide
    if not payload:
        return "Error: No data to update"

    req = requests.put(f"{self.__host}/zonages/{zonage_id}", json=payload)

    if req.status_code == 200:
        return f"Zonage {zonage_id} updated successfully"

    return f"Error: Unable to update zonage {zonage_id}, status code: {req.status_code}"


def update_zone(
    self, zonage_id: int, zone_id: int, nom: str = None, points: List[Tuple[float, float]] = None
) -> str:
    """
    Met à jour une zone spécifique dans un zonage.

    Parameters
    ----------
    zonage_id : int
        L'ID du zonage contenant la zone à mettre à jour.
    zone_id : int
        L'ID de la zone à mettre à jour.
    nom : str, optional
        Le nouveau nom de la zone (si nécessaire).
    points : List[Tuple[float, float]], optional
        Les nouveaux points délimitant la zone (si nécessaire).

    Returns
    -------
    str
        Message indiquant si la mise à jour a réussi ou échoué.
    """
    payload = {}

    # Ajouter les champs mis à jour au payload seulement s'ils sont fournis
    if nom is not None:
        payload["nom"] = nom
    if points is not None:
        payload["points"] = [{"lat": lat, "lon": lon} for lat, lon in points]

    # Vérification pour ne pas envoyer un payload vide
    if not payload:
        return "Error: No data to update"

    req = requests.put(f"{self.__host}/zonages/{zonage_id}/zones/{zone_id}", json=payload)

    if req.status_code == 200:
        return f"Zone {zone_id} in zonage {zonage_id} updated successfully"

    return f"Error: Unable to update zone {zone_id}, status code: {req.status_code}"
