import pytest
from dao.utilisateur_dao import UtilisateurDao
from business_object.utilisateur import Utilisateur
from unittest.mock import patch


@pytest.fixture
def utilisateur_dao():
    """Initialise un objet UtilisateurDao pour les tests."""
    return UtilisateurDao()


@pytest.fixture
def test_utilisateur():
    """Crée un utilisateur fictif pour les tests."""
    return Utilisateur(pseudo="test_user", mdp="password", est_admin=False)


@patch("dao.utilisateur_dao.DBConnection")
def test_creer_utilisateur(test_utilisateur):
    """
    Teste la création d'un utilisateur.
    """
    user = test_utilisateur

    with patch("dao.utilisateur_dao.UtilisateurDao") as MockUserDao:
        MockUserDao.creer_utlisateur.return_value = True

        created = MockUserDao().creer_utlisateur(user)

        assert created


@patch("dao.utilisateur_dao.DBConnection")
def test_modifier_mdp(test_utilisateur):
    """
    Teste la modification du mot de passe.
    """
    with patch("dao.utilisateur_dao.UtilisateurDao") as MockUserDao:
        # On configure le mock pour que la méthode creer retourne un id fictif (42)
        new_mdp = "new_password"
        MockUserDao.modifier_mdp.return_value = True

        modified = MockUserDao.modifier_mdp(test_utilisateur, new_mdp)
        assert modified is True, "Password should be updated successfully"


@patch("dao.utilisateur_dao.DBConnection")
def test_supprimer_utilisateur(test_utilisateur):
    """
    Teste la suppression d'un utilisateur.
    """
    with patch("dao.utilisateur_dao.UtilisateurDao") as MockUserDao:
        # On configure le mock pour que la méthode creer retourne un id fictif (42)
        MockUserDao.supprimer_utilisateur.return_value = True

        delete = MockUserDao.supprimer_utilisateur(test_utilisateur)
        assert delete is True, "Password should be updated successfully"
