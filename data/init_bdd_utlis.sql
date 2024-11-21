DROP SCHEMA IF EXISTS utilisateur_bdd CASCADE;
CREATE SCHEMA utlisateur_bdd;
CREATE TABLE utlisateur_bdd.donnees_utilisateur (
    pseudo VARCHAR(50) UNIQUE NOT NULL,
    mdp VARCHAR(255) NOT NULL
);



