import os
import re
import requests

# Daftar channel yang ingin ditarik
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

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://tvmalaysia.com.co/"
}

def get_stream_url(slug):
    try:
        page_url = f"https://tvmalaysia.com.co/{slug}/"
        res = requests.get(page_url, headers=headers, timeout=15)
        if res.status_code != 200:
            return None
        
        # Cari pola link m3u8 yang ada di dalam halaman HTML/script website
        match = re.search(r'https?://[^\s<>"]+?\.b-cdn\.net[^\s<>"]+?\.m3u8[^\s<>"]*', res.text)
        if match:
            return match.group(0)
    except Exception as e:
        print(f"Error fetching {slug}: {e}")
    return None

def generate_m3u():
    m3u_content = "#EXTM3U\n"
    
    for ch in channels:
        print(f"Mencari link untuk {ch['name']}...")
        stream_url = get_stream_url(ch['slug'])
        
        if stream_url:
            print(f"Ditemukan: {stream_url}")
            m3u_content += f"#EXTINF:-1 tvg-id=\"{ch['slug']}\" tvg-logo=\"{ch['logo']}\" group-title=\"Malaysian Channels\",{ch['name']}\n"
            m3u_content += f"#EXTVLCOPT:http-referrer=https://tvmalaysia.com.co/\n"
            m3u_content += f"#EXTVLCOPT:http-user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)\n"
            m3u_content += f"{stream_url}\n"
        else:
            print(f"Gagal mendapatkan link untuk {ch['name']}")

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)
    print("File playlist.m3u berhasil diperbarui!")

if __name__ == "__main__":
    generate_m3u()
