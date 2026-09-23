import time
from playwright.sync_api import sync_playwright
import re

def discover_channels():
    print("Scanning the channel list from malaysia-tv.net...")
    channels = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36"
        )
        
        try:
            page.goto("https://malaysia-tv.net/", timeout=60000, wait_until="networkidle")
            links = page.eval_on_selector_all("a", "elements => elements.map(e => e.href)")
            
            seen_slugs = set()
            for link in links:
                if "malaysia-tv.net" in link and not any(x in link for x in ["wp-content", "wp-admin", "tag", "category", "page", "privacy", "disclaimer", "terms"]):
                    parts = [p for p in link.split("/") if p]
                    if len(parts) >= 4:
                        slug = parts[-1]
                        if slug not in seen_slugs and slug != "malaysia-tv.net":
                            seen_slugs.add(slug)
                            name = slug.replace("-", " ").title()
                            channels.append({"name": name, "slug": slug})
                            
        except Exception as e:
            print(f"Failed to scan channels: {e}")
        finally:
            browser.close()
            
    print(f"{len(channels)} channels found.")
    return channels

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
    # 1. Channel detection
    channels = discover_channels()
    
    m3u_content = "#EXTM3U\n"
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36"
    headers_suffix = f"|User-Agent={user_agent}&Origin=https://malaysia-tv.net&Referer=https://malaysia-tv.net/"
    
    # 2. Get the link
    for ch in channels:
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

    # 3. Save the playlist.m3u file
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)
    print("The M3U playlist has been successfully updated!")

if __name__ == "__main__":
    update_m3u()
