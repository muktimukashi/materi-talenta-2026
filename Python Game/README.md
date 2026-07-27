# Python Adventure — versi browser (tetap Python/Pygame)

Proyek ini memakai **Pygbag** agar kode Python + Pygame dapat berjalan di browser melalui WebAssembly.

## Menjalankan dan menguji

1. Pastikan Python sudah terpasang.
2. Buka terminal pada folder yang berisi folder `python_adventure_web`.
3. Instal Pygbag:

```bash
python -m pip install pygbag
```

4. Jalankan:

```bash
python -m pygbag python_adventure_web
```

5. Buka alamat localhost yang ditampilkan oleh terminal.

## Membuat file untuk diunggah

Setelah proses build, hasil web biasanya tersedia di folder:

```text
python_adventure_web/build/web/
```

Isi folder tersebut dapat dipublikasikan melalui GitHub Pages atau layanan hosting statis lain yang mendukung HTTPS.

## Perubahan dari kode asli

- Tetap menggunakan Python dan Pygame.
- Menambahkan `asyncio`.
- Game loop dibuat asynchronous.
- Menambahkan `await asyncio.sleep(0)` agar browser tetap dapat memperbarui canvas dan menerima input.
- Nama berkas utama dibuat `main.py`, sesuai struktur proyek Pygbag.

## Catatan skor

`skor.json` tetap dipertahankan sebagai materi pembelajaran file JSON. Pada browser, penyimpanan berkas virtual mungkin tidak bertahan permanen setelah halaman atau cache browser dibersihkan. Untuk leaderboard bersama antarpemain diperlukan server/database terpisah.
