import threading
import urllib.request
import time

# dosyalar
TARGETS = [
    "http://speed.hetzner.de/100MB.bin",
    "http://speedtest.tele2.net/10MB.zip",
    "http://ipv4.download.thinkbroadband.com/10MB.zip",
]

def download_loop(url):
    while True:
        try:
            # Dosyayı parça parça oku — RAM'e tamamen yükleme
            with urllib.request.urlopen(url, timeout=10) as r:
                while True:
                    chunk = r.read(65536)  # 64KB 
                    if not chunk:
                        break
        except:
            pass
        time.sleep(0.5)

if __name__ == "__main__":
    print("Yüksek trafik üretiliyor...")
    for url in TARGETS:
        t = threading.Thread(target=download_loop, args=(url,), daemon=True)
        t.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Durduruldu.")