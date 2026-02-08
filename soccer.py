import pygame
import math


GEN, YUK = 1100, 650
FPS = 60
SURTUNME = 0.985
TOP_SURTUNME = 0.99
MAX_GUC = 25
GUC_CARPANI = 0.15


CIM_KOYU = (34, 139, 34)
CIM_ACIK = (50, 205, 50)
CIZGI_BEYAZ = (240, 240, 240)
KIRMIZI_TAKIM = (220, 40, 40)
MAVI_TAKIM = (40, 80, 220)
TOP_RENK = (255, 255, 255)
SIYAH = (20, 20, 20)
SARI_UI = (255, 215, 0)


class Top:
    def __init__(self):
        self.r = 14
        self.reset()

    def reset(self):
        self.x, self.y = GEN // 2, YUK // 2
        self.vx, self.vy = 0, 0

    def hareket(self):
        self.x += self.vx
        self.y += self.vy
        self.vx *= TOP_SURTUNME
        self.vy *= TOP_SURTUNME


        # Üst ve Alt
        if self.y - self.r < 50: self.y = 50 + self.r; self.vy *= -0.8
        if self.y + self.r > YUK - 50: self.y = YUK - 50 - self.r; self.vy *= -0.8


        kale_ust = YUK // 2 - 80
        kale_alt = YUK // 2 + 80


        if not (kale_ust < self.y < kale_alt):
            if self.x - self.r < 50: self.x = 50 + self.r; self.vx *= -0.8
            if self.x + self.r > GEN - 50: self.x = GEN - 50 - self.r; self.vx *= -0.8

    def durdu_mu(self):
        return abs(self.vx) < 0.05 and abs(self.vy) < 0.05

    def ciz(self, ekran):

        pygame.draw.circle(ekran, TOP_RENK, (int(self.x), int(self.y)), self.r)

        pygame.draw.circle(ekran, SIYAH, (int(self.x), int(self.y)), self.r - 4, 2)
        pygame.draw.circle(ekran, SIYAH, (int(self.x), int(self.y)), 4)


        offset = int((self.x + self.y) / 5) % 10
        pygame.draw.circle(ekran, SIYAH, (int(self.x) + 5, int(self.y) + 5), 2)


class Oyuncu:
    def __init__(self, x, y, takim):
        self.baslangic_x = x
        self.baslangic_y = y
        self.x, self.y = x, y
        self.vx, self.vy = 0, 0
        self.takim = takim
        self.r = 22  # Oyuncu boyutu
        self.renk = KIRMIZI_TAKIM if takim == 'kirmizi' else MAVI_TAKIM
        # Oyuncu parlaklık efekti
        self.renk_ic = (min(self.renk[0] + 50, 255), min(self.renk[1] + 50, 255), min(self.renk[2] + 50, 255))

    def reset(self):
        self.x, self.y = self.baslangic_x, self.baslangic_y
        self.vx, self.vy = 0, 0

    def hareket(self):
        self.x += self.vx
        self.y += self.vy
        self.vx *= SURTUNME
        self.vy *= SURTUNME


        if self.x - self.r < 50: self.x = 50 + self.r; self.vx *= -0.5
        if self.x + self.r > GEN - 50: self.x = GEN - 50 - self.r; self.vx *= -0.5
        if self.y - self.r < 50: self.y = 50 + self.r; self.vy *= -0.5
        if self.y + self.r > YUK - 50: self.y = YUK - 50 - self.r; self.vy *= -0.5

    def durdu_mu(self):
        return abs(self.vx) < 0.05 and abs(self.vy) < 0.05

    def ciz(self, ekran):

        pygame.draw.circle(ekran, (255, 255, 255), (int(self.x), int(self.y)), self.r + 2)

        pygame.draw.circle(ekran, self.renk, (int(self.x), int(self.y)), self.r)

        pygame.draw.circle(ekran, self.renk_ic, (int(self.x - 3), int(self.y - 3)), self.r - 8)


def carpisma_coz(p1, p2):
    dx = p1.x - p2.x
    dy = p1.y - p2.y
    mesafe = math.hypot(dx, dy)

    if mesafe < p1.r + p2.r:
        angle = math.atan2(dy, dx)
        sin_a, cos_a = math.sin(angle), math.cos(angle)


        overlap = (p1.r + p2.r - mesafe) / 2
        p1.x += cos_a * overlap
        p1.y += sin_a * overlap
        p2.x -= cos_a * overlap
        p2.y -= sin_a * overlap


        v1 = math.hypot(p1.vx, p1.vy)
        v2 = math.hypot(p2.vx, p2.vy)


        p1.vx = cos_a * v2 * 0.8
        p1.vy = sin_a * v2 * 0.8
        p2.vx = -cos_a * v1 * 0.8
        p2.vy = -sin_a * v1 * 0.8


def saha_ciz(ekran):

    ekran.fill(CIM_KOYU)
    for x in range(50, GEN - 50, 100):
        pygame.draw.rect(ekran, CIM_ACIK, (x, 50, 50, YUK - 100))


    pygame.draw.rect(ekran, CIZGI_BEYAZ, (50, 50, GEN - 100, YUK - 100), 5)


    pygame.draw.line(ekran, CIZGI_BEYAZ, (GEN // 2, 50), (GEN // 2, YUK - 50), 4)
    pygame.draw.circle(ekran, CIZGI_BEYAZ, (GEN // 2, YUK // 2), 80, 4)
    pygame.draw.circle(ekran, CIM_KOYU, (GEN // 2, YUK // 2), 76)  # İçi boş olsun diye
    pygame.draw.circle(ekran, CIZGI_BEYAZ, (GEN // 2, YUK // 2), 8)  # Orta nokta


    kale_h = 160
    kale_y = YUK // 2 - kale_h // 2

    pygame.draw.rect(ekran, CIZGI_BEYAZ, (50, kale_y, 60, kale_h), 4)

    pygame.draw.rect(ekran, CIZGI_BEYAZ, (GEN - 110, kale_y, 60, kale_h), 4)


def ok_ciz(ekran, baslangic, fare_pos, guc_orani):

    r = min(255, int(255 * guc_orani * 2))
    g = min(255, int(255 * (1 - guc_orani) * 2))
    renk = (r, g, 0)

    dx = baslangic[0] - fare_pos[0]
    dy = baslangic[1] - fare_pos[1]
    aci = math.atan2(dy, dx)

    uzunluk = min(math.hypot(dx, dy), 200)  # Okun maksimum görsel uzunluğu

    bitis_x = baslangic[0] + math.cos(aci) * uzunluk
    bitis_y = baslangic[1] + math.sin(aci) * uzunluk


    pygame.draw.line(ekran, renk, baslangic, (bitis_x, bitis_y), 6)


    ok_ucu_boyutu = 15
    uc1 = (bitis_x + math.cos(aci + 2.5) * ok_ucu_boyutu, bitis_y + math.sin(aci + 2.5) * ok_ucu_boyutu)
    uc2 = (bitis_x + math.cos(aci - 2.5) * ok_ucu_boyutu, bitis_y + math.sin(aci - 2.5) * ok_ucu_boyutu)
    pygame.draw.polygon(ekran, renk, [(bitis_x, bitis_y), uc1, uc2])


    font = pygame.font.SysFont("Arial", 16, bold=True)
    yuzde = font.render(f"%{int(guc_orani * 100)}", True, (255, 255, 255))
    ekran.blit(yuzde, (bitis_x + 10, bitis_y + 10))


def main():
    pygame.init()
    ekran = pygame.display.set_mode((GEN, YUK))
    pygame.display.set_caption("Pro Soccer Stars 2026")
    saat = pygame.time.Clock()
    font_skor = pygame.font.SysFont("Impact", 60)
    font_ui = pygame.font.SysFont("Arial", 20)


    k_takim = [
        Oyuncu(100, YUK // 2, 'kirmizi'),  # GK
        Oyuncu(250, YUK // 2 - 100, 'kirmizi'),  # DEF 1
        Oyuncu(250, YUK // 2 + 100, 'kirmizi'),  # DEF 2
        Oyuncu(400, YUK // 2, 'kirmizi')  # FWD
    ]
    m_takim = [
        Oyuncu(GEN - 100, YUK // 2, 'mavi'),
        Oyuncu(GEN - 250, YUK // 2 - 100, 'mavi'),
        Oyuncu(GEN - 250, YUK // 2 + 100, 'mavi'),
        Oyuncu(GEN - 400, YUK // 2, 'mavi')
    ]

    tum_oyuncular = k_takim + m_takim
    top = Top()

    sira = 'kirmizi'
    skor_k, skor_m = 0, 0
    hareket_var = False
    secili_oyuncu = None
    oyun_bitti = False

    while True:
        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: return

            if oyun_bitti:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        skor_k, skor_m = 0, 0
                        oyun_bitti = False
                        sira = 'kirmizi'
                        top.reset()
                        for o in tum_oyuncular: o.reset()
                    if event.key == pygame.K_q: return
                continue

            if not hareket_var and event.type == pygame.MOUSEBUTTONDOWN:
                aktif_takim = k_takim if sira == 'kirmizi' else m_takim
                for o in aktif_takim:
                    if math.hypot(mx - o.x, my - o.y) < o.r + 10:
                        secili_oyuncu = o

            if event.type == pygame.MOUSEBUTTONUP and secili_oyuncu:
                dx = secili_oyuncu.x - mx
                dy = secili_oyuncu.y - my
                guc = math.hypot(dx, dy) * GUC_CARPANI

                if guc > 1.5:
                    guc = min(guc, MAX_GUC)
                    aci = math.atan2(dy, dx)

                    secili_oyuncu.vx = math.cos(aci) * guc
                    secili_oyuncu.vy = math.sin(aci) * guc

                    hareket_var = True
                    sira = 'mavi' if sira == 'kirmizi' else 'kirmizi'

                secili_oyuncu = None


        hepsi_durdu = True


        for i in range(len(tum_oyuncular)):
            o1 = tum_oyuncular[i]
            o1.hareket()
            if not o1.durdu_mu(): hepsi_durdu = False

            for j in range(i + 1, len(tum_oyuncular)):
                carpisma_coz(o1, tum_oyuncular[j])


            carpisma_coz(o1, top)

        top.hareket()
        if not top.durdu_mu(): hepsi_durdu = False

        if hareket_var and hepsi_durdu:
            hareket_var = False


        kale_ust = YUK // 2 - 80
        kale_alt = YUK // 2 + 80
        gol_oldu = False

        if top.x < 50 and kale_ust < top.y < kale_alt:
            skor_m += 1
            gol_oldu = True
            sira = 'kirmizi'
        elif top.x > GEN - 50 and kale_ust < top.y < kale_alt:
            skor_k += 1
            gol_oldu = True
            sira = 'mavi'

        if gol_oldu:
            top.reset()
            for o in tum_oyuncular: o.reset()
            hareket_var = False

            pygame.time.delay(500)

        if skor_k >= 3 or skor_m >= 3:
            oyun_bitti = True


        saha_ciz(ekran)


        if secili_oyuncu:
            pygame.draw.circle(ekran, SARI_UI, (int(secili_oyuncu.x), int(secili_oyuncu.y)), secili_oyuncu.r + 5, 2)

        for o in tum_oyuncular: o.ciz(ekran)
        top.ciz(ekran)


        if secili_oyuncu and pygame.mouse.get_pressed()[0]:
            dx = secili_oyuncu.x - mx
            dy = secili_oyuncu.y - my
            ham_guc = math.hypot(dx, dy) * GUC_CARPANI
            guc_orani = min(ham_guc / MAX_GUC, 1.0)

            ok_ciz(ekran, (secili_oyuncu.x, secili_oyuncu.y), (mx, my), guc_orani)


        skor_txt = font_skor.render(f"{skor_k} - {skor_m}", True, (255, 255, 255))
        ekran.blit(skor_txt, (GEN // 2 - skor_txt.get_width() // 2, 10))

        if not oyun_bitti:
            sira_renk = KIRMIZI_TAKIM if sira == 'kirmizi' else MAVI_TAKIM
            pygame.draw.rect(ekran, sira_renk, (GEN // 2 - 70, 70, 140, 30), border_radius=10)
            sira_txt = font_ui.render(f"SIRA: {sira.upper()}", True, (255, 255, 255))
            ekran.blit(sira_txt, (GEN // 2 - sira_txt.get_width() // 2, 75))


        if oyun_bitti:
            overlay = pygame.Surface((GEN, YUK))
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))
            ekran.blit(overlay, (0, 0))

            kazanan = "KIRMIZI" if skor_k >= 3 else "MAVİ"
            renk = KIRMIZI_TAKIM if skor_k >= 3 else MAVI_TAKIM

            yazi1 = font_skor.render(f"{kazanan} KAZANDI!", True, renk)
            yazi2 = font_ui.render("Tekrar Oyna: [R]  |  Çıkış: [Q]", True, (255, 255, 255))

            ekran.blit(yazi1, (GEN // 2 - yazi1.get_width() // 2, YUK // 2 - 50))
            ekran.blit(yazi2, (GEN // 2 - yazi2.get_width() // 2, YUK // 2 + 50))

        pygame.display.flip()
        saat.tick(FPS)


if __name__ == "__main__":
    main()