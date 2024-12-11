from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from service.services_trouver_zone_par import ServicesRechercheZone
from service.services_recherche_point import ServicesRecherchePoint
from service.services_fichier import ServicesFichierLecture

app = FastAPI()


# Rutes
@app.get("/recherche_info/code_insee/")
def recherche_tout_par_code_insee(code_insee: str, annee: int):
    try:
        result = ServicesRechercheZone().tout_par_code_insee(code_insee, annee)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/recherche_info/nom/")
def recherche_tout_par_nom(nom: str, annee: int):
    try:
        result = ServicesRechercheZone().tout_par_nom(nom, annee)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/recherche_nom/code_insee/")
def recherche_nom_par_code_insee(code_insee: str, annee: int):
    try:
        result = ServicesRechercheZone().nom_par_code_insee(code_insee, annee)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/recherche_zone/point/")
def recherche_zone_par_point(
    nom_zonage: str, longitude: float, latitude: float, annee: str, type_coord: str = None
):
    try:
        result = ServicesRecherchePoint().trouver_zone_point(
            nom_zonage, latitude, longitude, annee, type_coord
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/recherche_zones/point/")
def recherche_zones_par_point(
    longitude: float, latitude: float, annee: str, type_coord: str = None
):
    try:
        result = ServicesRecherchePoint().trouver_chemin_zones_point(
            latitude, longitude, annee, type_coord
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class PointsRequest(BaseModel):
    nom_zonage: str
    annee: int
    liste_points: list[list[float]]


@app.post("/recherche_zone/multiple_point/")
def recherche_zones_par_dict_point(request: PointsRequest):
    try:

        output_file = ServicesRecherchePoint().trouver_multiple_zone_point(
            nom_zonage=request.nom_zonage,
            liste_points=request.liste_points,
            annee=request.annee,
        )

        return output_file
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))


class PointsRequestSave(BaseModel):
    path_enregistrement: str
    nom_zonage: str
    annee: int
    liste_points: list[list[float]]
    type_fichier: str


@app.post("/sauvegarde_zone/multiple_point/")
def sauvegarde_zone_par_dict_point(request: PointsRequestSave):
    try:

        output_file = ServicesFichierLecture().trouver_multiple_zone_point(
            path_enregistrement=request.path_enregistrement,
            nom_zonage=request.nom_zonage,
            liste_points=request.liste_points,
            annee=request.annee,
            type_fichier=request.type_fichier,
        )

        return output_file
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8501)
