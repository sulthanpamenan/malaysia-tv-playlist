import sys
import os
from playwright.sync_api import sync_playwright

BASE_URL = "https://malaysia-tv.net/tv3-live/"

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

        print("[*] Tahap 1: Membuka indeks & me-scan seluruh 72 channel grid...")
        found_urls = set()
        
        try:
            page.goto(BASE_URL, timeout=60000, wait_until="domcontentloaded")
            page.wait_for_timeout(4000)

            # Scroll lebih lambat agar lazy loading memuat semua gambar/link
            for _ in range(12):
                page.mouse.wheel(0, 1200)
                page.wait_for_timeout(600)

            # Ambil semua <a> yang ada di dalam main wrapper
            all_links = page.locator("a").all()
            ignore_keywords = ["/category/", "/tag/", "/contact", "/privacy", "/terms", ".png", ".jpg", ".jpeg", ".css", ".js", "#", "facebook.com", "twitter.com"]

            for link in all_links:
                href = link.get_attribute("href")
                if href and "malaysia-tv.net" in href:
                    clean_url = href.split("#")[0].rstrip("/") + "/"
                    if not any(kw in clean_url for kw in ignore_keywords) and clean_url != "https://malaysia-tv.net/":
                        found_urls.add(clean_url)

            found_urls.add(BASE_URL)
            print(f"[✓] Berhasil mengindeks {len(found_urls)} URL dari grid situs!")

        except Exception as e:
            print(f"[!] Error saat membaca grid halaman: {e}")
            browser.close()
            return []

        page.close()

        print("\n[*] Tahap 2: Mengekstrak token M3U8...")
        for ch_url in sorted(found_urls):
            slug = ch_url.rstrip("/").split("/")[-1].replace("-live", "").replace("-", " ").title()
            ch_page = context.new_page()
            print(f"[*] Scraping channel: {slug}...")

            stream_url = None

            def handle_request(request):
                nonlocal stream_url
                req_url = request.url
                # Cari pola manifest m3u8 atau hls stream
                if ".m3u8" in req_url and ("b-cdn.net" in req_url or "streamer" in req_url or "playlist" in req_url or "live" in req_url or "hls" in req_url):
                    if not stream_url:
                        stream_url = req_url

            ch_page.on("request", handle_request)

            try:
                ch_page.goto(ch_url, timeout=40000, wait_until="domcontentloaded")
                ch_page.wait_for_timeout(3000)

                # Paksa trigger play pada player iframe
                try:
                    for frame in ch_page.frames:
                        play_btn = frame.locator("video, .play-button, #player, .vjs-big-play-button, .player-poster, iframe")
                        if play_btn.count() > 0:
                            play_btn.first.click(timeout=1000)
                except Exception:
                    pass

                # Berikan jeda toleransi lebih lama agar CDN merespons token
                for _ in range(10):
                    if stream_url:
                        break
                    ch_page.wait_for_timeout(1000)

            except Exception as e:
                print(f"[!] Error/Timeout saat memuat {slug}: {e}")

            if stream_url:
                print(f"[✓] Berhasil M3U8: {slug}")
                valid_channels.append({
                    "name": slug,
                    "url": f"{stream_url}{header_pipe}"
                })
            else:
                print(f"[x] Bukan M3U8 / Embed luar: {slug}")

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
        m3u_lines.append(f'#EXTINF:-1 group-title="Malaysia TV Net", (🇲🇾) {ch["name"]}\n')
        m3u_lines.append(f'#EXTVLCOPT:http-user-agent={ua}\n')
        m3u_lines.append(f'#EXTVLCOPT:http-referrer={referer}\n')
        m3u_lines.append(f'{ch["url"]}\n')

    m3u_content = "".join(m3u_lines)

    for filename in ["playlist.txt", "playlist.m3u"]:
        with open(filename, "w", encoding="utf-8", newline="\n") as f:
            f.write(m3u_content)

    print(f"\n[SUCCESS] Berhasil memperbarui {len(channels)} saluran M3U8 aktif ke playlist.m3u!")

if __name__ == "__main__":
    main()
