from player import Player
from background import Background
from hud import HUD
from enemy import Enemy, FinalBoss
from game_plataform import Platform
from coins import Coin
import random
import pygame

class Game:
    """
    Clase Game que representa el juego principal.
    Atributos:
    -----------
    screen : pygame.Surface
        La superficie de la pantalla donde se dibuja el juego.
    clock : pygame.time.Clock
        El reloj del juego para controlar la velocidad de fotogramas.
    running : bool
        Indica si el juego está en ejecución.
    game_over : bool
        Indica si el juego ha terminado.
    victory : bool
        Indica si el jugador ha ganado.
    player : Player
        El jugador del juego.
    background : Background
        El fondo del juego.
    hud : HUD
        La interfaz de usuario del juego.
    level : int
        El nivel actual del juego.
    max_levels : int
        El número máximo de niveles en el juego.
    enemies : list
        Lista de enemigos en el nivel actual.
    platforms : list
        Lista de plataformas en el nivel.
    coins : list
        Lista de monedas en el nivel.
    final_boss : FinalBoss or None
        El jefe final del juego, si existe.
    arrow_animation_offset : int
        Desplazamiento de la animación de la flecha.
    arrow_animation_direction : int
        Dirección de la animación de la flecha.
    tile_images : list
        Lista de rutas de imágenes de las plataformas.
    coin_sound : pygame.mixer.Sound
        Sonido de recogida de monedas.
    jump_sound : pygame.mixer.Sound
        Sonido de salto.
    death_sound : pygame.mixer.Sound
        Sonido de muerte.
    background_music : str
        Ruta de la música de fondo.
    victory_music : str
        Ruta de la música de victoria.
    game_over_music : str
        Ruta de la música de game over.
    Métodos:
    --------
    __init__(self, screen, start_level=1):
        Inicializa el juego con la pantalla y el nivel de inicio.
    setup_level(self, level):
        Configura el nivel especificado.
    generate_pattern_1(self):
        Genera el patrón 1 de plataformas.
    generate_pattern_2(self):
        Genera el patrón 2 de plataformas.
    generate_pattern_3(self):
        Genera el patrón 3 de plataformas.
    run(self):
        Ejecuta el bucle principal del juego.
    handle_events(self):
        Maneja los eventos del juego.
    update(self):
        Actualiza el estado del juego.
    check_collisions_with_enemies(self):
        Verifica colisiones con enemigos.
    check_collisions_with_power_balls(self):
        Verifica colisiones con bolas de poder.
    check_if_player_fell(self):
        Verifica si el jugador ha caído.
    check_collisions_with_coins(self):
        Verifica colisiones con monedas.
    check_if_level_completed(self):
        Verifica si el nivel ha sido completado.
    reset_player(self):
        Reinicia la posición del jugador.
    reset_game(self):
        Reinicia el juego.
    draw(self):
        Dibuja todos los elementos del juego en la pantalla.
    draw_next_level_arrow(self):
        Dibuja la flecha para avanzar al siguiente nivel.
    check_collisions(self):
        Verifica colisiones entre bolas de poder y enemigos o el jefe final.
    """
    def __init__(self, screen, start_level=1):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_over = False
        self.victory = False
        self.player = Player()
        self.background = Background()
        self.hud = HUD()
        self.level = start_level
        self.max_levels = 6
        self.enemies = []
        self.platforms = []
        self.coins = []
        self.final_boss = None
        self.arrow_animation_offset = 0
        self.arrow_animation_direction = 1

        self.tile_images = [
            "assets/images/plataform/1.png",
            "assets/images/plataform/2.png",
            "assets/images/plataform/3.png"
        ]

        pygame.mixer.init()
        self.coin_sound = pygame.mixer.Sound("assets/images/soundtrack/coins-sound-effect-1-241818.mp3")
        self.jump_sound = pygame.mixer.Sound("assets/images/soundtrack/jump-up-245782.mp3")
        self.death_sound = pygame.mixer.Sound("assets/images/soundtrack/monster-death-grunt-131480.mp3")
        self.background_music = "assets/images/soundtrack/Juhani Junkala [Retro Game Music Pack] Title Screen.wav"
        self.victory_music = "assets/images/soundtrack/level-win-6416.mp3"
        self.game_over_music = "assets/images/soundtrack/mixkit-arcade-retro-game-over-213.wav"

        pygame.mixer.music.load(self.background_music)
        pygame.mixer.music.play(-1)

        self.setup_level(self.level)

    def setup_level(self, level):
        self.platforms = []
        self.enemies = []
        self.coins = []
        self.final_boss = None

        if level % 3 == 1:
            self.generate_pattern_1()
        elif level % 3 == 2:
            self.generate_pattern_2()
        else:
            self.generate_pattern_3()

        if level == 6:
            self.final_boss = FinalBoss(1130, 570)
        else:
            for _ in range(level):
                speed = 2 + level
                x = random.randint(100, 1180)
                y = random.randint(100, 620)
                self.enemies.append(Enemy(x, y, speed))

        for platform in self.platforms:
            x = platform.rect.x + platform.rect.width // 2 - 15
            y = platform.rect.y - 30
            self.coins.append(Coin(x, y))

        self.reset_player()

    def generate_pattern_1(self):
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
                    self.jump_sound.play()
                if event.key == pygame.K_RETURN and (self.game_over or self.victory):
                    self.reset_game()
                if event.key == pygame.K_ESCAPE and (self.game_over or self.victory):
                    self.running = False

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

        self.arrow_animation_offset += self.arrow_animation_direction
        if self.arrow_animation_offset > 10 or self.arrow_animation_offset < -10:
            self.arrow_animation_direction *= -1

    def check_collisions_with_enemies(self):
        for enemy in self.enemies:
            enemy.update()
            if self.player.rect.colliderect(enemy.rect):
                print("Colisión detectada!")
                self.hud.lives -= 1
                self.death_sound.play()
                if self.hud.lives <= 0:
                    self.game_over = True
                    pygame.mixer.music.load(self.game_over_music)
                    pygame.mixer.music.play()
                else:
                    self.reset_player()

        if self.final_boss:
            self.final_boss.update()
            if self.player.rect.colliderect(self.final_boss.rect):
                print("Colisión con el jefe final!")
                self.hud.lives -= 1
                self.death_sound.play()
                if self.hud.lives <= 0:
                    self.game_over = True
                    pygame.mixer.music.load(self.game_over_music)
                    pygame.mixer.music.play()
                else:
                    self.reset_player()
                    self.final_boss.increase_attack_delay()

            for ball in self.final_boss.power_balls:
                if self.player.rect.colliderect(ball.rect):
                    print("Colisión con bola de poder!")
                    self.hud.lives -= 1
                    self.death_sound.play()
                    self.final_boss.power_balls.remove(ball)
                    if self.hud.lives <= 0:
                        self.game_over = True
                        pygame.mixer.music.load(self.game_over_music)
                        pygame.mixer.music.play()
                    else:
                        self.reset_player()
                        self.final_boss.increase_attack_delay()

        self.check_collisions_with_power_balls()

    def check_collisions_with_power_balls(self):
        for ball in self.player.power_balls:
            for enemy in self.enemies:
                if ball.rect.colliderect(enemy.rect):
                    enemy.take_damage()
                    self.player.power_balls.remove(ball)
                    break
            if self.final_boss and ball.rect.colliderect(self.final_boss.rect):
                self.final_boss.take_damage(1)
                self.player.power_balls.remove(ball)
                if self.final_boss.health <= 0:
                    self.victory = True
                    pygame.mixer.music.load(self.victory_music)
                    pygame.mixer.music.play()
                break

    def check_if_player_fell(self):
        if self.player.rect.top > 720:
            print("Has caído!")
            self.hud.lives -= 1
            self.death_sound.play()
            if self.hud.lives <= 0:
                self.game_over = True
                pygame.mixer.music.load(self.game_over_music)
                pygame.mixer.music.play()
            else:
                self.reset_player()
                if self.final_boss:
                    self.final_boss.increase_attack_delay()

    def check_collisions_with_coins(self):
        for coin in self.coins[:]:
            if self.player.rect.colliderect(coin.rect):
                self.coins.remove(coin)
                self.hud.score += 10
                self.coin_sound.play()

    def check_if_level_completed(self):
        if self.player.rect.right >= 1280:
            if self.level < self.max_levels:
                self.level += 1
                self.setup_level(self.level)
            else:
                print("¡Has completado todos los niveles!")
                self.victory = True
                pygame.mixer.music.load(self.victory_music)
                pygame.mixer.music.play()

    def reset_player(self):
        first_platform = self.platforms[0]
        self.player.rect.x = first_platform.rect.x + first_platform.rect.width // 2 - self.player.rect.width // 2
        self.player.rect.y = first_platform.rect.y - self.player.rect.height
        self.player.speed_y = 0
        self.player.on_ground = False
        self.player.jump_count = 0

    def reset_game(self):
        self.level = 1
        self.hud.lives = 6
        self.hud.score = 0
        self.game_over = False
        self.victory = False
        pygame.mixer.music.load(self.background_music)
        pygame.mixer.music.play(-1)
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
            self.final_boss.draw_health_bar(self.screen)
        self.hud.draw(self.screen, self.level)
        if self.game_over:
            self.hud.draw_game_over_screen(self.screen)
        if self.victory:
            self.hud.draw_victory_screen(self.screen)
        self.draw_next_level_arrow()
        pygame.display.flip()

    def draw_next_level_arrow(self):
        if self.level < 6:
            arrow_color = (255, 255, 0)
            arrow_points = [
                (1260, 360 + self.arrow_animation_offset),
                (1280, 340 + self.arrow_animation_offset),
                (1280, 380 + self.arrow_animation_offset)
            ]
            pygame.draw.polygon(self.screen, arrow_color, arrow_points)
            font = pygame.font.Font(None, 36)
            continue_text = font.render("Sigue", True, (255, 255, 0))
            self.screen.blit(continue_text, (1180, 360 + self.arrow_animation_offset - 10))

    def check_collisions(self):
        for ball in self.player.power_balls:
            for enemy in self.enemies:
                if ball.rect.colliderect(enemy.rect):
                    enemy.take_damage()
                    self.player.power_balls.remove(ball)
                    break
            if self.final_boss and ball.rect.colliderect(self.final_boss.rect):
                self.final_boss.take_damage(10)
                self.player.power_balls.remove(ball)
                break
