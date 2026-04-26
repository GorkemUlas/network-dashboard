import { useEffect, useState } from "react";
import { io } from "socket.io-client";

// Tek bir socket bağlantısı oluştur — modülün dışında 
// her render'da yeniden bağlanmak istemiyoruz
const socket = io("http://localhost:5000");

export function useWebSocket() {
  // useState — React'ta değişkeni "reaktif" yapıyor
  // değişken değişince bileşen otomatik yeniden render oluor
  const [stats, setStats] = useState(null);
  const [connected, setConnected] = useState(false);

  // useEffect — bileşen ekrana ilk yüklendiğinde çalışır
  // ikinci parametre [] → sadece bir kez çalış demek
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
    // event listener'ları temizlemek bellek sızıntısını önler
    return () => {
      socket.off("connect");
      socket.off("stats_update");
      socket.off("disconnect");
    };
  }, []);

  return { stats, connected };
}