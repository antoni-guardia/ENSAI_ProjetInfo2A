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
        """Creation d'un objet dans la base de données

        Parameters
        ----------

        objet : Objet
            Objet à ajouter dans la bdd

        Returns

        id_objet : int
            None si l'objet n'a pas pu être crée
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
        """trouver un objet grace à ces données

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
            renvoie le objet que l'on cherche par id
        """
        pass

    @log
    def requete(self, text_sql, dict_param=dict()):
        """Réalisation d'une reauete sur la bdd

        Parameters
        ----------
        text_sql : string
            commande à executer

        dict_param : dict
            dictionnaire des parametres de la requete

        Returns
        -------
        result : List
            renvoie le resultat de la requete
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(text_sql, dict_param)
                    results = cursor.fetchall()

        except Exception as e:
            logging.info(e)
            results = None

        return results

    def requete_row_count(self, text_sql, dict_param=dict()):
        """Réalisation d'une reauete sur la bdd

        Parameters
        ----------
        text_sql : string
            commande à executer

        dict_param : dict
            dictionnaire des parametres de la requete

        Returns
        -------
        result : List
            renvoie le resultat de la requete
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(text_sql, dict_param)
                    results = cursor.rowcount

        except Exception as e:
            logging.info(e)
            results = None

        return results
