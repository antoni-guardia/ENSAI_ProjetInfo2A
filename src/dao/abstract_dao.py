from abc import ABC, abstractmethod
from dao.bdd_connection import DBConnection
import logging
from utils.log_decorator import log


class AbstractDao(ABC):
    """
    Classe contenant les méthodes pour accéder à l'objet de la base de données
    """

    @abstractmethod
    def creer(self):
        """Création d'un objet dans la base de données

        Parameters
        ----------

        objet : Objet
            Objet à ajouter dans la bdd

        Returns

        id_objet : int
            None si l'objet n'a pas pu être créé
        """
        pass

    @abstractmethod
    def supprimer(self):
        """Suppression de la base de données

        Parameters
        ----------
        objet : Objet
            Objet à supprimer de la base de données

        Returns
        -------
            True si l'objet a bien été supprimé
        """
        pass

    @abstractmethod
    def trouver_id(self):
        """Trouver un objet grâce à ces données

        Parameters
        ----------
        objet : Objet
            Objet dont on cherche l'id

        Returns
        -------
        id_objet : int
            renvoie l'id du point que l'on cherche par ces coordonnées
        """
        pass

    @abstractmethod
    def trouver_par_id(self):
        """trouver un point grace à son id

        Parameters
        ----------
        id_objet : int
            numéro id de l'objet que l'on souhaite trouver

        Returns
        -------
        objet : Objet
            renvoie l'objet que l'on cherche par id
        """
        pass

    @log
    def requete(self, text_sql, dict_param=dict()):
        """Exécute une requête SQL sur la base de données et renvoie le résultat.

        Parameters
        ----------
        text_sql : str
            Commande SQL à exécuter.

        dict_param : dict
            Dictionnaire des paramètres de la requête.

        Returns
        -------
        result : list ou tuple
            Le résultat de la requête, ou None en cas d'erreur.

        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(text_sql, dict_param)
                    # Commit the transaction if it's an INSERT/UPDATE/DELETE
                    return cursor.fetchall()

        except Exception as e:
            logging.error(f"Query failed: {e}")
            return None

    @log
    def requete_no_return(self, text_sql, dict_param=dict()):
        """Exécute une requête SQL sur la base de données et renvoie le résultat.

        Parameters
        ----------
        text_sql : str
            Commande SQL à exécuter.

        dict_param : dict
            Dictionnaire des paramètres de la requête.

        Returns
        -------
        result : list ou tuple
            Le résultat de la requête, ou None en cas d'erreur.

        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(text_sql, dict_param)

        except Exception as e:
            logging.error(f"Query failed: {e}")
