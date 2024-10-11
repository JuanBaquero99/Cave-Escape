import pygame
import sys
from menu import show_menu
from game import Game
from hud import HUD
from background import Background  

def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))  
    pygame.display.set_caption("Cave Escape")

    show_menu(screen)

    hud = HUD()
    background = Background()  
    show_instructions(screen, hud, background)

    game = Game(screen, start_level=1)  
    game.run()

    pygame.quit()
    sys.exit()

def show_instructions(screen, hud, background):
    """
    Muestra la pantalla de instrucciones del juego.

    Args:
        screen (pygame.Surface): La superficie de la pantalla donde se dibujarán los elementos.
        hud (HUD): El objeto HUD que contiene los métodos para dibujar la pantalla de instrucciones.
        background (Background): El objeto Background que contiene el método para dibujar el fondo.

    El bucle se ejecuta hasta que el usuario cierra la ventana o presiona la tecla Enter.
    """
    running = True
    while running:
        background.draw(screen)  
        hud.draw_instructions_screen(screen)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    running = False

if __name__ == "__main__":
    main()