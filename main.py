import pygame
import sys
from menu import show_menu
from game import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))  
    pygame.display.set_caption("Alien Escape")

    show_menu(screen)

    game = Game(screen, start_level=6)  # Iniciar en el nivel 5
    game.run()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()