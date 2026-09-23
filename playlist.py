import time
from playwright.sync_api import sync_playwright

CHANNELS = [
    {"name": "Sukan+", "slug": "sukan-rtm"},
    {"name": "TV3", "slug": "tv3"}
]

def get_stream_url(slug):
    target_url = f"https://malaysia-tv.net/{slug}/"
    stream_url = ""
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36"
        )
        
        def handle_request(request):
            nonlocal stream_url
            if ".m3u8" in request.url:
                stream_url = request.url

        page.on("request", handle_request)
        
        try:
            page.goto(target_url, timeout=60000, wait_until="networkidle")
            if not stream_url:
                time.sleep(5)
        except Exception as e:
            print(f"Error mengambil {slug}: {e}")
        finally:
            browser.close()
            
    return stream_url

def update_m3u():
    m3u_content = "#EXTM3U\n"
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36"
    headers_suffix = f"|User-Agent={user_agent}&Origin=https://malaysia-tv.net&Referer=https://malaysia-tv.net/"
    
    for ch in CHANNELS:
        print(f"Mencari link untuk: {ch['name']}...")
        url = get_stream_url(ch['slug'])
        if url:
            print(f"Berhasil mendapatkan link: {url}")
            # Format lengkap dengan KODIPROP dan suffix header pipe
            m3u_content += f'#EXTINF:-1 tvg-id="" tvg-name="" tvg-logo="" group-title="Sports",{ch["name"]}\n'
            m3u_content += '#KODIPROP:inputstreamaddon=inputstream.adaptive\n'
            m3u_content += '#KODIPROP:inputstream.adaptive.manifest_type=hls\n'
            m3u_content += f'#KODIPROP:inputstream.adaptive.stream_headers=User-Agent={user_agent}&Origin=https://malaysia-tv.net&Referer=https://malaysia-tv.net/\n'
            m3u_content += f'{url}{headers_suffix}\n'
        else:
            print(f"Gagal mendapatkan link untuk {ch['name']}")
            m3u_content += f'#EXTINF:-1 group-title="Sports",{ch["name"]}\nhttps://error-link-not-found\n'

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)
    print("Playlist M3U berhasil diperbarui dengan format yang valid!")

if __name__ == "__main__":
    update_m3u()
