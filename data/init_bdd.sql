CREATE TABLE Point(
    id SERIAL PRIMARY KEY,
    x DECIMAL(12, 2) NOT NULL,
    y DECIMAL(12, 2) NOT NULL,
    UNIQUE(x, y)
);

CREATE TABLE Contour(
    id SERIAL PRIMARY KEY
);

CREATE TABLE OrdrePointContour(
    cardinal DECIMAL(8) NOT NULL,
    FOREIGN KEY (id_point) REFERENCES Point(id),
    FOREIGN KEY (id_contour) REFERENCES Contour(id),
    UNIQUE cardinal
);

CREATE TABLE Polygone(
    id SERIAL PRIMARY KEY
);

CREATE TABLE EstEnclave(
    est_enclave BIT NOT NULL,
    FOREIGN KEY (id_contour) REFERENCES Contour(id),
    FOREIGN KEY (id_polygone) REFERENCES Polygone(id),
    UNIQUE(id_contour, id_polygone)
);

CREATE TABLE MultiPolygone (
    annee DECIMAL(4) NOT NULL,
    FOREIGN KEY (id_polygone) REFERENCES Polygone(id),
    UNIQUE(annee, id_polygone)
);

CREATE TABLE Zone(
    id SERIAL PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,
    population DECIMAL(6),
    code_insee VARCHAR(10) OR NULL,
    FOREIGN KEY (id_zonage) REFERENCES Zonage(id)
);

CREATE TABLE Zonage (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,
);

CREATE TABLE ZoneFille(
    FOREIGN KEY (id_zone_mere) REFERENCES Zone(id),
    FOREIGN KEY (id_zone_fille) REFERENCES Zone(id),
    UNIQUE(id_zone_mere, id_zone_fille)
);


CREATE TABLE ZonageMere(
    FOREIGN KEY (id_zonage_mere) REFERENCES Zonage(id),
    FOREIGN KEY (id_zonage_fille) REFERENCES Zonage(id),
    UNIQUE (id_zonage_mere, id_zone_fille)
)