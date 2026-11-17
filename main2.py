import pygame
pygame.init()

WIDTH, HEIGHT = 600, 500
BG_COLOR = (200, 255, 255)
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Пинг-понг")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW_GREEN = (204, 255, 0)
RED = (200, 0, 0)

font = pygame.font.SysFont("Arial", 36, bold=True)
lose1_text = font.render("ИГРОК 1 ПРОИГРАЛ!", True, RED)
lose2_text = font.render("ИГРОК 2 ПРОИГРАЛ!", True, RED)

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, speed):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed

class Player(GameSprite):
    def update_left(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.y < HEIGHT - self.rect.height - 5:
            self.rect.y += self.speed

    def update_right(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.y < HEIGHT - self.rect.height - 5:
            self.rect.y += self.speed

    def draw(self):
        pygame.draw.rect(window, WHITE, self.rect)
        pygame.draw.rect(window, BLACK, self.rect, 4)

racket1 = Player(30, 200, 20, 100, 5)
racket2 = Player(WIDTH - 50, 200, 20, 100, 5)
ball = GameSprite(WIDTH // 2, HEIGHT // 2, 30, 30, 4)

speed_x = 4
speed_y = 4

clock = pygame.time.Clock()
FPS = 60
run = True
finish = False

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if not finish:
        window.fill(BG_COLOR)

        racket1.update_left()
        racket2.update_right()

        ball.rect.x += speed_x
        ball.rect.y += speed_y

        if ball.rect.y <= 0 or ball.rect.y >= HEIGHT - ball.rect.height:
            speed_y *= -1

        if ball.rect.colliderect(racket1.rect) or ball.rect.colliderect(racket2.rect):
            speed_x *= -1

        if ball.rect.x < 0:
            finish = True
            window.blit(lose1_text, (130, 220))
        elif ball.rect.x > WIDTH - ball.rect.width:
            finish = True
            window.blit(lose2_text, (130, 220))

        racket1.draw()
        racket2.draw()
        pygame.draw.ellipse(window, YELLOW_GREEN, ball.rect)
        pygame.draw.ellipse(window, BLACK, ball.rect, 2)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
