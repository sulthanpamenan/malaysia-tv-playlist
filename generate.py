import sys
import re
from playwright.sync_api import sync_playwright

BASE_URL = "https://malaysia-tv.net/tv3-live/"

def run_scraper():
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    referer = "https://malaysia-tv.net/"
    header_pipe = f"|User-Agent={ua}&Referer={referer}"

    valid_channels = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent=ua, permissions=["autoplay"])
        page = context.new_page()

        print("[*] Tahap 1: Membuka indeks situs & mengumpulkan semua link channel dari grid...")
        try:
            page.goto(BASE_URL, timeout=40000, wait_until="domcontentloaded")
            page.wait_for_timeout(3000)

            # Mengambil semua tautan <a> yang mengarah ke halaman channel
            links = page.locator("a[href*='malaysia-tv.net/']").all()
            found_urls = set()

            for link in links:
                href = link.get_attribute("href")
                if href and href != BASE_URL and not href.endswith(".png") and not href.endswith(".jpg"):
                    # Pastikan URL bersih dari fragment
                    clean_url = href.split("#")[0]
                    found_urls.add(clean_url)

            # Tambahkan halaman awal
            found_urls.add(BASE_URL)
            print(f"[✓] Berhasil menemukan {len(found_urls)} URL halaman channel di situs!")

        except Exception as e:
            print(f"[!] Error saat mengambil indeks grid: {e}")
            browser.close()
            return []

        page.close()

        print("\n[*] Tahap 2: Mengekstrak token M3U8 untuk setiap channel...")
        for ch_url in sorted(found_urls):
            # Membuat nama channel bersih dari URL slug
            slug = ch_url.rstrip("/").split("/")[-1].replace("-live", "").replace("-", " ").title()
            ch_page = context.new_page()
            print(f"[*] Scraping channel: {slug} ({ch_url})...")

            stream_url = None

            # Tangkap network request ke BunnyCDN / Streamer
            def handle_request(request):
                nonlocal stream_url
                req_url = request.url
                if ".m3u8" in req_url and ("b-cdn.net" in req_url or "streamer" in req_url or "playlist" in req_url):
                    if not stream_url:
                        stream_url = req_url

            ch_page.on("request", handle_request)

            try:
                ch_page.goto(ch_url, timeout=35000, wait_until="domcontentloaded")
                ch_page.wait_for_timeout(2000)

                # Coba klik player jika ada iframe
                try:
                    for frame in ch_page.frames:
                        play_btn = frame.locator("video, .play-button, #player, .vjs-big-play-button")
                        if play_btn.count() > 0:
                            play_btn.first.click(timeout=1500)
                except Exception:
                    pass

                # Tunggu request .m3u8 tertangkap
                for _ in range(8):
                    if stream_url:
                        break
                    ch_page.wait_for_timeout(1000)

            except Exception as e:
                print(f"[!] Error saat memuat {slug}: {e}")

            if stream_url:
                print(f"[✓] Berhasil mengekstrak stream untuk {slug}!")
                valid_channels.append({
                    "name": slug,
                    "url": f"{stream_url}{header_pipe}"
                })
            else:
                print(f"[!] Stream M3U8 tidak ditemukan untuk {slug}")

            ch_page.close()

        browser.close()

    return valid_channels

def main():
    channels = run_scraper()

    if not channels:
        print("[X] Gagal mengekstrak channel.")
        sys.exit(1)

    m3u_lines = ["#EXTM3U"]
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    referer = "https://malaysia-tv.net/"

    for ch in channels:
        m3u_lines.append(f'#EXTINF:-1 group-title="Malaysia TV Net", (🇲🇾) {ch["name"]}')
        m3u_lines.append(f'#EXTVLCOPT:http-user-agent={ua}')
        m3u_lines.append(f'#EXTVLCOPT:http-referrer={referer}')
        m3u_lines.append(ch["url"])

    m3u_content = "\r\n".join(m3u_lines)

    with open("playlist.txt", "w", encoding="utf-8") as f:
        f.write(m3u_content)

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)

    print(f"\n[SUCCESS] Berhasil memperbarui {len(channels)} saluran dari malaysia-tv.net!")

if __name__ == "__main__":
    main()
