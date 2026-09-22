import os
import requests

WORKER_URL = "https://tvmalaysia-proxy.sulthan-pamenan.workers.dev/"

channels = [
    {"name": "TV1", "slug": "tv1", "logo": "https://tvmalaysia.com.co/wp-content/uploads/2025/04/TV1-Live-Streaming-TVMalaysia.com_.co_.webp"},
    {"name": "TV2", "slug": "tv2", "logo": "https://tvmalaysia.com.co/wp-content/uploads/2025/04/TV2-Live-Streaming-TVMalaysia.com_.co_.webp"},
    {"name": "TV3", "slug": "tv3", "logo": "https://tvmalaysia.com.co/wp-content/uploads/2025/04/TV3-Live-Streaming-TVMalaysia.com_.co_.webp"},
    {"name": "TV9", "slug": "tv9", "logo": "https://tvmalaysia.com.co/wp-content/uploads/2025/04/TV9-Live-Streaming-TVMalaysia.com_.co_.webp"},
    {"name": "TV6", "slug": "tv6", "logo": "https://tvmalaysia.com.co/wp-content/uploads/2025/04/TV6-Live-Streaming-TVMalaysia.com_.co_.webp"},
    {"name": "TV AlHijrah", "slug": "alhijrah", "logo": "https://tvmalaysia.com.co/wp-content/uploads/2025/04/TV-Alhijrah-Live-Streaming-TVMalaysia.com_.co_.webp"},
    {"name": "RTM Sukan", "slug": "sukan-rtm", "logo": "https://tvmalaysia.com.co/wp-content/uploads/2025/04/RTM-Sukan-Live-Streaming-TVMalaysia.com_.co_.webp"},
    {"name": "RTM Parlimen", "slug": "parliament", "logo": "https://tvmalaysia.com.co/wp-content/uploads/2025/04/RTM-Parlimen-Live-Streaming-TVMalaysia.com_.co_.webp"},
    {"name": "Astro Awani", "slug": "astro-awani", "logo": "https://tvmalaysia.com.co/wp-content/uploads/2025/04/Astro-Awani-Live-Streaming-TVMalaysia.com_.co_.webp"},
    {"name": "Astro Arena", "slug": "astro-arena", "logo": "https://tvmalaysia.com.co/wp-content/uploads/2025/04/Astro-Arena-Live-Streaming-TVMalaysia.com_.co_.webp"},
]

def generate_m3u():
    m3u_content = "#EXTM3U\n"
    success_count = 0
    
    for ch in channels:
        print(f"Mengambil link untuk {ch['name']} via Worker...")
        try:
            # Panggil Cloudflare Worker untuk mengambil link m3u8 terbaru
            res = requests.get(f"{WORKER_URL}?channel={ch['slug']}&format=json", timeout=15)
            if res.status_code == 200:
                data = res.json()
                stream_url = data.get("streamUrl")
                if stream_url:
                    print(f"  -> Berhasil: {stream_url}")
                    m3u_content += f"#EXTINF:-1 tvg-id=\"{ch['slug']}\" tvg-logo=\"{ch['logo']}\" group-title=\"Malaysian Channels\",{ch['name']}\n"
                    m3u_content += f"#EXTVLCOPT:http-referrer=https://tvmalaysia.com.co/\n"
                    m3u_content += f"#EXTVLCOPT:http-user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)\n"
                    m3u_content += f"{stream_url}\n"
                    success_count += 1
                    continue
            print(f"  -> Gagal mendapatkan link untuk {ch['name']}")
        except Exception as e:
            print(f"  -> Error: {e}")

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)
    print(f"Selesai! Berhasil memperbarui {success_count} channel ke playlist.m3u")

if __name__ == "__main__":
    generate_m3u()
