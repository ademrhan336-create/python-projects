import pygame

WIDTH, HEIGHT = 800, 500
PADDLE_W, PADDLE_H = 10, 100
BALL_SIZE = 15
WHITE = (255, 255, 255)
BLACK = (10, 10, 15)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Classic Pong")
    clock = pygame.time.Clock()

    p1_y = HEIGHT // 2 - PADDLE_H // 2
    p2_y = HEIGHT // 2 - PADDLE_H // 2
    ball_x, ball_y = WIDTH // 2, HEIGHT // 2
    ball_dx, ball_dy = 5, 5

    p1_score, p2_score = 0, 0
    font = pygame.font.SysFont("Consolas", 40)

    run = True
    while run:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and p1_y > 0: p1_y -= 7
        if keys[pygame.K_s] and p1_y < HEIGHT - PADDLE_H: p1_y += 7
        if keys[pygame.K_UP] and p2_y > 0: p2_y -= 7
        if keys[pygame.K_DOWN] and p2_y < HEIGHT - PADDLE_H: p2_y += 7

        ball_x += ball_dx
        ball_y += ball_dy

        if ball_y <= 0 or ball_y >= HEIGHT - BALL_SIZE:
            ball_dy *= -1

        p1_rect = pygame.Rect(20, p1_y, PADDLE_W, PADDLE_H)
        p2_rect = pygame.Rect(WIDTH - 30, p2_y, PADDLE_W, PADDLE_H)
        ball_rect = pygame.Rect(ball_x, ball_y, BALL_SIZE, BALL_SIZE)

        if ball_rect.colliderect(p1_rect) or ball_rect.colliderect(p2_rect):
            ball_dx *= -1.1

        if ball_x < 0:
            p2_score += 1
            ball_x, ball_y = WIDTH // 2, HEIGHT // 2
            ball_dx = 5
        elif ball_x > WIDTH:
            p1_score += 1
            ball_x, ball_y = WIDTH // 2, HEIGHT // 2
            ball_dx = -5

        pygame.draw.rect(screen, WHITE, p1_rect)
        pygame.draw.rect(screen, WHITE, p2_rect)
        pygame.draw.ellipse(screen, WHITE, ball_rect)
        pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

        s1_text = font.render(str(p1_score), True, WHITE)
        s2_text = font.render(str(p2_score), True, WHITE)
        screen.blit(s1_text, (WIDTH // 4, 20))
        screen.blit(s2_text, (WIDTH * 3 // 4, 20))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()