-- Assuming the tables have been created already as per your structure

-- Populate Zonage
INSERT INTO Zonage (nom) VALUES 
('Corona d Aragò'),
('Corones Europees');

-- Populate Zone cle_hash = sum(id_polygone* 37^i) mod 10^4 +7
-- i allant de 1 jusqu'a nombre de contours dans polygone
INSERT INTO Zone (id, id_zonage, nom, population, code_insee, annee, max_x, min_x, max_y, min_y, cle_hash) VALUES 
(1, 1, 'Principat', 5000, '0', 1315, 11.49, 8.79, 8.19, 5.53, 3602988),
(2, 1, 'Regne de València', 2000, '1', 1315, 8.87, 7.57, 7.53, 4.09, 5194271),
(3, 1, 'Aragó', 40, '2', 1315, 8.87, 7.57, 8.19, 5.53, 5680654),
(4, 2, 'Corona d Aragò', 800, '3', 1315, 11.49, 7.57, 8.19, 4.09, 4603439),
(5, 2, 'Corona França', 1000, '4', 1315, 13.39, 6.75, 16.31, 8.0, 1084790);

-- Populate Point
INSERT INTO Point (id, x, y) VALUES 
(1, 8.77, 4.09),
(2, 8.87, 5.53),
(3, 10.55, 6.53),
(4, 11.49, 7.53),
(5, 11.35, 8.05),
(6, 8.79, 8.19),
(7, 7.57, 7.53),
(8, 7.97, 4.15),
(9, 7.69, 6.27),
(10, 8.33, 6.13),
(11, 8.87, 7.11),
(12, 12.55, 8.63),
(13, 13.39, 13.45),
(14, 12.15, 16.31),
(15, 6.75, 14.07),
(16, 9.69, 10.33),
(17, 10, 8);


-- Populate Contour ; hash == sum(x)*37 - sum(y)*73 mod 10^5 + 3
INSERT INTO Contour (id, cle_hash) VALUES 
(1, 4830567),
(2, 358277),
(3, 5978687),
(4, 2284894),
(5, 704578)
;

-- Populate OrdrePointContour
INSERT INTO OrdrePointContour (id_contour, id_point, cardinal) VALUES 
(1, 1, 1),
(1, 2, 2),
(1, 3, 3),
(1, 4, 4),
(1, 5, 5),
(1, 17, 6),
(1, 6, 7),
(1, 7, 8),
(1, 9, 9),
(1, 8, 10),
(2, 2, 1),
(2, 3, 2),
(2, 4, 3),
(2, 5, 4),
(2, 17, 5),
(2, 6, 6),
(2, 11, 7),
(3, 2, 1),
(3, 11, 2),
(3, 6, 3),
(3, 7, 4),
(3, 10, 5),
(4, 1, 1),
(4, 2, 2),
(4, 10, 3),
(4, 7, 4),
(4, 9, 5),
(4, 8, 6),
(5, 5, 1),
(5, 12, 2),
(5, 13, 3),
(5, 14, 4),
(5, 15, 5),
(5, 16, 6),
(5, 6, 7),
(5, 17, 8)
;

-- Populate Polygone ; cle_hash = sum(id_contour* 37^i) mod 10^4 +7
-- i allant de 1 jusqu'a nombre de contours dans polygone
INSERT INTO Polygone (id, cle_hash) VALUES 
(1, 7348671),
(2, 830115),
(3, 9072229),
(4, 9497098),
(5, 5518345);

-- Populate EstEnclave
INSERT INTO EstEnclave (est_enclave, id_contour, id_polygone) VALUES 
(FALSE, 1, 1),
(FALSE, 2, 2),
(FALSE, 3, 3),
(FALSE, 5, 5);
-- Populate MultiPolygone
INSERT INTO MultiPolygone (id_polygone, id_zone) VALUES 
(1, 4),
(2, 3),
(3, 2),
(4, 1),
(5, 5);

-- Populate ZoneFille
INSERT INTO ZoneFille (id_zone_mere, id_zone_fille) VALUES 
(4, 1),
(4, 2),
(4, 3);

-- Populate ZonageMere
INSERT INTO ZonageMere (id_zonage_mere, id_zonage_fille) VALUES 
(2, 1)
;
