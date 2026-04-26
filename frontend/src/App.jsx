import { useWebSocket } from "./hooks/useWebSocket";
import { BandwidthChart } from "./components/BandwidthChart";
import { ProtocolPie } from "./components/ProtocolPie";
import { TopTalkers } from "./components/TopTalkers";
import { AlertFeed } from "./components/AlertFeed";


function App() {
  const { stats, connected } = useWebSocket();

  return (
    <div style={{
      padding: "2rem",
      fontFamily: "monospace",
      background: "#0f0f0f",
      minHeight: "100vh",
      color: "#e0e0e0"
    }}>

      <h1 style={{ fontSize: "18px", marginBottom: "4px" }}>
        Network Monitor
      </h1>
      <p style={{
        fontSize: "12px",
        color: connected ? "#4ade80" : "#ef4444",
        marginBottom: "2rem"
      }}>
        {connected ? "● Bağlı" : "● Bağlantı bekleniyor..."}
      </p>

      {stats && (
        <>
          {/* Üst metrik kartları */}
          <div style={{ display: "flex", gap: "1rem", marginBottom: "2rem" }}>
            <MetricCard label="Bant Genişliği" value={`${stats.bandwidth_mbps} Mbps`} />
            <MetricCard label="Paket/saniye"   value={stats.packets_per_second} />
            <MetricCard label="TCP"             value={`${stats.protocols.TCP}%`} />
            <MetricCard label="UDP"             value={`${stats.protocols.UDP}%`} />
          </div>

          {/* Canlı grafik */}
          <BandwidthChart bandwidthMbps={stats.bandwidth_mbps} />

          {/* Alt satır: pasta + tablo yan yana */}
          <div style={{ display: "flex", gap: "2rem" }}>
            <div style={{ flex: 1 }}>
              <ProtocolPie protocols={stats.protocols} />
            </div>
            <div style={{ flex: 2 }}>
              <TopTalkers talkers={stats.top_talkers} />
            </div>
          </div>
          <AlertFeed alerts={stats.alerts} />
        </>
      )}

    </div>
  );
}

// Küçük yardımcı bileşen — tekrar eden kart yapısı için
function MetricCard({ label, value }) {
  return (
    <div style={{
      background: "#1a1a1a",
      border: "1px solid #2a2a2a",
      borderRadius: "8px",
      padding: "12px 16px",
      minWidth: "120px"
    }}>
      <div style={{ fontSize: "11px", color: "#888", marginBottom: "4px" }}>
        {label}
      </div>
      <div style={{ fontSize: "20px", fontWeight: "500" }}>
        {value}
      </div>
    </div>
  );
}

export default App;