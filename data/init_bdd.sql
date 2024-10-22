-- DROP SCHEMA IF EXISTS project CASCADE;
CREATE SCHEMA project;
-----------------------------------------------------------------
--Point
-------------------------------------------
CREATE TABLE project.Point(
    id SERIAL PRIMARY KEY,
    x DECIMAL(12, 2) NOT NULL,
    y DECIMAL(12, 2) NOT NULL,
    UNIQUE(x, y)
);
-----------------------------------------------------------------
--Contour
-------------------------------------------
CREATE TABLE project.Contour(
    id SERIAL PRIMARY KEY
);
-----------------------------------------------------------------
--OrdrePointContour
-------------------------------------------
CREATE TABLE project.OrdrePointContour(
    id_contour INTEGER,
    id_point INTEGER,
    cardinal DECIMAL(8) NOT NULL,
    PRIMARY KEY (cardinal, id_contour),
    FOREIGN KEY (id_point) REFERENCES project.Point(id),
    FOREIGN KEY (id_contour) REFERENCES project.Contour(id)
);
-----------------------------------------------------------------
--Polygone
-------------------------------------------
CREATE TABLE project.Polygone(
    id SERIAL PRIMARY KEY
);
-----------------------------------------------------------------
--EstEnclave
-------------------------------------------
CREATE TABLE project.EstEnclave(
    est_enclave BIT NOT NULL,
    id_contour INTEGER,
    id_polygone INTEGER,
    PRIMARY KEY (id_polygone, id_contour),
    FOREIGN KEY (id_contour) REFERENCES project.Contour(id),
    FOREIGN KEY (id_polygone) REFERENCES project.Polygone(id)
);
-----------------------------------------------------------------
--MultiPolygone
-------------------------------------------
CREATE TABLE project.MultiPolygone(
    id_polygone INTEGER,
    id_zone INTEGER,
    PRIMARY KEY (id_zone, id_polygone),
    FOREIGN KEY (id_polygone) REFERENCES project.Polygone(id),
    FOREIGN KEY (id_zone) REFERENCES project.Zone(id)
);
-----------------------------------------------------------------
--Zonage
-------------------------------------------
CREATE TABLE project.Zonage (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(255) NOT NULL
);
-----------------------------------------------------------------
--Zone
-------------------------------------------
CREATE TABLE project.Zone(
    id SERIAL PRIMARY KEY,
    id_zonage INTEGER,
    nom VARCHAR(255) NOT NULL,
    population DECIMAL(6),
    code_insee VARCHAR(10),
    annee DECIMAL(4) NOT NULL,
    FOREIGN KEY (id_zonage) REFERENCES project.Zonage(id)
);

-----------------------------------------------------------------
--ZoneFille
-------------------------------------------
CREATE TABLE project.ZoneFille(
    id_zone_mere INTEGER,
    id_zone_fille INTEGER,
    FOREIGN KEY (id_zone_mere) REFERENCES project.Zone(id),
    FOREIGN KEY (id_zone_fille) REFERENCES project.Zone(id),
    PRIMARY KEY (id_zone_mere, id_zone_fille)
);

-----------------------------------------------------------------
--ZonageMere
-------------------------------------------
CREATE TABLE project.ZonageMere(
    id_zonage_mere INTEGER,
    id_zonage_fille INTEGER,
    FOREIGN KEY (id_zonage_mere) REFERENCES project.Zonage(id),
    FOREIGN KEY (id_zonage_fille) REFERENCES project.Zonage(id),
    PRIMARY KEY (id_zonage_mere, id_zonage_fille)
)


