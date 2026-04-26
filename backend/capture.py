from scapy.all import sniff, IP, TCP, UDP, ICMP
from collections import defaultdict, deque
import threading
import time

# Thread-safe veri paylaşımı için lock
# İki thread aynı anda aynı veriye yazamasın diye
lock = threading.Lock()

# Kayan pencere — son 1 saniyelik paketleri tutacak
packet_window = deque()

# Her IP'nin byte sayısını tut
ip_bytes = defaultdict(int)  # defaultdict — olmayan key'e erişince 0 döndürür

# Son hesaplanan istatistikler — app.py buradan okuyo
current_stats = {
    "bandwidth_mbps": 0.0,
    "packets_per_second": 0,
    "protocols": {"TCP": 0, "UDP": 0, "ICMP": 0, "Other": 0},
    "top_talkers": []
}

def process_packet(packet):
    """Her yakalanan paket için scapy bu fonksiyonu çağırcak."""
    if not packet.haslayer(IP):
        return  # IP katmanı yoksa atla — ARP gibi paketler

    now = time.time()
    size = len(packet)  # paketin byte cinsinden boyutu
    src_ip = packet[IP].src

    with lock:
        # (zaman, boyut, protokol, kaynak_ip) tuple olarak sakla
        proto = "Other"
        if packet.haslayer(TCP):
            proto = "TCP"
        elif packet.haslayer(UDP):
            proto = "UDP"
        elif packet.haslayer(ICMP):
            proto = "ICMP"

        packet_window.append((now, size, proto, src_ip))
        ip_bytes[src_ip] += size

def compute_stats():
    """
    Her saniye çalışır.
    Son 1 saniyelik penceredeki paketlerden istatistik hesaplar.
    """
    global current_stats

    while True:
        time.sleep(1)
        now = time.time()
        window_start = now - 1.0  # son 1 saniye

        with lock:
            # Pencereden 1 saniyeden eski paketleri temizle
            while packet_window and packet_window[0][0] < window_start:
                packet_window.popleft()

            # Penceredeki paketleri analiz et
            packets = list(packet_window)

        if not packets:
            current_stats = {
                "bandwidth_mbps": 0.0,
                "packets_per_second": 0,
                "protocols": {"TCP": 0, "UDP": 0, "ICMP": 0, "Other": 0},
                "top_talkers": []
            }
            continue

        # Toplam byte → Mbps
        # 1 Mbps = 1,000,000 bit/s = 125,000 byte/s
        total_bytes = sum(p[1] for p in packets)
        bandwidth = round((total_bytes * 8) / 1_000_000, 2)

        # Paket sayısı
        pps = len(packets)

        # Protokol sayımı
        proto_counts = {"TCP": 0, "UDP": 0, "ICMP": 0, "Other": 0}
        for p in packets:
            proto_counts[p[2]] += 1

        # Yüzdeye çevir
        total = len(packets)
        proto_pct = {
            k: round((v / total) * 100)
            for k, v in proto_counts.items()
        }

        # Top talkers — en çok byte gönderen IP'ler
        with lock:
            sorted_ips = sorted(
                ip_bytes.items(),          # (ip, byte_sayısı) çiftleri
                key=lambda x: x[1],        # byte_sayısına göre sırala
                reverse=True               # büyükten küçüğe
            )[:5]                          # ilk 5

            talkers = [
                {
                    "ip": ip,
                    "mbps": round((byte_count * 8) / 1_000_000, 2)
                }
                for ip, byte_count in sorted_ips
            ]

            # ip_bytes sıfırla
            ip_bytes.clear()

        current_stats = {
            "bandwidth_mbps": bandwidth,
            "packets_per_second": pps,
            "protocols": proto_pct,
            "top_talkers": talkers
        }

def get_stats():
    """app.py buradan okuyacak."""
    with lock:
        return dict(current_stats)

def start_capture(interface=None):
    """
    Paket yakalamayı başlatır.
    interface=None → scapy varsayılan arayüzü seçer
    """
    # İstatistik hesaplama thread'i
    stats_thread = threading.Thread(target=compute_stats, daemon=True)
    stats_thread.start()

    print(f"Paket yakalama başlıyor — arayüz: {interface or 'varsayılan'}")

    # sniff — scapy'nin ana fonksiyonu
    # prn → her pakette çağrılacak fonksiyon
    # store=False → paketleri RAM'de biriktirme, sadece işle
    # iface → hangi ağ arayüzünden dinle
    sniff(prn=process_packet, store=False, iface=interface)