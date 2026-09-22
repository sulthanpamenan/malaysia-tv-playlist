import base64
import json
import time
import urllib.parse
import requests

def encrypt_payload(payload_dict):
    json_str = json.dumps(payload_dict, separators=(',', ':'))
    current_data = json_str
    for _ in range(3):
        b64_encoded = base64.b64encode(current_data.encode('utf-8')).decode('utf-8')
        current_data = urllib.parse.quote(b64_encoded, safe='')
    return current_data

def get_stream_link(channel_name):
    publisher_id = "default_publisher"
    payload = {
        "p": publisher_id,
        "c": channel_name,
        "q": "auto",
        "e": "main",
        "n": int(time.time() * 1000)
    }
    encrypted_v = encrypt_payload(payload)
    worker_url = f"https://tvmalaysia-proxy.sulthan-pamenan.workers.dev/?channel={channel_name.lower()}&format=json"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://domain-utama.com/"
    }
    
    try:
        response = requests.get(worker_url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get('streamUrl')
    except Exception as e:
        print(f"Error pada channel {channel_name}: {e}")
    return None

# Daftar channel yang ingin dimasukkan ke playlist
channels = [
    {"name": "TV1", "id": "tv1"},
    {"name": "Astro Awani", "id": "astro-awani"},
    {"name": "TV3", "id": "tv3"}
]

# Membuat file playlist.m3u secara otomatis
m3u_content = "#EXTM3U\n"

for ch in channels:
    print(f"Mengambil link untuk {ch['name']}...")
    stream_url = get_stream_link(ch['id'])
    if stream_url:
        m3u_content += f"#EXTINF:-1 tvg-id=\"{ch['id']}\" ,{ch['name']}\n"
        m3u_content += f"{stream_url}\n"

# Simpan ke file playlist.m3u
with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write(m3u_content)

print("\nBerhasil! File 'playlist.m3u' telah dibuat dan siap digunakan di aplikasi IPTV.")
