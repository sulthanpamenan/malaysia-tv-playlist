import time
from flask import Flask, Response
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
        
        def handle_request(request):
            nonlocal stream_url
            if ".m3u8" in request.url:
                stream_url = request.url

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
    m3u_content = "#EXTM3U\n"
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36"
    headers_suffix = f"|User-Agent={user_agent}&Origin=https://malaysia-tv.net&Referer=https://malaysia-tv.net/"
    
    for ch in CHANNELS:
        url = get_stream_url(ch['slug'])
        if url:
            m3u_content += f'#EXTINF:-1 tvg-id="" tvg-name="" tvg-logo="" group-title="Malaysian Channels",{ch["name"]}\n'
            m3u_content += '#KODIPROP:inputstreamaddon=inputstream.adaptive\n'
            m3u_content += '#KODIPROP:inputstream.adaptive.manifest_type=hls\n'
            m3u_content += f'#KODIPROP:inputstream.adaptive.stream_headers=User-Agent={user_agent}&Origin=https://malaysia-tv.net&Referer=https://malaysia-tv.net/\n'
            m3u_content += f'{url}{headers_suffix}\n'
            
    return Response(m3u_content, mimetype="audio/x-mpegurl")

@app.route('/')
def home():
    return "IPTV Dynamic Server is running! Use /playlist.m3u in your IPTV player."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
