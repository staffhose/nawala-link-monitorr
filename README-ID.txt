PANDUAN PEMASANGAN NAWALA LINK MONITOR 24 JAM
================================================

ISI PAKET
- index.html                 Dashboard laporan
- links.txt                  Daftar website, satu URL per baris
- monitor.py                 Mesin pemeriksa link
- report.json                Dibuat otomatis setelah pemeriksaan pertama
- .github/workflows/check-links.yml  Jadwal otomatis harian
- requirements.txt           Dependensi Python

BAGIAN A — BUAT REPOSITORY GITHUB
1. Buka https://github.com lalu daftar / masuk.
2. Klik tombol "+" > New repository.
3. Isi nama: nawala-link-monitor
4. Pilih Public agar GitHub Pages gratis dapat menampilkan dashboard.
   Jangan masukkan link privat, kredensial, atau data rahasia ke repository publik.
5. Klik Create repository.
6. Ekstrak ZIP ini di komputer.
7. Upload semua ISI folder (termasuk folder .github) ke repository.
   Cara termudah: buka repository > Add file > Upload files, seret semua file.
   Pastikan folder .github/workflows/check-links.yml ikut terunggah.
8. Klik Commit changes.

BAGIAN B — MASUKKAN DAFTAR LINK
1. Di GitHub buka links.txt lalu klik ikon pensil (Edit).
2. Hapus example.com dan wikipedia jika tidak diperlukan.
3. Masukkan hingga 100 URL, satu URL per baris, contoh:
   https://domain-anda.com
   https://www.domain-lain.com
4. Klik Commit changes.
5. Jangan menaruh username, password, token, atau URL admin privat di sini.

BAGIAN C — AKTIFKAN DASHBOARD GITHUB PAGES
1. Buka repository > Settings > Pages.
2. Pada "Build and deployment", pilih "Deploy from a branch".
3. Branch: main; Folder: /(root); klik Save.
4. Tunggu beberapa menit. Alamat dashboard biasanya:
   https://USERNAME.github.io/nawala-link-monitor/
   Ganti USERNAME dengan username GitHub Anda.
5. File report.json akan muncul setelah pemeriksaan pertama berhasil.

BAGIAN D — AKTIFKAN PEMERIKSAAN OTOMATIS
1. Buka tab Actions di repository.
2. Jika diminta, klik "I understand my workflows, go ahead and enable them".
3. Pilih workflow "Check links every 24 hours".
4. Klik Run workflow untuk pemeriksaan pertama.
5. Buka run yang berjalan dan pastikan semua langkah hijau.
6. Selanjutnya workflow dijadwalkan setiap hari pukul 00:00 UTC (07:00 WIB).
   Jadwal GitHub Actions dapat terlambat beberapa menit saat antrean padat.
7. Untuk menjalankan kapan saja: Actions > Check links every 24 hours > Run workflow.

BAGIAN E — NOTIFIKASI TELEGRAM (OPSIONAL, DIREKOMENDASIKAN)
1. Di Telegram, cari akun resmi BotFather dan kirim /newbot.
2. Ikuti instruksi sampai BotFather memberi BOT TOKEN. Rahasiakan token tersebut.
3. Buka bot yang baru dibuat dan tekan Start.
4. Dapatkan CHAT ID:
   - Kirim satu pesan ke bot Anda.
   - Buka https://api.telegram.org/botTOKEN/getUpdates
   - Ganti TOKEN dengan token bot. Cari "chat":{"id":...}; angka id itu CHAT ID.
   - Jika hasil kosong, kirim pesan lagi ke bot lalu buka getUpdates kembali.
5. Di GitHub repository buka Settings > Secrets and variables > Actions.
6. Klik New repository secret:
   Name: TELEGRAM_BOT_TOKEN
   Secret: token dari BotFather
7. Buat secret kedua:
   Name: TELEGRAM_CHAT_ID
   Secret: angka chat ID Anda
8. Jalankan workflow manual sekali lagi untuk tes.
9. Telegram mengirim pesan saat ada status indikasi pemblokiran atau gangguan.

CARA MEMBACA STATUS
- Dapat diakses: server memberi respons HTTP sukses/redirect.
- Indikasi blokir: ada teks pemblokiran yang dikenali atau HTTP 401/403/407/451.
- Tidak dapat diakses: timeout, DNS/koneksi gagal, atau HTTP error lain.
- Gagal diperiksa: URL tidak valid atau kesalahan lain.

BATASAN PENTING
- Ini pemeriksaan ketersediaan HTTP dari server GitHub, bukan pengujian dari semua ISP/lokasi.
- Sistem tidak terhubung ke daftar resmi Nawala/Komdigi dan tidak dapat memastikan status blokir resmi.
- Kata "nawala", "Kominfo", dan istilah sejenis di halaman biasa dapat menimbulkan false positive.
  Periksa URL hasil secara manual sebelum menyimpulkan pemblokiran.
- Website yang memerlukan login, JavaScript berat, CAPTCHA, atau perlindungan anti-bot
  bisa gagal diperiksa walaupun sebenarnya aktif.
- GitHub Actions menyediakan kuota penggunaan; jadwal dapat terlambat.
- Jangan memasukkan situs yang tidak Anda miliki/kelola jika pemeriksaan tidak diizinkan.

TROUBLESHOOTING
- Dashboard kosong: jalankan workflow manual dan pastikan report.json berhasil dibuat.
- Workflow tidak muncul: pastikan file berada tepat di .github/workflows/check-links.yml.
- Pages 404: periksa Settings > Pages, branch main, folder /(root), dan tunggu beberapa menit.
- Telegram tidak masuk: periksa token/chat ID, tekan Start pada bot, lalu jalankan workflow manual.
- Link salah: pastikan setiap URL satu baris dan diawali https:// atau http://.
