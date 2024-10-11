DROP SCHEMA IF EXISTS project CASCADE;
CREATE SCHEMA project;
-----------------------------------------------------------------
--Point
-------------------------------------------
DROP TABLE IF EXISTS project.Point CASCADE ;
CREATE TABLE project.Point(
    id SERIAL PRIMARY KEY,
    x DECIMAL(12, 2) NOT NULL,
    y DECIMAL(12, 2) NOT NULL,
    UNIQUE(x, y)
);

-----------------------------------------------------------------
--Contour
-------------------------------------------
DROP TABLE IF EXISTS project.Contour CASCADE ;

CREATE TABLE project.Contour(
    id SERIAL PRIMARY KEY
);
-----------------------------------------------------------------
--OrdrePointContour
-------------------------------------------
DROP TABLE IF EXISTS project.OrdrePointContour CASCADE ;
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
DROP TABLE IF EXISTS project.Polygone CASCADE ;
CREATE TABLE project.Polygone(
    id SERIAL PRIMARY KEY
);
-----------------------------------------------------------------
--EstEnclave
-------------------------------------------
DROP TABLE IF EXISTS project.EstEnclave CASCADE ;
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
------------------------------------------
DROP TABLE IF EXISTS project.MultiPolygone CASCADE ;
CREATE TABLE project.MultiPolygone (
    annee DECIMAL(4) NOT NULL,
    id_polygone INTEGER,
    PRIMARY KEY (annee, id_polygone),
    FOREIGN KEY (id_polygone) REFERENCES project.Polygone(id)
);
-----------------------------------------------------------------
--Zonage
-------------------------------------------
DROP TABLE IF EXISTS project.Zonage CASCADE ;
CREATE TABLE project.Zonage (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(255) NOT NULL
);
-----------------------------------------------------------------
--Zone
-------------------------------------------
DROP TABLE IF EXISTS project.Zone CASCADE ;
CREATE TABLE project.Zone(
    id SERIAL PRIMARY KEY,
    id_zonage INTEGER,
    nom VARCHAR(255) NOT NULL,
    population DECIMAL(6),
    code_insee VARCHAR(10),
    FOREIGN KEY (id_zonage) REFERENCES project.Zonage(id)
);

-----------------------------------------------------------------
--ZoneFille
-------------------------------------------
DROP TABLE IF EXISTS project.Fille CASCADE ;
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
DROP TABLE IF EXISTS project.ZonageMere CASCADE ;
CREATE TABLE project.ZonageMere(
    id_zonage_mere INTEGER,
    id_zonage_fille INTEGER,
    FOREIGN KEY (id_zonage_mere) REFERENCES project.Zonage(id),
    FOREIGN KEY (id_zonage_fille) REFERENCES project.Zonage(id),
    PRIMARY KEY (id_zonage_mere, id_zonage_fille)
)


