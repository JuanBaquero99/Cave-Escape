import pygame
import sys
from background import Background

def show_menu(screen):
    background = Background()
    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 36)
    
    title_text = font.render("Alien Escape", True, (255, 255, 255))
    start_text = small_font.render("Presiona ENTER para jugar", True, (255, 255, 255))
    quit_text = small_font.render("Presiona ESC para salir", True, (255, 255, 255))
    
    title_rect = title_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 100))
    start_rect = start_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    quit_rect = quit_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 50))
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        
        background.update(1)  # Actualizar el fondo en movimiento
        background.draw(screen)  # Dibujar el fondo en la pantalla
        
        screen.blit(title_text, title_rect)
        screen.blit(start_text, start_rect)
        screen.blit(quit_text, quit_rect)
        
        pygame.display.flip()