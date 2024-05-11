import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Пинг-Понг")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

paddle_width, paddle_height = 15, 90

paddle_speed = 1

class Paddle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([paddle_width, paddle_height])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def move(self, speed):
        self.rect.y += speed
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        ball_radius = 20
        ball_speed_x = 0.7
        ball_speed_y = 0.5

        super().__init__()
        self.image = pygame.Surface([ball_radius*2, ball_radius*2], pygame.SRCALPHA)
        pygame.draw.circle(self.image, WHITE, (ball_radius, ball_radius), ball_radius)
        self.rect = self.image.get_rect(center=(WIDTH//2, HEIGHT//2))
        self.speed_x = ball_speed_x * random.choice((-1, 1))
        self.speed_y = ball_speed_y * random.choice((-1, 1))

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed_y *= -1
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.kill()
            pygame.quit()
            sys.exit()

paddle_a = Paddle(30, HEIGHT//2 - paddle_height//2)
paddle_b = Paddle(WIDTH - 30 - paddle_width, HEIGHT//2 - paddle_height//2)
ball = Ball()

all_sprites = pygame.sprite.Group()
paddles = pygame.sprite.Group()
all_sprites.add(paddle_a, paddle_b, ball)
paddles.add(paddle_a, paddle_b)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        paddle_a.move(-paddle_speed)
    if keys[pygame.K_s]:
        paddle_a.move(paddle_speed)
    if keys[pygame.K_UP]:
        paddle_b.move(-paddle_speed)
    if keys[pygame.K_DOWN]:
        paddle_b.move(paddle_speed)

    all_sprites.update()

    if pygame.sprite.spritecollide(ball, paddles, False):
        ball.speed_x *= -1

    screen.fill(BLACK)
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()