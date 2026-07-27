# Python Adventure — Versi Per Part

Dokumen ini digunakan sebagai pendamping pembelajaran bertahap. Setiap part menambahkan satu konsep baru ke proyek **Platform Game sederhana dengan Pygame**.

## Persiapan

Instal Pygame melalui terminal VS Code:

```bash
pip install pygame
```

Buat folder proyek:

```text
python-adventure/
└── main.py
```

Setiap part menggunakan file `main.py`. Kode pada part baru menggantikan atau mengembangkan kode pada part sebelumnya.

---

# Part 1 — Membuka Jendela Pygame

## Materi

- Import library
- Inisialisasi Pygame
- Variabel ukuran layar
- Game loop
- Event `QUIT`

## Tujuan

Siswa dapat membuka jendela game dan menutupnya dengan benar.

## Kode

```python
import pygame

pygame.init()

LEBAR = 900
TINGGI = 550

layar = pygame.display.set_mode((LEBAR, TINGGI))
pygame.display.set_caption("Python Adventure")

jam = pygame.time.Clock()
game_aktif = True

while game_aktif:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_aktif = False

    layar.fill((30, 40, 70))

    pygame.display.update()
    jam.tick(60)

pygame.quit()
```

## Keterangan

- `pygame.init()` mengaktifkan modul-modul Pygame.
- `pygame.display.set_mode()` membuat layar game.
- `while game_aktif` menjaga game terus berjalan.
- `pygame.QUIT` mendeteksi saat tombol tutup ditekan.
- `jam.tick(60)` membatasi game pada 60 FPS.

## Challenge

Ubah judul game dan warna latar.

---

# Part 2 — Variabel dan Karakter Pemain

## Materi

- Variabel
- Integer
- Boolean
- Warna RGB
- Menggambar bentuk

## Tujuan

Siswa dapat membuat karakter pemain menggunakan persegi sederhana.

## Kode

```python
import pygame

pygame.init()

LEBAR = 900
TINGGI = 550
FPS = 60

BIRU_LANGIT = (90, 180, 240)
HIJAU = (80, 190, 100)
BIRU = (50, 110, 240)
PUTIH = (245, 245, 245)

layar = pygame.display.set_mode((LEBAR, TINGGI))
pygame.display.set_caption("Python Adventure")
jam = pygame.time.Clock()

player_x = 80
player_y = 440
player_lebar = 42
player_tinggi = 52

skor = 0
nyawa = 3
game_aktif = True

while game_aktif:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_aktif = False

    layar.fill(BIRU_LANGIT)

    pygame.draw.rect(
        layar,
        HIJAU,
        (0, 500, LEBAR, 50)
    )

    pygame.draw.rect(
        layar,
        BIRU,
        (player_x, player_y, player_lebar, player_tinggi),
        border_radius=8
    )

    pygame.draw.circle(
        layar,
        PUTIH,
        (player_x + 13, player_y + 16),
        4
    )

    pygame.draw.circle(
        layar,
        PUTIH,
        (player_x + 29, player_y + 16),
        4
    )

    pygame.display.update()
    jam.tick(FPS)

pygame.quit()
```

## Keterangan

- Posisi pemain disimpan dalam `player_x` dan `player_y`.
- Ukuran pemain disimpan dalam `player_lebar` dan `player_tinggi`.
- `pygame.draw.rect()` menggambar badan pemain.
- `pygame.draw.circle()` menggambar mata pemain.

## Challenge

Tambahkan mulut atau aksesori pada pemain.

---

# Part 3 — Gerak Kiri dan Kanan

## Materi

- Input keyboard
- Percabangan `if`
- Operator penjumlahan dan pengurangan
- Batas layar

## Tujuan

Siswa dapat menggerakkan pemain ke kiri dan kanan.

## Tambahkan sebelum game loop

```python
kecepatan = 6
```

## Tambahkan di dalam game loop

Letakkan setelah bagian event:

```python
tombol = pygame.key.get_pressed()

if tombol[pygame.K_LEFT] or tombol[pygame.K_a]:
    player_x -= kecepatan

if tombol[pygame.K_RIGHT] or tombol[pygame.K_d]:
    player_x += kecepatan

if player_x < 0:
    player_x = 0

if player_x + player_lebar > LEBAR:
    player_x = LEBAR - player_lebar
```

## Keterangan

- `pygame.key.get_pressed()` membaca tombol yang sedang ditekan.
- `player_x -= kecepatan` memindahkan pemain ke kiri.
- `player_x += kecepatan` memindahkan pemain ke kanan.
- Kondisi batas mencegah pemain keluar layar.

## Challenge

Ubah kecepatan pemain menjadi lebih cepat atau lebih lambat.

---

# Part 4 — Lompat dan Gravitasi

## Materi

- Float
- Boolean
- Percabangan
- Simulasi gravitasi

## Tujuan

Siswa dapat membuat karakter melompat dan kembali ke tanah.

## Tambahkan sebelum game loop

```python
kecepatan_y = 0
gravitasi = 0.8
kekuatan_lompat = -15
di_tanah = True
```

## Tambahkan di dalam game loop

```python
if tombol[pygame.K_SPACE] and di_tanah:
    kecepatan_y = kekuatan_lompat
    di_tanah = False

kecepatan_y += gravitasi
player_y += kecepatan_y

lantai_y = 500

if player_y + player_tinggi >= lantai_y:
    player_y = lantai_y - player_tinggi
    kecepatan_y = 0
    di_tanah = True
```

## Keterangan

- Nilai negatif membuat pemain bergerak ke atas.
- Gravitasi terus menambah `kecepatan_y` sehingga pemain turun.
- `di_tanah` mencegah pemain melompat berkali-kali di udara.

## Challenge

Buat lompatan lebih tinggi atau lebih rendah.

---

# Part 5 — Fungsi

## Materi

- Fungsi
- Parameter
- Pemanggilan fungsi
- Modularisasi

## Tujuan

Siswa dapat memecah program menjadi fungsi-fungsi sederhana.

## Kode fungsi

Tambahkan sebelum game loop:

```python
def gambar_latar(layar):
    layar.fill((90, 180, 240))

    pygame.draw.circle(
        layar,
        (255, 230, 90),
        (760, 90),
        45
    )


def gambar_player(layar, x, y, lebar, tinggi):
    pygame.draw.rect(
        layar,
        (50, 110, 240),
        (x, y, lebar, tinggi),
        border_radius=8
    )

    pygame.draw.circle(layar, (255, 255, 255), (x + 13, y + 16), 4)
    pygame.draw.circle(layar, (255, 255, 255), (x + 29, y + 16), 4)


def gambar_platform(layar, platform):
    pygame.draw.rect(
        layar,
        (70, 170, 90),
        platform,
        border_radius=5
    )
```

## Gunakan dalam game loop

```python
gambar_latar(layar)

gambar_platform(
    layar,
    pygame.Rect(0, 500, LEBAR, 50)
)

gambar_player(
    layar,
    player_x,
    player_y,
    player_lebar,
    player_tinggi
)
```

## Keterangan

- Fungsi membuat program lebih teratur.
- Parameter membuat satu fungsi dapat dipakai untuk berbagai posisi atau ukuran.
- Nama fungsi sebaiknya menjelaskan tugasnya.

## Challenge

Buat fungsi `gambar_awan()`.

---

# Part 6 — List Platform dan Collision

## Materi

- List
- Perulangan `for`
- Object `pygame.Rect`
- Collision detection

## Tujuan

Siswa dapat membuat banyak platform dan membuat pemain berdiri di atasnya.

## Tambahkan sebelum game loop

```python
platforms = [
    pygame.Rect(0, 500, 900, 50),
    pygame.Rect(150, 410, 180, 20),
    pygame.Rect(400, 330, 180, 20),
    pygame.Rect(650, 250, 160, 20)
]
```

## Buat Rect pemain

Di dalam game loop setelah posisi diperbarui:

```python
player_rect = pygame.Rect(
    int(player_x),
    int(player_y),
    player_lebar,
    player_tinggi
)
```

## Collision platform

```python
di_tanah = False

for platform in platforms:
    if player_rect.colliderect(platform):
        if kecepatan_y > 0:
            jarak_sebelumnya = (
                player_rect.bottom - int(kecepatan_y)
            )

            if jarak_sebelumnya <= platform.top + 10:
                player_y = platform.top - player_tinggi
                kecepatan_y = 0
                di_tanah = True
                player_rect.y = int(player_y)
```

## Menggambar semua platform

```python
for platform in platforms:
    gambar_platform(layar, platform)
```

## Keterangan

- `platforms` menyimpan banyak objek `Rect`.
- `for` digunakan untuk memproses semua platform.
- `colliderect()` memeriksa tabrakan dua persegi.
- Pemeriksaan arah jatuh mencegah pemain menempel dari bawah.

## Challenge

Tambahkan satu platform baru.

---

# Part 7 — Koin dan Skor

## Materi

- List
- Dictionary sederhana
- Perulangan
- Menghapus data
- Operator skor

## Tujuan

Siswa dapat membuat koin yang dapat dikumpulkan.

## Tambahkan sebelum game loop

```python
coins = [
    pygame.Rect(220, 370, 24, 24),
    pygame.Rect(480, 290, 24, 24),
    pygame.Rect(710, 210, 24, 24)
]
```

## Collision koin

Tambahkan di dalam game loop:

```python
for coin in coins[:]:
    if player_rect.colliderect(coin):
        coins.remove(coin)
        skor += 10
```

## Menggambar koin

```python
for coin in coins:
    pygame.draw.circle(
        layar,
        (255, 210, 40),
        coin.center,
        12
    )
```

## Menampilkan skor

Tambahkan sebelum game loop:

```python
font = pygame.font.Font(None, 34)
```

Tambahkan fungsi:

```python
def gambar_teks(layar, teks, font, warna, x, y):
    gambar = font.render(teks, True, warna)
    layar.blit(gambar, (x, y))
```

Gunakan di game loop:

```python
gambar_teks(
    layar,
    f"Skor: {skor}",
    font,
    (255, 255, 255),
    20,
    20
)
```

## Keterangan

- `coins[:]` membuat salinan list agar aman saat item dihapus.
- `coins.remove(coin)` menghilangkan koin yang sudah diambil.
- Setiap koin menambah skor sebesar 10.

## Challenge

Tambahkan koin bonus bernilai 30.

---

# Part 8 — Class Player

## Materi

- Class
- Object
- Constructor
- Attribute
- Method

## Tujuan

Siswa dapat mengubah data dan perilaku pemain menjadi object.

## Kode class

```python
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

    def gambar(self, layar):
        pygame.draw.rect(
            layar,
            (50, 110, 240),
            self.rect,
            border_radius=8
        )

        pygame.draw.circle(
            layar,
            (255, 255, 255),
            (self.rect.x + 13, self.rect.y + 16),
            4
        )

        pygame.draw.circle(
            layar,
            (255, 255, 255),
            (self.rect.x + 29, self.rect.y + 16),
            4
        )
```

## Membuat object

```python
player = Player(80, 440)
```

## Menggunakannya

```python
gerak_x = player.baca_input()
gerak_y = player.terapkan_gravitasi()

player.rect.x += gerak_x
player.rect.y += gerak_y
```

## Keterangan

- `self` menunjuk pada object pemain yang sedang digunakan.
- Attribute menyimpan data pemain.
- Method menyimpan aksi pemain.
- Class membuat kode lebih mudah dikembangkan.

## Challenge

Tambahkan attribute `warna` pada class Player.

---

# Part 9 — Musuh dan Nyawa

## Materi

- Class tambahan
- Gerakan otomatis
- Percabangan arah
- Collision
- Nyawa

## Tujuan

Siswa dapat membuat musuh bergerak dan mengurangi nyawa pemain.

## Class Enemy

```python
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
            self.arah = 1

        if self.rect.right >= self.batas_kanan:
            self.arah = -1

    def gambar(self, layar):
        pygame.draw.rect(
            layar,
            (220, 70, 70),
            self.rect,
            border_radius=8
        )
```

## Membuat object musuh

```python
enemy = Enemy(430, 292, 400, 580)
```

## Update dan gambar

```python
enemy.update()
enemy.gambar(layar)
```

## Collision dengan pemain

```python
if player.rect.colliderect(enemy.rect):
    player.nyawa -= 1
    player.rect.x = 80
    player.rect.y = 440
```

## Keterangan

- Musuh bergerak bolak-balik di area tertentu.
- Ketika menyentuh musuh, nyawa pemain berkurang.
- Posisi pemain dikembalikan ke titik awal.

## Challenge

Buat musuh bergerak lebih cepat.

---

# Part 10 — Pintu Keluar dan Kondisi Menang

## Materi

- Percabangan
- Boolean
- Kondisi gabungan
- Tampilan status

## Tujuan

Siswa dapat menyelesaikan level setelah semua koin terkumpul.

## Tambahkan sebelum game loop

```python
pintu = pygame.Rect(800, 180, 55, 70)
menang = False
```

## Menggambar pintu

```python
warna_pintu = (80, 200, 120) if len(coins) == 0 else (120, 120, 130)

pygame.draw.rect(
    layar,
    warna_pintu,
    pintu,
    border_radius=6
)
```

## Kondisi menang

```python
if player.rect.colliderect(pintu):
    if len(coins) == 0:
        menang = True
        game_aktif = False
```

## Keterangan

- Pintu berwarna abu-abu ketika terkunci.
- Pintu berubah hijau setelah semua koin diambil.
- Pemain hanya menang jika menyentuh pintu saat koin sudah habis.

## Challenge

Tampilkan pesan “Ambil semua koin!” saat pintu masih terkunci.

---

# Part 11 — File JSON dan Skor Tertinggi

## Materi

- Import library
- File
- JSON
- Try-except
- Dictionary

## Tujuan

Siswa dapat menyimpan skor tertinggi ke file.

## Tambahkan import

```python
import json
import os
```

## Fungsi membaca skor

```python
def baca_skor_tertinggi():
    if not os.path.exists("skor.json"):
        return 0

    try:
        with open("skor.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            return data.get("skor_tertinggi", 0)

    except (OSError, json.JSONDecodeError):
        return 0
```

## Fungsi menyimpan skor

```python
def simpan_skor_tertinggi(skor):
    skor_lama = baca_skor_tertinggi()

    if skor > skor_lama:
        data = {
            "skor_tertinggi": skor
        }

        with open("skor.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
```

## Keterangan

- JSON menyimpan data dalam bentuk pasangan key dan value.
- `try-except` mencegah game berhenti jika file rusak.
- Skor hanya ditulis jika lebih tinggi dari skor sebelumnya.

## Challenge

Simpan juga nama pemain.

---

# Part 12 — Debugging, Testing, dan Dokumentasi

## Materi

- Testing
- Debugging
- Dokumentasi
- Refleksi proyek

## Pengujian

| Bagian | Pengujian | Hasil yang diharapkan |
|---|---|---|
| Jendela | Klik tombol tutup | Program berhenti dengan benar |
| Gerakan | Tahan tombol kiri | Pemain bergerak ke kiri |
| Batas | Bergerak ke ujung layar | Pemain tidak keluar layar |
| Lompat | Tekan Space | Pemain melompat satu kali |
| Platform | Jatuh ke platform | Pemain berdiri di atas platform |
| Koin | Menyentuh koin | Koin hilang dan skor bertambah |
| Musuh | Menyentuh musuh | Nyawa berkurang |
| Pintu | Masuk sebelum semua koin diambil | Level belum selesai |
| Menang | Ambil semua koin lalu masuk pintu | Muncul layar menang |
| File | Hapus `skor.json` | Game tetap berjalan |

## Struktur akhir proyek

```text
python-adventure/
├── main.py
├── skor.json
└── README.md
```

## Refleksi siswa

1. Fitur apa yang paling sulit dibuat?
2. Bug apa yang ditemukan?
3. Bagaimana cara memperbaikinya?
4. Materi Python apa yang paling sering digunakan?
5. Fitur apa yang ingin ditambahkan selanjutnya?

---

# Ringkasan Perkembangan

| Part | Materi | Hasil proyek |
|---:|---|---|
| 1 | Import dan game loop | Jendela game |
| 2 | Variabel | Karakter pemain |
| 3 | Percabangan | Gerak kiri-kanan |
| 4 | Boolean dan operator | Lompat dan gravitasi |
| 5 | Fungsi | Kode lebih teratur |
| 6 | List dan loop | Banyak platform |
| 7 | Struktur data | Koin dan skor |
| 8 | OOP | Class Player |
| 9 | OOP dan collision | Musuh dan nyawa |
| 10 | Kondisi | Pintu dan kemenangan |
| 11 | File JSON | Skor tertinggi |
| 12 | Debugging | Pengujian dan dokumentasi |
