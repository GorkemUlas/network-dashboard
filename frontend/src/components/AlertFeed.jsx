import { useState, useEffect } from "react";

const MAX_ALERTS = 20  // ekranda en fazla 20 alert tut

export function AlertFeed({ alerts }) {
  // Gelen alertleri biriktir
  const [history, setHistory] = useState([]);

  useEffect(() => {
    if (!alerts || alerts.length === 0) return;

    const timestamped = alerts.map((alert) => ({
      ...alert,  // alert objesinin tüm alanlarını kopyala
      id: Date.now() + Math.random(),  // benzersiz key için
      time: new Date().toLocaleTimeString("tr-TR")
    }));

    // Yeni alert'leri başa ekle, toplamı MAX_ALERTS ile sınırla
    setHistory((prev) => [...timestamped, ...prev].slice(0, MAX_ALERTS));
  }, [alerts]);

  return (
    <div style={{ marginBottom: "2rem" }}>
      <h2 style={{ fontSize: "14px", marginBottom: "8px", color: "#888" }}>
        Anomali Uyarıları
      </h2>

      {history.length === 0 ? (
        <p style={{ fontSize: "12px", color: "#444" }}>Henüz anomali tespit edilmedi</p>
      ) : (
        <div style={{ display: "flex", flexDirection: "column", gap: "6px" }}>
          {history.map((alert) => (
            <div
              key={alert.id}
              style={{
                background: alert.severity === "high" ? "#2a1010" : "#1a1a10",
                border: `1px solid ${alert.severity === "high" ? "#7f1d1d" : "#3f3f10"}`,
                borderRadius: "6px",
                padding: "8px 12px",
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                gap: "1rem"
              }}
            >
              <div>
                <span style={{
                  fontSize: "11px",
                  fontWeight: "500",
                  color: alert.severity === "high" ? "#ef4444" : "#eab308",
                  marginRight: "8px"
                }}>
                  {alert.type}
                </span>
                <span style={{ fontSize: "12px", color: "#ccc" }}>
                  {alert.message}
                </span>
              </div>
              <span style={{ fontSize: "11px", color: "#555", whiteSpace: "nowrap" }}>
                {alert.time}
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}