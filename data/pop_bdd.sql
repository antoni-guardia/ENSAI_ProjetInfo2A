-- Assuming the tables have been created already as per your structure

-- Populate Zonage
INSERT INTO Zonage (nom) VALUES 
('Zonage 1'),
('Zonage 2'),
('Zonage 3');

-- Populate Zone
INSERT INTO Zone (id_zonage, nom, population, code_insee, annee) VALUES 
(1, 'Zone A', 1500, '12345', 2023),
(1, 'Zone B', 2000, '67890', 2022),
(2, 'Zone C', 800, '54321', 2023);

-- Populate Point
INSERT INTO Point (x, y) VALUES 
(1.50, 2.50),
(3.00, 4.00),
(5.25, 6.75),
(2.00, 3.00);

-- Populate Contour
INSERT INTO Contour (id) VALUES 
(1),
(2);

-- Populate OrdrePointContour
INSERT INTO OrdrePointContour (id_contour, id_point, cardinal) VALUES 
(1, 1, 1),
(1, 2, 2),
(2, 3, 1),
(2, 4, 2);

-- Populate Polygone
INSERT INTO Polygone (id) VALUES 
(1),
(2),
(3);

-- Populate EstEnclave
INSERT INTO EstEnclave (est_enclave, id_contour, id_polygone) VALUES 
(1, 1, 1),
(0, 2, 2),
(1, 1, 3);

-- Populate MultiPolygone
INSERT INTO MultiPolygone (id_polygone, id_zone) VALUES 
(1, 1),
(2, 2),
(3, 3);

-- Populate ZoneFille
INSERT INTO ZoneFille (id_zone_mere, id_zone_fille) VALUES 
(1, 2),
(2, 3);

-- Populate ZonageMere
INSERT INTO ZonageMere (id_zonage_mere, id_zonage_fille) VALUES 
(1, 2),
(2, 3);
