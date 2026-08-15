import sys
import os
import re
from playwright.sync_api import sync_playwright

BASE_URL = "https://malaysia-tv.net/tv3-live/"

# Database Metadata Resmi & Pemetaan Kategori Hasil Audit
CHANNEL_DB = {
    # Malaysia - General
    "tv3": {"id": "TV3.my", "name": "TV3", "logo": "https://upload.wikimedia.org/wikipedia/commons/2/22/TV3_logo_%28Malaysia%29.svg", "group": "General"},
    "tv1": {"id": "TV1.my", "name": "TV1", "logo": "https://upload.wikimedia.org/wikipedia/commons/a/a2/TV1_logo.png", "group": "General"},
    "tv2": {"id": "TV2.my", "name": "TV2", "logo": "https://upload.wikimedia.org/wikipedia/commons/e/e0/TV2_logo.png", "group": "General"},
    "tv9": {"id": "TV9.my", "name": "TV9", "logo": "https://upload.wikimedia.org/wikipedia/commons/e/e5/TV9_Logo_%28Malaysia%29.svg", "group": "General"},
    "tv okey": {"id": "TVOkey.my", "name": "TV Okey", "logo": "https://upload.wikimedia.org/wikipedia/commons/c/c2/TV_Okey_logo.png", "group": "General"},
    "mytv": {"id": "MYTV.my", "name": "MYTV Broadcasting", "logo": "", "group": "General"},

    # Malaysia - News
    "astro awani": {"id": "AstroAwani.my", "name": "Astro Awani", "logo": "https://upload.wikimedia.org/wikipedia/commons/6/60/Astro_Awani.png", "group": "News"},
    "berita rtm": {"id": "BeritaRTM.my", "name": "Berita RTM", "logo": "https://upload.wikimedia.org/wikipedia/commons/2/22/Berita_RTM.png", "group": "News"},
    "bernama tv": {"id": "BernamaTV.my", "name": "Bernama TV", "logo": "https://upload.wikimedia.org/wikipedia/commons/a/a8/Bernama_TV.png", "group": "News"},
    "rtm parlimen": {"id": "RTMParlimen.my", "name": "RTM Parlimen", "logo": "", "group": "News"},
    "rtm asean": {"id": "RTMASEAN.my", "name": "RTM ASEAN", "logo": "", "group": "News"},

    # Malaysia - Kids / Entertainment / Religious / Shopping / Local
    "didiktv": {"id": "DidikTVKPM.my", "name": "DidikTV KPM", "logo": "https://upload.wikimedia.org/wikipedia/commons/a/a2/NTV7_logo.svg", "group": "Kids"},
    "ntv7": {"id": "DidikTVKPM.my", "name": "DidikTV KPM", "logo": "https://upload.wikimedia.org/wikipedia/commons/a/a2/NTV7_logo.svg", "group": "Kids"},
    "tv6": {"id": "TV6.my", "name": "TV6", "logo": "", "group": "Entertainment"},
    "astro ria": {"id": "AstroRia.my", "name": "Astro Ria", "logo": "", "group": "Entertainment"},
    "astro ceria": {"id": "AstroCeria.my", "name": "Astro Ceria", "logo": "", "group": "Kids"},
    "boo": {"id": "BOO.my", "name": "BOO", "logo": "", "group": "Movies"},
    "suke tv": {"id": "SukeTV.my", "name": "Suke TV", "logo": "", "group": "Shopping"},
    "tvs": {"id": "TVS.my", "name": "TVS", "logo": "", "group": "Local"},
    "selangor tv": {"id": "SelangorTV.my", "name": "SelangorTV", "logo": "", "group": "Local"},
    "tv ikim": {"id": "TVIKIM.my", "name": "TV IKIM", "logo": "", "group": "Religious"},

    # Sports
    "sukan rtm": {"id": "SukanRTM.my", "name": "Sukan RTM", "logo": "", "group": "Sports"},
    "afl": {"id": "AFL.au", "name": "AFL TV", "logo": "", "group": "Sports"},
    "spotv2": {"id": "SPOTV2.kr", "name": "SPOTV 2", "logo": "", "group": "Sports"},
    "bein sports": {"id": "beINSports.qa", "name": "beIN Sports", "logo": "", "group": "Sports"},
    "pickle tv": {"id": "PickleTV.us", "name": "Pickle TV", "logo": "", "group": "Sports"},
    "court sports network": {"id": "CourtSportsNetwork.us", "name": "Court Sports Network", "logo": "", "group": "Sports"},
    "eurosport": {"id": "Eurosport.fr", "name": "Eurosport", "logo": "", "group": "Sports"},
    "wwe network": {"id": "WWENetwork.us", "name": "WWE Network", "logo": "", "group": "Sports"},
    "golf channel": {"id": "GolfChannel.us", "name": "Golf Channel", "logo": "", "group": "Sports"},
    "mutv": {"id": "MUTV.uk", "name": "MUTV", "logo": "", "group": "Sports"},
    "unifi sports": {"id": "unifiSports.my", "name": "unifi Sports", "logo": "", "group": "Sports"},
    "astro arena": {"id": "AstroArena.my", "name": "Astro Arena", "logo": "", "group": "Sports"},
    "astro arena bola": {"id": "AstroArenaBola.my", "name": "Astro Arena Bola", "logo": "", "group": "Sports"},
    "astro arena bola 2": {"id": "AstroArenaBola2.my", "name": "Astro Arena Bola 2", "logo": "", "group": "Sports"},
    "astro badminton": {"id": "AstroBadminton.my", "name": "Astro Badminton", "logo": "", "group": "Sports"},
    "astro cricket": {"id": "AstroCricket.my", "name": "Astro Cricket", "logo": "", "group": "Sports"},
    "astro football": {"id": "AstroFootball.my", "name": "Astro Football", "logo": "", "group": "Sports"},
    "bola sepak": {"id": "BolaSepak.my", "name": "Bola Sepak", "logo": "", "group": "Sports"},

    # International & FAST Channels
    "al jazeera": {"id": "AlJazeera.qa", "name": "Al Jazeera", "logo": "", "group": "News"},
    "shemaroo classic": {"id": "ShemarooClassic.in", "name": "Shemaroo Classic", "logo": "", "group": "Entertainment"},
    "bollywood prime": {"id": "BollywoodPrime.in", "name": "Bollywood Prime", "logo": "", "group": "Movies"},
    "bollywood masala": {"id": "BollywoodMasala.in", "name": "Bollywood Masala", "logo": "", "group": "Entertainment"},
    "shemaroo songs": {"id": "ShemarooSongs.in", "name": "Shemaroo Songs", "logo": "", "group": "Music"},
    "pitaara tv": {"id": "PitaaraTV.in", "name": "Pitaara TV", "logo": "", "group": "Movies"},
    "shemaroo umang": {"id": "ShemarooUmang.in", "name": "Shemaroo Umang", "logo": "", "group": "Series"},
    "mastiii": {"id": "Mastiii.in", "name": "Mastiii", "logo": "", "group": "Music"},
    "shemaroo bollywood": {"id": "ShemarooBollywood.in", "name": "Shemaroo Bollywood", "logo": "", "group": "Entertainment"},
    "miramax movie channel": {"id": "MiramaxMovieChannel.us", "name": "Miramax Movie Channel", "logo": "", "group": "Movies"},
    "filmrise": {"id": "FilmRise.us", "name": "FilmRise", "logo": "", "group": "Entertainment"},
    "tv one": {"id": "TVOne.us", "name": "TV One", "logo": "", "group": "Entertainment"},
    "bbc earth": {"id": "BBCEarth.uk", "name": "BBC Earth", "logo": "", "group": "Documentary"},
    "gousa tv": {"id": "GoUSATV.us", "name": "GoUSA TV", "logo": "", "group": "Lifestyle"},
    "the unexplained zone": {"id": "TheUnexplainedZone.us", "name": "The Unexplained Zone", "logo": "", "group": "Documentary"},
    "scripps news": {"id": "ScrippsNews.us", "name": "Scripps News", "logo": "", "group": "News"},
    "euronews": {"id": "Euronews.fr", "name": "Euronews", "logo": "", "group": "News"},
    "ion television": {"id": "IONTelevision.us", "name": "ION Television", "logo": "", "group": "Series"},
    "livenow from fox": {"id": "LiveNOWfromFOX.us", "name": "LiveNOW from FOX", "logo": "", "group": "News"},
    "nosey": {"id": "Nosey.us", "name": "Nosey", "logo": "", "group": "Entertainment"},
    "failarmy": {"id": "FailArmy.us", "name": "FailArmy", "logo": "", "group": "Entertainment"},
    "nbc news now": {"id": "NBCNewsNOW.us", "name": "NBC News NOW", "logo": "", "group": "News"},
    "warner tv": {"id": "WarnerTV.us", "name": "Warner TV", "logo": "", "group": "Movies"},
    "bbc news": {"id": "BBCNews.uk", "name": "BBC News", "logo": "", "group": "News"}
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
