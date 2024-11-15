--DROP SCHEMA IF EXISTS utilisateur_bdd CASCADE;
CREATE SCHEMA utlisateur_bdd;
CREATE TABLE utlisateur_bdd.donnees_utilisateur (
    -- id --
    username VARCHAR(50) UNIQUE NOT NULL,
    mot_de_passe VARCHAR(255) NOT NULL
    est_admin BOOLEAN DEFAULT FALSE
);



