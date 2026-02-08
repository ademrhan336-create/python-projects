import pygame
import random

GEN, YUK = 400, 600
KUS_BOYUT = 30
PLATFORM_G, PLATFORM_Y = 60, 10


def main():
    pygame.init()
    ekran = pygame.display.set_mode((GEN, YUK))
    saat = pygame.time.Clock()

    oyuncu = pygame.Rect(GEN // 2, YUK - 100, KUS_BOYUT, KUS_BOYUT)
    hiz_y = 0
    ziplama_gucu = -10
    yercekimi = 0.4

    platformlar = [pygame.Rect(GEN // 2 - 30, YUK - 50, PLATFORM_G, PLATFORM_Y)]
    for i in range(10):
        platformlar.append(pygame.Rect(random.randint(0, GEN - PLATFORM_G), YUK - i * 80, PLATFORM_G, PLATFORM_Y))

    skor = 0
    kamera_y = 0

    while True:
        ekran.fill((20, 20, 30))
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return

        tuslar = pygame.key.get_pressed()
        if tuslar[pygame.K_LEFT]: oyuncu.x -= 7
        if tuslar[pygame.K_RIGHT]: oyuncu.x += 7

        hiz_y += yercekimi
        oyuncu.y += hiz_y

        if oyuncu.y < 200:
            kamera_kayma = 200 - oyuncu.y
            oyuncu.y = 200
            skor += int(kamera_kayma)
            for p in platformlar:
                p.y += kamera_kayma
                if p.y > YUK:
                    p.y = random.randint(-50, 0)
                    p.x = random.randint(0, GEN - PLATFORM_G)

        for p in platformlar:
            if oyuncu.colliderect(p) and hiz_y > 0 and oyuncu.bottom < p.bottom + 10:
                hiz_y = ziplama_gucu

        if oyuncu.y > YUK: return

        if oyuncu.x < 0: oyuncu.x = GEN
        if oyuncu.x > GEN: oyuncu.x = 0

        pygame.draw.rect(ekran, (255, 255, 0), oyuncu)
        for p in platformlar:
            pygame.draw.rect(ekran, (0, 255, 100), p)

        f = pygame.font.SysFont("Arial", 25).render(f"Skor: {skor}", True, (255, 255, 255))
        ekran.blit(f, (10, 10))

        pygame.display.flip()
        saat.tick(60)


if __name__ == "__main__":
    main()