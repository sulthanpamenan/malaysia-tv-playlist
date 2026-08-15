import sys
from playwright.sync_api import sync_playwright

# Daftar channel dengan URL halaman yang terverifikasi di malaysia-tv.net
CHANNELS = [
    {"name": "TV3", "url": "https://malaysia-tv.net/tv3-live/", "logo": "https://upload.wikimedia.org/wikipedia/commons/2/22/TV3_logo_%28Malaysia%29.svg"},
    {"name": "Astro Awani", "url": "https://malaysia-tv.net/astro-awani-live/", "logo": "https://upload.wikimedia.org/wikipedia/commons/6/60/Astro_Awani.png"},
]

def scrape_bcdn_streams():
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    referer = "https://malaysia-tv.net/"
    header_pipe = f"|User-Agent={ua}&Referer={referer}"

    valid_channels = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent=ua)

        for ch in CHANNELS:
            page = context.new_page()
            print(f"[*] Scraping stream untuk: {ch['name']} ({ch['url']})...")
            
            stream_url = None

            # Tangkap request jaringan yang mengarah ke .m3u8 di BunnyCDN
            def handle_request(request):
                nonlocal stream_url
                req_url = request.url
                if ("b-cdn.net" in req_url or "streamer" in req_url) and ".m3u8" in req_url:
                    stream_url = req_url

            page.on("request", handle_request)

            try:
                page.goto(ch["url"], timeout=30000, wait_until="networkidle")
                page.wait_for_timeout(4000)  # Tunggu player memuat token
            except Exception as e:
                print(f"[!] Error saat memuat {ch['name']}: {e}")

            if stream_url:
                print(f"[✓] Berhasil menemukan token M3U8 untuk {ch['name']}!")
                valid_channels.append({
                    "name": ch["name"],
                    "logo": ch["logo"],
                    "url": f"{stream_url}{header_pipe}"
                })
            else:
                print(f"[!] Token stream tidak ditemukan untuk {ch['name']}")

            page.close()

        browser.close()

    return valid_channels

def main():
    channels = scrape_bcdn_streams()

    if not channels:
        print("[X] Tidak ada channel yang berhasil diekstrak.")
        sys.exit(1)

    m3u_lines = ["#EXTM3U"]
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    referer = "https://malaysia-tv.net/"

    for ch in channels:
        m3u_lines.append(f'#EXTINF:-1 group-title="Malaysia" tvg-logo="{ch["logo"]}", (🇲🇾) {ch["name"]}')
        m3u_lines.append(f'#EXTVLCOPT:http-user-agent={ua}')
        m3u_lines.append(f'#EXTVLCOPT:http-referrer={referer}')
        m3u_lines.append(ch["url"])

    m3u_content = "\r\n".join(m3u_lines)

    with open("playlist.txt", "w", encoding="utf-8") as f:
        f.write(m3u_content)

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)

    print(f"[SUCCESS] Berhasil memperbarui {len(channels)} saluran Malaysia TV Net!")

if __name__ == "__main__":
    main()
