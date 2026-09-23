import time
from flask import Flask, Response, redirect, request
from playwright.sync_api import sync_playwright

app = Flask(__name__)

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
        
        def handle_request(req):
            nonlocal stream_url
            if ".m3u8" in req.url:
                stream_url = req.url

        page.on("request", handle_request)
        
        try:
            page.goto(target_url, timeout=30000, wait_until="networkidle")
            if not stream_url:
                time.sleep(3)
        except Exception:
            pass
        finally:
            browser.close()
            
    return stream_url

@app.route('/playlist.m3u')
def generate_playlist():
    # Menggunakan domain server secara dinamis
    server_base = request.host_url.rstrip('/')
    
    m3u_content = "#EXTM3U\n"
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36"
    
    for ch in CHANNELS:
        # Setiap channel mengarah ke endpoint proxy /play/<slug>
        play_url = f"{server_base}/play/{ch['slug']}"
        headers_suffix = f"|User-Agent={user_agent}&Origin=https://malaysia-tv.net&Referer=https://malaysia-tv.net/"
        
        m3u_content += f'#EXTINF:-1 tvg-id="" tvg-name="" tvg-logo="" group-title="Malaysian Channels",{ch["name"]}\n'
        m3u_content += '#KODIPROP:inputstreamaddon=inputstream.adaptive\n'
        m3u_content += '#KODIPROP:inputstream.adaptive.manifest_type=hls\n'
        m3u_content += f'#KODIPROP:inputstream.adaptive.stream_headers=User-Agent={user_agent}&Origin=https://malaysia-tv.net&Referer=https://malaysia-tv.net/\n'
        m3u_content += f'{play_url}{headers_suffix}\n'
            
    return Response(m3u_content, mimetype="audio/x-mpegurl")

@app.route('/play/<slug>')
def play_channel(slug):
    # Hanya cari token untuk 1 channel yang sedang diklik saat itu juga
    url = get_stream_url(slug)
    if url:
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36"
        headers_suffix = f"|User-Agent={user_agent}&Origin=https://malaysia-tv.net&Referer=https://malaysia-tv.net/"
        final_url = f"{url}{headers_suffix}"
        return redirect(final_url)
    
    return "Stream link not found or expired", 404

@app.route('/')
def home():
    return "IPTV Proxy Server is running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
