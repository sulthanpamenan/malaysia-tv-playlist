import re
from playwright.sync_api import sync_playwright

# Daftar channel yang ingin Anda ambil
CHANNELS = [
    {"name": "sukan rtm", "slug": "sukan-rtm"},
    {"name": "TV3", "slug": "tv3"}
]

def get_stream_url(slug):
    target_url = f"https://malaysia-tv.net/{slug}/"
    stream_url = ""
    
    with sync_playwright() as p:
        # Gunakan browser headless untuk merender JavaScript situs
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        try:
            # Buka halaman dan tunggu hingga jaringan utama stabil
            page.goto(target_url, timeout=60000, wait_until="networkidle")
            
            # Ambil seluruh isi HTML atau cari request m3u8 yang terpanggil
            content = page.content()
            
            # Cari pola m3u8 di dalam halaman
            match = re.search(r'https?://[^\s"\'<>]+?\.m3u8[^\s"\'<>]*', content)
            if match:
                stream_url = match.group(0).replace(r'\/', '/')
            else:
                # Jika tidak ketemu di HTML, cari lewat frame/iframe
                frames = page.frames
                for frame in frames:
                    frame_content = frame.content()
                    frame_match = re.search(r'https?://[^\s"\'<>]+?\.m3u8[^\s"\'<>]*', frame_content)
                    if frame_match:
                        stream_url = frame_match.group(0).replace(r'\/', '/')
                        break
        except Exception as e:
            print(f"Error mengambil {slug}: {e}")
        finally:
            browser.close()
            
    return stream_url

def update_m3u():
    m3u_content = "#EXTM3U\n"
    
    for ch in CHANNELS:
        print(f"Mencari link untuk: {ch['name']}...")
        url = get_stream_url(ch['slug'])
        if url:
            print(f"Berhasil mendapatkan link: {url}")
            m3u_content += f'#EXTINF:-1 group-title="Malaysian Channels",{ch["name"]}\n{url}\n'
        else:
            print(f"Gagal mendapatkan link untuk {ch['name']}")
            # Masukkan fallback kosong atau biarkan
            m3u_content += f'#EXTINF:-1 group-title="Malaysian Channels",{ch["name"]}\nhttps://error-link-not-found\n'

    # Simpan ke file playlist.m3u
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)
    print("Playlist M3U berhasil diperbarui!")

if __name__ == "__main__":
    update_m3u()
