import os
from urllib.parse import unquote, urljoin
from flask import Flask, Response, request
import requests
import time
import json

app = Flask(__name__)

CHANNELS = [
    # --- TV Category ---
    {"name": "TV3", "slug": "tv3-live", "group": "General", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/General/TV3.png", "type": "tv"},
    {"name": "Drama Sangat", "slug": "drama-sangat", "group": "Drama", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/Drama/Drama_Sangat.png", "type": "tv"},
    {"name": "DidikTV KPM", "slug": "didik-tv-live", "group": "Education", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/Education/DidikTV_KPM.png", "type": "tv"},
    {"name": "FIFA+", "slug": "fifa-plus", "group": "Sports", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/Sports/FIFA+.png", "type": "tv"},
    {"name": "TV9", "slug": "tv9-malaysia", "group": "General", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/General/TV9_(Malaysia).png", "type": "tv"},
    {"name": "TV2", "slug": "tv2-live", "group": "General", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/General/RTM_TV2.png", "type": "tv"},
    {"name": "TV AlHijrah", "slug": "al-hijrah", "group": "Religious", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/Religious/TV_AlHijrah.png", "type": "tv"},
    {"name": "Sukan+", "slug": "sukan-rtm", "group": "Sports", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/Sports/RTM_Sukan+.png", "type": "tv"},
    {"name": "Bernama TV", "slug": "bernama", "group": "News + Opinion", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/News_+_Opinion/Bernama_TV.png", "type": "tv"},
    {"name": "Okey", "slug": "okey", "group": "General", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/General/Okey.png", "type": "tv"},
    {"name": "TV IKIM", "slug": "ikim-live", "group": "Religious", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/Religious/TV_IKIM.png", "type": "tv"},
    {"name": "8TV", "slug": "8-tv", "group": "General", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/General/8TV.png", "type": "tv"},
    {"name": "TV Sarawak", "slug": "tv-sarawak-live", "group": "Local", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/Local/TV_Sarawak.png", "type": "tv"},
    {"name": "MPL Malaysia", "slug": "mpl-malaysia", "group": "Sports", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/Sports/MPL_Malaysia.png", "type": "tv"},
    {"name": "Free Movies", "slug": "free-movies", "group": "Movies", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/Movies/Free_Movies.png", "type": "tv"},
    {"name": "PPA Asia Tier Badges KL Cup", "slug": "ppa-kl-cup", "group": "Live Sports", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/Live_Events/PPA_Asia_Tier_Badges_KL_Cup.png", "type": "tv"},
    {"name": "Siara TV", "slug": "siara-tv", "group": "Testing", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/Testing/Siara_TV.png", "type": "tv"},
    {"name": "MySports", "slug": "mysport", "group": "Sports", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/Sports/MySports.png", "type": "tv"},
    {"name": "USIMTV", "slug": "usim-tv", "group": "Education", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/Education/USIMTV.png", "type": "tv"},
    {"name": "Borneo TV", "slug": "borneo-tv", "group": "Local", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/Local/Borneo_TV.png", "type": "tv"},
    {"name": "ION", "slug": "ion-ncis", "group": "True Crime", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/True_Crime/ION.png", "type": "tv"},
    {"name": "BeIN Sports 1", "slug": "being-sports-1", "group": "Sports", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/Sports/beIN_Sports_1.png", "type": "tv"},

    # --- Radio Category ---
    {"name": "Manis FM", "slug": "manis-fm", "group": "Radio - Malaysia", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/Radio/Manis_FM.png", "type": "radio"},
    {"name": "Suria FM", "slug": "suria-fm", "group": "Radio - Malaysia", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/Radio/Suria_FM.png", "type": "radio"},
    {"name": "Fly FM", "slug": "fly-fm", "group": "Radio - Malaysia", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/Radio/Fly_FM.png", "type": "radio"},
    {"name": "Hot FM", "slug": "hot-fm", "group": "Radio - Malaysia", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/Radio/Hot_FM.png", "type": "radio"},
    {"name": "IKIM FM", "slug": "ikim-fm", "group": "Radio - Malaysia", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/Radio/IKIM_FM.png", "type": "radio"},
    {"name": "Molek FM", "slug": "molek-fm", "group": "Radio - Malaysia", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/Radio/Molek_FM.png", "type": "radio"},
    {"name": "Eight无限", "slug": "eight-fm", "group": "Radio - Malaysia", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/Radio/Eight无限.png", "type": "radio"},
    {"name": "Kool FM", "slug": "kool-fm", "group": "Radio - Malaysia", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/Radio/Kool_FM.png", "type": "radio"},
    {"name": "Bernama Radio", "slug": "bernama-radio", "group": "Radio - Malaysia", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/Radio/Bernama_Radio.png", "type": "radio"},
    {"name": "Best FM", "slug": "best-fm", "group": "Radio - Malaysia", "logo": "https://raw.githubusercontent.com/sulthanpamenan/IPTV_Master/main/Logos/Radio/Best_FM.png", "type": "radio"}
]

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36"
GIST_ID = os.environ.get("GIST_ID", "6055fb9a0d9c3754edc6cf956cdbf762")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GIST_FILENAME = "malaysia_tv.json"
GIST_API_URL = f"https://api.github.com/gists/{GIST_ID}"

_token_cache = {"data": {}, "expires_at": 0}

def load_tokens():
    global _token_cache
    if _token_cache["data"] and time.time() < _token_cache["expires_at"]:
        return _token_cache["data"]

    try:
        headers = {"Authorization": f"Bearer {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
        res = requests.get(GIST_API_URL, headers=headers, timeout=10)
        if res.status_code == 200:
            files = res.json().get("files", {})
            content = files.get(GIST_FILENAME, {}).get("content", "{}")
            _token_cache["data"] = json.loads(content)
            _token_cache["expires_at"] = time.time() + 30
    except Exception as e:
        print(f"[!] Error loading Gist: {e}")
    return _token_cache["data"]

@app.route("/playlist.m3u")
def get_master_playlist():
    host_url = request.host
    m3u_text = "#EXTM3U\n"
    
    for ch in CHANNELS:
        slug = ch["slug"]
        m3u_text += f'#EXTINF:-1 tvg-logo="{ch.get("logo", "")}" group-title="{ch.get("group", "General")}",{ch["name"]}\n'
        m3u_text += f'#KODIPROP:inputstreamaddon=inputstream.adaptive\n'
        m3u_text += f'#KODIPROP:inputstream.adaptive.manifest_type=hls\n'
        m3u_text += f"http://{host_url}/live/{slug}\n"

    return Response(m3u_text, content_type="audio/x-mpegurl")

@app.route("/live/<slug>")
def stream_proxy(slug):
    tokens = load_tokens()
    ch_data = tokens.get(slug, {})
    m3u8_url = ch_data.get("url")
    
    if not m3u8_url:
        return "Stream URL not found in Gist", 503

    headers = {
        "User-Agent": USER_AGENT,
        "Origin": "https://malaysia-tv.net",
        "Referer": "https://malaysia-tv.net/"
    }

    try:
        res = requests.get(m3u8_url, headers=headers, timeout=10)
        if res.status_code != 200:
            return f"Error upstream: {res.status_code}", res.status_code

        base_url = m3u8_url.rsplit("/", 1)[0] + "/"
        host_url = request.host
        lines = res.text.splitlines()
        new_lines = []

        for line in lines:
            if line.startswith("#") or not line.strip():
                new_lines.append(line)
            else:
                full_url = line if line.startswith("http") else urljoin(base_url, line)
                encoded_url = requests.utils.quote(full_url)
                new_lines.append(f"http://{host_url}/ts_proxy?slug={slug}&url={encoded_url}")

        return Response("\n".join(new_lines), content_type="application/vnd.apple.mpegurl")
    except Exception as e:
        return f"Proxy Error: {e}", 500

@app.route("/ts_proxy")
def ts_proxy():
    segment_url = request.args.get("url")
    slug = request.args.get("slug")
    if not segment_url:
        return "Invalid URL", 400

    target_url = unquote(segment_url)
    tokens = load_tokens()
    m3u8_url = tokens.get(slug, {}).get("url", "")
    base_domain = m3u8_url.rsplit("/", 3)[0] + "/" if m3u8_url else "https://malaysia-tv.net/"

    headers = {
        "User-Agent": USER_AGENT,
        "Origin": "https://malaysia-tv.net",
        "Referer": "https://malaysia-tv.net/"
    }

    try:
        res = requests.get(target_url, headers=headers, stream=True, timeout=15)
        return Response(res.iter_content(chunk_size=32768), content_type="video/MP2T")
    except Exception as e:
        return f"Segment Error: {e}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, threaded=True)
