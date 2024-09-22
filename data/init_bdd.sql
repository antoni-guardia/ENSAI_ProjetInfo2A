CREATE TABLE MultiPolygone (
    id_multipolygone SERIAL PRIMARY KEY,
    contour GEOMETRY -- PostGIS extension à savoir utiliser
);

CREATE TABLE Zone (
    id_zone SERIAL PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,
    id_multipolygone INT NOT NULL,
    id_zones_fille INT[] DEFAULT NULL,
    FOREIGN KEY (id_multipolygone) REFERENCES MultiPolygone(id_multipolygone)
);


CREATE TABLE Zonage (
    id_zonage SERIAL PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,
    id_zonage_mere INT DEFAULT NULL,
    annee VARCHAR(255) NOT NULL,
);
