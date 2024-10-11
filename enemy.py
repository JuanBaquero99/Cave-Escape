import pygame
import random

class Enemy:
    def __init__(self, speed=1):
        self.rect = pygame.Rect(random.randint(0, 1210), random.randint(0, 550), 70, 70)  # Ajustar la posición inicial del enemigo
        self.speed = speed
        self.image = pygame.image.load("assets/images/character/enemy/Enemy.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (70, 70))  # Aumentar el tamaño de la imagen del enemigo

    def update(self):
        self.rect.x += self.speed
        if self.rect.x > 1280:  # Ajustar el límite derecho de la pantalla
            self.rect.x = -70  # Reiniciar el enemigo desde el borde izquierdo

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

class PowerBall:
    def __init__(self, x, y, speed=-5):  # Cambiar la dirección de la bola de poder hacia la izquierda
        self.rect = pygame.Rect(x, y, 30, 30)
        self.speed = speed
        self.image = pygame.image.load("assets/images/character/enemy/magic1.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))

    def update(self):
        self.rect.x += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

class FinalBoss:
    def __init__(self, speed=4):  # Aumentar la velocidad del jefe final
        self.rect = pygame.Rect(1140, 0, 200, 200)  # Posición inicial del jefe final en la esquina derecha superior
        self.speed = speed
        self.normal_image = pygame.image.load("assets/images/character/enemy/boss_1.png").convert_alpha()
        self.attack_image = pygame.image.load("assets/images/character/enemy/boss_2.png").convert_alpha()
        self.normal_image = pygame.transform.scale(self.normal_image, (200, 200))  # Tamaño más grande del jefe final
        self.attack_image = pygame.transform.scale(self.attack_image, (200, 200))  # Tamaño más grande del jefe final
        self.image = self.normal_image
        self.health = 100  # Salud del jefe final
        self.attack_timer = 0  # Temporizador para el ataque
        self.power_balls = []  # Lista de bolas de poder
        self.attacking = False  # Estado del jefe final
        self.balls_to_fire = 0  # Contador de bolas de poder a disparar
        self.attack_delay = 60  # Retraso inicial entre ataques

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 520 or self.rect.y < 0:  # Rebotar en los bordes superior e inferior de la pantalla
            self.speed = -self.speed

        self.attack_timer += 1
        if self.attack_timer > self.attack_delay:  # Usar el retraso dinámico entre ataques
            self.attack()
            self.attack_timer = 0

        if self.balls_to_fire > 0:
            self.fire_power_ball()
            self.balls_to_fire -= 1

        for ball in self.power_balls:
            ball.update()
            if ball.rect.x < 0:  # Eliminar bolas de poder que salen de la pantalla
                self.power_balls.remove(ball)

    def attack(self):
        # Cambiar a la imagen de ataque
        self.image = self.attack_image
        self.attacking = True

        # Configurar el número de bolas de poder a disparar
        self.balls_to_fire = 3

        # Volver a la imagen normal después de un breve periodo
        pygame.time.set_timer(pygame.USEREVENT, 500)

    def fire_power_ball(self):
        # Crear una nueva bola de poder y añadirla a la lista
        new_ball = PowerBall(self.rect.centerx, self.rect.centery)
        self.power_balls.append(new_ball)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        for ball in self.power_balls:
            ball.draw(screen)

    def handle_event(self, event):
        if event.type == pygame.USEREVENT and self.attacking:
            self.image = self.normal_image
            self.attacking = False

    def increase_attack_delay(self):
        self.attack_delay += 30  # Incrementar el retraso entre ataques en 30 fotogramas