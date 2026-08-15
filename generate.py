import re
import requests
import sys
from bs4 import BeautifulSoup

# Daftar channel yang ada di malaysia-tv.net
CHANNELS = [
    {"name": "TV3", "slug": "tv3-live", "logo": "https://upload.wikimedia.org/wikipedia/commons/2/22/TV3_logo_%28Malaysia%29.svg"},
    {"name": "TV9", "slug": "tv9-live", "logo": "https://upload.wikimedia.org/wikipedia/commons/e/e5/TV9_Logo_%28Malaysia%29.svg"},
    {"name": "NTV7", "slug": "ntv7-live", "logo": "https://upload.wikimedia.org/wikipedia/commons/a/a2/NTV7_logo.svg"},
    {"name": "8TV", "slug": "8tv-live", "logo": "https://upload.wikimedia.org/wikipedia/commons/4/4e/8TV_logo.svg"},
    {"name": "Astro Awani", "slug": "astro-awani-live", "logo": "https://upload.wikimedia.org/wikipedia/commons/6/60/Astro_Awani.png"},
]

def get_bcdn_stream_url(slug):
    url = f"https://malaysia-tv.net/{slug}/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Referer": "https://malaysia-tv.net/"
    }

    try:
        print(f"[*] Mengambil stream untuk: {slug}...")
        res = requests.get(url, headers=headers, timeout=15)
        if res.status_code != 200:
            print(f"[!] Gagal akses {url} (Status: {res.status_code})")
            return None

        # Cari iframe atau source embed video
        soup = BeautifulSoup(res.text, 'html.parser')
        iframes = soup.find_all('iframe')
        
        target_src = None
        for iframe in iframes:
            src = iframe.get('src', '')
            if 'streamer' in src or 'b-cdn.net' in src or 'embed' in src:
                target_src = src
                break

        # Jika link tertanam di iframe player terpisah
        if target_src:
            if target_src.startswith('//'):
                target_src = 'https:' + target_src
            res_embed = requests.get(target_src, headers=headers, timeout=15)
            content_to_search = res_embed.text
        else:
            content_to_search = res.text

        # Regex pola BunnyCDN: https://*.b-cdn.net/*.m3u8?expires=...&token=...
        pattern = r'https://[a-zA-Z0-9\.-]+\.b-cdn\.net/[^"\'\s<>]+\.m3u8\?[^"\'\s<>]+'
        matches = re.findall(pattern, content_to_search)

        if matches:
            print(f"[✓] Berhasil menemukan token M3U8!")
            return matches[0]
        else:
            print(f"[!] Token stream tidak ditemukan di {slug}")

    except Exception as e:
        print(f"[!] Error ekstraksi {slug}: {e}")

    return None

def main():
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    referer = "https://malaysia-tv.net/"
    header_pipe = f"|User-Agent={ua}&Referer={referer}"

    valid_channels = []

    for ch in CHANNELS:
        stream_url = get_bcdn_stream_url(ch["slug"])
        if stream_url:
            valid_channels.append({
                "name": ch["name"],
                "logo": ch["logo"],
                "url": f"{stream_url}{header_pipe}"
            })

    if not valid_channels:
        print("[X] Tidak ada channel yang berhasil diekstrak.")
        sys.exit(1)

    m3u_lines = ["#EXTM3U"]
    for ch in valid_channels:
        m3u_lines.append(f'#EXTINF:-1 group-title="Malaysia" tvg-logo="{ch["logo"]}", (🇲🇾) {ch["name"]}')
        m3u_lines.append(f'#EXTVLCOPT:http-user-agent={ua}')
        m3u_lines.append(f'#EXTVLCOPT:http-referrer={referer}')
        m3u_lines.append(ch["url"])

    m3u_content = "\r\n".join(m3u_lines)

    with open("playlist.txt", "w", encoding="utf-8") as f:
        f.write(m3u_content)

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)

    print(f"[SUCCESS] Berhasil memperbarui {len(valid_channels)} saluran Malaysia TV Net!")

if __name__ == "__main__":
    main()
