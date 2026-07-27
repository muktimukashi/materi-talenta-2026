# =========================================================
# PART 1 — IMPORT LIBRARY
# Materi: import, library, file JSON
# =========================================================

import pygame
import json
import os


# =========================================================
# PART 2 — KONSTANTA DAN VARIABEL GLOBAL
# Materi: variabel, integer, string, tuple warna
# =========================================================

LEBAR = 900
TINGGI = 550
FPS = 60

JUDUL_GAME = "Python Adventure"
FILE_SKOR = "skor.json"

BIRU_LANGIT = (85, 175, 235)
BIRU_GELAP = (35, 55, 100)
BIRU_PLAYER = (55, 115, 245)
HIJAU_PLATFORM = (65, 170, 90)
HIJAU_PINTU = (45, 190, 100)
ABU_PINTU = (115, 120, 135)
KUNING = (255, 210, 45)
MERAH = (220, 65, 65)
PUTIH = (245, 245, 245)
HITAM = (25, 25, 35)
COKELAT = (135, 85, 50)


# =========================================================
# PART 3 — FUNGSI FILE JSON
# Materi: fungsi, dictionary, try-except, file
# =========================================================

def baca_data_skor():
    data_awal = {
        "nama": "-",
        "skor_tertinggi": 0
    }

    if not os.path.exists(FILE_SKOR):
        return data_awal

    try:
        with open(FILE_SKOR, "r", encoding="utf-8") as file:
            data = json.load(file)

        return {
            "nama": data.get("nama", "-"),
            "skor_tertinggi": data.get("skor_tertinggi", 0)
        }

    except (OSError, json.JSONDecodeError):
        return data_awal


def simpan_data_skor(nama, skor):
    data_lama = baca_data_skor()

    if skor <= data_lama["skor_tertinggi"]:
        return False

    data_baru = {
        "nama": nama,
        "skor_tertinggi": skor
    }

    try:
        with open(FILE_SKOR, "w", encoding="utf-8") as file:
            json.dump(data_baru, file, indent=4)

        return True

    except OSError:
        return False


# =========================================================
# PART 4 — CLASS PLAYER
# Materi: class, object, attribute, method
# =========================================================

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 42, 52)

        self.kecepatan = 6
        self.kecepatan_y = 0
        self.gravitasi = 0.8
        self.kekuatan_lompat = -15

        self.di_tanah = False
        self.skor = 0
        self.nyawa = 3

        self.posisi_awal = (x, y)
        self.kebal = False
        self.waktu_kebal = 0

    def baca_input(self):
        tombol = pygame.key.get_pressed()
        gerak_x = 0

        if tombol[pygame.K_LEFT] or tombol[pygame.K_a]:
            gerak_x = -self.kecepatan

        if tombol[pygame.K_RIGHT] or tombol[pygame.K_d]:
            gerak_x = self.kecepatan

        if tombol[pygame.K_SPACE] and self.di_tanah:
            self.kecepatan_y = self.kekuatan_lompat
            self.di_tanah = False

        return gerak_x

    def terapkan_gravitasi(self):
        self.kecepatan_y += self.gravitasi
        return int(self.kecepatan_y)

    def batasi_layar(self):
        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > LEBAR:
            self.rect.right = LEBAR

    def reset_posisi(self):
        self.rect.x = self.posisi_awal[0]
        self.rect.y = self.posisi_awal[1]
        self.kecepatan_y = 0

    def terkena_musuh(self):
        sekarang = pygame.time.get_ticks()

        if self.kebal and sekarang - self.waktu_kebal < 1500:
            return

        self.nyawa -= 1
        self.kebal = True
        self.waktu_kebal = sekarang
        self.reset_posisi()

    def update_kebal(self):
        if self.kebal:
            sekarang = pygame.time.get_ticks()

            if sekarang - self.waktu_kebal >= 1500:
                self.kebal = False

    def gambar(self, layar):
        # Berkedip saat kebal
        if self.kebal:
            sekarang = pygame.time.get_ticks()

            if (sekarang // 120) % 2 == 0:
                return

        pygame.draw.rect(
            layar,
            BIRU_PLAYER,
            self.rect,
            border_radius=8
        )

        # Mata pemain
        pygame.draw.circle(
            layar,
            PUTIH,
            (self.rect.x + 13, self.rect.y + 16),
            4
        )

        pygame.draw.circle(
            layar,
            PUTIH,
            (self.rect.x + 29, self.rect.y + 16),
            4
        )

        # Mulut
        pygame.draw.line(
            layar,
            HITAM,
            (self.rect.x + 14, self.rect.y + 35),
            (self.rect.x + 28, self.rect.y + 35),
            2
        )


# =========================================================
# PART 5 — CLASS ENEMY
# Materi: class tambahan, gerak otomatis, percabangan
# =========================================================

class Enemy:
    def __init__(self, x, y, batas_kiri, batas_kanan):
        self.rect = pygame.Rect(x, y, 42, 38)
        self.kecepatan = 2
        self.arah = 1
        self.batas_kiri = batas_kiri
        self.batas_kanan = batas_kanan

    def update(self):
        self.rect.x += self.kecepatan * self.arah

        if self.rect.left <= self.batas_kiri:
            self.rect.left = self.batas_kiri
            self.arah = 1

        if self.rect.right >= self.batas_kanan:
            self.rect.right = self.batas_kanan
            self.arah = -1

    def gambar(self, layar):
        pygame.draw.rect(
            layar,
            MERAH,
            self.rect,
            border_radius=8
        )

        pygame.draw.circle(
            layar,
            PUTIH,
            (self.rect.x + 12, self.rect.y + 13),
            4
        )

        pygame.draw.circle(
            layar,
            PUTIH,
            (self.rect.x + 30, self.rect.y + 13),
            4
        )

        pygame.draw.line(
            layar,
            HITAM,
            (self.rect.x + 13, self.rect.y + 29),
            (self.rect.x + 29, self.rect.y + 29),
            3
        )


# =========================================================
# PART 6 — FUNGSI TAMPILAN
# Materi: fungsi, parameter, modularisasi
# =========================================================

def gambar_teks(layar, teks, font, warna, x, y, posisi="kiri"):
    gambar = font.render(teks, True, warna)
    rect = gambar.get_rect()

    if posisi == "tengah":
        rect.center = (x, y)
    elif posisi == "kanan":
        rect.topright = (x, y)
    else:
        rect.topleft = (x, y)

    layar.blit(gambar, rect)


def gambar_latar(layar):
    layar.fill(BIRU_LANGIT)

    # Matahari
    pygame.draw.circle(
        layar,
        (255, 230, 100),
        (780, 85),
        45
    )

    # Awan
    pygame.draw.circle(layar, PUTIH, (145, 95), 28)
    pygame.draw.circle(layar, PUTIH, (180, 85), 35)
    pygame.draw.circle(layar, PUTIH, (215, 100), 26)

    pygame.draw.circle(layar, PUTIH, (520, 125), 24)
    pygame.draw.circle(layar, PUTIH, (552, 112), 31)
    pygame.draw.circle(layar, PUTIH, (585, 128), 23)

    # Bukit belakang
    pygame.draw.circle(
        layar,
        (80, 155, 105),
        (170, 540),
        210
    )

    pygame.draw.circle(
        layar,
        (65, 145, 95),
        (650, 560),
        260
    )


def gambar_platform(layar, platform):
    pygame.draw.rect(
        layar,
        HIJAU_PLATFORM,
        platform,
        border_radius=5
    )

    pygame.draw.rect(
        layar,
        COKELAT,
        (
            platform.x,
            platform.y + 8,
            platform.width,
            max(0, platform.height - 8)
        ),
        border_radius=4
    )


def gambar_koin(layar, coin):
    pygame.draw.circle(
        layar,
        KUNING,
        coin.center,
        12
    )

    pygame.draw.circle(
        layar,
        PUTIH,
        (coin.centerx - 4, coin.centery - 4),
        3
    )


def gambar_pintu(layar, pintu, terbuka):
    warna = HIJAU_PINTU if terbuka else ABU_PINTU

    pygame.draw.rect(
        layar,
        warna,
        pintu,
        border_radius=6
    )

    pygame.draw.rect(
        layar,
        HITAM,
        pintu,
        3,
        border_radius=6
    )

    pygame.draw.circle(
        layar,
        KUNING,
        (pintu.right - 13, pintu.centery),
        4
    )


def gambar_hud(layar, player, font, jumlah_koin, skor_tertinggi):
    pygame.draw.rect(
        layar,
        BIRU_GELAP,
        (0, 0, LEBAR, 60)
    )

    gambar_teks(
        layar,
        f"Skor: {player.skor}",
        font,
        PUTIH,
        18,
        17
    )

    gambar_teks(
        layar,
        f"Koin tersisa: {jumlah_koin}",
        font,
        KUNING,
        180,
        17
    )

    gambar_teks(
        layar,
        f"Nyawa: {player.nyawa}",
        font,
        PUTIH,
        425,
        17
    )

    gambar_teks(
        layar,
        f"High score: {skor_tertinggi}",
        font,
        PUTIH,
        LEBAR - 18,
        17,
        posisi="kanan"
    )


# =========================================================
# PART 7 — DATA LEVEL
# Materi: list, dictionary, pygame.Rect
# =========================================================

def buat_level():
    platforms = [
        pygame.Rect(0, 500, 900, 50),
        pygame.Rect(130, 415, 190, 22),
        pygame.Rect(385, 340, 190, 22),
        pygame.Rect(650, 255, 175, 22)
    ]

    coins = [
        pygame.Rect(210, 380, 24, 24),
        pygame.Rect(470, 305, 24, 24),
        pygame.Rect(720, 220, 24, 24)
    ]

    pintu = pygame.Rect(790, 185, 58, 70)

    enemy = Enemy(
        x=430,
        y=302,
        batas_kiri=385,
        batas_kanan=575
    )

    return platforms, coins, pintu, enemy


# =========================================================
# PART 8 — COLLISION PLATFORM
# Materi: loop, kondisi, collision detection
# =========================================================

def gerakkan_player(player, platforms):
    gerak_x = player.baca_input()

    # Gerak horizontal
    player.rect.x += gerak_x
    player.batasi_layar()

    # Gerak vertikal
    gerak_y = player.terapkan_gravitasi()
    posisi_sebelum = player.rect.copy()
    player.rect.y += gerak_y

    player.di_tanah = False

    for platform in platforms:
        if player.rect.colliderect(platform):
            if gerak_y > 0 and posisi_sebelum.bottom <= platform.top + 8:
                player.rect.bottom = platform.top
                player.kecepatan_y = 0
                player.di_tanah = True

            elif gerak_y < 0 and posisi_sebelum.top >= platform.bottom - 8:
                player.rect.top = platform.bottom
                player.kecepatan_y = 0

    # Jika jatuh keluar layar
    if player.rect.top > TINGGI:
        player.nyawa -= 1
        player.reset_posisi()


# =========================================================
# PART 9 — MENU AWAL
# Materi: string, event keyboard, input nama
# =========================================================

def menu_awal(layar, jam, font_besar, font, font_kecil):
    nama = ""
    data_skor = baca_data_skor()

    while True:
        jam.tick(FPS)

        gambar_latar(layar)

        pygame.draw.rect(
            layar,
            BIRU_GELAP,
            (120, 85, 660, 390),
            border_radius=18
        )

        gambar_teks(
            layar,
            "PYTHON ADVENTURE",
            font_besar,
            KUNING,
            LEBAR // 2,
            145,
            posisi="tengah"
        )

        gambar_teks(
            layar,
            "Platform game sederhana dengan Pygame",
            font,
            PUTIH,
            LEBAR // 2,
            205,
            posisi="tengah"
        )

        gambar_teks(
            layar,
            "A / D atau panah: bergerak   |   Space: melompat",
            font_kecil,
            PUTIH,
            LEBAR // 2,
            250,
            posisi="tengah"
        )

        gambar_teks(
            layar,
            (
                f"Skor tertinggi: {data_skor['skor_tertinggi']} "
                f"oleh {data_skor['nama']}"
            ),
            font_kecil,
            KUNING,
            LEBAR // 2,
            290,
            posisi="tengah"
        )

        gambar_teks(
            layar,
            "Nama pemain:",
            font,
            PUTIH,
            260,
            335
        )

        kotak_input = pygame.Rect(260, 375, 380, 48)

        pygame.draw.rect(
            layar,
            PUTIH,
            kotak_input,
            2,
            border_radius=8
        )

        gambar_teks(
            layar,
            nama,
            font,
            PUTIH,
            kotak_input.x + 12,
            kotak_input.y + 9
        )

        gambar_teks(
            layar,
            "Tekan ENTER untuk mulai",
            font_kecil,
            HIJAU_PINTU,
            LEBAR // 2,
            450,
            posisi="tengah"
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None

                if event.key == pygame.K_RETURN:
                    if nama.strip() == "":
                        return "Pemain"

                    return nama.strip()

                if event.key == pygame.K_BACKSPACE:
                    nama = nama[:-1]

                elif event.unicode.isprintable() and len(nama) < 15:
                    nama += event.unicode

        pygame.display.update()


# =========================================================
# PART 10 — HALAMAN HASIL
# Materi: fungsi, percabangan, status menang/kalah
# =========================================================

def halaman_hasil(
    layar,
    jam,
    menang,
    nama,
    player,
    font_besar,
    font,
    font_kecil
):
    rekor_baru = simpan_data_skor(nama, player.skor)

    while True:
        jam.tick(FPS)
        gambar_latar(layar)

        pygame.draw.rect(
            layar,
            BIRU_GELAP,
            (170, 100, 560, 340),
            border_radius=18
        )

        judul = "LEVEL SELESAI!" if menang else "GAME OVER"
        warna_judul = HIJAU_PINTU if menang else MERAH

        gambar_teks(
            layar,
            judul,
            font_besar,
            warna_judul,
            LEBAR // 2,
            165,
            posisi="tengah"
        )

        gambar_teks(
            layar,
            f"Pemain: {nama}",
            font,
            PUTIH,
            LEBAR // 2,
            245,
            posisi="tengah"
        )

        gambar_teks(
            layar,
            f"Skor akhir: {player.skor}",
            font,
            KUNING,
            LEBAR // 2,
            290,
            posisi="tengah"
        )

        if rekor_baru:
            gambar_teks(
                layar,
                "Rekor baru!",
                font,
                HIJAU_PINTU,
                LEBAR // 2,
                335,
                posisi="tengah"
            )

        gambar_teks(
            layar,
            "Tekan R untuk mengulang atau ESC untuk menu",
            font_kecil,
            PUTIH,
            LEBAR // 2,
            390,
            posisi="tengah"
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "keluar"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "ulang"

                if event.key == pygame.K_ESCAPE:
                    return "menu"

        pygame.display.update()


# =========================================================
# PART 11 — GAMEPLAY UTAMA
# Materi: game loop, list, collision, skor, nyawa
# =========================================================

def jalankan_game(layar, jam, nama, font, font_kecil):
    player = Player(75, 430)
    platforms, coins, pintu, enemy = buat_level()

    data_skor = baca_data_skor()
    pesan = "Ambil semua koin lalu masuk ke pintu!"
    waktu_pesan = pygame.time.get_ticks()

    while True:
        jam.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "keluar", player

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "menu", player

        # Update pemain dan musuh
        gerakkan_player(player, platforms)
        player.update_kebal()
        enemy.update()

        # Collision koin
        for coin in coins[:]:
            if player.rect.colliderect(coin):
                coins.remove(coin)
                player.skor += 10
                pesan = "+10! Koin berhasil diambil."
                waktu_pesan = pygame.time.get_ticks()

        # Collision musuh
        if player.rect.colliderect(enemy.rect):
            nyawa_sebelum = player.nyawa
            player.terkena_musuh()

            if player.nyawa < nyawa_sebelum:
                pesan = "Awas! Kamu menyentuh Bug Monster."
                waktu_pesan = pygame.time.get_ticks()

        # Collision pintu
        pintu_terbuka = len(coins) == 0

        if player.rect.colliderect(pintu):
            if pintu_terbuka:
                return "menang", player

            pesan = "Pintu terkunci. Ambil semua koin!"
            waktu_pesan = pygame.time.get_ticks()

        # Game over
        if player.nyawa <= 0:
            return "kalah", player

        # Menggambar
        gambar_latar(layar)

        for platform in platforms:
            gambar_platform(layar, platform)

        for coin in coins:
            gambar_koin(layar, coin)

        gambar_pintu(layar, pintu, pintu_terbuka)
        enemy.gambar(layar)
        player.gambar(layar)

        gambar_hud(
            layar,
            player,
            font,
            len(coins),
            data_skor["skor_tertinggi"]
        )

        gambar_teks(
            layar,
            f"Pemain: {nama}",
            font_kecil,
            PUTIH,
            15,
            TINGGI - 30
        )

        sekarang = pygame.time.get_ticks()

        if sekarang - waktu_pesan < 2200:
            gambar_teks(
                layar,
                pesan,
                font_kecil,
                HITAM,
                LEBAR // 2,
                85,
                posisi="tengah"
            )

        pygame.display.update()


# =========================================================
# PART 12 — PROGRAM UTAMA
# Materi: fungsi main, percabangan, alur aplikasi
# =========================================================

def main():
    pygame.init()

    layar = pygame.display.set_mode((LEBAR, TINGGI))
    pygame.display.set_caption(JUDUL_GAME)

    jam = pygame.time.Clock()

    font_besar = pygame.font.Font(None, 58)
    font = pygame.font.Font(None, 32)
    font_kecil = pygame.font.Font(None, 24)

    aplikasi_aktif = True

    while aplikasi_aktif:
        nama = menu_awal(
            layar,
            jam,
            font_besar,
            font,
            font_kecil
        )

        if nama is None:
            break

        bermain = True

        while bermain:
            hasil, player = jalankan_game(
                layar,
                jam,
                nama,
                font,
                font_kecil
            )

            if hasil == "keluar":
                aplikasi_aktif = False
                bermain = False

            elif hasil == "menu":
                bermain = False

            elif hasil in ("menang", "kalah"):
                pilihan = halaman_hasil(
                    layar,
                    jam,
                    hasil == "menang",
                    nama,
                    player,
                    font_besar,
                    font,
                    font_kecil
                )

                if pilihan == "ulang":
                    bermain = True

                elif pilihan == "menu":
                    bermain = False

                else:
                    aplikasi_aktif = False
                    bermain = False

    pygame.quit()


if __name__ == "__main__":
    main()