from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
import threading
import time
#import random  # sahte veri için 
from anomaly import check_anomalies 
from capture import get_stats, start_capture
app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")



def broadcast_loop():
    while True:
        stats = get_stats()  # gerçek veri

        alerts = check_anomalies(
            stats["bandwidth_mbps"],
            stats["packets_per_second"]
        )
        stats["alerts"] = alerts

        socketio.emit("stats_update", stats)
        time.sleep(1)

@app.route("/")
def index():
    return {"status": "running"}

@socketio.on("connect")
def handle_connect():
    print("Client bağlandı")

if __name__ == "__main__":
    # broadcast_loop'u ayrı bir thread'de başlat
    # daemon=True → ana program kapanınca bu thread de kapanır
    # Paket yakalama thread'i — yönetici yetkisiyle çalışması lazım

    capture_thread = threading.Thread(
        target=start_capture,
        kwargs={"interface": None},  # None → varsayılan arayüz
        daemon=True
    )
    capture_thread.start()

    broadcast_thread = threading.Thread(target=broadcast_loop, daemon=True)
    broadcast_thread.start()

    socketio.run(app, debug=True, port=5000, use_reloader=False)