import pygame
import random
from player import Player
from background import Background
from hud import HUD
from enemy import Enemy, FinalBoss, PowerBall
from game_plataform import Platform
from coins import Coin

class Game:
    def __init__(self, screen, start_level=1):  # Añadir parámetro start_level
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_over = False
        self.victory = False
        self.player = Player()
        self.background = Background()
        self.hud = HUD()
        self.level = start_level  # Usar start_level como nivel inicial
        self.max_levels = 6  # Cambiar el número máximo de niveles a 6
        self.enemies = []
        self.platforms = []
        self.coins = []
        self.final_boss = None  # Añadir un atributo para el jefe final

        # Lista de imágenes de tiles para las plataformas
        self.tile_images = [
            "assets/images/plataform/1.png",
            "assets/images/plataform/2.png",
            "assets/images/plataform/3.png"
        ]

        # Cargar sonidos
        pygame.mixer.init()
        self.coin_sound = pygame.mixer.Sound("assets/images/soundtrack/coins-sound-effect-1-241818.mp3")
        self.jump_sound = pygame.mixer.Sound("assets/images/soundtrack/jump-up-245782.mp3")
        self.death_sound = pygame.mixer.Sound("assets/images/soundtrack/monster-death-grunt-131480.mp3")
        self.background_music = "assets/images/soundtrack/Juhani Junkala [Retro Game Music Pack] Title Screen.wav"

        # Reproducir música de fondo en bucle
        pygame.mixer.music.load(self.background_music)
        pygame.mixer.music.play(-1)

        self.setup_level(self.level)

    def setup_level(self, level):
        self.platforms = []
        self.enemies = []
        self.coins = []
        self.final_boss = None  # Reiniciar el jefe final

        # Seleccionar un patrón de plataformas basado en el nivel
        if level % 3 == 1:
            self.generate_pattern_1()
        elif level % 3 == 2:
            self.generate_pattern_2()
        else:
            self.generate_pattern_3()

        if level == 6:
            self.final_boss = FinalBoss(speed=4)  # Aumentar la velocidad del jefe final
        else:
            for _ in range(level):
                self.enemies.append(Enemy(speed=level))

        for platform in self.platforms:
            x = platform.rect.x + platform.rect.width // 2 - 15
            y = platform.rect.y - 30
            self.coins.append(Coin(x, y))

        self.reset_player()

    def generate_pattern_1(self):
        # Generar plataformas de manera escalonada
        platform_width = 200
        platform_height = 40
        num_platforms = 5
        x_gap = (1280 - platform_width) // (num_platforms - 1)
        y_positions = [600, 500, 400, 300, 200]

        for i in range(num_platforms):
            x = i * x_gap
            y = y_positions[i % len(y_positions)]
            self.platforms.append(Platform(x, y, platform_width, platform_height, self.tile_images))

    def generate_pattern_2(self):
        # Generar plataformas en zigzag
        platform_width = 200
        platform_height = 40
        num_platforms = 5
        x_gap = (1280 - platform_width) // (num_platforms - 1)
        y_positions = [600, 400, 500, 300, 200]

        for i in range(num_platforms):
            x = i * x_gap
            y = y_positions[i % len(y_positions)]
            self.platforms.append(Platform(x, y, platform_width, platform_height, self.tile_images))

    def generate_pattern_3(self):
        # Generar plataformas en forma de escalera
        platform_width = 200
        platform_height = 40
        num_platforms = 5
        x_gap = (1280 - platform_width) // (num_platforms - 1)
        y_start = 600
        y_step = -100

        for i in range(num_platforms):
            x = i * x_gap
            y = y_start + i * y_step
            self.platforms.append(Platform(x, y, platform_width, platform_height, self.tile_images))

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.game_over and not self.victory:
                    self.player.jump()
                    self.jump_sound.play()  # Reproducir sonido de salto
                if event.key == pygame.K_RETURN and (self.game_over or self.victory):
                    self.reset_game()
                if event.key == pygame.K_ESCAPE and (self.game_over or self.victory):
                    self.running = False

            if self.final_boss:
                self.final_boss.handle_event(event)

    def update(self):
        if self.game_over or self.victory:
            return

        keys = pygame.key.get_pressed()
        self.player.update(keys)
        if keys[pygame.K_LEFT]:
            self.background.update(5)
        elif keys[pygame.K_RIGHT]:
            self.background.update(-5)

        self.player.speed_y += self.player.gravity
        self.player.rect.y += self.player.speed_y

        if self.player.rect.left < 0:
            self.player.rect.left = 0
        if self.player.rect.right > 1280:
            self.player.rect.right = 1280

        self.player.on_ground = False
        for platform in self.platforms:
            if self.player.rect.colliderect(platform.rect) and self.player.speed_y > 0:
                self.player.rect.bottom = platform.rect.top
                self.player.speed_y = 0
                self.player.on_ground = True
                self.player.jump_count = 0

        self.check_collisions_with_enemies()
        self.check_if_player_fell()
        self.check_collisions_with_coins()
        self.check_if_level_completed()

        if not self.player.on_ground:
            self.player.update_jump_animation()

    def check_collisions_with_enemies(self):
        for enemy in self.enemies:
            enemy.update()
            if self.player.rect.colliderect(enemy.rect):
                print("Colisión detectada!")
                self.hud.lives -= 1
                self.death_sound.play()  # Reproducir sonido de muerte
                if self.hud.lives <= 0:
                    self.game_over = True
                else:
                    self.reset_player()

        if self.final_boss:
            self.final_boss.update()
            if self.player.rect.colliderect(self.final_boss.rect):
                print("Colisión con el jefe final!")
                self.hud.lives -= 1
                self.death_sound.play()  # Reproducir sonido de muerte
                if self.hud.lives <= 0:
                    self.game_over = True
                else:
                    self.reset_player()
                    self.final_boss.increase_attack_delay()  # Aumentar el retraso entre ataques

            for ball in self.final_boss.power_balls:
                if self.player.rect.colliderect(ball.rect):
                    print("Colisión con bola de poder!")
                    self.hud.lives -= 1
                    self.death_sound.play()  # Reproducir sonido de muerte
                    self.final_boss.power_balls.remove(ball)
                    if self.hud.lives <= 0:
                        self.game_over = True
                    else:
                        self.reset_player()
                        self.final_boss.increase_attack_delay()  # Aumentar el retraso entre ataques

    def check_if_player_fell(self):
        if self.player.rect.top > 720:
            print("Has caído!")
            self.hud.lives -= 1
            self.death_sound.play()  # Reproducir sonido de muerte
            if self.hud.lives <= 0:
                self.game_over = True
            else:
                self.reset_player()
                if self.final_boss:
                    self.final_boss.increase_attack_delay()  # Aumentar el retraso entre ataques

    def check_collisions_with_coins(self):
        for coin in self.coins[:]:
            if self.player.rect.colliderect(coin.rect):
                self.coins.remove(coin)
                self.hud.score += 10
                self.coin_sound.play()  # Reproducir sonido de moneda

    def check_if_level_completed(self):
        if self.player.rect.right >= 1280:
            if self.level < self.max_levels:
                self.level += 1
                self.setup_level(self.level)
            else:
                print("¡Has completado todos los niveles!")
                self.victory = True

    def reset_player(self):
        first_platform = self.platforms[0]
        self.player.rect.x = first_platform.rect.x + first_platform.rect.width // 2 - self.player.rect.width // 2
        self.player.rect.y = first_platform.rect.y - self.player.rect.height
        self.player.speed_y = 0
        self.player.on_ground = False
        self.player.jump_count = 0

    def reset_game(self):
        self.level = 1
        self.hud.lives = 3
        self.hud.score = 0
        self.game_over = False
        self.victory = False
        self.setup_level(self.level)

    def draw(self):
        self.background.draw(self.screen)
        self.player.draw(self.screen)
        for platform in self.platforms:
            platform.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)
        for coin in self.coins:
            coin.draw(self.screen)
        if self.final_boss:
            self.final_boss.draw(self.screen)
        self.hud.draw(self.screen, self.level)
        if self.game_over:
            self.hud.draw_game_over_screen(self.screen)
        if self.victory:
            self.hud.draw_victory_screen(self.screen)
        pygame.display.flip()