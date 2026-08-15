# 🇲🇾 Malaysia TV Net IPTV Playlist Auto-Generator

This repository automatically scrapes, parses, and refreshes dynamic CDN tokens from television channels available on `malaysia-tv.net`. The output is generated as `.m3u` and `.txt` playlists, ready to be added to various IPTV player applications (such as TiviMate, OTT Navigator, VLC, PlayerX, etc.).

---

## 🔗 M3U Playlist Links

Use either of the links below to import into your IPTV player:

* **M3U Playlist (Standard IPTV Player)**:
  `https://sulthanpamenan.github.io/malaysia-tv-playlist/playlist.m3u`

* **Plain Text Playlist**:
  `https://sulthanpamenan.github.io/malaysia-tv-playlist/playlist.txt`

---

## ⚡ Key Features

* **Automated 24/7**: Updated every **3 hours** via GitHub Actions to ensure BunnyCDN tokens (`expires` & `token`) never expire.
* **VPN Free**: All extracted channel streams in this playlist can be played directly from Indonesian / International IPs without requiring a VPN.
* **Complete Metadata**: Includes official `tvg-id`, `tvg-name`, `tvg-logo`, and `group-title` (Category) attributes for clean EPG integration.
* **Self-Healing Grid Scraper**: Uses Playwright to dynamically scan the entire source site grid. If new channels are added to the source website, they will automatically be detected and included.

---

## 📺 Channel Categories (Group Titles)

Channels in this playlist are categorized into official groups as follows:

| Category | Description | Example Channels |
| :--- | :--- | :--- |
| **General** | General / Multi-genre broadcasting | TV3 |
| **News** | News & Information | Astro Awani, Al Jazeera, Scripps News, NBC News NOW |
| **Sports** | Sports & Live Matches | beIN Sports, Eurosport, WWE Network, AFL TV, Bola Sepak |
| **Movies** | Feature Films | Bollywood Prime, Pitaara TV, Miramax Movie Channel |
| **Entertainment** | Entertainment & Variety Shows | Shemaroo Bollywood, FilmRise, TV One, Nosey |
| **Documentary** | Knowledge & Nature | BBC Earth, The Unexplained Zone |
| **Lifestyle** | Travel & Lifestyle | GoUSA TV |
| **Music** | Music Videos | Shemaroo Songs, Mastiii |
| **Series** | TV Drama Series | Shemaroo Umang, ION Television |

---

## ⚙️ How It Works

1. **GitHub Actions Workflow** runs automatically every 3 hours.
2. **Playwright (Headless Chromium)** opens the source website, scrolls through the full grid display, and visits each stream page.
3. The script intercepts network requests (*network intercept*) containing valid `.m3u8` manifest URLs alongside active access tokens.
4. The script maps channel metadata against an internal database and regenerates the `playlist.m3u` file.
5. Updated files are automatically committed and pushed back to this repository.

---

## ⚠️ Disclaimer

This repository does not store, host, or broadcast any media content directly. All stream links are automatically extracted from publicly accessible domains. This project is created purely for educational purposes and personal automation.

---

## ☕ Support the Developer

If the **pluto-playlist** project is helpful to you, consider supporting the developer to keep this project alive and maintained!

<div align="center">

### 🇮🇩 Local Donation (QRIS / E-Wallet / Mobile Banking)

<!-- BILA MENGGUNAKAN UPLOAD GITHUB (CARA 1): Ganti URL gambar di bawah dengan URL dari GitHub -->
<a href="https://saweria.co/sulthanpamenan" target="_blank">
  <img width="290" height="290" alt="Saweria" src="https://github.com/user-attachments/assets/f2846d1f-a391-4daf-9ce5-a48aadc992a0" />
</a>

<br>

*Scan the QRIS code above using GoPay, DANA, OVO, ShopeePay, LinkAja, or Mobile Banking.*

<br>

<a href="https://saweria.co/sulthanpamenan" target="_blank">
  <img src="https://img.shields.io/badge/Saweria-Support_Project-orange?style=for-the-badge&logo=coffee" alt="Support via Saweria">
</a>

---

### 🌐 International Donation

<a href="https://buymeacoffee.com/sulthanpamenan" target="_blank">
  <img src="https://img.shields.io/badge/Buy_Me_A_Coffee-Donate-yellow?style=for-the-badge&logo=buy-me-a-coffee" alt="Buy Me A Coffee">
</a>

</div>
