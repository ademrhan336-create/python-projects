import pygame
import random

GEN, YUK = 400, 600
YER_CEKIMI = 0.25
ZIPLAMA = -6
BORU_HIZ = 3


def main():
    pygame.init()
    ekran = pygame.display.set_mode((GEN, YUK))
    saat = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 32)

    kus_rect = pygame.Rect(50, YUK // 2, 30, 30)
    kus_hareket = 0

    borular = []
    boru_zaman = 0
    skor = 0

    while True:
        ekran.fill((0, 200, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT: return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    kus_hareket = ZIPLAMA

        kus_hareket += YER_CEKIMI
        kus_rect.y += kus_hareket

        boru_zaman += 1
        if boru_zaman > 90:
            yukseklik = random.randint(150, 400)
            borular.append(pygame.Rect(GEN, 0, 50, yukseklik - 150))
            borular.append(pygame.Rect(GEN, yukseklik, 50, YUK - yukseklik))
            boru_zaman = 0

        for b in borular[:]:
            b.x -= BORU_HIZ
            if b.right < 0:
                borular.remove(b)
                if len(borular) % 2 == 0: skor += 0.5

            if kus_rect.colliderect(b): return

        if kus_rect.top <= 0 or kus_rect.bottom >= YUK: return

        pygame.draw.rect(ekran, (255, 255, 0), kus_rect)
        for b in borular:
            pygame.draw.rect(ekran, (0, 150, 0), b)

        skor_yazi = font.render(f"Skor: {int(skor)}", True, (255, 255, 255))
        ekran.blit(skor_yazi, (10, 10))

        pygame.display.flip()
        saat.tick(60)


if __name__ == "__main__":
    main()