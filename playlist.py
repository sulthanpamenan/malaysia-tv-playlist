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

# Daftar channel yang ingin dikelola beserta token bootstrap-nya
channels = [
    {
        "name": "TV1", 
        "id": "tv1", 
        "v": "WlhsS2QwbHFiMmxpVjBaMVdWUkpkR0pZYTJsTVEwcHFTV3B2YVdSSVdYaEphWGRwWTFOSk5rbHRNV2hoVnpScFRFTktiRWxxYjJsTlZHZDNUVWhOYVV4RFNuVkphbTlwVFZSak5VMUVRVEZOUkVFelQwUmpOVTlETURSTmVrbDRUa1JWTVU5RFNqaz0%3D"
    },
    {
        "name": "TV2", 
        "id": "tv2", 
        "v": "WlhsS2QwbHFiMmxpVjBaMVdWUkpkR0pZYTJsTVEwcHFTV3B2YVdSSVdYbEphWGRwWTFOSk5rbHRNV2hoVnpScFRFTktiRWxxYjJsTlZHZDNUVWhOYVV4RFNuVkphbTlwVFZSak5VMUVRVEZOUkVVMFRXcEpNVTlETURKTmFtY3lUMVJOZDAxcFNqaz0%3D"
    },
    {
        "name": "TV3", 
        "id": "tv3", 
        "v": "WlhsS2QwbHFiMmxrUnpsMVpFYzVkVWxwZDJsWmVVazJTVzVTTWsxNVNYTkpia1ZwVDJsS2RGbFhiSFZKYVhkcFdsTkpOa2xxUlRSTlJFSjZTV2wzYVdKcFNUWkpha1V6VDFSQmQwNVVRWGROYWxFd1RVUlZkRTE2VFRGTmVtY3lUbFJyYVdaUlBUMD0%3D"
    },
    {
        "name": "Astro Awani", 
        "id": "astro-awani", 
        "v": "WlhsS2QwbHFiMmxpVjBaMVdWUkpkR0pZYTJsTVEwcHFTV3B2YVdSSVdYaEphWGRwWTFOSk5rbHRNV2hoVnpScFRFTktiRWxxYjJsTlZHZDNUVWhOYVV4RFNuVkphbTlwVFZSak5VMUVRVEJQUkd0NVQxUlZOVTE1TURGUFZFa3lUMVJWZDA1VFNqaz0%3D"
    }
]

# Mulai isi file M3U
m3u_content = "#EXTM3U\n"

for ch in channels:
    print(f"Mengambil link segar untuk {ch['name']}...")
    bootstrap_url = f"https://tvmalaysia.com.co/wp-json/media-hub/v1/bootstrap?v={ch['v']}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": f"https://tvmalaysia.com.co/{ch['id']}/"
    }
    
    try:
        response = requests.get(bootstrap_url, headers=headers, timeout=10)
        if response.status_code == 200:
            raw_text = response.text.strip('"')
            decoded_data = raw_text
            for _ in range(3):
                decoded_data = urllib.parse.unquote(decoded_data)
                buffer = base64.b64decode(decoded_data.encode('utf-8'))
                decoded_data = buffer.decode('utf-8')
            
            data = json.loads(decoded_data)
            stream_url = data.get('streamUrl') or data.get('url') or data.get('file')
            
            if stream_url:
                # Menambahkan informasi channel dan opsi header EXTVLCOPT secara otomatis
                m3u_content += f'#EXTINF:-1 tvg-id="{ch["id"]}" group-title="Malaysian Channels",{ch["name"]}\n'
                m3u_content += '#EXTVLCOPT:http-referrer=https://tvmalaysia.com.co/\n'
                m3u_content += '#EXTVLCOPT:http-origin=https://tvmalaysia.com.co\n'
                m3u_content += f"{stream_url}\n"
    except Exception as e:
        print(f"Gagal pada {ch['name']}: {e}")

# Simpan hasilnya ke file playlist.m3u
with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write(m3u_content)

print("File playlist.m3u berhasil diperbarui dengan opsi header lengkap!")
