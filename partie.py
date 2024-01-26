from piece import Piece
from position import Position
from damier import Damier

class Partie:
    """Gestionnaire de partie de dames.

    Attributes:
        damier (Damier): Le damier de la partie, contenant notamment les pièces.
        couleur_joueur_courant (str): Le joueur à qui c'est le tour de jouer.
        doit_prendre (bool): Un booléen représentant si le joueur actif doit absolument effectuer une prise
            de pièce. Sera utile pour valider les mouvements et pour gérer les prises multiples.
        position_source_selectionnee (Position): La position source qui a été sélectionnée. Utile pour sauvegarder
            cette information avant de poursuivre. Contient None si aucune pièce n'est sélectionnée.
        position_source_forcee (Position): Une position avec laquelle le joueur actif doit absolument jouer. Le
            seul moment où cette position est utilisée est après une prise: si le joueur peut encore prendre
            d'autres pièces adverses, il doit absolument le faire. Ce membre contient None si aucune position n'est
            forcée.

    """
    def __init__(self):
        """Constructeur de la classe Partie. Initialise les attributs à leur valeur par défaut. Le damier est construit
        avec les pièces à leur valeur initiales, le joueur actif est le joueur blanc, et celui-ci n'est pas forcé
        de prendre une pièce adverse. Aucune position source n'est sélectionnée, et aucune position source n'est forcée.

        """
        self.damier = Damier()
        self.couleur_joueur_courant = "blanc"
        self.doit_prendre = False
        self.position_source_selectionnee = None
        self.position_source_forcee = None

    def position_source_valide(self, position_source):
        """Vérifie la validité de la position source, notamment:
            - Est-ce que la position contient une pièce?
            - Est-ce que cette pièce est de la couleur du joueur actif?
            - Si le joueur doit absolument continuer son mouvement avec une prise supplémentaire, a-t-il choisi la
              bonne pièce?

        Cette méthode retourne deux valeurs. La première valeur est Booléenne (True ou False), et la seconde valeur est
        un message d'erreur indiquant la raison pourquoi la position n'est pas valide (ou une chaîne vide s'il n'y a pas
        d'erreur).

        ATTENTION: Utilisez les attributs de la classe pour connaître les informations sur le jeu! (le damier, le joueur
            actif, si une position source est forcée, etc.

        ATTENTION: Vous avez accès ici à un attribut de type Damier. vous avez accès à plusieurs méthodes pratiques
            dans le damier qui vous simplifieront la tâche ici :)

        Args:
            position_source (Position): La position source à valider.

        Returns:
            bool, str: Un couple où le premier élément représente la validité de la position (True ou False), et le
                 deuxième élément est un message d'erreur (ou une chaîne vide s'il n'y a pas d'erreur).

        """
        if not self.damier.recuperer_piece_a_position(position_source):
            return False, "Erreur, la position n'a pas des pieces"
        if not self.damier.cases[position_source].couleur==self.couleur_joueur_courant:
            return False, "Erreur, la piece n'est pas le couleur courant"
        if self.position_source_forcee:
            if not self.damier.cases[position_source].couleur == self.couleur_joueur_courant:
                return False, "Erreur, la piece n'est pas le couleur courant"

        self.position_source_selectionnee = position_source

        return True, ""

    def position_cible_valide(self, position_cible):
        """Vérifie si la position cible est valide (en fonction de la position source sélectionnée). Doit non seulement
        vérifier si le déplacement serait valide (utilisez les méthodes que vous avez programmées dans le Damier!), mais
        également si le joueur a respecté la contrainte de prise obligatoire.

        Returns:
            bool, str: Deux valeurs, la première étant Booléenne et indiquant si la position cible est valide, et la
                seconde valeur est une chaîne de caractères indiquant un message d'erreur (ou une chaîne vide s'il n'y
                a pas d'erreur).
        """
        if self.damier.piece_peut_sauter_vers(self.position_source_selectionnee, position_cible):
            return True, ""
        if self.damier.piece_peut_se_deplacer_vers(self.position_source_selectionnee, position_cible):
            return True, ""
        return False, "Erreur, position incorrect"

    def demander_positions_deplacement(self):
        """Demande à l'utilisateur les positions sources et cible, et valide ces positions. Cette méthode doit demander
        les positions à l'utilisateur tant que celles-ci sont invalides.

        Cette méthode ne doit jamais planter, peu importe ce que l'utilisateur entre.

        Returns:
            Position, Position: Un couple de deux positions (source et cible).

        """
        while True:
            try:
                # Demander à l'utilisateur la position source
                source_str = input("Entrez la position source (ligne,colonne) : ")
                position_source = Position(*map(int, source_str.split(',')))

                # Vérifier la validité de la position source

                valide, erreur_source = self.position_source_valide(position_source)
                if not valide:
                    print(f"Position source invalide : {erreur_source}")
                    continue
                else:
                    break
            except Exception as e:
                print(f"Erreur : {e}")
                continue

        while True:
            try:
                # Demander à l'utilisateur la position cible
                cible_str = input("Entrez la position cible (ligne,colonne) : ")
                position_cible = Position(*map(int, cible_str.split(',')))

                # Vérifier la validité de la position cible

                valide, erreur_cible = self.position_cible_valide(position_cible)
                if not valide:
                    print(f"Position cible invalide : {erreur_cible}")
                    continue

                # Si les positions sont valides, retourner le couple de positions
                return position_source, position_cible

            except Exception as e:
                print(f"Erreur : {e}")
                continue
    def tour(self):
        """Cette méthode effectue le tour d'un joueur, et doit effectuer les actions suivantes:
        - Assigne self.doit_prendre à True si le joueur courant a la possibilité de prendre une pièce adverse.
        - Affiche l'état du jeu
        - Demander les positions source et cible (utilisez self.demander_positions_deplacement!)
        - Effectuer le déplacement (à l'aide de la méthode du damier appropriée)
        - Si une pièce a été prise lors du déplacement, c'est encore au tour du même joueur si celui-ci peut encore
          prendre une pièce adverse en continuant son mouvement. Utilisez les membres self.doit_prendre et
          self.position_source_forcee pour forcer ce prochain tour!
        - Si aucune pièce n'a été prise ou qu'aucun coup supplémentaire peut être fait avec la même pièce, c'est le
          tour du joueur adverse. Mettez à jour les attributs de la classe en conséquence.

        """

        # Détermine si le joueur courant a la possibilité de prendre une pièce adverse.
        if self.damier.piece_de_couleur_peut_faire_une_prise(self.couleur_joueur_courant):
            self.doit_prendre = True

        # Affiche l'état du jeu
        print(self.damier)
        print("")
        print("Tour du joueur", self.couleur_joueur_courant, end=".")
        if self.doit_prendre:
            if self.position_source_forcee is None:
                print(" Doit prendre une pièce.")
            else:
                print(" Doit prendre avec la pièce en position {}.".format(self.position_source_forcee))
        else:
            print("")
        # Détermine si le joueur courant a la possibilité de prendre une pièce adverse.
        if self.damier.piece_de_couleur_peut_faire_une_prise(self.couleur_joueur_courant):
            self.doit_prendre = True

        # Demander les positions
        position_source, position_cible = self.demander_positions_deplacement()

        resultat_deplacement = self.damier.deplacer(position_source, position_cible)

        # Mettre à jour les attributs de la classe
        if resultat_deplacement == "erreur":
            print("Déplacement invalide. Veuillez réessayer.")

            # Effectuer le déplacement (à l'aide de la méthode du damier appropriée)
        if resultat_deplacement == "prise" and self.damier.piece_de_couleur_peut_faire_une_prise(
                self.couleur_joueur_courant):
            # Si une pièce a été prise et le joueur peut encore prendre, forcer le prochain tour
            self.position_source_forcee = position_cible
            print("Vous pouvez prendre une autre pièce avec la même pièce.")

        else:
            # Si aucune pièce n'a été prise ou qu'aucun coup supplémentaire peut être fait avec la même pièce,
            # c'est le tour du joueur adverse
            self.doit_prendre = False
            self.position_source_forcee = None
            self.couleur_joueur_courant = "blanc" if self.couleur_joueur_courant == "noir" else "noir"
            print("Tour terminé.")


    def jouer(self):
        """Démarre une partie. Tant que le joueur courant a des déplacements possibles (utilisez les méthodes
        appriopriées!), un nouveau tour est joué.

        Returns:
            str: La couleur du joueur gagnant.
        """

        while self.damier.piece_de_couleur_peut_se_deplacer(self.couleur_joueur_courant) or \
                self.damier.piece_de_couleur_peut_faire_une_prise(self.couleur_joueur_courant):
            self.tour()

        if self.couleur_joueur_courant == "blanc":
            return "noir"
        else:
            return "blanc"


if __name__ == '__main__':
    p1 = Partie()

    p1.jouer()




