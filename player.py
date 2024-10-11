import pygame

class PlayerPowerBall:
    def __init__(self, x, y, speed=10):  # Velocidad hacia la derecha
        self.rect = pygame.Rect(x, y, 30, 30)
        self.speed = speed
        self.image = pygame.image.load("assets/images/character/player/magic1.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))

    def update(self):
        self.rect.x += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

class Player:
    def __init__(self):
        self.rect = pygame.Rect(100, 360, 70, 70)
        self.gravity = 0.5
        self.jump_speed = -10
        self.speed_y = 0
        self.on_ground = False
        self.jump_count = 0
        self.direction = "right"
        self.walk_images = [self.load_and_scale_image(f"assets/images/character/player/Player_{i}.png", (70, 70)) for i in range(6)]
        self.jump_images = [self.load_and_scale_image(f"assets/images/character/player/Player_jump_{i}.png", (70, 70)) for i in range(6)]
        self.attack_images = [self.load_and_scale_image(f"assets/images/character/player/Player_attack_{i}.png", (70, 70)) for i in range(4)]  # Asegúrate de que los nombres de los archivos sean correctos
        self.walk_left_images = [pygame.transform.flip(image, True, False) for image in self.walk_images]
        self.attack_left_images = [pygame.transform.flip(image, True, False) for image in self.attack_images]
        self.current_image = 0
        self.image_counter = 0
        self.image_speed = 5
        self.image = self.walk_images[0]
        self.attacking = False
        self.power_balls = []
        self.attack_cooldown = 0  # Temporizador para el enfriamiento del ataque

    def load_and_scale_image(self, filename, size):
        image = pygame.image.load(filename).convert_alpha()
        image = pygame.transform.scale(image, size)
        return image

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
            self.direction = "left"
            if not self.attacking:
                self.update_walk_animation()
        elif keys[pygame.K_RIGHT]:
            self.rect.x += 5
            self.direction = "right"
            if not self.attacking:
                self.update_walk_animation()
        else:
            if not self.attacking:
                self.image_counter = 0
                self.current_image = 0
                self.image = self.walk_images[0] if self.direction == "right" else self.walk_left_images[0]

        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump()
        if keys[pygame.K_x]:  # Tecla para lanzar poder
            self.attacking = True
            self.attack()
        else:
            self.attacking = False

        self.update_power_balls()

        if self.attacking:
            self.update_attack_animation()

    def update_walk_animation(self):
        self.image_counter += 1
        if self.image_counter >= self.image_speed:
            self.image_counter = 0
            self.current_image = (self.current_image + 1) % len(self.walk_images)
            if self.direction == "right":
                self.image = self.walk_images[self.current_image]
            else:
                self.image = self.walk_left_images[self.current_image]

    def update_jump_animation(self):
        self.current_image = (self.current_image + 1) % len(self.jump_images)
        self.image = self.jump_images[self.current_image] if self.direction == "right" else pygame.transform.flip(self.jump_images[self.current_image], True, False)

    def update_attack_animation(self):
        self.image_counter += 1
        if self.image_counter >= self.image_speed:
            self.image_counter = 0
            self.current_image = (self.current_image + 1) % len(self.attack_images)
            if self.direction == "right":
                self.image = self.attack_images[self.current_image]
            else:
                self.image = self.attack_left_images[self.current_image]

    def jump(self):
        self.speed_y = self.jump_speed
        self.on_ground = False

    def attack(self):
        if self.attack_cooldown == 0:
            self.fire_power_ball()
            self.attack_cooldown = 20  # Enfriamiento de 20 fotogramas (ajusta según sea necesario)

    def fire_power_ball(self):
        if self.direction == "right":
            new_ball = PlayerPowerBall(self.rect.right, self.rect.centery)
        else:
            new_ball = PlayerPowerBall(self.rect.left - 30, self.rect.centery, speed=-10)
        self.power_balls.append(new_ball)

    def update_power_balls(self):
        for ball in self.power_balls:
            ball.update()
            if ball.rect.x > 1280 or ball.rect.x < 0:  # Eliminar bolas de poder que salen de la pantalla
                self.power_balls.remove(ball)

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        for ball in self.power_balls:
            ball.draw(screen)