import pygame
import random

KARE = 30
GEN, YUK = 10, 20
PENCERE_G, PENCERE_Y = 500, 600

RENKLER = [
    (15, 15, 20), (0, 255, 255), (255, 255, 0),
    (128, 0, 128), (0, 255, 0), (255, 0, 0),
    (0, 0, 255), (255, 165, 0)
]

SEKILLER = [
    [[1, 1, 1, 1]], [[1, 1], [1, 1]], [[0, 1, 0], [1, 1, 1]],
    [[0, 1, 1], [1, 1, 0]], [[1, 1, 0], [0, 1, 1]],
    [[1, 0, 0], [1, 1, 1]], [[0, 0, 1], [1, 1, 1]]
]


class Tetris:
    def __init__(self):
        self.alan = [[0] * GEN for _ in range(YUK)]
        self.bitti = False
        self.skor = 0
        self.yeni_parca()

    def yeni_parca(self):
        self.sekil = random.choice(SEKILLER)
        self.renk = SEKILLER.index(self.sekil) + 1
        self.x, self.y = GEN // 2 - len(self.sekil[0]) // 2, 0
        if self.carpisma(0, 0): self.bitti = True

    def carpisma(self, dx, dy, s=None):
        s = s or self.sekil
        for r, satir in enumerate(s):
            for c, v in enumerate(satir):
                if v:
                    nx, ny = self.x + c + dx, self.y + r + dy
                    if nx < 0 or nx >= GEN or ny >= YUK or (ny >= 0 and self.alan[ny][nx]):
                        return True
        return False

    def sabitle(self):
        for r, satir in enumerate(self.sekil):
            for c, v in enumerate(satir):
                if v: self.alan[self.y + r][self.x + c] = self.renk
        self.temizle()
        self.yeni_parca()

    def temizle(self):
        yeni = [s for s in self.alan if 0 in s]
        n = YUK - len(yeni)
        self.alan = [[0] * GEN for _ in range(n)] + yeni
        self.skor += n * 100


def main():
    pygame.init()
    ekran = pygame.display.set_mode((PENCERE_G, PENCERE_Y))
    pygame.display.set_caption("Turbo FPS Tetris")
    saat = pygame.time.Clock()
    oyun = Tetris()

    d_zamani = 0
    hiz = 300

    while not oyun.bitti:
        dt = saat.tick(120)
        d_zamani += dt

        for e in pygame.event.get():
            if e.type == pygame.QUIT: return
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_LEFT and not oyun.carpisma(-1, 0): oyun.x -= 1
                if e.key == pygame.K_RIGHT and not oyun.carpisma(1, 0): oyun.x += 1
                if e.key == pygame.K_DOWN and not oyun.carpisma(0, 1): oyun.y += 1
                if e.key == pygame.K_UP:
                    d = [list(r) for r in zip(*oyun.sekil[::-1])]
                    if not oyun.carpisma(0, 0, d): oyun.sekil = d

        if d_zamani > hiz:
            if not oyun.carpisma(0, 1):
                oyun.y += 1
            else:
                oyun.sabitle()
            d_zamani = 0

        ekran.fill((10, 10, 15))

        for y in range(YUK):
            for x in range(GEN):
                renk_id = oyun.alan[y][x]
                rect = (x * KARE, y * KARE, KARE - 1, KARE - 1)
                if renk_id:
                    pygame.draw.rect(ekran, RENKLER[renk_id], rect)
                else:
                    pygame.draw.rect(ekran, (25, 25, 30), rect, 1)

        for r, satir in enumerate(oyun.sekil):
            for c, v in enumerate(satir):
                if v:
                    pygame.draw.rect(ekran, RENKLER[oyun.renk],
                                     ((oyun.x + c) * KARE, (oyun.y + r) * KARE, KARE - 1, KARE - 1))

        f = pygame.font.SysFont("Arial", 25, bold=True)
        ekran.blit(f.render(f"SKOR: {oyun.skor}", True, (255, 255, 255)), (320, 50))

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()