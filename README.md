# Real-Time Network Traffic Monitoring Dashboard
<img width="1878" height="982" alt="Ekran görüntüsü 2026-04-26 192058" src="https://github.com/user-attachments/assets/5f7f1f48-adde-4151-aef6-d5cecff98b9b" />

Wireless and Mobile Networks dersi projesi.

Gerçek zamanlı ağ trafiğini yakalayıp analiz eden ve web tabanlı bir dashboard üzerinde görselleştiren full-stack uygulama.

## Özellikler

- Gerçek zamanlı paket yakalama (scapy / libpcap)
- Canlı bant genişliği grafiği (WebSocket ile güncelleme)
- Protokol dağılımı — TCP / UDP / ICMP
- En çok trafik üreten IP'ler (top talkers)
- Otomatik anomali tespiti — kayan pencere ortalaması ile spike algılama

## Stack

| Katman |                      |Teknoloji |

| Paket yakalama|               |Python, scapy |
| Backend |                     |Python, Flask, Flask-SocketIO |
| Frontend |                    |React, Recharts |
| Gerçek zamanlı iletişim |     |WebSocket (socket.io) |

## Kurulum

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate      # Windows
pip install -r requirements.txt
python app.py              # Yönetici yetkisi gerekebilir
```

### Frontend

```bash
cd frontend
npm install
npm start
```

Uygulama `http://localhost:3000` adresinde açılır.

## Mimari
Ağ Arayüzü (NIC)
↓
Paket Yakalama (scapy)
↓
İstatistik Motoru + Anomali Tespiti
↓
Flask WebSocket Sunucusu
↓
React Dashboard

## Proje Yapısı

network-dashboard/
├── backend/
│   ├── app.py          # Flask sunucusu, WebSocket
│   ├── capture.py      # Paket yakalama ve istatistik
│   ├── anomaly.py      # Anomali tespiti
│   └── requirements.txt
└── frontend/
└── src/
├── hooks/
│   └── useWebSocket.js
└── components/
├── BandwidthChart.jsx
├── ProtocolPie.jsx
├── TopTalkers.jsx
└── AlertFeed.jsx
