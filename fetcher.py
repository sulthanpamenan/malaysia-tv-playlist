import os
import time
import json
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from playwright.sync_api import sync_playwright

GIST_ID = os.environ.get("GIST_ID", "6055fb9a0d9c3754edc6cf956cdbf762")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN") 
GIST_FILENAME = os.environ.get("GIST_FILENAME", "malaysia_tv.json")
GIST_API_URL = f"https://api.github.com/gists/{GIST_ID}"

CHANNELS = [
    # --- TV Category ---
    {"name": "TV3", "slug": "tv3-live", "group": "General", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/General/TV3.png", "type": "tv"},
    {"name": "Drama Sangat", "slug": "drama-sangat", "group": "Drama", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/Drama/Drama%20Sangat.png", "type": "tv"},
    {"name": "TV1", "slug": "rtm-tv1-live", "group": "General", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/General/RTM%20TV1.png", "type": "tv"},
    {"name": "DidikTV KPM", "slug": "didik-tv-live", "group": "Education", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/Education/DidikTV%20KPM.png", "type": "tv"},
    {"name": "FIFA+", "slug": "fifa-plus", "group": "Sports", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/Sports/FIFA+.png", "type": "tv"},
    {"name": "TV9", "slug": "tv9-malaysia", "group": "General", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/General/TV9%20(Malaysia).png", "type": "tv"},
    {"name": "TV2", "slug": "tv2-live", "group": "General", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/General/RTM%20TV2.png", "type": "tv"},
    {"name": "TV AlHijrah", "slug": "al-hijrah", "group": "Religious", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/Religious/TV%20AlHijrah.png", "type": "tv"},
    {"name": "Sukan+", "slug": "sukan-rtm", "group": "Sports", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/Sports/RTM%20Sukan+.png", "type": "tv"},
    {"name": "Berita RTM", "slug": "berita-waliyah", "group": "News + Opinion", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/News%20+%20Opinion/Berita%20RTM.png", "type": "tv"},
    {"name": "Bernama TV", "slug": "bernama", "group": "News + Opinion", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/News%20+%20Opinion/Bernama%20TV.png", "type": "tv"},
    {"name": "Okey", "slug": "okey", "group": "General", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/General/Okey.png", "type": "tv"},
    {"name": "TV IKIM", "slug": "ikim-live", "group": "Religious", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/Religious/TV%20IKIM.png", "type": "tv"},
    {"name": "8TV", "slug": "8-tv", "group": "General", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/General/8TV.png", "type": "tv"},
    {"name": "TV Sarawak", "slug": "tv-sarawak-live", "group": "Local", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/Local/TV%20Sarawak.png", "type": "tv"},
    {"name": "MPL Malaysia", "slug": "mpl-malaysia", "group": "Sports", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/Sports/MPL%20Malaysia.png", "type": "tv"},
    {"name": "Free Movies", "slug": "free-movies", "group": "Movies", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/Movies/Free%20Movies.png", "type": "tv"},
    {"name": "PPA Asia Tier Badges KL Cup", "slug": "ppa-kl-cup", "group": "Live Sports", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/Live%20Events/PPA%20Asia%20Tier%20Badges%20KL%20Cup.png", "type": "tv"},
    {"name": "Siara TV", "slug": "siara-tv", "group": "Testing", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/Testing/Siara%20TV.png", "type": "tv"},
    {"name": "MySports", "slug": "mysport", "group": "Sports", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/Sports/MySports.png", "type": "tv"},
    {"name": "USIM TV", "slug": "usim-tv", "group": "Education", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/Education/USIM%20TV.png", "type": "tv"},
    {"name": "Borneo TV", "slug": "borneo-tv", "group": "Local", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/Local/Borneo%20TV.png", "type": "tv"},
    {"name": "BeIN Sports 1", "slug": "being-sports-1", "group": "Sports", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/Sports/beIN%20Sports%201.png", "type": "tv"},
    {"name": "Tennis+", "slug": "tennis", "group": "Sports", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/Sports/Tennis+.png", "type": "tv"},
    {"name": "Pickle TV", "slug": "pickle-tv", "group": "Sports", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/Sports/Pickle%20TV%20-%20white.png", "type": "tv"},
    {"name": "Shemaroo Bollywood Classic", "slug": "shemaroo-bollywood-classic", "group": "Classic TV", "logo": "", "type": "tv"},
    {"name": "Bollywood Prime", "slug": "bollywood-prime-live", "group": "Movies", "logo": "", "type": "tv"},
    {"name": "Bollywood Masala", "slug": "bollywood-masala-live", "group": "Movies", "logo": "", "type": "tv"},
    {"name": "Shemaroo Filmigaane", "slug": "shemaroo-filmigaane-live", "group": "Music Videos", "logo": "", "type": "tv"},
    {"name": "Pitaara Movie", "slug": "pitaara-movie-live", "group": "Movies", "logo": "", "type": "tv"},
    {"name": "Shemaroo Umang Plus", "slug": "shemaroo-umang-plus-live", "group": "Drama", "logo": "", "type": "tv"},
    {"name": "Mastiii TV", "slug": "mastiii-tv-live", "group": "Music Videos", "logo": "", "type": "tv"},
    {"name": "Miramax Movie", "slug": "miramax-movie", "group": "Movies", "logo": "", "type": "tv"},
    {"name": "FILMRISE Movies", "slug": "filmrise-movies", "group": "Movies", "logo": "", "type": "tv"},
    {"name": "GoUSA TV", "slug": "gousa-tv-live", "group": "Lifestyle", "logo": "", "type": "tv"},
    {"name": "euro News", "slug": "euro-news-live", "group": "News + Opinion", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/News%20+%20Opinion/Euronews.png", "type": "tv"},
    {"name": "ION NCIS", "slug": "ion-ncis", "group": "Drama", "logo": "", "type": "tv"},
    {"name": "Nosey TV", "slug": "nosey-tv", "group": "Entertainment", "logo": "", "type": "tv"},
    {"name": "FailArmy Channel", "slug": "failarmy-tv", "group": "Comedy", "logo": "", "type": "tv"},
    {"name": "BBC News", "slug": "bbc-news-live", "group": "News + Opinion", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/News%20+%20Opinion/BBC%20News.png", "type": "tv"},

    # --- Radio Category ---
    {"name": "Manis FM", "slug": "manis-fm", "group": "Radio - Malaysia", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/Radio/Manis%20FM.png", "type": "radio"},
    {"name": "Suria FM", "slug": "suria-fm", "group": "Radio - Malaysia", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/Radio/Suria%20FM.png", "type": "radio"},
    {"name": "Fly FM", "slug": "fly-fm", "group": "Radio - Malaysia", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/Radio/Fly%20FM.png", "type": "radio"},
    {"name": "Hot FM", "slug": "hot-fm", "group": "Radio - Malaysia", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/Radio/Hot%20FM.png", "type": "radio"},
    {"name": "IKIM FM", "slug": "ikim-fm", "group": "Radio - Malaysia", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/Radio/IKIM%20FM.png", "type": "radio"},
    {"name": "Molek FM", "slug": "molek-fm", "group": "Radio - Malaysia", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/Radio/Molek%20FM.png", "type": "radio"},
    {"name": "Eight无限", "slug": "eight-fm", "group": "Radio - Malaysia", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/Radio/Eight无限.png", "type": "radio"},
    {"name": "Kool FM", "slug": "kool-fm", "group": "Radio - Malaysia", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/Radio/Kool%20FM.png", "type": "radio"},
    {"name": "Bernama Radio", "slug": "bernama-radio", "group": "Radio - Malaysia", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/Radio/Bernama%20Radio.png", "type": "radio"},
    {"name": "Best FM", "slug": "best-fm", "group": "Radio - Malaysia", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/Radio/Best%20FM.png", "type": "radio"}
]

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36"

def get_stream_url(slug):
    target_url = f"https://malaysia-tv.net/{slug}/"
    stream_url = ""
    
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox"]
        )
        page = browser.new_page(user_agent=USER_AGENT)
        
        def handle_request(request):
            nonlocal stream_url
            url = request.url
            if ".m3u8" in url and not any(ext in url for ext in [".aac", ".ts", ".mp3", ".js", "player-init"]):
                if not stream_url or "streamer/" in url:
                    stream_url = url

        page.on("request", handle_request)
        
        try:
            page.goto(target_url, timeout=30000, wait_until="domcontentloaded")
            for _ in range(12):
                if stream_url:
                    break
                time.sleep(0.5)
        except Exception:
            pass
        finally:
            browser.close()
            
    return stream_url

def process_single_channel(ch):
    url = get_stream_url(ch['slug'])
    if url:
        print(f"[{ch['name']}] -> Success")
        return ch['slug'], url
    else:
        print(f"[{ch['name']}] -> Failed")
        return ch['slug'], None

def save_gist_tokens(tokens):
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json"
    }
    payload = {
        "files": {
            GIST_FILENAME: {
                "content": json.dumps(tokens, indent=4)
            }
        }
    }
    res = requests.patch(GIST_API_URL, headers=headers, json=payload, timeout=10)
    res.raise_for_status()
    print("[✓] Malaysia TV tokens successfully updated to Gist!")

if __name__ == "__main__":
    print(f"Processing total {len(CHANNELS)} items with Multi-threading...")
    results = {}
    
    with ThreadPoolExecutor(max_workers=9) as executor:
        future_to_channel = {executor.submit(process_single_channel, ch): ch for ch in CHANNELS}
        for future in as_completed(future_to_channel):
            slug, url = future.result()
            if url:
                results[slug] = {"url": url}

    if results:
        try:
            save_gist_tokens(results)
        except Exception as e:
            print(f"[!] Failed to save tokens to Gist: {e}")
