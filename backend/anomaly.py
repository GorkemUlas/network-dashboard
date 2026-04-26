from collections import deque

# deque — çift uçlu kuyruk
WINDOW_SIZE = 10
THRESHOLD_MULTIPLIER = 2.0  # ortalamanın kaç katı aşılırsa alert

bw_window = deque(maxlen=WINDOW_SIZE)   # bant genişliği geçmişi
pps_window = deque(maxlen=WINDOW_SIZE)  # paket/saniye geçmişi

def check_anomalies(bandwidth_mbps, packets_per_second):
    """
    Yeni değerleri geçmişle karşılaştır.
    Anomali varsa alert listesi döndürür, yoksa boş liste.
    """
    alerts = []

    # Pencere dolmuşsa kontrol et — ilk 10 değerde ortalama anlamlı değil
    if len(bw_window) == WINDOW_SIZE:
        bw_avg = sum(bw_window) / len(bw_window)

        if bandwidth_mbps > bw_avg * THRESHOLD_MULTIPLIER:
            alerts.append({
                "type": "BANDWIDTH_SPIKE",
                "message": f"Bant genişliği spike: {bandwidth_mbps} Mbps "
                           f"(ortalama: {bw_avg:.1f} Mbps)",
                "severity": "high"
            })

    if len(pps_window) == WINDOW_SIZE:
        pps_avg = sum(pps_window) / len(pps_window)

        if packets_per_second > pps_avg * THRESHOLD_MULTIPLIER:
            alerts.append({
                "type": "PACKET_FLOOD",
                "message": f"Paket sayısı spike: {packets_per_second} pps "
                           f"(ortalama: {pps_avg:.1f} pps)",
                "severity": "high"
            })

    # Değerleri her durumda pencereye ekle
    bw_window.append(bandwidth_mbps)
    pps_window.append(packets_per_second)

    return alerts