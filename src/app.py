from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from dao.zonage_dao import ZonageDAO
from business_object.zonage import Zonage
from service.ajouter_donnees_par_path import AjouterDonneesParPath
from service.services_fichier import ServicesFichierLecture
from service.services_recherche_point import ServicesRecherchePoint
from service.services_trouver_zone_par import ServicesRechercheZone

app = FastAPI()


class ZoneModel(BaseModel):
    id: int
    name: str


class ZonageModel(BaseModel):
    id: Optional[int] = None
    nom: str
    zones: List[ZoneModel] = []
    zonage_mere: Optional[int] = None  # Assuming zonage_mere is an ID


# Create a zonage
@app.post("/zonage/", response_model=int)
async def create_zonage(zonage: ZonageModel):
    zonage_dao = ZonageDAO()
    id_zonage = zonage_dao.creer(
        Zonage(nom=zonage.nom, zones=zonage.zones, zonage_mere=zonage.zonage_mere)
    )
    if id_zonage is None:
        raise HTTPException(status_code=400, detail="Error creating zonage")
    return id_zonage


# Get zonage by ID
@app.get("/zonage/{id_zonage}", response_model=ZonageModel)
async def get_zonage(id_zonage: int):
    zonage_dao = ZonageDAO()
    zonage = zonage_dao.trouver_par_id(id_zonage)
    if zonage is None:
        raise HTTPException(status_code=404, detail="Zonage not found")
    return ZonageModel(
        id=zonage.id, nom=zonage.nom, zones=zonage.zones, zonage_mere=zonage.zonage_mere
    )


# Get all zones associated with a zonage
@app.get("/zonage/{id_zonage}/zones", response_model=List[ZoneModel])
async def get_zones(id_zonage: int):
    zonage_dao = ZonageDAO()
    zones = zonage_dao.get_zones(id_zonage)
    if zones is None:
        raise HTTPException(status_code=404, detail="No zones found")
    return [ZoneModel(id=zone.id, name=zone.name) for zone in zones]


# Delete a zonage
@app.delete("/zonage/{id_zonage}", response_model=bool)
async def delete_zonage(id_zonage: int):
    zonage_dao = ZonageDAO()
    result = zonage_dao.supprimer(id_zonage)
    if not result:
        raise HTTPException(status_code=404, detail="Zonage not found or cannot be deleted")
    return result


class DataModel(BaseModel):
    path: str
    annee: int
    reinitialiser: bool = False
    attrib_zones_zonages: bool = False
    dict_hierarchique: dict = dict()


# Create a zonage
@app.post("/donnees/creation", response_model=int)
async def create_data(data: DataModel):
    create = AjouterDonneesParPath()
    create.creer(
        path=data.path,
        annee=data.annee,
        reinitialiser=data.reinitialiser,
        attrib_zones_zonages=data.attrib_zones_zonages,
        given_dict=data.dict_hierarchique,
    )


# Get all zones associated with a zonage


class ZoneModel(BaseModel):
    path_enregistrement: str
    nom_zonage: str
    annee: int
    attrib_zones_zonages: bool = False
    liste_points: list[tuple]
    type_coord: tuple = None
    type_fichier: str = ".txt"


@app.get("/trouver_multiple_zone_point", response_model=List[ZoneModel])
async def trouver_point(zone: ZoneModel):
    fichier = ServicesFichierLecture()
    fichier.trouver_multiple_zone_point(
        path_enregistrement=zone.path_enregistrement,
        nom_zonage=zone.nom_zonage,
        annee=zone.annee,
        attrib_zones_zonages=zone.attrib_zones_zonages,
        liste_points=zone.liste_points,
        type_coord=zone.type_coord,
        type_fichier=zone.type_fichier,
    )


class pointModel(BaseModel):
    nom_zonage: str
    x: float
    y: float
    type_coord: str = None


@app.get("/recherche zone par point", response_model=List[ZoneModel])
async def recherche_zone(recherche: pointModel):
    fichier = ServicesRecherchePoint()
    fichier.trouver_zone_point(
        nom_zonage=recherche.nom_zonage,
        x=recherche.x,
        y=recherche.y,
        type_coord=recherche.type_coord,
    )


class pathModel(BaseModel):
    nom_zonage: str
    x: float
    y: float
    type_coord: str = None


@app.get("/recherche path zone par point", response_model=List[ZoneModel])
async def recherche_path(recherche: pathModel):
    fichier = ServicesRecherchePoint()
    fichier.trouver_chemin_zones_point(
        nom_zonage=recherche.nom_zonage,
        x=recherche.x,
        y=recherche.y,
        type_coord=recherche.type_coord,
    )


class pointsModel(BaseModel):
    nom_zonage: str
    liste_points: list[tuple]
    annee: int
    type_coord: str = None


@app.get("/recherche les zones de multiples point", response_model=List[ZoneModel])
async def recherche_zone_multiples_points(recherche: pointsModel):
    fichier = ServicesRecherchePoint()
    fichier.trouver_multiple_zone_point(
        nom_zonage=recherche.nom_zonage,
        points=recherche.liste_points,
        annee=recherche.annee,
        type_coord=recherche.type_coord,
    )


class zoneparcodeinsee(BaseModel):
    code_insee: int
    annee: int


@app.get("/recherche les zones par code insee", response_model=List[ZoneModel])
async def recherche_zone_code_insee(recherche: zoneparcodeinsee):
    fichier = ServicesRechercheZone()
    fichier.nom_par_code_insee(
        code_insee=recherche.code_insee,
        annee=recherche.annee,
    )


class info_nom(BaseModel):
    nom: str
    annee: int


@app.get("/recherche des info du zone par nom", response_model=List[ZoneModel])
async def recherche_zone_nom(recherche: info_nom):
    fichier = ServicesRechercheZone()
    fichier.tout_par_nom(
        nom=recherche.nom,
        annee=recherche.annee,
    )


class infos_code_insee(BaseModel):
    code_insee: int
    annee: int


@app.get("/recherche des info du zone par code insee", response_model=List[ZoneModel])
async def recherche_zone_nom(recherche: infos_code_insee):
    fichier = ServicesRechercheZone()
    fichier.tout_par_code_insee(
        code_insee == recherche.code_insee,
        annee=recherche.annee,
    )


# Run the FastAPI application
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8501)
