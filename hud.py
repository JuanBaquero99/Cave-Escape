import pygame

class HUD:
    """
    Clase HUD (Heads-Up Display) para gestionar y mostrar la interfaz gráfica del usuario en el juego.
    Métodos:
    --------
    __init__():
        Inicializa los atributos del HUD, incluyendo las fuentes, vidas y puntuación.
    update():
        Método de actualización (actualmente vacío).
    draw(screen, level):
        Dibuja el HUD en la pantalla, mostrando las vidas, puntuación y nivel actual.
    draw_boss_health(screen, boss_health):
        Dibuja la salud del jefe en la pantalla.
    draw_game_over_screen(screen):
        Dibuja la pantalla de "Game Over" con opciones para reiniciar o salir del juego.
    draw_victory_screen(screen):
        Dibuja la pantalla de victoria con opciones para reiniciar o salir del juego.
    draw_instructions_screen(screen):
        Dibuja la pantalla de instrucciones con las teclas y acciones del juego.
    """
    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        self.large_font = pygame.font.Font(None, 72)
        self.lives = 6
        self.score = 0

    def update(self):
        pass

    def draw(self, screen, level):
        lives_text = self.font.render(f"Lives: {self.lives}", True, (255, 255, 255))
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        level_text = self.font.render(f"Level: {level}", True, (255, 255, 255))
        screen.blit(lives_text, (10, 10))
        screen.blit(score_text, (10, 50))
        screen.blit(level_text, (10, 90))

    def draw_boss_health(self, screen, boss_health):
        health_text = self.font.render(f"Boss Health: {boss_health}", True, (255, 0, 0))
        screen.blit(health_text, (10, 130))

    def draw_game_over_screen(self, screen):
        game_over_text = self.large_font.render("Game Over", True, (255, 0, 0))
        restart_text = self.font.render("Press Enter to Restart", True, (255, 255, 255))
        exit_text = self.font.render("Press Esc to Exit", True, (255, 255, 255))
        screen.blit(game_over_text, (640 - game_over_text.get_width() // 2, 300 - game_over_text.get_height() // 2))
        screen.blit(restart_text, (640 - restart_text.get_width() // 2, 360 - restart_text.get_height() // 2))
        screen.blit(exit_text, (640 - exit_text.get_width() // 2, 420 - exit_text.get_height() // 2))

    def draw_victory_screen(self, screen):
        victory_text = self.large_font.render("Victory!", True, (0, 255, 0))
        restart_text = self.font.render("Press Enter to Restart", True, (255, 255, 255))
        exit_text = self.font.render("Press Esc to Exit", True, (255, 255, 255))
        screen.blit(victory_text, (640 - victory_text.get_width() // 2, 300 - victory_text.get_height() // 2))
        screen.blit(restart_text, (640 - restart_text.get_width() // 2, 360 - restart_text.get_height() // 2))
        screen.blit(exit_text, (640 - exit_text.get_width() // 2, 420 - exit_text.get_height() // 2))

    def draw_instructions_screen(self, screen):
        instructions = [
            "Instrucciones:",
            "Presiona X para atacar",
            "Deja oprimido X para atacar continuamente",
            "Presiona SPACE para saltar",
            "Presiona SPACE dos veces para doble salto",
            "Usa las flechas del teclado para moverte",
            "Presiona ENTER para iniciar el juego",
        ]
        y_offset = 200
        for line in instructions:
            instruction_text = self.font.render(line, True, (0, 255, 255))
            screen.blit(instruction_text, (640 - instruction_text.get_width() // 2, y_offset))
            y_offset += 50
