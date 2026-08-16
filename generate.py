import sys
import os
import re
from playwright.sync_api import sync_playwright

BASE_URL = "https://malaysia-tv.net/tv3-live/"
EPG_URL = "https://iptv-org.github.io/epg/guides/my/astro.com.my.epg.xml"

# Pemetaan ID EPG Resmi Internasional
EPG_ID_MAP = {
    "tv1": "TV1.my",
    "tv2": "TV2.my",
    "tv3": "TV3.my",
    "tv9": "TV9.my",
    "8tv": "8TV.my",
    "8 tv": "8TV.my",
    "tv okey": "TVOkey.my",
    "ntv7": "NTV7.my",
    "drama sangat": "DramaSangat.my",
    "astro awani": "AstroAwani.my",
    "awesome tv": "AwesomeTV.my",
    "bernama tv": "BernamaTV.my",
    "sinar tv": "SinarTV.my",
    "sukan rtm": "SukanRTM.my",
    "berita rtm": "BeritaRTM.my",
    "ikim tv": "IKIMTV.my",
    "suke tv": "SukeTV.my",
    "selangor tv": "SelangorTV.my",
    "al jazeera": "AlJazeeraEnglish.qa",
    "al jazeera english": "AlJazeeraEnglish.qa",
    "bbc earth": "BBCEarth.uk",
    "bbc news": "BBCNews.uk",
    "bein sports 1": "beINSports1.qa",
    "mastiii tv": "Mastiii.in",
    "miramax movie channel": "MiramaxMovieChannel.us",
    "pitaara tv": "PitaaraTV.in",
    "scripps news": "ScrippsNews.us",
    "filmrise movies": "FilmRise.us",
    "livenow from fox": "LiveNOWfromFOX.us",
    "the unxplained zone": "TheUnXplainedZone.us"
}

# 15 Kategori Resmi Baku
CATEGORY_KEYWORD_MAP = {
    "News": ["news", "berita", "warta", "informasi", "politics", "politik"],
    "Movies": ["movie", "cinema", "film", "wayang", "box office", "sinema", "dunia sinema"],
    "Series": ["series", "drama", "sinetron", "serial"],
    "Kids": ["kids", "kartun", "cartoon", "children", "kanak", "anak", "ceria", "didik"],
    "Sports": ["sport", "sukan", "bola", "football", "racing", "stadium", "espn", "afl", "mlb", "raket", "tennis", "cricket", "golf", "wwe", "eurosport"],
    "Music": ["music", "musik", "lagu", "hits", "radio", "mastiii"],
    "Documentary": ["documentary", "dokumentari", "history", "sejarah", "nat geo", "discovery", "earth", "unxplained"],
    "Religious": ["religion", "religious", "islam", "agama", "rohani", "dakwah", "ikim", "salam"],
    "Lifestyle": ["lifestyle", "gaya hidup", "fashion", "food", "masak"],
    "Shopping": ["shopping", "shop", "belanja", "suke", "cj wow"],
    "Travel": ["travel", "pelancongan", "wisata", "explore"],
    "Knowledge": ["knowledge", "education", "pendidikan", "sains", "didik"],
    "Local": ["local", "lokal", "daerah", "negeri", "selangor", "perak", "sabah", "sarawak", "rtm"],
    "Entertainment": ["entertainment", "hiburan", "variety", "show", "warna", "ria"]
}

def clean_channel_name(raw_text, slug):
    if raw_text and len(raw_text) > 1 and not raw_text.startswith("?"):
        name = raw_text.strip()
    else:
        name = slug.rstrip("/").split("/")[-1].replace("-live", "").replace("-tv", " TV").replace("-", " ").title()
    return name

def get_category_and_epg(name):
    clean_key = name.lower().strip()
    
    # Matching EPG ID
    epg_id = f"{re.sub(r'[^a-zA-Z0-9]', '', name)}.my"
    for k, v in EPG_ID_MAP.items():
        if k == clean_key or k in clean_key:
            epg_id = v
            break
            
    # Matching Kategori
    group = "General"
    for cat, keywords in CATEGORY_KEYWORD_MAP.items():
        if any(kw in clean_key for kw in keywords):
            group = cat
            break

    return group, epg_id

def run_scraper():
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    referer = "https://malaysia-tv.net/"
    header_pipe = f"|User-Agent={ua}&Referer={referer}"

    valid_channels = []
    seen_stream_urls = set()

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--autoplay-policy=no-user-gesture-required", "--no-sandbox"]
        )
        context = browser.new_context(user_agent=ua)
        page = context.new_page()

        print("[*] Tahap 1: Mengambil daftar channel & LOGO dari grid web...")
        channels_to_scrape = []
        
        try:
            page.goto(BASE_URL, timeout=60000, wait_until="domcontentloaded")
            page.wait_for_timeout(4000)

            for _ in range(15):
                page.mouse.wheel(0, 1200)
                page.wait_for_timeout(500)

            grid_items = page.locator("a").all()
            visited_urls = set()

            for item in grid_items:
                try:
                    href = item.get_attribute("href")
                    if not href or "malaysia-tv.net" not in href:
                        continue
                    
                    # 1. PERBAIKAN: Hapus URL query parameter (seperti ?Tierand=1, ?T=1)
                    clean_url = href.split("?")[0].split("#")[0].rstrip("/") + "/"
                    
                    if clean_url in visited_urls or clean_url == "https://malaysia-tv.net/":
                        continue

                    # Filter tautan kategori non-channel
                    if "category" in clean_url or "tag" in clean_url or "contact" in clean_url or "privacy" in clean_url:
                        continue

                    img_elem = item.locator("img").first
                    logo_url = ""
                    if img_elem.count() > 0:
                        src = img_elem.get_attribute("src") or img_elem.get_attribute("data-src")
                        if src and "http" in src:
                            logo_url = src

                    raw_text = item.inner_text().strip()
                    ch_name = clean_channel_name(raw_text, clean_url)

                    # Pastikan nama saluran tidak diawali tanda tanya
                    if ch_name.startswith("?"):
                        continue

                    visited_urls.add(clean_url)
                    channels_to_scrape.append({
                        "url": clean_url,
                        "name": ch_name,
                        "logo": logo_url
                    })
                except Exception:
                    pass

            print(f"[✓] Berhasil mengumpulkan {len(channels_to_scrape)} saluran bersih tanpa query garbage!")

        except Exception as e:
            print(f"[!] Error saat membaca grid halaman utama: {e}")
            browser.close()
            return []

        page.close()

        print("\n[*] Tahap 2: Intersepsi URL Stream M3U8 & Deduplikasi...")
        for item in channels_to_scrape:
            ch_url = item["url"]
            ch_name = item["name"]
            web_logo = item["logo"]
            
            ch_page = context.new_page()
            print(f"[*] Scraping stream: {ch_name}...")

            stream_url = None

            def handle_request(request):
                nonlocal stream_url
                req_url = request.url
                if ".m3u8" in req_url and ("b-cdn.net" in req_url or "streamer" in req_url or "playlist" in req_url or "live" in req_url or "hls" in req_url):
                    if not stream_url:
                        stream_url = req_url

            ch_page.on("request", handle_request)

            try:
                ch_page.goto(ch_url, timeout=35000, wait_until="domcontentloaded")
                ch_page.wait_for_timeout(2500)

                try:
                    for frame in ch_page.frames:
                        play_btn = frame.locator("video, .play-button, #player, .vjs-big-play-button, .player-poster, iframe")
                        if play_btn.count() > 0:
                            play_btn.first.click(timeout=1000)
                except Exception:
                    pass

                for _ in range(8):
                    if stream_url:
                        break
                    ch_page.wait_for_timeout(1000)

            except Exception as e:
                print(f"[!] Error/Timeout pada {ch_name}: {e}")

            if stream_url:
                # 2. PERBAIKAN: Deduplikasi stream URL (mencegah channel ganda/re-stream)
                if stream_url in seen_stream_urls:
                    print(f"[x] Skip Duplikat Stream: {ch_name}")
                else:
                    seen_stream_urls.add(stream_url)
                    group, epg_id = get_category_and_epg(ch_name)
                    print(f"[✓] Berhasil [{group}]: {ch_name} | Logo: {'Ada' if web_logo else 'Kosong'} | EPG: {epg_id}")

                    valid_channels.append({
                        "id": epg_id,
                        "name": ch_name,
                        "logo": web_logo,
                        "group": group,
                        "url": f"{stream_url}{header_pipe}"
                    })
            else:
                print(f"[x] Skip (Stream tidak ditemukan): {ch_name}")

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

    m3u_lines = [f'#EXTM3U url-tvg="{EPG_URL}"\n\n']

    for ch in channels:
        extinf = f'#EXTINF:-1 tvg-id="{ch["id"]}" tvg-name="{ch["name"]}" tvg-logo="{ch["logo"]}" group-title="{ch["group"]}",{ch["name"]}\n'
        m3u_lines.append(extinf)
        m3u_lines.append(f'#EXTVLCOPT:http-user-agent={ua}\n')
        m3u_lines.append(f'#EXTVLCOPT:http-referrer={referer}\n')
        m3u_lines.append(f'{ch["url"]}\n')

    m3u_content = "".join(m3u_lines)

    for filename in ["playlist.txt", "playlist.m3u"]:
        with open(filename, "w", encoding="utf-8", newline="\n") as f:
            f.write(m3u_content)

    print(f"\n[SUCCESS] Berhasil memperbarui {len(channels)} saluran tanpa duplikat & query sampah!")

if __name__ == "__main__":
    main()
