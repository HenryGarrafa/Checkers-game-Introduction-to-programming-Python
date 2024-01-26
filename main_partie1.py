from partie import Partie
from position import Position
from damier import Damier
from piece import Piece

if __name__ == "__main__":
    # Point d'entrée du programme. On initialise une nouvelle partie, et on appelle la méthode jouer().
    partie = Partie()

    gagnant = partie.jouer()

    print("------------------------------------------------------")
    print("Partie terminée! Le joueur gagnant est le joueur", gagnant)