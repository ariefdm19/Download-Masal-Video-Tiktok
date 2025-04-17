# TikTok Video Downloader - Batch (GUI)

Aplikasi desktop untuk mengunduh banyak video TikTok sekaligus (batch) dengan tampilan antarmuka grafis (GUI) berbasis Python.

## Fitur
- Unduh banyak video TikTok sekaligus (batch download)
- Tempel URL langsung dari clipboard
- Pilih lokasi penyimpanan file hasil unduhan
- Progress bar untuk total dan per video
- Log status unduhan
- Validasi otomatis URL TikTok

## Persyaratan
- Python 3.8+
- Paket Python: `customtkinter`, `tkinter`, `yt-dlp`

## Instalasi
1. Clone atau download source code ini.
2. Install dependencies dengan perintah:
   ```
   pip install customtkinter yt-dlp
   ```

## Cara Menggunakan
1. Jalankan aplikasi dengan klik dua kali file berikut:
   ```
   jalankan_tiktok_downloader.bat
   ```
   Atau, jalankan manual dengan perintah:
   ```
   python tiktok_downloader.py
   ```
2. Masukkan satu atau beberapa URL video TikTok (satu URL per baris).
3. Pilih lokasi penyimpanan file hasil unduhan.
4. Klik "Mulai Download".
5. Lihat progress dan log unduhan di aplikasi.

## Catatan
- Hanya mendukung URL video TikTok, bukan playlist.
- Jika ada error, cek log pada aplikasi.

---

Aplikasi dibuat oleh [Arief Dwi Muhidin](https://www.19adm.com/)
