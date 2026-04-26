import {
    PieChart,
    Pie,
    Sector,
    Cell,
    Tooltip,
    Legend,
    ResponsiveContainer
} from "recharts";//*dizi

// prtokollerin renkler,
const COLORS ={
  TCP: "#4ade80",   // yeşil
  UDP: "#60a5fa",   // mavi
  ICMP: "#f97316"   // turuncu
}
/*
const renderSector = (props) => {
  const { payload } = props;
  return <Sector {...props} fill={COLORS[payload.name] ?? "#888"} />;
};*/

export function ProtocolPie({protocols}){

    const data = Object.entries(protocols).map(([name, value]) => ({
    name,
    value
  }));//destruct

    return(
        <div style={{ marginBottom: "2rem" }}>
        <h2 style={{ fontSize: "14px", marginBottom: "8px", color: "#888" }}>
            Protokol Dağılımı
        </h2>

        <ResponsiveContainer width="100%" height={220}>
            <PieChart>
            <Pie
                data={data}
                dataKey="value"       // dilim büyüklüğü
                nameKey="name"        // etiket
                cx="50%"              
                cy="50%"              
                outerRadius={80}      
                innerRadius={40} 
                isAnimationActive={false}
                //shape={renderSector}
                
            >   

                {/* Her dilime  renk */}
                {data.map((entry) => (
                <Cell
                    key={entry.name}
                    fill={COLORS[entry.name] ?? "#888"}  // renk yoksa gri
                />
                ))}
            </Pie>

            <Tooltip
                contentStyle={{ background: "#1a1a1a", border: "1px solid #333" }}
                itemStyle={{ color: "#e0e0e0" }}
                formatter={(value) => `${value}%`}  // tooltip'te değerin yanına % ekle
            />

            <Legend
                iconType="circle"
                iconSize={8}
                formatter={(value) => (
                <span style={{ color: "#888", fontSize: "12px" }}>{value}</span>
                )}
            />
            </PieChart>
        </ResponsiveContainer>
        </div>
    
    );


}

