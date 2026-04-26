import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";

// HTML'deki <div id="root"> elementini bul
// tüm React uygulaması oraya mount edilecek
const root = ReactDOM.createRoot(document.getElementById("root"));

root.render(<App />);