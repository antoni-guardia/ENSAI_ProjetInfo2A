import pytest
from dao.utilisateur_dao import UtilisateurDao
from business_object.utilisateur import Utilisateur


@pytest.fixture
def utilisateur_dao():
    return UtilisateurDao()


@pytest.fixture
def test_utilisateur():
    return Utilisateur(pseudo="test_user", mdp="password", est_admin=False)


@patch("dao.utilisateur_dao.DBConnection")
def test_creer_utilisateur(test_utilisateur):
    # GIVEN
    user = test_utilisateur

    # Utilisation du patch pour remplacer PointDao
    with patch("dao.utilisateur_dao.UtilisateurDao") as MockUserDao:
        # On configure le mock pour que la méthode creer retourne un id fictif (42)
        MockUserDao.creer_utlisateur.return_value = True

        # WHEN
        created = MockUserDao().creer_utlisateur(user)

        # THEN
        assert created


@patch("dao.utilisateur_dao.DBConnection")
def test_trouver_par_pseudo(test_utilisateur):
    # Mock the connection and cursor
    with patch("dao.utilisateur_dao.UtilisateurDao") as MockUserDao:
        # On configure le mock pour que la méthode creer retourne un id fictif (42)
        MockUserDao.trouver_par_pseudo.return_value = Utilisateur(
            **{
                "pseudo": test_utilisateur.pseudo,
                "mdp": test_utilisateur.mdp,
                "est_admin": test_utilisateur.est_admin,
            }
        )
        # Test finding a user by pseudo
        found_user = MockUserDao.trouver_par_pseudo(test_utilisateur.pseudo)
        assert found_user is not None, "User should be found by pseudo"
        assert found_user.pseudo == test_utilisateur.pseudo, "Pseudo should match"
        assert found_user.mdp == test_utilisateur.mdp, "Password should match"


@patch("dao.utilisateur_dao.DBConnection")
def test_lister_tous(test_utilisateur):
    # Mock the connection and cursor
    # Mock the connection and cursor
    with patch("dao.utilisateur_dao.UtilisateurDao") as MockUserDao:
        # On configure le mock pour que la méthode creer retourne un id fictif (42)
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
    with patch("dao.utilisateur_dao.UtilisateurDao") as MockUserDao:
        # On configure le mock pour que la méthode creer retourne un id fictif (42)
        new_mdp = "new_password"
        MockUserDao.modifier_mdp.return_value = True

        modified = MockUserDao.modifier_mdp(test_utilisateur, new_mdp)
        assert modified is True, "Password should be updated successfully"


@patch("dao.utilisateur_dao.DBConnection")
def test_supprimer_utilisateur(test_utilisateur):
    with patch("dao.utilisateur_dao.UtilisateurDao") as MockUserDao:
        # On configure le mock pour que la méthode creer retourne un id fictif (42)
        MockUserDao.supprimer_utilisateur.return_value = True

        delete = MockUserDao.supprimer_utilisateur(test_utilisateur)
        assert delete is True, "Password should be updated successfully"
