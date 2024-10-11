import fiona

path = ("data/ADMIN-EXPRESS_3-2__SHP_WGS84G_FRA_2024-08-26/ADMIN-EXPRESS/1_DONNEES_LIVRAISON_2024-08-00122/ADE_3-2_SHP_WGS84G_FRA-ED2024-08-26/EPCI.shp")
shp = fiona.open(path, 'r')
features = shp[0]
print(features)
