import { useEffect, useState } from "react";
import { io } from "socket.io-client";

// Tek bir socket bağlantısı oluştur — modülün dışında 
// her render'da yeniden bağlanmasın
const socket = io("http://localhost:5000");

export function useWebSocket() {

  const [stats, setStats] = useState(null);
  const [connected, setConnected] = useState(false);


  useEffect(() => {
    // Socket bağlandığında
    socket.on("connect", () => {
      console.log("WebSocket bağlandı");
      setConnected(true);
    });

    // Flask'tan "stats_update" eventi geldiğinde
    // backend her saniye bu eventi yayınlayacak
    socket.on("stats_update", (data) => {
      setStats(data);
    });

    // Bağlantı koptuğunda
    socket.on("disconnect", () => {
      setConnected(false);
    });

    // Cleanup — bileşen sayfadan kaldırılınca çalışır
    // event listener'ları temizleme
    return () => {
      socket.off("connect");
      socket.off("stats_update");
      socket.off("disconnect");
    };
  }, []);

  return { stats, connected };
}