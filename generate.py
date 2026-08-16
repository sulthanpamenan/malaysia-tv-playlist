import sys
import os
import re
from playwright.sync_api import sync_playwright

BASE_URL = "https://malaysia-tv.net/tv3-live/"
EPG_URL = "https://iptv-org.github.io/epg/guides/my/astro.com.my.epg.xml"

# Database EPG ID Presisi & Logo CDN Publik Berkualitas Tinggi
EPG_LOGO_DB = {
    # Saluran Malaysia Utama
    "tv1": {"id": "TV1.my", "name": "TV1", "logo": "https://raw.githubusercontent.com/iptv-org/iptv/master/logos/TV1.my.png", "group": "General"},
    "tv2": {"id": "TV2.my", "name": "TV2", "logo": "https://raw.githubusercontent.com/iptv-org/iptv/master/logos/TV2.my.png", "group": "General"},
    "tv3": {"id": "TV3.my", "name": "TV3", "logo": "https://raw.githubusercontent.com/iptv-org/iptv/master/logos/TV3.my.png", "group": "Entertainment"},
    "tv9": {"id": "TV9.my", "name": "TV9", "logo": "https://raw.githubusercontent.com/iptv-org/iptv/master/logos/TV9.my.png", "group": "Entertainment"},
    "8tv": {"id": "8TV.my", "name": "8TV", "logo": "https://raw.githubusercontent.com/iptv-org/iptv/master/logos/8TV.my.png", "group": "Entertainment"},
    "8 tv": {"id": "8TV.my", "name": "8TV", "logo": "https://raw.githubusercontent.com/iptv-org/iptv/master/logos/8TV.my.png", "group": "Entertainment"},
    "tv okey": {"id": "TVOkey.my", "name": "TV Okey", "logo": "https://raw.githubusercontent.com/iptv-org/iptv/master/logos/TVOkey.my.png", "group": "Entertainment"},
    "ntv7": {"id": "NTV7.my", "name": "NTV7", "logo": "https://raw.githubusercontent.com/iptv-org/iptv/master/logos/NTV7.my.png", "group": "Entertainment"},
    "drama sangat": {"id": "DramaSangat.my", "name": "Drama Sangat", "logo": "https://raw.githubusercontent.com/iptv-org/iptv/master/logos/DramaSangat.my.png", "group": "Series"},
    "astro awani": {"id": "AstroAwani.my", "name": "Astro Awani", "logo": "https://raw.githubusercontent.com/iptv-org/iptv/master/logos/AstroAwani.my.png", "group": "News"},
    "awesome tv": {"id": "AwesomeTV.my", "name": "Awesome TV", "logo": "https://raw.githubusercontent.com/iptv-org/iptv/master/logos/AwesomeTV.my.png", "group": "Entertainment"},
    "bernama tv": {"id": "BernamaTV.my", "name": "Bernama TV", "logo": "https://raw.githubusercontent.com/iptv-org/iptv/master/logos/BernamaTV.my.png", "group": "News"},
    "sinar tv": {"id": "SinarTV.my", "name": "Sinar TV", "logo": "https://raw.githubusercontent.com/iptv-org/iptv/master/logos/SinarTV.my.png", "group": "News"},
    "sukan rtm": {"id": "SukanRTM.my", "name": "Sukan RTM", "logo": "https://raw.githubusercontent.com/iptv-org/iptv/master/logos/SukanRTM.my.png", "group": "Sports"},
    "berita rtm": {"id": "BeritaRTM.my", "name": "Berita RTM", "logo": "https://raw.githubusercontent.com/iptv-org/iptv/master/logos/BeritaRTM.my.png", "group": "News"},
    "ikim": {"id": "IKIMTV.my", "name": "IKIM TV", "logo": "https://raw.githubusercontent.com/iptv-org/iptv/master/logos/IKIMTV.my.png", "group": "Religious"},
    "suke": {"id": "SukeTV.my", "name": "Suke TV", "logo": "https://raw.githubusercontent.com/iptv-org/iptv/master/logos/SukeTV.my.png", "group": "Shopping"},
    "selangor": {"id": "SelangorTV.my", "name": "Selangor TV", "logo": "https://raw.githubusercontent.com/iptv-org/iptv/master/logos/SelangorTV.my.png", "group": "Local"},

    # Saluran Internasional Publik
    "al jazeera": {"id": "AlJazeeraEnglish.qa", "name": "Al Jazeera English", "logo": "https://raw.githubusercontent.com/iptv-org/iptv/master/logos/AlJazeeraEnglish.qa.png", "group": "News"},
    "bbc earth": {"id": "BBCEarth.uk", "name": "BBC Earth", "logo": "https://raw.githubusercontent.com/iptv-org/iptv/master/logos/BBCEarth.uk.png", "group": "Documentary"},
    "bbc news": {"id": "BBCNews.uk", "name": "BBC News", "logo": "https://raw.githubusercontent.com/iptv-org/iptv/master/logos/BBCNews.uk.png", "group": "News"},
    "being sports 1": {"id": "beINSports1.qa", "name": "beIN Sports 1", "logo": "https://raw.githubusercontent.com/iptv-org/iptv/master/logos/beINSports1.qa.png", "group": "Sports"},
    "mastiii tv": {"id": "Mastiii.in", "name": "Mastiii TV", "logo": "https://raw.githubusercontent.com/iptv-org/iptv/master/logos/Mastiii.in.png", "group": "Music"},
    "miramax movie": {"id": "MiramaxMovieChannel.us", "name": "Miramax Movie Channel", "logo": "https://raw.githubusercontent.com/iptv-org/iptv/master/logos/MiramaxMovieChannel.us.png", "group": "Movies"},
    "pitaara movie": {"id": "PitaaraTV.in", "name": "Pitaara TV", "logo": "https://raw.githubusercontent.com/iptv-org/iptv/master/logos/PitaaraTV.in.png", "group": "Movies"},
    "scripps news": {"id": "ScrippsNews.us", "name": "Scripps News", "logo": "https://raw.githubusercontent.com/iptv-org/iptv/master/logos/ScrippsNews.us.png", "group": "News"},
    "filmrise movies": {"id": "FilmRise.us", "name": "FilmRise Movies", "logo": "https://raw.githubusercontent.com/iptv-org/iptv/master/logos/FilmRise.us.png", "group": "Entertainment"},
    "livenow from fox news": {"id": "LiveNOWfromFOX.us", "name": "LiveNOW from FOX", "logo": "https://raw.githubusercontent.com/iptv-org/iptv/master/logos/LiveNOWfromFOX.us.png", "group": "News"},
    "unxplained zone": {"id": "TheUnXplainedZone.us", "name": "The UnXplained Zone", "logo": "https://raw.githubusercontent.com/iptv-org/iptv/master/logos/TheUnXplainedZone.us.png", "group": "Documentary"}
}

# 15 Kategori Resmi Baku
CATEGORY_KEYWORD_MAP = {
    "News": ["news", "berita", "warta", "informasi", "politics", "politik"],
    "Movies": ["movie", "cinema", "film", "wayang", "box office"],
    "Series": ["series", "drama", "sinetron", "serial"],
    "Kids": ["kids", "kartun", "cartoon", "children", "kanak", "anak", "ceria"],
    "Sports": ["sport", "sukan", "bola", "football", "racing", "stadium", "espn", "afl", "mlb", "raket"],
    "Music": ["music", "musik", "lagu", "hits", "radio", "mastiii"],
    "Documentary": ["documentary", "dokumentari", "history", "sejarah", "nat geo", "discovery", "earth", "unxplained"],
    "Religious": ["religion", "religious", "islam", "agama", "rohani", "dakwah", "ikim"],
    "Lifestyle": ["lifestyle", "gaya hidup", "fashion", "food", "masak"],
    "Shopping": ["shopping", "shop", "belanja", "suke"],
    "Travel": ["travel", "pelancongan", "wisata", "explore"],
    "Knowledge": ["knowledge", "education", "pendidikan", "sains"],
    "Local": ["local", "lokal", "daerah", "negeri", "selangor", "perak", "sabah", "sarawak"],
    "Entertainment": ["entertainment", "hiburan", "variety", "show"]
}

def clean_slug(slug):
    name = slug.rstrip("/").split("/")[-1]
    name = name.replace("-live", "").replace("-tv", " TV").replace("-", " ")
    return name.lower().strip()

def get_smart_metadata(raw_slug_name, web_logo=""):
    clean_key = clean_slug(raw_slug_name)

    # 1. Matching dengan database EPG presisi
    for key, data in EPG_LOGO_DB.items():
        if key == clean_key or key in clean_key or clean_key in key:
            return data

    # 2. Fallback Kategori Otomatis jika tidak terdaftar di EPG_LOGO_DB
    final_group = "General"
    for cat, keywords in CATEGORY_KEYWORD_MAP.items():
        if any(kw in clean_key for kw in keywords):
            final_group = cat
            break

    formatted_name = raw_slug_name.replace("-live", "").replace("-", " ").title()
    formatted_id = f"{re.sub(r'[^a-zA-Z0-9]', '', formatted_name)}.my"

    return {
        "id": formatted_id,
        "name": formatted_name,
        "logo": web_logo,
        "group": final_group
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

        print("[*] Membuka halaman indeks...")
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
                    # Abaikan halaman kategori non-channel seperti bola-sepak
                    if not any(kw in clean_url for kw in ignore_keywords) and clean_url != "https://malaysia-tv.net/":
                        if "bola-sepak" not in clean_url:  # Filter halaman kategori sports ganda
                            found_urls.add(clean_url)

            found_urls.add(BASE_URL)
            print(f"[✓] Berhasil mengindeks {len(found_urls)} URL saluran!")

        except Exception as e:
            print(f"[!] Error saat membaca grid halaman: {e}")
            browser.close()
            return []

        page.close()

        print("\n[*] Mengekstrak Stream, Matching EPG ID, & Logo CDN...")
        for ch_url in sorted(found_urls):
            raw_slug = ch_url.rstrip("/").split("/")[-1]
            ch_page = context.new_page()

            stream_url = None
            extracted_logo = ""

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
                    og_image = ch_page.locator('meta[property="og:image"]').get_attribute("content")
                    if og_image and "http" in og_image:
                        extracted_logo = og_image
                except Exception:
                    pass

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
                meta = get_smart_metadata(raw_slug, web_logo=extracted_logo)
                print(f"[✓] [{meta['group']}] {meta['name']} -> EPG ID: {meta['id']}")

                valid_channels.append({
                    "id": meta["id"],
                    "name": meta["name"],
                    "logo": meta["logo"],
                    "group": meta["group"],
                    "url": f"{stream_url}{header_pipe}"
                })

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

    print(f"\n[SUCCESS] Berhasil memperbarui {len(channels)} saluran dengan EPG & Logo presisi!")

if __name__ == "__main__":
    main()
