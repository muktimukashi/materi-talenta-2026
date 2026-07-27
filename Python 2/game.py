import random
from datetime import datetime


class Player:
    def __init__(self, nama, karakter):
        self.nama = nama
        self.karakter = karakter
        self.nyawa = 100
        self.skor = 0
        self.level = 1
        self.inventaris = ["Potion"]

    def tampilkan_status(self):
        print("\n=== STATUS PEMAIN ===")
        print("Nama       :", self.nama)
        print("Karakter   :", self.karakter)
        print("Nyawa      :", self.nyawa)
        print("Skor       :", self.skor)
        print("Level      :", self.level)
        print("Inventaris :", self.inventaris)

    def tambah_skor(self, jumlah):
        self.skor += jumlah

        if self.skor >= self.level * 100:
            self.level += 1
            self.nyawa += 20

            print(
                "Selamat! Kamu naik ke level",
                self.level
            )


def pilih_karakter():
    daftar_karakter = (
        "Warrior",
        "Mage",
        "Healer"
    )

    print("\nPilih karakter:")

    for nomor, karakter in enumerate(
        daftar_karakter,
        start=1
    ):
        print(f"{nomor}. {karakter}")

    pilihan = input("Masukkan pilihan: ")

    if pilihan in ["1", "2", "3"]:
        return daftar_karakter[int(pilihan) - 1]

    return "Petualang"


def kuis_python(player):
    soal = [
        {
            "pertanyaan":
                "Tipe data untuk teks adalah?",
            "jawaban": "string"
        },
        {
            "pertanyaan":
                "Perintah percabangan Python?",
            "jawaban": "if"
        },
        {
            "pertanyaan":
                "Fungsi menerima input pengguna?",
            "jawaban": "input"
        }
    ]

    soal_terpilih = random.choice(soal)

    print("\n=== KUIS PYTHON ===")
    print(soal_terpilih["pertanyaan"])

    jawaban = input("Jawaban: ").lower().strip()

    if jawaban == soal_terpilih["jawaban"]:
        print("Jawaban benar!")
        player.tambah_skor(30)

    else:
        print("Jawaban belum tepat.")
        player.nyawa -= 10


def lawan_musuh(player):
    nama_musuh = random.choice([
        "Bug Monster",
        "Syntax Dragon",
        "Error Goblin"
    ])

    nyawa_musuh = random.randint(30, 60)

    print("\nKamu bertemu", nama_musuh)

    while nyawa_musuh > 0 and player.nyawa > 0:
        print("\nNyawa pemain:", player.nyawa)
        print("Nyawa musuh :", nyawa_musuh)

        print("\n1. Serang")
        print("2. Gunakan potion")
        print("3. Kabur")

        pilihan = input("Pilih tindakan: ")

        if pilihan == "1":
            serangan = random.randint(10, 25)
            serangan_musuh = random.randint(5, 15)

            nyawa_musuh -= serangan
            player.nyawa -= serangan_musuh

            print("Seranganmu:", serangan)
            print("Serangan musuh:", serangan_musuh)

        elif pilihan == "2":
            if "Potion" in player.inventaris:
                player.nyawa += 30
                player.inventaris.remove("Potion")

                print("Nyawamu bertambah 30.")
            else:
                print("Potion sudah habis.")

        elif pilihan == "3":
            print("Kamu berhasil kabur.")
            return

        else:
            print("Pilihan tidak tersedia.")

    if nyawa_musuh <= 0:
        print("Musuh berhasil dikalahkan!")

        player.tambah_skor(50)
        player.inventaris.append("Koin Emas")


def jelajah(player):
    lokasi = random.choice([
        "Hutan Variabel",
        "Gua Percabangan",
        "Menara Perulangan"
    ])

    print("\nKamu memasuki", lokasi)

    kejadian = random.choice([
        "kuis",
        "musuh"
    ])

    if kejadian == "kuis":
        kuis_python(player)
    else:
        lawan_musuh(player)


def simpan_hasil(player):
    waktu = datetime.now().strftime(
        "%d-%m-%Y %H:%M"
    )

    with open(
        "hasil_permainan.txt",
        "a",
        encoding="utf-8"
    ) as file:
        file.write(
            f"{waktu} | "
            f"{player.nama} | "
            f"{player.karakter} | "
            f"Level {player.level} | "
            f"Skor {player.skor}\n"
        )

    print("Hasil permainan berhasil disimpan.")


def baca_hasil():
    print("\n=== RIWAYAT PERMAINAN ===")

    try:
        with open(
            "hasil_permainan.txt",
            "r",
            encoding="utf-8"
        ) as file:
            isi = file.read()

            if isi:
                print(isi)
            else:
                print("Riwayat masih kosong.")

    except FileNotFoundError:
        print("Belum ada riwayat permainan.")


def main():
    print("=" * 35)
    print("         PYTHON QUEST")
    print("=" * 35)

    nama = input("Masukkan nama pemain: ").strip()

    if nama == "":
        nama = "Pemain"

    karakter = pilih_karakter()
    player = Player(nama, karakter)

    game_aktif = True

    while game_aktif and player.nyawa > 0:
        print("\n=== MENU UTAMA ===")
        print("1. Jelajah")
        print("2. Lihat status")
        print("3. Lihat riwayat")
        print("4. Simpan dan keluar")

        menu = input("Pilih menu: ")

        if menu == "1":
            jelajah(player)

        elif menu == "2":
            player.tampilkan_status()

        elif menu == "3":
            baca_hasil()

        elif menu == "4":
            simpan_hasil(player)
            game_aktif = False

        else:
            print("Menu tidak tersedia.")

    if player.nyawa <= 0:
        print("\nGAME OVER")
        simpan_hasil(player)

    print(
        "\nTerima kasih sudah bermain,",
        player.nama
    )


if __name__ == "__main__":
    main()