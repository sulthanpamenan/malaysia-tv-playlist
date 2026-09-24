import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from playwright.sync_api import sync_playwright

CHANNELS = [
    # --- TV Category ---
    {"name": "TV3", "slug": "tv3-live", "group": "General", "logo": "", "type": "tv"},
    {"name": "Drama Sangat", "slug": "drama-sangat", "group": "Drama", "logo": "", "type": "tv"},
    {"name": "RTM TV1", "slug": "rtm-tv1-live", "group": "General", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/General/RTM%20TV1.png", "type": "tv"},
    {"name": "DidikTV KPM", "slug": "didik-tv-live", "group": "Education", "logo": "", "type": "tv"},
    {"name": "FIFA+", "slug": "fifa-plus", "group": "Sports", "logo": "", "type": "tv"},
    {"name": "TV9 Malaysia", "slug": "tv9-malaysia", "group": "General", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/General/TV9%20Malaysia.png", "type": "tv"},
    {"name": "TV2", "slug": "tv2-live", "group": "General", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/General/TV2%20(Malaysia).png", "type": "tv"},
    {"name": "TV AlHijrah", "slug": "al-hijrah", "group": "Religious", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/Religious/TV%20AlHijrah.png", "type": "tv"},
    {"name": "Sukan+", "slug": "sukan-rtm", "group": "Sports", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/Sports/Sukan+.png", "type": "tv"},
    {"name": "Berita RTM", "slug": "berita-waliyah", "group": "News + Opinion", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/News%20+%20Opinion/Berita%20RTM.png", "type": "tv"},
    {"name": "Bernama TV", "slug": "bernama", "group": "News + Opinion", "logo": "", "type": "tv"},
    {"name": "Okey", "slug": "okey", "group": "General", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/General/Okey.png", "type": "tv"},
    {"name": "Selangor TV", "slug": "selangor", "group": "Local", "logo": "", "type": "tv"},
    {"name": "TV IKIM", "slug": "ikim-live", "group": "Religious", "logo": "", "type": "tv"},
    {"name": "8 TV", "slug": "8-tv", "group": "General", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/General/8TV.png", "type": "tv"},
    {"name": "TV Sarawak", "slug": "tv-sarawak-live", "group": "Local", "logo": "", "type": "tv"},
    {"name": "MPL Malaysia", "slug": "mpl-malaysia", "group": "Sports", "logo": "", "type": "tv"},
    {"name": "CNA", "slug": "cna", "group": "News + Opinion", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/News%20+%20Opinion/CNA.png", "type": "tv"},
    {"name": "PPA KL Cup", "slug": "ppa-kl-cup", "group": "Live Events", "logo": "", "type": "tv"},
    {"name": "DW", "slug": "dw", "group": "News + Opinion", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/News%20+%20Opinion/DW-TV.png", "type": "tv"},
    {"name": "Arirang", "slug": "arirang", "group": "General", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/Entertainment/Arirang%20TV.png", "type": "tv"},
    {"name": "The Indonesia Channel", "slug": "the-indonesia-channel", "group": "General", "logo": "", "type": "tv"},
    {"name": "Al Jazeera", "slug": "al-jazeera", "group": "News + Opinion", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/News%20+%20Opinion/Al%20Jazeera.png", "type": "tv"},
    {"name": "BeIN Sports 1", "slug": "being-sports-1", "group": "Sports", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/Sports/beIN%20Sports%201.png", "type": "tv"},
    {"name": "Tennis+", "slug": "tennis", "group": "Sports", "logo": "", "type": "tv"},
    {"name": "Pickle TV", "slug": "pickle-tv", "group": "Sports", "logo": "", "type": "tv"},
    {"name": "Cricket Gold", "slug": "cricket-live", "group": "Sports", "logo": "", "type": "tv"},
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
    {"name": "Rakita FM", "slug": "rakita-fm", "group": "Radio - Malaysia", "logo": "", "type": "radio"},
    {"name": "Hot FM", "slug": "hot-fm", "group": "Radio - Malaysia", "logo": "", "type": "radio"},
    {"name": "IKIM FM", "slug": "ikim-fm", "group": "Radio - Malaysia", "logo": "", "type": "radio"},
    {"name": "Molek FM", "slug": "molek-fm", "group": "Radio - Malaysia", "logo": "", "type": "radio"},
    {"name": "Eight FM", "slug": "eight-fm", "group": "Radio - Malaysia", "logo": "", "type": "radio"},
    {"name": "Kool FM", "slug": "kool-fm", "group": "Radio - Malaysia", "logo": "", "type": "radio"},
    {"name": "Nasional FM", "slug": "nasional-fm", "group": "Radio - Malaysia", "logo": "", "type": "radio"},
    {"name": "Minnal FM", "slug": "minnal-fm", "group": "Radio - Malaysia", "logo": "", "type": "radio"},
    {"name": "Ai FM", "slug": "ai-fm", "group": "Radio - Malaysia", "logo": "", "type": "radio"},
    {"name": "Radio Klasik", "slug": "radio-klasik", "group": "Radio - Malaysia", "logo": "", "type": "radio"},
    {"name": "Sabah FM", "slug": "sabah-fm", "group": "Radio - Malaysia", "logo": "", "type": "radio"},
    {"name": "Sarawak FM", "slug": "sarawak-fm", "group": "Radio - Malaysia", "logo": "", "type": "radio"},
    {"name": "Bernama Radio", "slug": "bernama-radio", "group": "Radio - Malaysia", "logo": "", "type": "radio"},
    {"name": "Asyik FM", "slug": "asyik-fm", "group": "Radio - Malaysia", "logo": "", "type": "radio"},
    {"name": "Best FM", "slug": "best-fm", "group": "Radio - Malaysia", "logo": "", "type": "radio"}
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

def update_m3u():
    m3u_content = """<!--more-->
<html>
<head>
<meta charset="utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script language="javascript">
window.location.replace("https://sulthanpamenan.github.io/malaysia-tv-playlist/");
</script>
</head></html>

<=================== PLAYLIST AUTOGENERATED BY SUTAN PAMENAN ===================>
<=================== IF YOU FIND THIS PLAYLIST, PLEASE DO NOT SELL OR DISTRIBUTE IT FOR PERSONAL GAIN ===================>

#EXTM3U
"""
    
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36"
    headers_suffix = f"|User-Agent={user_agent}&Origin=https://malaysia-tv.net&Referer=https://malaysia-tv.net/"
    
    print(f"Processing total {len(CHANNELS)} items with Multi-threading...")
    
    results = {}
    with ThreadPoolExecutor(max_workers=9) as executor:
        future_to_channel = {executor.submit(process_single_channel, ch): ch for ch in CHANNELS}
        for future in as_completed(future_to_channel):
            slug, url = future.result()
            if url:
                results[slug] = url

    for ch in CHANNELS:
        slug = ch['slug']
        if slug in results:
            url = results[slug]
            group_title = ch.get("group", "Others")
            tv_logo = ch.get("logo", "")
            item_type = ch.get("type", "tv")
            
            if item_type == "radio":
                m3u_content += f'#EXTINF:-1 radio="true" tvg-country="MY" tvg-logo="{tv_logo}" group-title="{group_title}",{ch["name"]}\n'
                m3u_content += f'{url}{headers_suffix}\n'
            else:
                m3u_content += f'#EXTINF:-1 tvg-id="" tvg-name="" tvg-logo="{tv_logo}" group-title="{group_title}",{ch["name"]}\n'
                m3u_content += '#KODIPROP:inputstreamaddon=inputstream.adaptive\n'
                m3u_content += '#KODIPROP:inputstream.adaptive.manifest_type=hls\n'
                m3u_content += f'#KODIPROP:inputstream.adaptive.stream_headers=User-Agent={user_agent}&Origin=https://malaysia-tv.net&Referer=https://malaysia-tv.net/\n'
                m3u_content += f'{url}{headers_suffix}\n'

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)
    print("The unified M3U playlist has been successfully updated and cleaned!")

if __name__ == "__main__":
    update_m3u()
