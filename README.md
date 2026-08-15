# 🇲🇾 Malaysia TV Net IPTV Playlist Auto-Generator

Repositori ini secara otomatis mengikis (*scrape*), me-parse, dan menyegarkan token CDN dinamis dari saluran televisi yang tersedia di `malaysia-tv.net`. Hasilnya disajikan dalam bentuk playlist format `.m3u` dan `.txt` yang siap dipasang pada berbagai aplikasi IPTV player (TiviMate, OTT Navigator, VLC, PlayerX, dll.).

---

## 🔗 Tautan Playlist M3U

Gunakan salah satu tautan di bawah ini untuk dimasukkan ke dalam aplikasi IPTV Player kamu:

* **M3U Playlist (Standar IPTV Player)**:
  `https://raw.githubusercontent.com/sulthanpamenan/malaysia-tv-playlist/main/playlist.m3u`

* **Plain Text Playlist**:
  `https://raw.githubusercontent.com/sulthanpamenan/malaysia-tv-playlist/main/playlist.txt`

---

## ⚡ Fitur Utama

* **Otomatis 24/7**: Diperbarui setiap **3 jam sekali** menggunakan GitHub Actions untuk memastikan token BunnyCDN (`expires` & `token`) tidak kedaluwarsa.
* **Bebas VPN**: Seluruh saluran yang diekstrak dalam playlist ini dapat diputar langsung dari IP Indonesia / Internasional tanpa memerlukan VPN.
* **Metadata Lengkap**: Dilengkapi atribut `tvg-id`, `tvg-name`, `tvg-logo`, dan `group-title` (Kategori) resmi untuk integrasi EPG yang rapi.
* **Self-Healing Grid Scraper**: Menggunakan Playwright untuk me-scan seluruh grid situs secara dinamis. Jika ada saluran baru yang ditambahkan di web sumber, saluran tersebut akan otomatis terdeteksi.

---

## 📺 Kategori Saluran (Group Titles)

Daftar saluran dalam playlist ini dikelompokkan ke dalam kategori resmi sebagai berikut:

| Kategori | Deskripsi | Contoh Channel |
| :--- | :--- | :--- |
| **General** | Siaran umum/multigenre | TV3 |
| **News** | Berita & Informasi | Astro Awani, Al Jazeera, Scripps News, NBC News NOW |
| **Sports** | Olahraga & Live Match | beIN Sports, Eurosport, WWE Network, AFL TV, Bola Sepak |
| **Movies** | Film Layar Lebar | Bollywood Prime, Pitaara TV, Miramax Movie Channel |
| **Entertainment** | Hiburan & Variety Show | Shemaroo Bollywood, FilmRise, TV One, Nosey |
| **Documentary** | Pengetahuan & Alam | BBC Earth, The Unexplained Zone |
| **Lifestyle** | Gaya Hidup & Travel | GoUSA TV |
| **Music** | Video Musik | Shemaroo Songs, Mastiii |
| **Series** | Serial Drama TV | Shemaroo Umang, ION Television |

---

## ⚙️ Cara Kerja Sistem

1. **GitHub Actions Workflow** berjalan otomatis setiap 3 jam.
2. **Playwright (Headless Chromium)** membuka situs sumber, me-scroll seluruh grid tampilan, dan menembak halaman siaran.
3. Skrip menangkap permintaan jaringan (*network intercept*) yang berisi URL manifest `.m3u8` beserta token akses aktif.
4. Skrip melakukan pencocokan metadata dengan database lokal dan menyusun ulang file `playlist.m3u`.
5. Hasil pembaruan otomatis di-*commit* dan di-*push* kembali ke repositori ini.

---

## ⚠️ Penolakan Tanggung Jawab (Disclaimer)

Repositori ini tidak menyimpan, meng-host, atau menyiarkan konten media apa pun secara langsung. Seluruh tautan siaran diekstrak secara otomatis dari domain publik penyedia siaran. Proyek ini dibuat murni untuk tujuan pendidikan dan otomatisasi pribadi.
