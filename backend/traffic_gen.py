import threading
import requests
import time

# Sürekli istek atacağımız siteler
TARGETS = [
    "http://example.com",
    "http://httpbin.org/get",
    "http://google.com",
    "http://github.com",
    "http://cloudflare.com",
]

def spam_requests(target):
    """Tek bir hedefe sürekli istek atar."""
    while True:
        
        try:
            requests.get(target, timeout=3)
        except:
            pass  # hata olursa sessizce geç, durmadan devam et
        time.sleep(0.01)  # 100ms bekle — çok agresif olmasın

if __name__ == "__main__":
    print(f"{len(TARGETS)} hedefe paralel istek başlıyor...")
    
    # Her hedef için ayrı thread
    threads = []
    for target in TARGETS:
        t = threading.Thread(target=spam_requests, args=(target,), daemon=True)
        t.start()
        threads.append(t)
    
    # Ana thread çalışmaya devam etsin
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Durduruldu.")
        
