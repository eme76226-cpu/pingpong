import pygame
import random

pygame.init()

WIDTH, HEIGHT = 600, 500
BG_COLOR = (200, 255, 255)
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Пинг-понг")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW_GREEN = (204, 255, 0)
RED = (200, 0, 0)

font_large = pygame.font.SysFont("Arial", 36, bold=True)
font_small = pygame.font.SysFont("Arial", 24, bold=True)

lose1_text = font_large.render("ИГРОК 1 ПРОИГРАЛ!", True, RED)
lose2_text = font_large.render("ИГРОК 2 ПРОИГРАЛ!", True, RED)


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


def reset_ball(ball, direction_x):
    ball.rect.x = WIDTH // 2 - ball.rect.width // 2
    ball.rect.y = HEIGHT // 2 - ball.rect.height // 2
    return 4 * direction_x, random.choice([-4, 4])

racket1 = Player(30, 200, 20, 100, 5)
racket2 = Player(WIDTH - 50, 200, 20, 100, 5)
ball = GameSprite(WIDTH // 2, HEIGHT // 2, 30, 30, 4)

speed_x = 4
speed_y = 4

score1 = 0
score2 = 0
MAX_SCORE = 5
start_ticks = pygame.time.get_ticks()

cooldown1 = 0
cooldown2 = 0
COOLDOWN_TIME = 180  # 3 секунды при 60 FPS

clock = pygame.time.Clock()
FPS = 60
run = True
finish = False

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN and not finish:
            if event.key == pygame.K_SPACE and cooldown1 == 0:
                speed_y *= -1
                cooldown1 = COOLDOWN_TIME
            if event.key == pygame.K_RETURN and cooldown2 == 0:
                speed_y *= -1
                cooldown2 = COOLDOWN_TIME

    if not finish:
        window.fill(BG_COLOR)

        if cooldown1 > 0:
            cooldown1 -= 1
        if cooldown2 > 0:
            cooldown2 -= 1

        racket1.update_left()
        racket2.update_right()

        ball.rect.x += speed_x
        ball.rect.y += speed_y

        if ball.rect.y <= 0 or ball.rect.y >= HEIGHT - ball.rect.height:
            speed_y *= -1

        if ball.rect.colliderect(racket1.rect) and speed_x < 0:
            speed_x *= -1
        if ball.rect.colliderect(racket2.rect) and speed_x > 0:
            speed_x *= -1

        if ball.rect.x < 0:
            score2 += 1
            if score2 >= MAX_SCORE:
                finish = True
                window.blit(lose1_text, (130, 220))
            else:
                speed_x, speed_y = reset_ball(ball, 1)

        elif ball.rect.x > WIDTH - ball.rect.width:
            score1 += 1
            if score1 >= MAX_SCORE:
                finish = True
                window.blit(lose2_text, (130, 220))
            else:
                speed_x, speed_y = reset_ball(ball, -1)

        racket1.draw()
        racket2.draw()
        pygame.draw.ellipse(window, YELLOW_GREEN, ball.rect)
        pygame.draw.ellipse(window, BLACK, ball.rect, 2)

        seconds = (pygame.time.get_ticks() - start_ticks) // 1000
        minutes = seconds // 60
        sec_display = seconds % 60
        time_text = font_small.render(f"Время: {minutes:02d}:{sec_display:02d}", True, BLACK)
        window.blit(time_text, (WIDTH // 2 - time_text.get_width() // 2, 10))

        score_text = font_large.render(f"{score1} : {score2}", True, BLACK)
        window.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 40))

        status1 = "Готов [SPACE]" if cooldown1 == 0 else f"Ждите: {cooldown1 // 60 + 1}с"
        status2 = "Готов [ENTER]" if cooldown2 == 0 else f"Ждите: {cooldown2 // 60 + 1}с"

        p1_skill_text = font_small.render(status1, True, BLACK)
        p2_skill_text = font_small.render(status2, True, BLACK)
        window.blit(p1_skill_text, (20, 10))
        window.blit(p2_skill_text, (WIDTH - p2_skill_text.get_width() - 20, 10))

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
