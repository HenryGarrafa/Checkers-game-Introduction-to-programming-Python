# Auteurs: À compléter

from piece import Piece
from position import Position


class Damier:
    """Plateau de jeu d'un jeu de dames. Contient un ensemble de pièces positionnées à une certaine position
    sur le plateau.

    Attributes:
        cases (dict): Dictionnaire dont une clé représente une Position, et une valeur correspond à la Piece
            positionnée à cet endroit sur le plateau. Notez bien qu'une case vide (sans pièce blanche ou noire)
            correspond à l'absence de clé la position de cette case dans le dictionnaire.

        n_lignes (int): Le nombre de lignes du plateau. La valeur est 8 (constante).
        n_colonnes (int): Le nombre de colonnes du plateau. La valeur est 8 (constante).

    """

    def __init__(self):
        """Constructeur du Damier. Initialise un damier initial de 8 lignes par 8 colonnes.

        """
        self.n_lignes = 8
        self.n_colonnes = 8

        self.cases = {
            Position(7, 0): Piece("blanc", "pion"),
            Position(7, 2): Piece("blanc", "pion"),
            Position(7, 4): Piece("blanc", "pion"),
            Position(7, 6): Piece("blanc", "pion"),
            Position(6, 1): Piece("blanc", "pion"),
            Position(6, 3): Piece("blanc", "pion"),
            Position(6, 5): Piece("blanc", "pion"),
            Position(6, 7): Piece("blanc", "pion"),
            Position(5, 0): Piece("blanc", "pion"),
            Position(5, 2): Piece("blanc", "pion"),
            Position(5, 4): Piece("blanc", "pion"),
            Position(5, 6): Piece("blanc", "pion"),
            Position(2, 1): Piece("noir", "pion"),
            Position(2, 3): Piece("noir", "pion"),
            Position(2, 5): Piece("noir", "pion"),
            Position(2, 7): Piece("noir", "pion"),
            Position(1, 0): Piece("noir", "pion"),
            Position(1, 2): Piece("noir", "pion"),
            Position(1, 4): Piece("noir", "pion"),
            Position(1, 6): Piece("noir", "pion"),
            Position(0, 1): Piece("noir", "pion"),
            Position(0, 3): Piece("noir", "pion"),
            Position(0, 5): Piece("noir", "pion"),
            Position(0, 7): Piece("noir", "pion"),
        }

    def recuperer_piece_a_position(self, position):
        """Récupère une pièce dans le damier à partir d'une position.

        Args:
            position (Position): La position où récupérer la pièce.

        Returns:
            La pièce (de type Piece) à la position reçue en argument, ou None si aucune pièce n'était à cette position.

        """
        if position not in self.cases:
            return None

        return self.cases[position]

    def position_est_dans_damier(self, position):
        """Vérifie si les coordonnées d'une position sont dans les bornes du damier (entre 0 inclusivement et le nombre
        de lignes/colonnes, exclusement.

        Args:
            position (Position): La position à valider.

        Returns:
            bool: True si la position est dans les bornes, False autrement.

        """

        return 0 <= position.ligne < self.n_lignes and 0 <= position.colonne < self.n_colonnes


    def piece_peut_se_deplacer_vers(self, position_piece, position_cible):
        """Cette méthode détermine si une pièce (à la position reçue) peut se déplacer à une certaine position cible.
        On parle ici d'un déplacement standard (et non une prise).

        Une pièce doit être positionnée à la position_piece reçue en argument (retourner False autrement).

        Une pièce de type pion ne peut qu'avancer en diagonale (vers le haut pour une pièce blanche, vers le bas pour
        une pièce noire). Une pièce de type dame peut avancer sur n'importe quelle diagonale, peu importe sa couleur.
        Une pièce ne peut pas se déplacer sur une case déjà occupée par une autre pièce. Une pièce ne peut pas se
        déplacer à l'extérieur du damier.

        Args:
            position_piece (Position): La position de la pièce source du déplacement.
            position_cible (Position): La position cible du déplacement.

        Returns:
            bool: True si la pièce peut se déplacer à la position cible, False autrement.

        """

        if not self.position_est_dans_damier(position_piece):
            return False

        if not self.position_est_dans_damier(position_cible):
            return False

        piece_piece = self.recuperer_piece_a_position(position_piece)
        if piece_piece is None:
            return False

        piece_cible = self.recuperer_piece_a_position(position_cible)

        if piece_cible is not None:
            return False

        for i in position_piece.quatre_positions_diagonales():

            if i == position_cible:

                if position_cible.ligne > position_piece.ligne and piece_piece.est_noire() and piece_piece.est_pion():
                    return True
                if position_cible.ligne < position_piece.ligne and piece_piece.est_blanche() and piece_piece.est_pion():
                    return True
                if piece_piece.est_dame():
                    return True

    def piece_peut_sauter_vers(self, position_piece, position_cible):
        """Cette méthode détermine si une pièce (à la position reçue) peut sauter vers une certaine position cible.
        On parle ici d'un déplacement qui "mange" une pièce adverse.

        Une pièce doit être positionnée à la position_piece reçue en argument (retourner False autrement).

        Une pièce ne peut que sauter de deux cases en diagonale. N'importe quel type de pièce (pion ou dame) peut sauter
        vers l'avant ou vers l'arrière. Une pièce ne peut pas sauter vers une case qui est déjà occupée par une autre
        pièce. Une pièce ne peut faire un saut que si elle saute par dessus une pièce de couleur adverse.

        Args:
            position_piece (Position): La position de la pièce source du saut.
            position_cible (Position): La position cible du saut.

        Returns:
            bool: True si la pièce peut sauter vers la position cible, False autrement.

        """

        if not self.position_est_dans_damier(position_piece):
            return False

        if not self.position_est_dans_damier(position_cible):
            return False

        piece_piece = self.recuperer_piece_a_position(position_piece)
        if piece_piece is None:
            return False

        piece_cible = self.recuperer_piece_a_position(position_cible)

        if piece_cible is None:
            position_media = Position((position_piece.ligne + position_cible.ligne) / 2, (position_piece.colonne + position_cible.colonne) / 2)
            piece_media = self.recuperer_piece_a_position(position_media)

            if piece_media is not None:
                if piece_piece.couleur != piece_media.couleur:
                    return True

    def piece_peut_se_deplacer(self, position_piece):
        """Vérifie si une pièce à une certaine position a la possibilité de se déplacer (sans faire de saut).

        ATTENTION: N'oubliez pas qu'étant donné une position, il existe une méthode dans la classe Position retournant
        les positions des quatre déplacements possibles.

        Args:
            position_piece (Position): La position source.

        Returns:
            bool: True si une pièce est à la position reçue et celle-ci peut se déplacer, False autrement.

        """
        if not self.position_est_dans_damier(position_piece):
            return False

        piece_piece = self.recuperer_piece_a_position(position_piece)
        if piece_piece is None:
            return False

        for i in position_piece.quatre_positions_diagonales():
            if not self.position_est_dans_damier(i):
                return False
            piece_cible = self.recuperer_piece_a_position(i)

            if piece_cible is None:
                return True

    def piece_peut_faire_une_prise(self, position_piece):
        """Vérifie si une pièce à une certaine position a la possibilité de faire une prise.

        Warning:
            N'oubliez pas qu'étant donné une position, il existe une méthode dans la classe Position retournant
            les positions des quatre sauts possibles.

        Args:
            position_piece (Position): La position source.

        Returns:
            bool: True si une pièce est à la position reçue et celle-ci peut faire une prise. False autrement.

        """

        if not self.position_est_dans_damier(position_piece):
            return False

        piece_piece = self.recuperer_piece_a_position(position_piece)
        if piece_piece is None:
            return False

        for i in position_piece.quatre_positions_sauts():
            # print(i)
            if self.piece_peut_sauter_vers(position_piece, i) == True:
                # print(i)
                if piece_piece.est_noire() and piece_piece.est_pion():
                    # print(i)
                    if position_piece.ligne < i.ligne:
                        return True

                if piece_piece.est_pion() and piece_piece.est_blanche():
                    if position_piece.ligne > i.ligne:
                        return True

                if piece_piece.est_dame():
                    print(i)
                    return print(True)

    def piece_de_couleur_peut_se_deplacer(self, couleur):
        """Vérifie si n'importe quelle pièce d'une certaine couleur reçue en argument a la possibilité de se déplacer
        vers une case adjacente (sans saut).

        ATTENTION: Réutilisez les méthodes déjà programmées!

        Args:
            couleur (str): La couleur à vérifier.

        Returns:
            bool: True si une pièce de la couleur reçue peut faire un déplacement standard, False autrement.
        """

        lista = []

        for position, piece in self.cases.items():
            if piece.couleur == couleur:
                lista.append(position)
        for i in lista:
            if self.piece_peut_se_deplacer(i) == True:
                return True

    def piece_de_couleur_peut_faire_une_prise(self, couleur):
        """Vérifie si n'importe quelle pièce d'une certaine couleur reçue en argument a la possibilité de faire un
        saut, c'est à dire vérifie s'il existe une pièce d'une certaine couleur qui a la possibilité de prendre une
        pièce adverse.

        ATTENTION: Réutilisez les méthodes déjà programmées!

        Args:
            couleur (str): La couleur à vérifier.

        Returns:
            bool: True si une pièce de la couleur reçue peut faire un saut (une prise), False autrement.
        """
        lista = []

        for position, piece in self.cases.items():
            #print(piece)
            if piece.couleur == couleur:
                #print(piece)
                lista.append(position)
        for i in lista:
            #print(i)
            if self.piece_peut_faire_une_prise(i) == True:
                print(i)
                return True
        return False

    def actualiser_sans_prise(self, position_source, position_cible):
        """Fait l'actualisation du diccionaire cases sans prise

        Args:
            position_source (Position): La position à remplaser et à enlever du dictionnaire.
            position_cible (Position): La position remplasantte dans le dictionnaire.
        Returns:
            Aucune

        """
        piece_suorce = self.recuperer_piece_a_position(position_source)
        self.cases[position_cible] = piece_suorce
        self.cases.pop(position_source)

    def actualiser_avec_prise(self, position_source, position_cible):
        """Fait l'actualisation du diccionaire cases avec prise (enlever la position du contraire)


        Args:
            position_source (Position): La position à remplaser et à enlever du dictionnaire.
            position_cible (Position): La position remplasantte dans le dictionnaire.
        Returns:
            Aucune

        """
        self.actualiser_sans_prise(position_source, position_cible)
        position_media = Position((position_source.ligne + position_cible.ligne) / 2,
                                  (position_source.colonne + position_cible.colonne) / 2)
        self.cases.pop(position_media)

    def actualiser_piece_pion(self, position_cible):
        """Fait l'actualisation du type de piece après une promotion


        Args:
            position_cible (Position): La position à faire l'actualisation

        Returns:
            Aucune

        """

        piece_cible = self.recuperer_piece_a_position(position_cible)

        if piece_cible.est_pion() and piece_cible.est_noire():
            if position_cible.ligne == 7:
                piece_cible.promouvoir()
        if piece_cible.est_pion() and piece_cible.est_blanche():
            if position_cible.ligne == 0:
                piece_cible.promouvoir()

    def deplacer(self, position_source, position_cible):
        """Effectue le déplacement sur le damier. Si le déplacement est valide, on doit mettre à jour le dictionnaire
        self.cases, en déplaçant la pièce à sa nouvelle position (et possiblement en supprimant une pièce adverse qui a
        été prise).

        Cette méthode doit également:
        - Promouvoir un pion en dame si celui-ci atteint l'autre extrémité du plateau.
        - Retourner un message indiquant "ok", "prise" ou "erreur".

        ATTENTION: Si le déplacement est effectué, cette méthode doit retourner "ok" si aucune prise n'a été faite,
            et "prise" si une pièce a été prise.
        ATTENTION: Ne dupliquez pas de code! Vous avez déjà programmé (ou allez programmer) des méthodes permettant
            de valider si une pièce peut se déplacer vers un certain endroit ou non.

        Args:
            position_source (Position): La position source du déplacement.
            position_cible (Position): La position cible du déplacement.

        Returns:
            str: "ok" si le déplacement a été effectué sans prise, "prise" si une pièce adverse a été prise, et
                "erreur" autrement.

        """
        if self.piece_peut_se_deplacer_vers(position_source, position_cible):
            self.actualiser_sans_prise(position_source,position_cible)
            self.actualiser_piece_pion(position_cible)

            return "ok"
        else:
            if self.piece_peut_faire_une_prise(position_source):
                self.actualiser_avec_prise(position_source,position_cible)
                self.actualiser_piece_pion(position_cible)
                return "prise"
            else:
                return "erreur"

    def __repr__(self):
        """Cette méthode spéciale permet de modifier le comportement d'une instance de la classe Damier pour
        l'affichage. Faire un print(un_damier) affichera le damier à l'écran.

        """
        s = " +-0-+-1-+-2-+-3-+-4-+-5-+-6-+-7-+\n"
        for i in range(0, 8):
            s += str(i)+"| "
            for j in range(0, 8):
                if Position(i, j) in self.cases:
                    s += str(self.cases[Position(i, j)])+" | "
                else:
                    s += "  | "
            s += "\n +---+---+---+---+---+---+---+---+\n"

        return s


if __name__ == "__main__":
    print('Test unitaires de la classe "Damier"...')
    print()

    d1 = Damier()
    p1 = Position(5, 0)
    p2 = Position(4, 1)
    assert d1.piece_peut_se_deplacer_vers(p1, p2)
    assert not d1.piece_peut_se_deplacer_vers(p2, p1)
    print('piece_peut_se_deplacer_vers = ok')

    p1 = Position(2, 3)
    p2 = Position(4, 5)
    p3 = Position(8, 1)
    d1 = Damier()
    assert not d1.piece_peut_sauter_vers(p1, p2)
    assert not d1.piece_peut_sauter_vers(p1, p3)
    print('piece_peut_sauter_vers = ok')

    p1 = Position(5, 6)
    p2 = Position(6, 5)
    d1 = Damier()
    assert d1.piece_peut_se_deplacer(p1)
    assert not d1.piece_peut_se_deplacer(p2)
    print('piece_peut_se_deplacer = ok')

    p1 = Position(5, 4)
    p2 = Position(2, 5)
    d1 = Damier()
    assert not d1.piece_peut_faire_une_prise(p1)
    assert not d1.piece_peut_faire_une_prise(p2)
    print('piece_peut_faire_une_prise = ok')

    d1 = Damier()
    d1.piece_de_couleur_peut_se_deplacer("noir")
    d1.piece_de_couleur_peut_se_deplacer("blanc")
    assert d1.piece_de_couleur_peut_se_deplacer("noir")
    assert d1.piece_de_couleur_peut_se_deplacer("blanc")
    print('piece_de_couleur_peut_se_deplacer = ok')

    d1 = Damier()
    assert not d1.piece_de_couleur_peut_faire_une_prise("noir")
    assert not d1.piece_de_couleur_peut_faire_une_prise("blanc")
    print('piece_de_couleur_peut_faire_une_prise = ok')

    d1 = Damier()
    p1 = Position(5, 2)
    p2 = Position(4, 3)
    p3 = Position(4, 1)
    assert d1.deplacer(p1, p2)
    assert d1.deplacer(p1, p3)
    print('deplacer = ok')

    print()
    print('Test unitaires passés avec succès!')

    un_damier = Damier()
    # NOTEZ BIEN: Pour vous aider lors du développement, affichez le damier!
    print(un_damier)