-----------------------------------------------------------------
--Zonage
-------------------------------------------
CREATE TABLE Zonage (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(255) NOT NULL
);
-----------------------------------------------------------------
--Zone
-------------------------------------------
CREATE TABLE Zone(
    id SERIAL PRIMARY KEY,
    id_zonage INTEGER,
    nom VARCHAR(255) NOT NULL,
    population DECIMAL(6),
    code_insee VARCHAR(10),
    annee DECIMAL(4) NOT NULL,
    FOREIGN KEY (id_zonage) REFERENCES Zonage(id),
    cle_hash INTEGER
);
-----------------------------------------------------------------
--Point
-------------------------------------------
CREATE TABLE Point(
    id SERIAL PRIMARY KEY,
    x DECIMAL(9, 7) NOT NULL,
    y DECIMAL(10, 7) NOT NULL,
    UNIQUE (x, y)
);
-----------------------------------------------------------------
--Contour
-------------------------------------------
CREATE TABLE Contour(
    id SERIAL PRIMARY KEY,
    cle_hash INTEGER
);
-----------------------------------------------------------------
--OrdrePointContour
-------------------------------------------
CREATE TABLE OrdrePointContour(
    id_contour INTEGER,
    id_point INTEGER,
    cardinal DECIMAL(8) NOT NULL,
    PRIMARY KEY (cardinal, id_contour, id_point),
    FOREIGN KEY (id_point) REFERENCES Point(id),
    FOREIGN KEY (id_contour) REFERENCES Contour(id)
);
-----------------------------------------------------------------
--Polygone
-------------------------------------------
CREATE TABLE Polygone(
    id SERIAL PRIMARY KEY,
    cle_hash INTEGER
);
-----------------------------------------------------------------
--EstEnclave
-------------------------------------------
CREATE TABLE EstEnclave(
    est_enclave BOOLEAN NOT NULL,
    id_contour INTEGER,
    id_polygone INTEGER,
    PRIMARY KEY (id_polygone, id_contour),
    FOREIGN KEY (id_contour) REFERENCES Contour(id),
    FOREIGN KEY (id_polygone) REFERENCES Polygone(id)
);
-----------------------------------------------------------------
--MultiPolygone
-------------------------------------------
CREATE TABLE MultiPolygone(
    id_polygone INTEGER,
    id_zone INTEGER,
    PRIMARY KEY (id_zone, id_polygone),
    FOREIGN KEY (id_polygone) REFERENCES Polygone(id),
    FOREIGN KEY (id_zone) REFERENCES Zone(id)
);


-----------------------------------------------------------------
--ZoneFille
-------------------------------------------
CREATE TABLE ZoneFille(
    id_zone_mere INTEGER,
    id_zone_fille INTEGER,
    FOREIGN KEY (id_zone_mere) REFERENCES Zone(id),
    FOREIGN KEY (id_zone_fille) REFERENCES Zone(id),
    PRIMARY KEY (id_zone_mere, id_zone_fille)
);

-----------------------------------------------------------------
--ZonageMere
-------------------------------------------
CREATE TABLE ZonageMere(
    id_zonage_mere INTEGER,
    id_zonage_fille INTEGER,
    FOREIGN KEY (id_zonage_mere) REFERENCES Zonage(id),
    FOREIGN KEY (id_zonage_fille) REFERENCES Zonage(id),
    PRIMARY KEY (id_zonage_mere, id_zonage_fille)
)


