import sys
import os
import re
from playwright.sync_api import sync_playwright

BASE_URL = "https://malaysia-tv.net/tv3-live/"

# Database Metadata Resmi & Pemetaan Kategori
CHANNEL_DB = {
    "al jazeera": {"id": "AlJazeera.qa", "name": "Al Jazeera", "logo": "", "group": "News"},
    "shemaroo classic": {"id": "ShemarooClassic.in", "name": "Shemaroo Classic", "logo": "", "group": "Movies"},
    "bollywood prime": {"id": "BollywoodPrime.in", "name": "Bollywood Prime", "logo": "", "group": "Movies"},
    "bollywood masala": {"id": "BollywoodMasala.in", "name": "Bollywood Masala", "logo": "", "group": "Movies"},
    "shemaroo songs": {"id": "ShemarooSongs.in", "name": "Shemaroo Songs", "logo": "", "group": "Music"},
    "pitaara tv": {"id": "PitaaraTV.in", "name": "Pitaara TV", "logo": "", "group": "Movies"},
    "shemaroo umang": {"id": "ShemarooUmang.in", "name": "Shemaroo Umang", "logo": "", "group": "Series"},
    "mastiii": {"id": "Mastiii.in", "name": "Mastiii", "logo": "", "group": "Music"},
    "shemaroo bollywood": {"id": "ShemarooBollywood.in", "name": "Shemaroo Bollywood", "logo": "", "group": "Movies"},
    "miramax movie channel": {"id": "MiramaxMovieChannel.us", "name": "Miramax Movie Channel", "logo": "", "group": "Movies"},
    "filmrise": {"id": "FilmRise.us", "name": "FilmRise", "logo": "", "group": "Entertainment"},
    "tv one": {"id": "TVOne.us", "name": "TV One", "logo": "", "group": "General"},
    "bbc earth": {"id": "BBCEarth.uk", "name": "BBC Earth", "logo": "", "group": "Documentary"},
    "gousa tv": {"id": "GoUSATV.us", "name": "GoUSA TV", "logo": "", "group": "Lifestyle"},
    "warner tv": {"id": "WarnerTV.us", "name": "Warner TV", "logo": "", "group": "Entertainment"}
}

def get_channel_metadata(slug_name):
    clean_name = slug_name.lower().strip()
    
    # Cari pencocokan kunci terdekat di database
    for key, meta in CHANNEL_DB.items():
        if key in clean_name or clean_name in key:
            return meta
            
    # Default jika channel baru belum terdaftar di database
    return {
        "id": f"{slug_name.replace(' ', '')}.tv",
        "name": slug_name,
        "logo": "",
        "group": "General"
    }

def run_scraper():
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    referer = "https://malaysia-tv.net/"
    header_pipe = f"|User-Agent={ua}&Referer={referer}"

    valid_channels = []

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--autoplay-policy=no-user-gesture-required", "--no-sandbox"]
        )
        context = browser.new_context(user_agent=ua)
        page = context.new_page()

        print("[*] Tahap 1: Membuka indeks & me-scan grid channel...")
        found_urls = set()
        
        try:
            page.goto(BASE_URL, timeout=60000, wait_until="domcontentloaded")
            page.wait_for_timeout(4000)

            for _ in range(12):
                page.mouse.wheel(0, 1200)
                page.wait_for_timeout(600)

            all_links = page.locator("a").all()
            ignore_keywords = ["/category/", "/tag/", "/contact", "/privacy", "/terms", ".png", ".jpg", ".jpeg", ".css", ".js", "#", "facebook.com", "twitter.com"]

            for link in all_links:
                href = link.get_attribute("href")
                if href and "malaysia-tv.net" in href:
                    clean_url = href.split("#")[0].rstrip("/") + "/"
                    if not any(kw in clean_url for kw in ignore_keywords) and clean_url != "https://malaysia-tv.net/":
                        found_urls.add(clean_url)

            found_urls.add(BASE_URL)
            print(f"[✓] Berhasil mengindeks {len(found_urls)} URL halaman channel!")

        except Exception as e:
            print(f"[!] Error saat membaca grid halaman: {e}")
            browser.close()
            return []

        page.close()

        print("\n[*] Tahap 2: Mengekstrak stream M3U8 & memasangkan metadata...")
        for ch_url in sorted(found_urls):
            raw_slug = ch_url.rstrip("/").split("/")[-1].replace("-live", "").replace("-", " ").title()
            ch_page = context.new_page()
            print(f"[*] Scraping channel: {raw_slug}...")

            stream_url = None

            def handle_request(request):
                nonlocal stream_url
                req_url = request.url
                if ".m3u8" in req_url and ("b-cdn.net" in req_url or "streamer" in req_url or "playlist" in req_url or "live" in req_url or "hls" in req_url):
                    if not stream_url:
                        stream_url = req_url

            ch_page.on("request", handle_request)

            try:
                ch_page.goto(ch_url, timeout=40000, wait_until="domcontentloaded")
                ch_page.wait_for_timeout(3000)

                try:
                    for frame in ch_page.frames:
                        play_btn = frame.locator("video, .play-button, #player, .vjs-big-play-button, .player-poster, iframe")
                        if play_btn.count() > 0:
                            play_btn.first.click(timeout=1000)
                except Exception:
                    pass

                for _ in range(10):
                    if stream_url:
                        break
                    ch_page.wait_for_timeout(1000)

            except Exception as e:
                print(f"[!] Error/Timeout saat memuat {raw_slug}: {e}")

            if stream_url:
                meta = get_channel_metadata(raw_slug)
                print(f"[✓] Berhasil [{meta['group']}]: {meta['name']}")
                valid_channels.append({
                    "id": meta["id"],
                    "name": meta["name"],
                    "logo": meta["logo"],
                    "group": meta["group"],
                    "url": f"{stream_url}{header_pipe}"
                })
            else:
                print(f"[x] Skip (Bukan M3U8): {raw_slug}")

            ch_page.close()

        browser.close()

    return valid_channels

def main():
    channels = run_scraper()

    if not channels:
        print("[X] Tidak ada channel yang berhasil diekstrak.")
        sys.exit(1)

    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    referer = "https://malaysia-tv.net/"

    m3u_lines = ["#EXTM3U\n"]
    for ch in channels:
        # Menuliskan baris EXTINF dengan atribut lengkap tvg-id, tvg-name, tvg-logo, dan group-title
        extinf = f'#EXTINF:-1 tvg-id="{ch["id"]}" tvg-name="{ch["name"]}" tvg-logo="{ch["logo"]}" group-title="{ch["group"]}", {ch["name"]}\n'
        m3u_lines.append(extinf)
        m3u_lines.append(f'#EXTVLCOPT:http-user-agent={ua}\n')
        m3u_lines.append(f'#EXTVLCOPT:http-referrer={referer}\n')
        m3u_lines.append(f'{ch["url"]}\n')

    m3u_content = "".join(m3u_lines)

    for filename in ["playlist.txt", "playlist.m3u"]:
        with open(filename, "w", encoding="utf-8", newline="\n") as f:
            f.write(m3u_content)

    print(f"\n[SUCCESS] Berhasil memperbarui {len(channels)} saluran dengan metadata & kategori otomatis!")

if __name__ == "__main__":
    main()
