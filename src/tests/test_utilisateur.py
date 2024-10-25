import unittest
from unittest.mock import patch, MagicMock
from dao.bdd_connection import DBConnection
from business_object.utilisateur import Utilisateur
from dao.utilisateur_dao import UtilisateurDao  # Remplacez 'votre_module' par le nom de votre fichier

class TestUtilisateurDao(unittest.TestCase):

    @patch('dao.bdd_connection.DBConnection')
    def test_creer_utilisateur(self, MockDBConnection):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        MockDBConnection.return_value.connection.__enter__.return_value = mock_connection
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        
        utilisateur = Utilisateur("testuser", "password", False)
        dao = UtilisateurDao()
        
        # Simuler un succès de l'insertion
        mock_cursor.rowcount = 1
        
        created = dao.creer_utlisateur(utilisateur)
        self.assertTrue(created)
        mock_cursor.execute.assert_called_once()  # Vérifier si execute a été appelé

    @patch('dao.bdd_connection.DBConnection')
    def test_trouver_par_pseudo(self, MockDBConnection):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        MockDBConnection.return_value.connection.__enter__.return_value = mock_connection
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        
        pseudo = "testuser"
        mock_cursor.fetchone.return_value = {"pseudo": "testuser", "mdp": "password", "est_admin": False}
        
        dao = UtilisateurDao()
        utilisateur = dao.trouver_par_pseudo(pseudo)
        
        self.assertIsNotNone(utilisateur)
        self.assertEqual(utilisateur.pseudo, pseudo)

    @patch('dao.bdd_connection.DBConnection')
    def test_lister_tous(self, MockDBConnection):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        MockDBConnection.return_value.connection.__enter__.return_value = mock_connection
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        
        mock_cursor.fetchall.return_value = [
            {"pseudo": "user1", "mdp": "pass1", "est_admin": False},
            {"pseudo": "user2", "mdp": "pass2", "est_admin": True},
        ]
        
        dao = UtilisateurDao()
        utilisateurs = dao.lister_tous()
        
        self.assertEqual(len(utilisateurs), 2)
        self.assertEqual(utilisateurs[0].pseudo, "user1")

    @patch('dao.bdd_connection.DBConnection')
    def test_modifier_mdp(self, MockDBConnection):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        MockDBConnection.return_value.connection.__enter__.return_value = mock_connection
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        
        utilisateur = Utilisateur("testuser", "oldpassword", False)
        
        # Simuler un succès de la mise à jour
        mock_cursor.rowcount = 1
        
        dao = UtilisateurDao()
        result = dao.modifier_mdp(utilisateur, "newpassword")
        
        self.assertTrue(result)

    @patch('dao.bdd_connection.DBConnection')
    def test_supprimer_utilisateur(self, MockDBConnection):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        MockDBConnection.return_value.connection.__enter__.return_value = mock_connection
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        
        utilisateur = Utilisateur("testuser", "password", False)
        
        # Simuler un succès de la suppression
        mock_cursor.rowcount = 1
        
        dao = UtilisateurDao()
        result = dao.supprimer_utlisateur(utilisateur)
        
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
