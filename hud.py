import pygame

class HUD:
    def __init__(self):
        self.lives = 3
        self.score = 0
        self.font = pygame.font.Font(None, 36)
        self.game_over_sound = pygame.mixer.Sound("assets/images/soundtrack/mixkit-arcade-retro-game-over-213.wav")
        self.victory_sound = pygame.mixer.Sound("assets/images/soundtrack/level-win-6416.mp3")

    def draw(self, screen, level):
        self.draw_level(screen, level)
        self.draw_lives(screen)
        self.draw_score(screen)

    def draw_level(self, screen, level):
        level_text = self.font.render(f"Nivel: {level}", True, (255, 255, 255))
        screen.blit(level_text, (10, 10))

    def draw_lives(self, screen):
        lives_text = self.font.render(f"Vidas: {self.lives}", True, (255, 255, 255))
        screen.blit(lives_text, (10, 50))

    def draw_score(self, screen):
        score_text = self.font.render(f"Puntaje: {self.score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 90))

    def draw_game_over_screen(self, screen):
        self.game_over_sound.play()
        font = pygame.font.Font(None, 74)
        text = font.render("Game Over", True, (255, 0, 0))
        text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 50))
        screen.blit(text, text_rect)

        font = pygame.font.Font(None, 36)
        retry_text = font.render("Presiona ENTER para intentar de nuevo", True, (255, 255, 255))
        quit_text = font.render("Presiona ESC para salir", True, (255, 255, 255))
        retry_rect = retry_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 50))
        quit_rect = quit_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 100))
        screen.blit(retry_text, retry_rect)
        screen.blit(quit_text, quit_rect)

    def draw_victory_screen(self, screen):
        pygame.mixer.music.stop()  # Detener la música de fondo
        self.victory_sound.play()
        font = pygame.font.Font(None, 74)
        text = font.render("¡Victoria!", True, (0, 255, 0))
        text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 50))
        screen.blit(text, text_rect)

        font = pygame.font.Font(None, 36)
        retry_text = font.render("Presiona ENTER para jugar de nuevo", True, (255, 255, 255))
        quit_text = font.render("Presiona ESC para salir", True, (255, 255, 255))
        retry_rect = retry_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 50))
        quit_rect = quit_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 100))
        screen.blit(retry_text, retry_rect)
        screen.blit(quit_text, quit_rect)