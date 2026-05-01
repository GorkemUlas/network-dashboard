export function TopTalkers({ talkers }) {
  return (
    <div style={{ marginBottom: "2rem" }}>
      <h2 style={{ fontSize: "14px", marginBottom: "8px", color: "#888" }}>
        En Çok Trafik Üretenler
      </h2>

      <table style={{ width: "100%", borderCollapse: "collapse", fontSize: "13px" }}>
        <thead>
          <tr style={{ borderBottom: "1px solid #2a2a2a" }}>
            <th style={{ textAlign: "left",  padding: "6px 8px", color: "#888", fontWeight: "400" }}>IP Adresi</th>
            <th style={{ textAlign: "right", padding: "6px 8px", color: "#888", fontWeight: "400" }}>Mbps</th>
            <th style={{ textAlign: "right", padding: "6px 8px", color: "#888", fontWeight: "400" }}>Trafik</th>
          </tr>
        </thead>
        <tbody>
          {talkers.map((talker, index) => {
            // En yüksek değeri bul — bar genişliği için yüzde hesaplancak
            const max = talkers.length ? Math.max(...talkers.map((t) => t.mbps)) : 0;
            const pct = max > 0 ? Math.round((talker.mbps / max) * 100) : 0;
            //const max = talkers[0].mbps;
            //const pct = Math.round((talker.mbps / max) * 100);

            return (
              <tr
                key={talker.ip}
                style={{ borderBottom: "1px solid #1a1a1a" }}
              >
                <td style={{ padding: "8px", color: "#e0e0e0" }}>
                  {/* İlk sır daha parlak */}
                  <span style={{ color: index === 0 ? "#4ade80" : "#e0e0e0" }}>
                    {talker.ip}
                  </span>
                </td>
                <td style={{ padding: "8px", textAlign: "right", color: "#4ade80" }}>
                  {talker.mbps}
                </td>
                <td style={{ padding: "8px", textAlign: "right", minWidth: "80px" }}>
                  {/*  inline bar */}
                  <div style={{
                    background: "#2a2a2a",
                    borderRadius: "2px",
                    height: "6px",
                    width: "100%"
                  }}>
                    <div style={{
                      background: "#4ade80",
                      borderRadius: "2px",
                      height: "6px",
                      width: `${pct}%`,  // yüzdeye göre genişlik
                      transition: "width 0.3s ease"  //  geçiş
                    }} />
                  </div>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}