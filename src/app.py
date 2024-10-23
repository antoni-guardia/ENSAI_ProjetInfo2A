from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from dao.zonage_dao import ZonageDAO
from business_object.zonage import Zonage

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


# Run the FastAPI application
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=80)
