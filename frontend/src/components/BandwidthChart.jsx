import { useRef, useEffect } from "react";
import {
  LineChart,    // çizgi grafik ana kapsayıcı
  Line,         // tek bir çizgi — birden fazla ekleyebilirsin
  XAxis,        // yatay eksen
  YAxis,        // dikey eksen
  CartesianGrid, // arka plan ızgarası
  Tooltip,      // üzerine gelince değer gösteren kutu
  ResponsiveContainer // grafiği ebeveyn genişliğine uyduruyor
} from "recharts";

// Kaç veri noktası tutacağız — 30 saniye
const MAX_POINTS = 30;

export function BandwidthChart({ bandwidthMbps }) {
  // useRef — değeri saklıyor ama değişince render tetiklemiyor
  // geçmiş veriyi biriktirmek için ideal — her güncelleme render istemiyoruz
  const historyRef = useRef([]);

  // Her yeni değer geldiğinde geçmişe ekle
  useEffect(() => {
    const now = new Date();
    const label = `${now.getMinutes()}:${String(now.getSeconds()).padStart(2, "0")}`;

    historyRef.current = [
      ...historyRef.current,
      { time: label, mbps: bandwidthMbps }
    ].slice(-MAX_POINTS); // sondan MAX_POINTS kadar tut, eskiyi at
  }, [bandwidthMbps]); // bandwidthMbps değişince çalış

  return (
    <div style={{ marginBottom: "2rem" }}>
      <h2 style={{ fontSize: "14px", marginBottom: "8px", color: "#888" }}>
        Bant Genişliği (Mbps)
      </h2>

      {/* ResponsiveContainer yüzde genişlik alıyor, height sabit */}
      <ResponsiveContainer width="100%" height={200}>
        <LineChart data={historyRef.current}>
          <CartesianGrid strokeDasharray="3 3" stroke="#2a2a2a" />
          <XAxis
            dataKey="time"      // her noktanın x eksenindeki etiketi
            tick={{ fontSize: 11, fill: "#888" }}
            interval="preserveStartEnd" // sadece ilk ve son etiketi göster
          />
          <YAxis
            domain={[0, 100]}   // y ekseninin min-max aralığı
            tick={{ fontSize: 11, fill: "#888" }}
            unit=" Mbps"
          />
          <Tooltip
            contentStyle={{ background: "#1a1a1a", border: "1px solid #333" }}
            labelStyle={{ color: "#888" }}
            itemStyle={{ color: "#4ade80" }}
          />
          <Line
            type="monotone"     // noktalar arası yumuşak eğri
            dataKey="mbps"      // historyRef içindeki hangi alanı çiz
            stroke="#4ade80"    // çizgi rengi
            strokeWidth={2}
            dot={false}         // her noktaya daire koyma — kalabalık görünür
            isAnimationActive={false} // canlı güncelleme için animasyonu kapat
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}