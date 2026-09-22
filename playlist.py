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
    publisher_id = "default_publisher"  # Sesuaikan dengan publisher asli
    
    payload = {
        "p": publisher_id,
        "c": channel_name,
        "q": "auto",
        "e": "main",
        "n": int(time.time() * 1000)
    }
    
    encrypted_v = encrypt_payload(payload)
    worker_url = f"https://worker-anda.workers.dev/stream?v={encrypted_v}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://domain-utama.com/"
    }
    
    try:
        response = requests.get(worker_url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"Berhasil mendapatkan link untuk {channel_name}: {data.get('url')}")
            return data.get('url')
        else:
            print(f"Gagal untuk {channel_name}, Status Code: {response.status_code}")
    except Exception as e:
        print(f"Error pada channel {channel_name}: {e}")

channels = ["TV1", "Astro Awani"]
for ch in channels:
    get_stream_link(ch)
