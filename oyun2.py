import pygame
import random
import sys


WIDTH, HEIGHT = 600, 700
FPS = 60
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Uzay Savunması - Ayberk Demirhan")
clock = pygame.time.Clock()


def load_image(name, size=None, color=(255, 0, 0)):
    try:
        img = pygame.image.load(name).convert_alpha()
        if size:
            img = pygame.transform.scale(img, size)
        return img
    except:
        surf = pygame.Surface(size if size else (50, 50))
        surf.fill(color)
        return surf


def load_sound(name):
    try:
        return pygame.mixer.Sound(name)
    except:
        print(f"UYARI: {name} bulunamadı!")
        return None


player_img = load_image('player_ship.png', (60, 50), GREEN)
ufo_img = load_image('ufo.png', (50, 40), RED)
laser_img = load_image('laser.png', (10, 30), (255, 255, 0))
background_img = load_image('background.png', (WIDTH, HEIGHT), (0, 0, 0))


shoot_sound = load_sound('mixkit-short-laser-gun-shot-1670.wav')
game_over_sound = load_sound('mixkit-arcade-fast-game-over-233.wav')
start_sound = load_sound('game-start-6104.wav')



def draw_text(surf, text, size, x, y):
    font = pygame.font.SysFont("Arial", size, bold=True)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def draw_shield_bar(surf, x, y, pct):
    if pct < 0: pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN if pct > 30 else RED, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)



class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= 8
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += 8
        if keys[pygame.K_SPACE]:
            self.shoot()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            b = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(b)
            bullets.add(b)
            if shoot_sound:
                shoot_sound.play()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, current_score):
        super().__init__()
        self.image = ufo_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)

        # Hız Mantığı: Başlangıç hızı 2-5 arası, her 500 puanda +2 hız bonusu
        speed_bonus = (current_score // 500) * 2
        self.speedy = random.randrange(2, 5) + speed_bonus

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = laser_img
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -12

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


def show_go_screen(display_score):
    screen.blit(background_img, (0, 0))
    draw_text(screen, "UZAY SAVUNMASI", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, f"SON SKORUN: {display_score}", 30, WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "Baslamak icin herhangi bir tusa bas", 20, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()

    if start_sound:
        start_sound.play()

    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                waiting = False



score = 0
game_over = True
running = True
bg_y = 0

while running:
    if game_over:
        show_go_screen(score)
        game_over = False
        all_sprites = pygame.sprite.Group()
        enemies = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(8):
            e = Enemy(score)
            all_sprites.add(e)
            enemies.add(e)
        score = 0

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()


    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for hit in hits:
        score += 10
        new_ufo = Enemy(score)  # Yeni gelen ufo skora göre hızlanacak
        all_sprites.add(new_ufo)
        enemies.add(new_ufo)

    hits = pygame.sprite.spritecollide(player, enemies, True)
    for hit in hits:
        player.shield -= 25
        new_ufo = Enemy(score)
        all_sprites.add(new_ufo)
        enemies.add(new_ufo)
        if player.shield <= 0:
            if game_over_sound:
                game_over_sound.play()
            game_over = True



    bg_y += 2
    if bg_y >= HEIGHT: bg_y = 0
    screen.blit(background_img, (0, bg_y))
    screen.blit(background_img, (0, bg_y - HEIGHT))

    all_sprites.draw(screen)
    draw_text(screen, f"Skor: {score}", 25, WIDTH // 2, 10)
    draw_shield_bar(screen, 10, 10, player.shield)

    pygame.display.flip()

pygame.quit()