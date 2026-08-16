import sys
import os
import re
from playwright.sync_api import sync_playwright

BASE_URL = "https://malaysia-tv.net/tv3-live/"
EPG_URL = "https://iptv-org.github.io/epg/guides/my/astro.com.my.epg.xml"

def clean_channel_name(slug):
    name = slug.rstrip("/").split("/")[-1]
    name = name.replace("-live", "").replace("-tv", " TV").replace("-", " ")
    return name.title().strip()

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
            ignore_keywords = [
                "/category/", "/tag/", "/contact", "/privacy", "/terms", 
                ".png", ".jpg", ".jpeg", ".css", ".js", "#", 
                "facebook.com", "twitter.com"
            ]

            for link in all_links:
                href = link.get_attribute("href")
                if href and "malaysia-tv.net" in href:
                    clean_url = href.split("#")[0].rstrip("/") + "/"
                    if not any(kw in clean_url for kw in ignore_keywords) and clean_url != "https://malaysia-tv.net/":
                        found_urls.add(clean_url)

            found_urls.add(BASE_URL)
            print(f"[✓] Berhasil mengindeks {len(found_urls)} URL saluran dari halaman web!")

        except Exception as e:
            print(f"[!] Error saat membaca grid halaman: {e}")
            browser.close()
            return []

        page.close()

        print("\n[*] Tahap 2: Mengekstrak Stream, Logo, & Kategori secara otomatis...")
        for ch_url in sorted(found_urls):
            raw_name = clean_channel_name(ch_url)
            ch_page = context.new_page()
            print(f"[*] Scraping channel: {raw_name}...")

            stream_url = None
            extracted_logo = ""
            extracted_group = "Malaysia"

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

                # 1. Ekstraksi Logo Otomatis dari Meta Tag / Elemen Gambar Halaman Web
                try:
                    og_image = ch_page.locator('meta[property="og:image"]').get_attribute("content")
                    if og_image and "http" in og_image:
                        extracted_logo = og_image
                    else:
                        img_element = ch_page.locator("article img, .entry-content img, #player img").first
                        if img_element.count() > 0:
                            src = img_element.get_attribute("src")
                            if src and "http" in src:
                                extracted_logo = src
                except Exception:
                    pass

                # 2. Ekstraksi Kategori Otomatis dari Category Tag / Breadcrumb Halaman Web
                try:
                    cat_element = ch_page.locator('.cat-links a, .entry-category a, a[rel="category tag"]').first
                    if cat_element.count() > 0:
                        cat_text = cat_element.inner_text().strip().title()
                        if cat_text:
                            extracted_group = cat_text
                except Exception:
                    pass

                # 3. Intersepsi Tombol Play / Player Video
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
                print(f"[!] Error/Timeout saat memuat {raw_name}: {e}")

            if stream_url:
                # Format EPG ID secara otomatis dari nama saluran
                epg_id = f"{re.sub(r'[^a-zA-Z0-9]', '', raw_name)}.my"
                print(f"[✓] Berhasil [{extracted_group}]: {raw_name} (EPG ID: {epg_id})")
                
                valid_channels.append({
                    "id": epg_id,
                    "name": raw_name,
                    "logo": extracted_logo,
                    "group": extracted_group,
                    "url": f"{stream_url}{header_pipe}"
                })
            else:
                print(f"[x] Skip (Bukan M3U8): {raw_name}")

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

    # Menyusun isi M3U dengan header url-tvg
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

    print(f"\n[SUCCESS] Berhasil memperbarui {len(channels)} saluran secara otomatis dari malaysia-tv.net!")

if __name__ == "__main__":
    main()
