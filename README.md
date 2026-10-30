# 📺 Malaysia TV & Radio IPTV Proxy

A lightweight, automated HLS/M3U8 proxy generator for **Malaysia TV & Radio** live streams. Designed for seamless integration with IPTV players such as **OTT Navigator**, **TiviMate**, and **IPTV Smarters**.

---

## 🚀 Quick Start / URLs

Directly import these URLs into your preferred IPTV client:

| Resource | URL |
| :--- | :--- |
| **Playlist (M3U)** | `http://<your-server-ip>:5001/playlist.m3u` *(or use your public URL distribution)* |

---

## 💻 Running Your Own Server Locally (`proxy.py`)

If you would like to host and run your own proxy server locally using the available scripts, follow these steps:

1. Ensure that you have installed Python on your local computer.
2. Install the required dependencies by running the following command in the terminal:
   pip install flask requests
3. Set the required environment variables (such as `GITHUB_TOKEN` and `GIST_ID`, if needed) or simply use the default configuration.
4. Run the local server script:
   python proxy.py
5. The server will be active and accessible on port `5001` (`http://localhost:5001/playlist.m3u`).

---

## 🛠️ Features & Benefits

- **Automated Token Handling**: Automatic retrieval of dynamic streaming links from Gist storage.
- **Dynamic Proxy**: Supports real-time *proxying* of HLS video stream segments.
- **Multi-Category Support**: Provides a centralized collection of various categories of Malaysian TV and radio broadcasts.
- **High Compatibility**: Compatible with various popular IPTV player applications on Android TV, mobile, and desktop.

---

## 📱 How to Use on an IPTV Player

1. Open your preferred IPTV player app (for example, **OTT Navigator** or **TiviMate**).
2. Add a new playlist source using your **M3U Playlist URL**.
3. Refresh/reload the playlist, then enjoy the live broadcast!

---

## ⚠️ Disclaimer

This repository and its automated proxy service are provided strictly for educational, personal, and non-commercial purposes.

- **Content Ownership:** All video streams, channel names, logos, and intellectual property rights are the sole property of their respective copyright holders.
- **No Hosting:** This service does not store or illegally re-broadcast media files; instead, it functions purely as a dynamic parser and reverse-proxy for public links.
- **Service Availability:** The developer provides no guarantees whatsoever regarding stream uptime, video quality, or playback smoothness, as performance depends entirely on the availability of third-party sources.

---

## 📄 License

Distributed under the MIT License. See the `LICENSE` file for more information.

---

## ☕ Support the Developer

If this project is useful to you, consider supporting the developer so that this service can remain active and maintained!

<div align="center">

### 🇮🇩 Local Donations (QRIS / E-Wallet / Mobile Banking)

<a href="[https://saweria.co/sulthanpamenan](https://saweria.co/sulthanpamenan)" target="_blank">
  <img width="290" height="290" alt="Saweria" src="[https://github.com/user-attachments/assets/f2846d1f-a391-4daf-9ce5-a48aadc992a0](https://github.com/user-attachments/assets/f2846d1f-a391-4daf-9ce5-a48aadc992a0)" />
</a>

<br>

*Scan the QRIS code above using GoPay, DANA, OVO, ShopeePay, LinkAja, or Mobile Banking.*

<br>

<a href="[https://saweria.co/sulthanpamenan](https://saweria.co/sulthanpamenan)" target="_blank">
  <img src="[https://img.shields.io/badge/Saweria-Support_Project-orange?style=for-the-badge&logo=coffee](https://img.shields.io/badge/Saweria-Support_Project-orange?style=for-the-badge&logo=coffee)" alt="Support via Saweria">
</a>

---

### 🌐 International Donations

<a href="[https://buymeacoffee.com/sulthanpamenan](https://buymeacoffee.com/sulthanpamenan)" target="_blank">
  <img src="[https://img.shields.io/badge/Buy_Me_A_Coffee-Donate-yellow?style=for-the-badge&logo=buy-me-a-coffee](https://img.shields.io/badge/Buy_Me_A_Coffee-Donate-yellow?style=for-the-badge&logo=buy-me-a-coffee)" alt="Buy Me A Coffee">
</a>

</div>
