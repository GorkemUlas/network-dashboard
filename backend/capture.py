from scapy.all import sniff, IP, TCP, UDP, ICMP
from collections import defaultdict, deque
import threading
import time
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("INFLUX_TOKEN")
org = os.getenv("INFLUX_ORG")
bucket = os.getenv("INFLUX_BUCKET")
url = os.getenv("INFLUX_URL")

client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)


lock = threading.Lock()

# Kayan pencere — son 1 saniyelik paketler
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
    """Her yakalanan paket hem istatistik için işlenir hem InfluxDB'ye yazılır."""
    if not packet.haslayer(IP):
        return 

    now = time.time()
    size = len(packet)
    src_ip = packet[IP].src
    proto_num = packet[IP].proto
    
    # Protokol Belirleme
    proto_name = "Other"
    if packet.haslayer(TCP): proto_name = "TCP"
    elif packet.haslayer(UDP): proto_name = "UDP"
    elif packet.haslayer(ICMP): proto_name = "ICMP"

    # 1. InfluxDB'ye Gönder (Grafana İçin)
    try:
        p = Point("network_traffic") \
            .tag("protocol", proto_name) \
            .tag("source_ip", src_ip) \
            .field("bytes", size)
        write_api.write(bucket=bucket, record=p)
    except Exception as e:
        print(f"InfluxDB Yazma Hatası: {e}")

    # 2. Yerel İstatistikler İçin Kaydet (React Dashboard İçin)
    with lock:
        packet_window.append((now, size, proto_name, src_ip))
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

def get_active_interface():
    """
    Aktif ağ arayüzünü otomatik bulur.
    Önce Wi-Fi, sonra Ethernet dener.
    """
    from scapy.arch.windows import get_windows_if_list
    import socket

    # Bilgisayarın dışarıya açılan IP'sini bul
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # bağlantı kurmaz, sadece routing bakar
        local_ip = s.getsockname()[0]
        s.close()
    except:
        return "Wi-Fi"  # bulamazsa Wi-Fi dene

    # O IP'ye sahip arayüzü bul
    for iface in get_windows_if_list():
        for addr in iface.get("ips", []):
            if addr == local_ip:
                print(f"Aktif arayüz bulundu: {iface['name']} ({local_ip})")
                return iface["name"]

    return "Wi-Fi"  # bulamazsa fallback

def start_capture(interface=None):
    stats_thread = threading.Thread(target=compute_stats, daemon=True)
    stats_thread.start()

    # interface verilmemişse otomatik bul
    if interface is None:
        interface = get_active_interface()

    print(f"Paket yakalama başlıyor — arayüz: {interface}")
    sniff(prn=process_packet, store=False, iface=interface)

if __name__ == "__main__":
    start_capture()