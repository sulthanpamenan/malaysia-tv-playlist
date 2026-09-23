import time
from playwright.sync_api import sync_playwright

CHANNELS = [
    # --- TV Category ---
    {"name": "TV3", "slug": "tv3-live", "group": "General", "logo": "https://example.com/tv3.png"},
    {"name": "Drama Sangat", "slug": "drama-sangat", "group": "Series", "logo": "https://example.com/drama-sangat.png"},
    {"name": "RTM TV1", "slug": "rtm-tv1-live", "group": "General", "logo": "https://example.com/rtm1.png"},
    {"name": "Didik TV", "slug": "didik-tv-live", "group": "Education", "logo": "https://example.com/didiktv.png"},
    {"name": "FIFA+", "slug": "fifa-plus", "group": "Sports", "logo": "https://example.com/fifaplus.png"},
    {"name": "TV9 Malaysia", "slug": "tv9-malaysia", "group": "General", "logo": "https://example.com/tv9.png"},
    {"name": "TV2", "slug": "tv2-live", "group": "General", "logo": "https://example.com/tv2.png"},
    {"name": "Al Hijrah TV", "slug": "al-hijrah", "group": "Religious", "logo": "https://example.com/alhijrah.png"},
    {"name": "Sukan RTM", "slug": "sukan-rtm", "group": "Sports", "logo": "https://example.com/sukanrtm.png"},
    {"name": "Berita RTM", "slug": "berita-waliyah", "group": "News + Opinion", "logo": "https://example.com/beritartm.png"},
    {"name": "Bernama TV", "slug": "bernama", "group": "News + Opinion", "logo": "https://example.com/bernama.png"},
    {"name": "TV Okey", "slug": "okey", "group": "General", "logo": "https://example.com/tvokey.png"},
    {"name": "Selangor TV", "slug": "selangor", "group": "General", "logo": "https://example.com/tvokey.png"},
    {"name": "TV IKIM", "slug": "ikim-live", "group": "General", "logo": "https://example.com/tvokey.png"},
    {"name": "8 TV", "slug": "8-tv", "group": "General", "logo": "https://example.com/tvokey.png"},
    {"name": "TV Sarawak", "slug": "tv-sarawak-live", "group": "General", "logo": "https://example.com/tvokey.png"},
    {"name": "MPL Malaysia", "slug": "mpl-malaysia", "group": "General", "logo": "https://example.com/tvokey.png"},
    {"name": "CNA", "slug": "cna", "group": "General", "logo": "https://example.com/tvokey.png"},
    {"name": "PPA KL Cup", "slug": "ppa-kl-cup", "group": "General", "logo": "https://example.com/tvokey.png"},
    {"name": "DW", "slug": "dw", "group": "General", "logo": "https://example.com/tvokey.png"},
    {"name": "Arirang", "slug": "arirang", "group": "General", "logo": "https://example.com/tvokey.png"},
    {"name": "The Indonesia Channel", "slug": "the-indonesia-channel", "group": "General", "logo": "https://example.com/tvokey.png"},
    {"name": "Al Jazeera", "slug": "al-jazeera", "group": "General", "logo": "https://example.com/tvokey.png"},
    {"name": "BeIN Sports 1", "slug": "being-sports-1", "group": "General", "logo": "https://example.com/tvokey.png"},
    {"name": "Tennis+", "slug": "tennis", "group": "General", "logo": "https://example.com/tvokey.png"},
    {"name": "Pickle TV", "slug": "pickle-tv", "group": "General", "logo": "https://example.com/tvokey.png"},
    {"name": "Cricket Gold", "slug": "cricket-live", "group": "General", "logo": "https://example.com/tvokey.png"},
    {"name": "Shemaroo Bollywood Classic", "slug": "shemaroo-bollywood-classic", "group": "General", "logo": "https://example.com/tvokey.png"},
    {"name": "Bollywood Prime", "slug": "bollywood-prime-live", "group": "General", "logo": "https://example.com/tvokey.png"},
    {"name": "Bollywood Masala", "slug": "bollywood-masala-live", "group": "General", "logo": "https://example.com/tvokey.png"},
    {"name": "Shemaroo Filmigaane", "slug": "shemaroo-filmigaane-live", "group": "General", "logo": "https://example.com/tvokey.png"},
    {"name": "Pitaara Movie", "slug": "pitaara-movie-live", "group": "General", "logo": "https://example.com/tvokey.png"},
    {"name": "Shemaroo Umang Plus", "slug": "shemaroo-umang-plus-live", "group": "General", "logo": "https://example.com/tvokey.png"},
    {"name": "Mastiii TV", "slug": "mastiii-tv-live", "group": "General", "logo": "https://example.com/tvokey.png"},
    {"name": "Miramax Movie", "slug": "miramax-movie", "group": "General", "logo": "https://example.com/tvokey.png"},
    {"name": "FILMRISE Movies", "slug": "filmrise-movies", "group": "General", "logo": "https://example.com/tvokey.png"},
    {"name": "GoUSA TV", "slug": "gousa-tv-live", "group": "General", "logo": "https://example.com/tvokey.png"},
    {"name": "euro News", "slug": "euro-news-live", "group": "General", "logo": "https://example.com/tvokey.png"},
    {"name": "ION NCIS", "slug": "ion-ncis", "group": "General", "logo": "https://example.com/tvokey.png"},
    {"name": "Nosey TV", "slug": "nosey-tv", "group": "General", "logo": "https://example.com/tvokey.png"},
    {"name": "FailArmy Channel", "slug": "failarmy-tv", "group": "General", "logo": "https://example.com/tvokey.png"},
    {"name": "BBC News", "slug": "bbc-news-live", "group": "General", "logo": "https://example.com/tvokey.png"},

    # --- Radio Category ---
    {"name": "Rakita FM", "slug": "rakita-fm", "group": "Radio - Malaysia", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/Radio/Rakita%20FM.png"},
    {"name": "Hot FM", "slug": "hot-fm", "group": "Radio - Malaysia", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/Radio/Rakita%20FM.png"},
    {"name": "IKIM FM", "slug": "ikim-fm", "group": "Radio - Malaysia", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/Radio/Rakita%20FM.png"},
    {"name": "Molek FM", "slug": "molek-fm", "group": "Radio - Malaysia", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/Radio/Rakita%20FM.png"},
    {"name": "Eight FM", "slug": "eight-fm", "group": "Radio - Malaysia", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/Radio/Rakita%20FM.png"},
    {"name": "Kool FM", "slug": "kool-fm", "group": "Radio - Malaysia", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/Radio/Rakita%20FM.png"},
    {"name": "Nasional FM", "slug": "nasional-fm", "group": "Radio - Malaysia", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/Radio/Rakita%20FM.png"},
    {"name": "Minnal FM", "slug": "minnal-fm", "group": "Radio - Malaysia", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/Radio/Rakita%20FM.png"},
    {"name": "Ai FM", "slug": "ai-fm", "group": "Radio - Malaysia", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/Radio/Rakita%20FM.png"},
    {"name": "Radio Klasik", "slug": "radio-klasik", "group": "Radio - Malaysia", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/Radio/Rakita%20FM.png"},
    {"name": "Sabah FM", "slug": "sabah-fm", "group": "Radio - Malaysia", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/Radio/Rakita%20FM.png"},
    {"name": "Sarawak FM", "slug": "sarawak-fm", "group": "Radio - Malaysia", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/Radio/Rakita%20FM.png"},
    {"name": "Bernama Radio", "slug": "bernama-radio", "group": "Radio - Malaysia", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/Radio/Rakita%20FM.png"},
    {"name": "Asyik FM", "slug": "asyik-fm", "group": "Radio - Malaysia", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/Radio/Rakita%20FM.png"},
    {"name": "Best FM", "slug": "best-fm", "group": "Radio - Malaysia", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/Radio/Rakita%20FM.png"}
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
            if any(ext in request.url for ext in [".m3u8", ".aac", ".mp3", "stream"]):
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
    
    print(f"Processing total {len(CHANNELS)} items (TV & Radio)...")
    
    for ch in CHANNELS:
        group_title = ch.get("group", "Others")
        tv_logo = ch.get("logo", "")
        item_type = ch.get("type", "tv")
        
        print(f"Processing: {ch['name']} [{group_title}] ({ch['slug']})...")
        url = get_stream_url(ch['slug'])
        
        if url:
            print(f"  -> Success: {url}")
            if item_type == "radio":
                # Special format for radio
                m3u_content += f'#EXTINF:-1 radio="true" tvg-country="MY" tvg-logo="{tv_logo}" group-title="{group_title}",{ch["name"]}\n'
                m3u_content += f'{url}{headers_suffix}\n'
            else:
                # Format for TV
                m3u_content += f'#EXTINF:-1 tvg-id="" tvg-name="" tvg-logo="{tv_logo}" group-title="{group_title}",{ch["name"]}\n'
                m3u_content += '#KODIPROP:inputstreamaddon=inputstream.adaptive\n'
                m3u_content += '#KODIPROP:inputstream.adaptive.manifest_type=hls\n'
                m3u_content += f'#KODIPROP:inputstream.adaptive.stream_headers=User-Agent={user_agent}&Origin=https://malaysia-tv.net&Referer=https://malaysia-tv.net/\n'
                m3u_content += f'{url}{headers_suffix}\n'
        else:
            print(f"  -> Failed to get the link for {ch['name']}")

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)
    print("The unified M3U playlist has been successfully updated!")

if __name__ == "__main__":
    update_m3u()
