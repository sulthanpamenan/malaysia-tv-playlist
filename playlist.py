import time
from playwright.sync_api import sync_playwright

CHANNELS = [
    {"name": "Sukan RTM", "slug": "sukan-rtm"},
    {"name": "TV1", "slug": "rtm-tv1-live"},
    {"name": "TV2", "slug": "rtm-tv2-live"},
    {"name": "TV3", "slug": "tv3"},
    {"name": "TV9", "slug": "tv9"},
    {"name": "TV Okey", "slug": "tv-okey"},
    {"name": "Berita RTM", "slug": "berita-rtm"},
    {"name": "TVNT", "slug": "tvnt"},
    {"name": "Awesome TV", "slug": "awesome-tv"}
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
                time.sleep(4)
        except Exception as e:
            print(f"Error retrieving {slug}: {e}")
        finally:
            browser.close()
            
    return stream_url

def update_m3u():
    m3u_content = "#EXTM3U\n"
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36"
    headers_suffix = f"|User-Agent={user_agent}&Origin=https://malaysia-tv.net&Referer=https://malaysia-tv.net/"
    
    print(f"Processing {len(CHANNELS)} channels...")
    
    for ch in CHANNELS:
        print(f"Processing: {ch['name']} ({ch['slug']})...")
        url = get_stream_url(ch['slug'])
        if url:
            print(f"  -> Success: {url}")
            m3u_content += f'#EXTINF:-1 tvg-id="" tvg-name="" tvg-logo="" group-title="Malaysian Channels",{ch["name"]}\n'
            m3u_content += '#KODIPROP:inputstreamaddon=inputstream.adaptive\n'
            m3u_content += '#KODIPROP:inputstream.adaptive.manifest_type=hls\n'
            m3u_content += f'#KODIPROP:inputstream.adaptive.stream_headers=User-Agent={user_agent}&Origin=https://malaysia-tv.net&Referer=https://malaysia-tv.net/\n'
            m3u_content += f'{url}{headers_suffix}\n'
        else:
            print(f"  -> Failed to get the link for {ch['name']}")

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)
    print("The M3U playlist has been successfully updated!")

if __name__ == "__main__":
    update_m3u()
