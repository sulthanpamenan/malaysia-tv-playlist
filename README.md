# 📺 Malaysia TV & Radio IPTV Proxy

A lightweight, automated HLS/M3U8 proxy generator for **Malaysia TV & Radio** live streams. Designed for seamless integration with IPTV players such as **OTT Navigator**, **TiviMate**, and **IPTV Smarters**.

---

## 🚀 Quick Start / URLs

Directly import these URLs into your preferred IPTV client:

| Resource | URL |
| :--- | :--- |
| **Playlist (M3U)** | `http://<your-server-ip>:5001/playlist.m3u` *(atau gunakan URL deployment publik Anda)* |

---

## 💻 Menjalankan Server Sendiri di Lokal (`proxy.py`)

Jika Anda ingin menghosting dan menjalankan server proxy sendiri secara lokal menggunakan skrip yang tersedia, ikuti langkah-langkah berikut:

1. Pastikan Anda telah menginstal Python di komputer lokal Anda.
2. Instal dependensi yang diperlukan dengan menjalankan perintah berikut di terminal:
   pip install flask requests
3. Atur environment variable yang dibutuhkan (seperti `GITHUB_TOKEN` dan `GIST_ID` jika diperlukan) atau biarkan menggunakan konfigurasi default.
4. Jalankan skrip server lokal:
   python proxy.py
5. Server akan aktif dan dapat diakses pada port `5001` (`http://localhost:5001/playlist.m3u`).

---

## 🛠️ Fitur & Keunggulan

- **Automated Token Handling**: Pengambilan tautan streaming dinamis secara otomatis dari penyimpanan Gist.
- **Dynamic Proxy**: Mendukung *proxying* segmen aliran video HLS secara real-time.
- **Multi-Category Support**: Menyediakan berbagai kategori siaran TV dan Radio Malaysia secara terpusat.
- **High Compatibility**: Kompatibel dengan berbagai aplikasi pemutar IPTV populer di Android TV, seluler, maupun desktop.

---

## 📱 Cara Menggunakan di Pemutar IPTV

1. Buka aplikasi Pemutar IPTV pilihan Anda (misalnya **OTT Navigator** atau **TiviMate**).
2. Tambahkan sumber playlist baru menggunakan **URL Playlist M3U** Anda.
3. Segarkan/muat ulang playlist, lalu nikmati siaran langsungnya!

---

## ⚠️ Penafian (Disclaimer)

Repositori ini dan layanan proxy otomatisnya disediakan secara ketat untuk tujuan edukasi, pribadi, dan non-komersial.

- **Kepemilikan Konten:** Semua aliran video, nama saluran, logo, serta hak kekayaan intelektual sepenuhnya adalah milik dari pemegang hak cipta masing-masing.
- **Tanpa Penyimpanan (No Hosting):** Layanan ini tidak menyimpan atau menyiarkan ulang file media secara ilegal, melainkan bertindak murni sebagai pengurai dinamis dan *reverse-proxy* untuk tautan publik.
- **Ketersediaan Layanan:** Pengembang tidak memberikan garansi apa pun terkait waktu aktif (*uptime*) aliran, kualitas video, atau kelancaran pemutaran, karena performa bergantung sepenuhnya pada ketersediaan sumber pihak ketiga.

---

## 📄 Lisensi

Didistribusikan di bawah Lisensi MIT. Lihat file `LICENSE` untuk informasi lebih lanjut.

---

## ☕ Dukung Pengembang

Jika proyek ini bermanfaat bagi Anda, pertimbangkan untuk mendukung pengembang agar layanan ini tetap aktif dan terpelihara!

<div align="center">

### 🇮🇩 Donasi Lokal (QRIS / E-Wallet / Mobile Banking)

<a href="[https://saweria.co/sulthanpamenan](https://saweria.co/sulthanpamenan)" target="_blank">
  <img width="290" height="290" alt="Saweria" src="[https://github.com/user-attachments/assets/f2846d1f-a391-4daf-9ce5-a48aadc992a0](https://github.com/user-attachments/assets/f2846d1f-a391-4daf-9ce5-a48aadc992a0)" />
</a>

<br>

*Pindai kode QRIS di atas menggunakan GoPay, DANA, OVO, ShopeePay, LinkAja, atau Mobile Banking.*

<br>

<a href="[https://saweria.co/sulthanpamenan](https://saweria.co/sulthanpamenan)" target="_blank">
  <img src="[https://img.shields.io/badge/Saweria-Support_Project-orange?style=for-the-badge&logo=coffee](https://img.shields.io/badge/Saweria-Support_Project-orange?style=for-the-badge&logo=coffee)" alt="Support via Saweria">
</a>

---

### 🌐 Donasi Internasional

<a href="[https://buymeacoffee.com/sulthanpamenan](https://buymeacoffee.com/sulthanpamenan)" target="_blank">
  <img src="[https://img.shields.io/badge/Buy_Me_A_Coffee-Donate-yellow?style=for-the-badge&logo=buy-me-a-coffee](https://img.shields.io/badge/Buy_Me_A_Coffee-Donate-yellow?style=for-the-badge&logo=buy-me-a-coffee)" alt="Buy Me A Coffee">
</a>

</div>
