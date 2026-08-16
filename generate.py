import sys
import os
import re
import asyncio
from playwright.async_api import async_playwright

BASE_URL = "https://malaysia-tv.net/tv3-live/"
EPG_URL = "https://iptv-org.github.io/epg/guides/my/astro.com.my.epg.xml"
CONCURRENCY_LIMIT = 4  # Menjalankan 4 halaman sekaligus secara paralel

EPG_ID_MAP = {
    "tv1": "TV1.my", "tv2": "TV2.my", "tv3": "TV3.my", "tv9": "TV9.my",
    "8tv": "8TV.my", "8 tv": "8TV.my", "tv okey": "TVOkey.my", "ntv7": "NTV7.my",
    "drama sangat": "DramaSangat.my", "astro awani": "AstroAwani.my",
    "awesome tv": "AwesomeTV.my", "bernama tv": "BernamaTV.my",
    "sinar tv": "SinarTV.my", "sukan rtm": "SukanRTM.my", "berita rtm": "BeritaRTM.my",
    "ikim tv": "IKIMTV.my", "suke tv": "SukeTV.my", "selangor tv": "SelangorTV.my",
    "al jazeera": "AlJazeeraEnglish.qa", "al jazeera english": "AlJazeeraEnglish.qa",
    "bbc earth": "BBCEarth.uk", "bbc news": "BBCNews.uk", "bein sports 1": "beINSports1.qa",
    "mastiii tv": "Mastiii.in", "miramax movie channel": "MiramaxMovieChannel.us",
    "pitaara tv": "PitaaraTV.in", "scripps news": "ScrippsNews.us",
    "filmrise movies": "FilmRise.us", "livenow from fox": "LiveNOWfromFOX.us",
    "the unxplained zone": "TheUnXplainedZone.us"
}

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
        return raw_text.strip()
    return slug.rstrip("/").split("/")[-1].replace("-live", "").replace("-tv", " TV").replace("-", " ").title()

def get_category_and_epg(name):
    clean_key = name.lower().strip()
    epg_id = f"{re.sub(r'[^a-zA-Z0-9]', '', name)}.my"
    for k, v in EPG_ID_MAP.items():
        if k == clean_key or k in clean_key:
            epg_id = v
            break
            
    group = "General"
    for cat, keywords in CATEGORY_KEYWORD_MAP.items():
        if any(kw in clean_key for kw in keywords):
            group = cat
            break

    return group, epg_id

async def scrape_single_channel(context, item, semaphore, seen_stream_urls, header_pipe):
    async with semaphore:
        ch_url = item["url"]
        ch_name = item["name"]
        web_logo = item["logo"]
        
        ch_page = await context.new_page()
        
        # Blokir elemen berat agar load halaman super cepat
        await ch_page.route("**/*.{png,jpg,jpeg,gif,svg,css,woff,woff2}", lambda route: route.abort())

        stream_url = None

        def handle_request(request):
            nonlocal stream_url
            req_url = request.url
            if ".m3u8" in req_url and ("b-cdn.net" in req_url or "streamer" in req_url or "playlist" in req_url or "live" in req_url or "hls" in req_url):
                if not stream_url:
                    stream_url = req_url

        ch_page.on("request", handle_request)

        try:
            await ch_page.goto(ch_url, timeout=15000, wait_until="domcontentloaded")
            await ch_page.wait_for_timeout(1500)

            # Klik tombol play otomatis di frame
            for frame in ch_page.frames:
                try:
                    play_btn = frame.locator("video, .play-button, #player, .vjs-big-play-button, .player-poster, iframe")
                    if await play_btn.count() > 0:
                        await play_btn.first.click(timeout=800)
                except Exception:
                    pass

            for _ in range(6):
                if stream_url:
                    break
                await ch_page.wait_for_timeout(500)

        except Exception as e:
            print(f"[!] Timeout pada {ch_name}")

        await ch_page.close()

        if stream_url and stream_url not in seen_stream_urls:
            seen_stream_urls.add(stream_url)
            group, epg_id = get_category_and_epg(ch_name)
            print(f"[✓] Berhasil [{group}]: {ch_name} | EPG: {epg_id}")
            return {
                "id": epg_id,
                "name": ch_name,
                "logo": web_logo,
                "group": group,
                "url": f"{stream_url}{header_pipe}"
            }
        return None

async def run_scraper():
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    referer = "https://malaysia-tv.net/"
    header_pipe = f"|User-Agent={ua}&Referer={referer}"

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--autoplay-policy=no-user-gesture-required", "--no-sandbox"]
        )
        context = await browser.new_context(user_agent=ua)
        page = await context.new_page()

        print("[*] Tahap 1: Membaca Grid Utama & Logo...")
        channels_to_scrape = []
        
        try:
            await page.goto(BASE_URL, timeout=30000, wait_until="domcontentloaded")
            await page.wait_for_timeout(2000)

            for _ in range(10):
                await page.mouse.wheel(0, 1500)
                await page.wait_for_timeout(300)

            grid_items = await page.locator("a").all()
            visited_urls = set()

            for item in grid_items:
                try:
                    href = await item.get_attribute("href")
                    if not href or "malaysia-tv.net" not in href:
                        continue
                    
                    clean_url = href.split("?")[0].split("#")[0].rstrip("/") + "/"
                    
                    if clean_url in visited_urls or clean_url == "https://malaysia-tv.net/":
                        continue

                    if any(kw in clean_url for kw in ["category", "tag", "contact", "privacy"]):
                        continue

                    img_elem = item.locator("img").first
                    logo_url = ""
                    if await img_elem.count() > 0:
                        src = await img_elem.get_attribute("src") or await img_elem.get_attribute("data-src")
                        if src and "http" in src:
                            logo_url = src

                    raw_text = await item.inner_text()
                    ch_name = clean_channel_name(raw_text.strip() if raw_text else "", clean_url)

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

            print(f"[✓] Terkumpul {len(channels_to_scrape)} saluran dari Grid!")

        except Exception as e:
            print(f"[!] Error saat membuka halaman utama: {e}")
            await browser.close()
            return []

        await page.close()

        print(f"\n[*] Tahap 2: Mengekstrak Stream Secara Paralel ({CONCURRENCY_LIMIT} worker)...")
        semaphore = asyncio.Semaphore(CONCURRENCY_LIMIT)
        seen_stream_urls = set()

        tasks = [
            scrape_single_channel(context, item, semaphore, seen_stream_urls, header_pipe)
            for item in channels_to_scrape
        ]
        
        results = await asyncio.gather(*tasks)
        valid_channels = [r for r in results if r is not None]

        await browser.close()

    return valid_channels

def main():
    valid_channels = asyncio.run(run_scraper())

    if not valid_channels:
        print("[X] Tidak ada channel yang berhasil diekstrak.")
        sys.exit(1)

    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    referer = "https://malaysia-tv.net/"

    m3u_lines = [f'#EXTM3U url-tvg="{EPG_URL}"\n\n']

    for ch in valid_channels:
        extinf = f'#EXTINF:-1 tvg-id="{ch["id"]}" tvg-name="{ch["name"]}" tvg-logo="{ch["logo"]}" group-title="{ch["group"]}",{ch["name"]}\n'
        m3u_lines.append(extinf)
        m3u_lines.append(f'#EXTVLCOPT:http-user-agent={ua}\n')
        m3u_lines.append(f'#EXTVLCOPT:http-referrer={referer}\n')
        m3u_lines.append(f'{ch["url"]}\n')

    m3u_content = "".join(m3u_lines)

    for filename in ["playlist.txt", "playlist.m3u"]:
        with open(filename, "w", encoding="utf-8", newline="\n") as f:
            f.write(m3u_content)

    print(f"\n[SUCCESS] Selesai! Berhasil memperbarui {len(valid_channels)} saluran dalam waktu singkat!")

if __name__ == "__main__":
    main()
