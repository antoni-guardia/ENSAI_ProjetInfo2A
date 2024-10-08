import fiona

path = "/home/rogerbernat/Documents/ENSAI_ProjetInfo2A/ADMIN-EXPRESS_3-2__SHP_LAMB93_FXX_2024-09-18/ADMIN-EXPRESS/1_DONNEES_LIVRAISON_2024-09-00118/ADE_3-2_SHP_LAMB93_FXX-ED2024-09-18/COMMUNE.shp"
with fiona.open(path, "r") as raw_zones:
    print(raw_zones[0]["properties"]["NOM"])
    print(raw_zones[0]["properties"]["POPULATION"])

