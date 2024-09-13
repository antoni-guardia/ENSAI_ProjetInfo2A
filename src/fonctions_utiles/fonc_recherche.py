import fiona
import matplotlib.pyplot as plt


# Path fichier test
path = ("data/ADMIN-EXPRESS_3-2__SHP_WGS84G_FRA_2024-08-26/ADMIN-EXPRESS/1_DONNEES_LIVRAISON_2024-08-00122/ADE_3-2_SHP_WGS84G_FRA-ED2024-08-26/COLLECTIVITE_TERRITORIALE.shp")


def point_dans_poly(polygone, point):
    """
    Determine si un point est dans un polygone en utilisant
    l'algorithme du lancer de rayons.

    Parameters
    ----------
    point : tuple
        Le point que l'on souhaite tester.

    polygon : list[tuple]
        Liste de tuples représentant les sommets du polygone.

    Returns
    -------
    bool
        Vrai si le point est dedans, faux sinon.
    """
    # prend les valeurs du point
    x, y = point
    # calcule le nombre de points du polygone
    n = len(polygone)
    # initialisation du flag inside
    dedans = False

    for i in range(n):
        # On prend les coord du premier point et celui qui le suit
        # Rq, j = i + 1 [mod n]
        xi, yi = polygone[i]
        xj, yj = polygone[(i + 1) % n]

        # On regarde si y est entre yi et yj
        if (yi > y) != (yj > y):
            # On verifie qu'il n'y a pas de divisio par 0

            intersection = (xj - xi) * (y - yi) / (yj - yi) + xi
            if x < intersection:
                # Inegalité des pentes des droites (P,Pi) vs (Pj, Pi)
                # Sachant que Pi -> Pj, si Pi_y > Pj_y, comme on sait que
                # le polygone se trouve à droite de la droite comprise
                # entre les y_i et Y_j (déjà testé)
                # Il suffit donc que la pente (P,Pi) > (Pj, Pi)
                dedans = not dedans
                # Comme modulo 2, il suffit de changer la valeur de dedans

    return dedans


def dessiner_poly(polygone, c="blue", style_ligne="-"):
    """
    Dessine sur matplotlib la figure du polygone

    Parameters
    ----------

    polygon : list[tuple]
        Liste de tuples représentant les sommets du polygone.


    """
    x, y = zip(*polygone)
    plt.plot(x, y, linestyle=style_ligne, color=c)


with fiona.open(path, 'r') as shp:

    p = (6.604E5, 1.81E6)
    n_p = 0
    feature = shp[0]
    # poly = feature['geometry']['coordinates'][n_p][0]
    print(feature)
    # print(point_dans_poly(poly, p))
    # dessiner_poly(poly)

    # Plot les points
    # plt.scatter(p[0], p[1], c="red")
    # plt.show()
