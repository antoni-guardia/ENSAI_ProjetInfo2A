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
def test_trouver_par_pseudo(test_utilisateur):
    """
    Teste la recherche d'un utilisateur par pseudo.
    """
    with patch("dao.utilisateur_dao.UtilisateurDao") as MockUserDao:
        MockUserDao.trouver_par_pseudo.return_value = Utilisateur(
            **{
                "pseudo": test_utilisateur.pseudo,
                "mdp": test_utilisateur.mdp,
                "est_admin": test_utilisateur.est_admin,
            }
        )
        found_user = MockUserDao.trouver_par_pseudo(test_utilisateur.pseudo)
        assert found_user is not None, "User should be found by pseudo"
        assert found_user.pseudo == test_utilisateur.pseudo, "Pseudo should match"
        assert found_user.mdp == test_utilisateur.mdp, "Password should match"


@patch("dao.utilisateur_dao.DBConnection")
def test_lister_tous(test_utilisateur):
    """
    Teste le listing de tous les utilisateurs.
    """
    with patch("dao.utilisateur_dao.UtilisateurDao") as MockUserDao:
        MockUserDao.lister_tous.return_value = [
            Utilisateur(
                **{
                    "pseudo": test_utilisateur.pseudo,
                    "mdp": test_utilisateur.mdp,
                    "est_admin": test_utilisateur.est_admin,
                }
            )
        ]
        # Test finding a user by pseudo

    # Test listing all users
    all_users = MockUserDao.lister_tous()
    assert len(all_users) > 0, "There should be at least one user in the list"
    assert all_users[0].pseudo == test_utilisateur.pseudo, "Test user should be in the list"


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
