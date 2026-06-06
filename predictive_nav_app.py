import { useState, useRef } from "react";
import {
  BarChart, Bar, LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell
} from "recharts";

// --- DATA & HELPERS ---
const LOCATIONS = {
  Home:     { lat: -25.7461, lon: 28.1881 },
  Work:     { lat: -25.7580, lon: 28.1890 },
  School:   { lat: -25.7400, lon: 28.2100 },
  Mall:     { lat: -25.7650, lon: 28.3120 },
  Hospital: { lat: -25.7320, lon: 28.2280 },
  Airport:  { lat: -25.9180, lon: 28.3820 },
  Park:     { lat: -25.7280, lon: 28.2450 },
  Garage:   { lat: -25.7500, lon: 28.1750 },
};
const LOC_NAMES = Object.keys(LOCATIONS);

function seededRand(seed) {
  let s = seed;
  return () => {
    s = (s * 1664525 + 1013904223) & 0xffffffff;
    return (s >>> 0) / 0xffffffff;
  };
}

function congestionFor(seed, hr) {
  const r = seededRand(seed);
  let v = Math.floor(r() * 55) + 15;
  if ((hr >= 7 && hr <= 9) || (hr >= 16 && hr <= 18)) v = Math.min(100, v + 30);
  return v;
}

function emissionLevel(c) {
  if (c > 65) return { label: "HIGH",   color: "#ef4444" };
  if (c > 40) return { label: "MEDIUM", color: "#f59e0b" };
  return             { label: "LOW",    color: "#22c55e" };
}

const now      = new Date();
const HOUR     = now.getHours();
const IS_RUSH  = (HOUR >= 7 && HOUR <= 9) || (HOUR >= 16 && HOUR <= 18);
const TIME_STR = now.toLocaleTimeString("en-ZA", { hour: "2-digit", minute: "2-digit" });
const DATE_STR = now.toLocaleDateString("en-ZA",  { day: "2-digit", month: "short", year: "numeric" });

// --- DESIGN TOKENS ---
const G = {
  bg0: "#030712", bg1: "#0a0f1e", bg2: "#0f1929",
  border: "#1e293b", text: "#e2e8f0", muted: "#475569",
  green: "#22c55e", green2: "#4ade80",
  red: "#ef4444", amber: "#f59e0b", blue: "#38bdf8",
};

// --- GLOBAL CSS ---
const css = `
@import url('https://fonts.googleapis.com/css2?family=Exo+2:wght@300;400;600;800;900&family=Share+Tech+Mono&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }
body { background: ${G.bg0}; color: ${G.text}; font-family: 'Exo 2', sans-serif; overflow-x: hidden; }
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: ${G.bg1}; }
::-webkit-scrollbar-thumb { background: #1e3a4f; border-radius: 4px; }
.mono { font-family: 'Share Tech Mono', monospace; }

/* Drawer overlay */
.drawer-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.6); z-index: 40; transition: opacity .25s; }
.drawer-overlay.hidden { opacity: 0; pointer-events: none; }

/* Drawer panel */
.drawer {
  position: fixed; top: 0; left: 0; bottom: 0; width: 280px;
  background: #070d1a; border-right: 1px solid ${G.border};
  z-index: 50; transform: translateX(-100%);
  transition: transform .28s cubic-bezier(.4,0,.2,1);
  display: flex; flex-direction: column;
}
.drawer.open { transform: translateX(0); }

/* Top bar */
.topbar {
  position: sticky; top: 0; z-index: 30;
  background: ${G.bg0}; border-bottom: 1px solid ${G.border};
  display: flex; align-items: center; gap: 12px; padding: 14px 16px;
}
.topbar-title { font-size: 18px; font-weight: 900; color: ${G.green2}; letter-spacing: 3px; }
.hamburger { background: none; border: none; cursor: pointer; display: flex; flex-direction: column; gap: 5px; padding: 4px; }
.hamburger span { display: block; width: 22px; height: 2px; background: ${G.green2}; border-radius: 2px; transition: .2s; }

/* Nav items */
.nav-item {
  display: flex; align-items: center; gap: 14px;
  padding: 14px 20px; cursor: pointer;
  color: #64748b; font-size: 15px; font-weight: 600;
  transition: background .15s, color .15s;
  border-left: 3px solid transparent;
}
.nav-item:hover  { background: #0d1f2e; color: #94a3b8; }
.nav-item.active { background: linear-gradient(90deg,#0d2318,#0a1f14); color: ${G.green2}; border-left-color: ${G.green}; }
.nav-icon { font-size: 20px; width: 28px; text-align: center; }

/* Page content */
.content { padding: 16px; max-width: 1100px; margin: 0 auto; }

/* Cards */
.card {
  background: linear-gradient(135deg,${G.bg1},${G.bg2});
  border: 1px solid ${G.border}; border-radius: 16px; padding: 20px;
  position: relative; overflow: hidden;
}
.card::before      { content:''; position:absolute; top:0;left:0;right:0;height:2px; background:linear-gradient(90deg,transparent,${G.green},transparent); }
.card-red::before   { background:linear-gradient(90deg,transparent,${G.red},transparent); }
.card-amber::before { background:linear-gradient(90deg,transparent,${G.amber},transparent); }
.card-blue::before  { background:linear-gradient(90deg,transparent,${G.blue},transparent); }

.kv        { font-size:28px; font-weight:900; font-family:'Share Tech Mono',monospace; }
.kv-green  { color:${G.green2}; }
.kv-red    { color:${G.red};    }
.kv-amber  { color:${G.amber};  }
.kv-blue   { color:${G.blue};   }
.kl { font-size:10px; letter-spacing:3px; color:${G.muted}; text-transform:uppercase; margin-top:4px; }

/* Alert banners */
.alert-red   { background:#1c0a0a; border:1px solid #7f1d1d; border-left:4px solid ${G.red};   border-radius:12px; padding:14px 18px; margin:8px 0; }
.alert-green { background:#071a0e; border:1px solid #14532d; border-left:4px solid ${G.green}; border-radius:12px; padding:14px 18px; margin:8px 0; }
.alert-amber { background:#1a1203; border:1px solid #78350f; border-left:4px solid ${G.amber}; border-radius:12px; padding:14px 18px; margin:8px 0; }

/* Progress bar */
.pbar-bg   { background:${G.border}; border-radius:20px; height:8px; margin:6px 0; }
.pbar-fill { height:8px; border-radius:20px; }

/* Badge */
.badge { display:inline-block; background:#0d2318; color:${G.green2}; border:1px solid #166534; border-radius:20px; padding:3px 12px; font-size:11px; letter-spacing:2px; }

/* Route boxes */
.route-blue { background:#071520; border:2px solid ${G.blue}; border-radius:14px; padding:16px; }
.route-red  { background:#1c0a0a; border:2px solid ${G.red};  border-radius:14px; padding:16px; }

/* Login */
.login-wrap { max-width:380px; margin:60px auto; background:${G.bg1}; border:1px solid ${G.border}; border-radius:24px; padding:40px; text-align:center; }
.inp { width:100%; background:${G.bg2}; border:1px solid ${G.border}; border-radius:10px; color:white; padding:10px 14px; font-size:14px; font-family:'Exo 2',sans-serif; outline:none; margin-bottom:12px; }
.inp:focus { border-color:${G.green}; }
.btn-green { width:100%; background:linear-gradient(135deg,#14532d,#166534); color:${G.green2}; border:1px solid #166534; border-radius:10px; padding:12px; font-weight:700; font-size:15px; font-family:'Exo 2',sans-serif; cursor:pointer; letter-spacing:1px; transition:.2s; }
.btn-green:hover { box-shadow:0 0 20px #22c55e44; }
.btn-sm { background:linear-gradient(135deg,#14532d,#166534); color:${G.green2}; border:1px solid #166534; border-radius:8px; padding:8px 16px; font-weight:700; font-size:13px; font-family:'Exo 2',sans-serif; cursor:pointer; letter-spacing:1px; }

/* Layout grids */
.grid-2 { display:grid; grid-template-columns:1fr 1fr; gap:12px; }
.grid-4 { display:grid; grid-template-columns:repeat(4,1fr); gap:12px; }
@media(max-width:640px){ .grid-4{grid-template-columns:1fr 1fr;} .grid-2{grid-template-columns:1fr;} }

/* Tabs */
.tabs { display:flex; border-bottom:1px solid ${G.border}; margin-bottom:16px; overflow-x:auto; }
.tab  { padding:10px 18px; cursor:pointer; font-size:13px; font-weight:600; color:#64748b; border-bottom:2px solid transparent; white-space:nowrap; }
.tab.active { color:${G.green2}; border-bottom-color:${G.green}; }

/* Form elements */
.sel { background:${G.bg2}; border:1px solid ${G.border}; border-radius:10px; color:white; padding:8px 12px; font-family:'Exo 2',sans-serif; font-size:13px; width:100%; }
.lbl { font-size:11px; color:${G.muted}; letter-spacing:2px; margin-bottom:4px; }
input[type=range] { accent-color:${G.green}; width:100%; }

/* Misc */
.action-card { background:#0a0f1e; border:1px solid ${G.border}; border-radius:10px; padding:14px; margin-bottom:8px; }
.reward-card { background:#0a0f1e; border:1px solid ${G.border}; border-radius:12px; padding:14px; margin-bottom:10px; }
.sec-head { color:${G.text}; font-size:15px; font-weight:700; margin:16px 0 10px; }
.page-head   { display:flex; align-items:center; gap:12px; margin-bottom:12px; }
.page-head h1 { color:${G.text}; font-weight:900; font-size:24px; }
.page-head p  { color:${G.muted}; font-size:12px; }

/* Map page */
@keyframes dash-blue { to { stroke-dashoffset: -200; } }
@keyframes dash-red  { to { stroke-dashoffset: -200; } }
@keyframes pulse-pin { 0%,100%{r:7;opacity:1} 50%{r:10;opacity:.7} }
@keyframes fadeInUp  { from{opacity:0;transform:translateY(12px)} to{opacity:1;transform:none} }
.map-route-card { animation: fadeInUp .35s ease both; }
.map-route-card:nth-child(2) { animation-delay:.1s; }
`;

// --- NAVIGATION CONFIG ---
const NAV = [
  { id: "dashboard", icon: "🏠", label: "Dashboard"       },
  { id: "citymap",   icon: "🗺️", label: "City Map"        },
  { id: "routes",    icon: "📍", label: "Smart Routes"    },
  { id: "alerts",    icon: "⚠️", label: "Emission Alerts" },
  { id: "analytics", icon: "📊", label: "Analytics"       },
  { id: "ecoscore",  icon: "⭐", label: "Eco Score"       },
  { id: "rewards",   icon: "🎁", label: "Rewards"         },
  { id: "profile",   icon: "👤", label: "Profile"         },
];

// --- SHARED COMPONENTS ---
function PageHead({ emoji, title, sub }) {
  return (
    <div>
      <div className="page-head">
        <span style={{ fontSize: 28 }}>{emoji}</span>
        <div><h1>{title}</h1><p>{sub}</p></div>
      </div>
      <hr style={{ border: "none", borderTop: `1px solid ${G.border}`, margin: "0 0 16px" }} />
    </div>
  );
}

function KpiCard({ value, label, cls = "", kvcls = "kv-green" }) {
  return (
    <div className={`card ${cls}`}>
      <div className={`kv ${kvcls}`}>{value}</div>
      <div className="kl">{label}</div>
    </div>
  );
}

// --- PAGE: DASHBOARD ---
function Dashboard({ state }) {
  const pulseData = LOC_NAMES.map((n, i) => ({ name: n, value: congestionFor(i * 7 + 1, HOUR) }));
  const savings   = +(state.greenPoints * 0.12).toFixed(2);
  const fuel      = +(state.greenPoints * 0.05).toFixed(2);

  return (
    <div>
      <PageHead emoji="🏠" title="Dashboard" sub="Live emission intelligence overview" />

      <div className="grid-4" style={{ marginBottom: 12 }}>
        <KpiCard value={TIME_STR} label={DATE_STR} cls="card-blue" kvcls="kv-blue" />
        <KpiCard value={IS_RUSH ? "RUSH HOUR" : "CLEAR"} label="TRAFFIC STATUS"
          cls={IS_RUSH ? "card-red" : ""} kvcls={IS_RUSH ? "kv-red" : "kv-green"} />
        <KpiCard value={`${state.ecoScore}/100`} label="ECO SCORE" />
        <KpiCard value={state.greenPoints} label="GREEN POINTS" />
      </div>

      {IS_RUSH
        ? <div className="alert-red">
            <b style={{ color: G.red }}>Warning HIGH EMISSION ALERT</b><br />
            <span style={{ color: "#fca5a5", fontSize: 13 }}>Rush hour -- consider delaying or choosing a clean route.</span>
          </div>
        : <div className="alert-green">
            <b style={{ color: G.green }}>OK LOW EMISSION CONDITIONS</b><br />
            <span style={{ color: "#86efac", fontSize: 13 }}>Traffic is clear -- great time to travel and earn Green Points.</span>
          </div>
      }

      <div className="sec-head">Real-Time City Emission Pulse</div>
      <div style={{ background: G.bg1, border: `1px solid ${G.border}`, borderRadius: 12, padding: 12 }}>
        <ResponsiveContainer width="100%" height={180}>
          <BarChart data={pulseData}>
            <XAxis dataKey="name" tick={{ fill: G.muted, fontSize: 10 }} />
            <YAxis tick={{ fill: G.muted, fontSize: 10 }} domain={[0, 100]} />
            <Tooltip contentStyle={{ background: G.bg2, border: `1px solid ${G.border}`, borderRadius: 8 }} />
            <Bar dataKey="value" radius={4}>
              {pulseData.map((d, i) => <Cell key={i} fill={emissionLevel(d.value).color} />)}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="sec-head">Today's Impact</div>
      <div className="grid-2" style={{ gap: 10 }}>
        <KpiCard value={`${savings} kg`} label="CO2 SAVED TODAY" />
        <KpiCard value={`R${fuel}`}      label="FUEL COST SAVED" cls="card-amber" kvcls="kv-amber" />
        <KpiCard value={state.trips}     label="TRIPS COMPLETED" cls="card-blue"  kvcls="kv-blue" />
        <KpiCard value={state.greenPoints} label="TOTAL GREEN POINTS" />
      </div>

      <div className="alert-green" style={{ marginTop: 12 }}>
        <b style={{ color: G.green }}>Why It Matters</b><br />
        <span style={{ color: "#86efac", fontSize: 13 }}>Every clean trip earns Green Points redeemable for real rewards while reducing urban air pollution.</span>
      </div>
    </div>
  );
}

// --- PAGE: CITY MAP ---
function CityMap({ navigate }) {
  const [selected, setSelected] = useState(null); // null | 'blue' | 'red'
  const [dest, setDest] = useState("Mall");
  const [animKey, setAnimKey] = useState(0);

  const destinations = ["Mall", "Work", "School", "Hospital", "Park", "Airport"];

  function chooseDest(d) {
    setDest(d);
    setSelected(null);
    setAnimKey(k => k + 1);
  }

  // Pretoria area landmarks (SVG coordinate space 0-700 x 0-460)
  // Home ~(215, 270), Menlyn Mall ~(490, 130)
  // Blue route: smooth, less congested via cleaner roads
  // Red route: congested direct path through heavy traffic
  const bluePoints = "215,270 190,240 170,200 185,165 220,145 270,130 330,118 390,112 445,120 490,130";
  const redPoints  = "215,270 240,255 275,240 310,225 350,215 390,200 430,175 460,155 490,130";

  // Landmarks for the map
  const landmarks = [
    { x: 215, y: 270, label: "Home", icon: "🏠", color: G.green2 },
    { x: 490, y: 130, label: "Menlyn Mall", icon: "🛍️", color: G.amber },
    { x: 90,  y: 190, label: "University\nof Pretoria", icon: "🎓", color: G.blue },
    { x: 280, y: 90,  label: "Mall", icon: "🏪", color: "#a78bfa" },
    { x: 120, y: 370, label: "Church", icon: "⛪", color: G.muted },
    { x: 310, y: 400, label: "High School", icon: "🏫", color: G.muted },
  ];

  const blueStats = { congestion: "18%", time: "14 min", co2: "0.8 kg", quality: "Clean Air", cars: "Low" };
  const redStats  = { congestion: "74%", time: "28 min", co2: "2.1 kg", quality: "Smoky Air", cars: "High" };

  return (
    <div>
      <PageHead emoji="🗺️" title="City Map" sub="Pretoria live route explorer — pick your destination" />

      {/* Destination selector */}
      <div style={{ marginBottom: 14 }}>
        <div className="lbl" style={{ marginBottom: 8 }}>SELECT DESTINATION</div>
        <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
          {destinations.map(d => (
            <button
              key={d}
              onClick={() => chooseDest(d)}
              style={{
                background: dest === d ? "linear-gradient(135deg,#14532d,#166534)" : G.bg2,
                color: dest === d ? G.green2 : G.muted,
                border: `1px solid ${dest === d ? G.green : G.border}`,
                borderRadius: 8, padding: "6px 14px", cursor: "pointer",
                fontFamily: "'Exo 2',sans-serif", fontWeight: 700, fontSize: 13,
                transition: ".2s",
              }}
            >
              {d}
            </button>
          ))}
        </div>
      </div>

      {/* Instruction when Mall selected */}
      {dest === "Mall" && !selected && (
        <div className="alert-green" style={{ marginBottom: 12 }}>
          <b style={{ color: G.green }}>Two Routes Found to {dest}</b><br />
          <span style={{ color: "#86efac", fontSize: 13 }}>Tap a route on the map or choose below to see details.</span>
        </div>
      )}

      {/* SVG Map */}
      <div style={{
        background: "linear-gradient(145deg,#060d1a,#0a1525)",
        border: `1px solid ${G.border}`, borderRadius: 16, padding: 0,
        overflow: "hidden", position: "relative", marginBottom: 14,
      }}>
        {/* Map title overlay */}
        <div style={{
          position: "absolute", top: 12, left: 16, zIndex: 5,
          background: "rgba(3,7,18,0.8)", borderRadius: 8, padding: "4px 10px",
          border: `1px solid ${G.border}`,
        }}>
          <span style={{ color: G.green2, fontSize: 11, fontWeight: 700, letterSpacing: 2 }}>PRETORIA CITY MAP</span>
        </div>

        {/* Rush hour badge */}
        {IS_RUSH && (
          <div style={{
            position: "absolute", top: 12, right: 16, zIndex: 5,
            background: "#1c0a0a", borderRadius: 8, padding: "4px 10px",
            border: `1px solid ${G.red}`,
          }}>
            <span style={{ color: G.red, fontSize: 11, fontWeight: 700 }}>RUSH HOUR</span>
          </div>
        )}

        <svg
          key={animKey}
          viewBox="0 0 700 460"
          style={{ width: "100%", display: "block" }}
          xmlns="http://www.w3.org/2000/svg"
        >
          {/* Background grid */}
          <defs>
            <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
              <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#0f1f35" strokeWidth="0.5" />
            </pattern>
            {/* Glow filters */}
            <filter id="glow-blue">
              <feGaussianBlur stdDeviation="3" result="b" />
              <feMerge><feMergeNode in="b" /><feMergeNode in="SourceGraphic" /></feMerge>
            </filter>
            <filter id="glow-red">
              <feGaussianBlur stdDeviation="3" result="b" />
              <feMerge><feMergeNode in="b" /><feMergeNode in="SourceGraphic" /></feMerge>
            </filter>
            <filter id="glow-green">
              <feGaussianBlur stdDeviation="4" result="b" />
              <feMerge><feMergeNode in="b" /><feMergeNode in="SourceGraphic" /></feMerge>
            </filter>
            {/* Animated dash */}
            <marker id="arrow-blue" markerWidth="6" markerHeight="6" refX="3" refY="3" orient="auto">
              <path d="M0,0 L6,3 L0,6 Z" fill="#38bdf8" />
            </marker>
            <marker id="arrow-red" markerWidth="6" markerHeight="6" refX="3" refY="3" orient="auto">
              <path d="M0,0 L6,3 L0,6 Z" fill="#ef4444" />
            </marker>
          </defs>

          <rect width="700" height="460" fill="#060d1a" />
          <rect width="700" height="460" fill="url(#grid)" />

          {/* City block shapes */}
          <rect x="50" y="50" width="120" height="80" rx="6" fill="#0a1525" stroke="#0f2035" strokeWidth="1" />
          <rect x="220" y="40" width="90" height="50" rx="6" fill="#0a1525" stroke="#0f2035" strokeWidth="1" />
          <rect x="380" y="50" width="140" height="70" rx="6" fill="#0a1525" stroke="#0f2035" strokeWidth="1" />
          <rect x="550" y="60" width="110" height="90" rx="6" fill="#0a1525" stroke="#0f2035" strokeWidth="1" />
          <rect x="40" y="300" width="100" height="80" rx="6" fill="#0a1525" stroke="#0f2035" strokeWidth="1" />
          <rect x="480" y="300" width="150" height="100" rx="6" fill="#0a1525" stroke="#0f2035" strokeWidth="1" />
          <rect x="180" y="360" width="200" height="70" rx="6" fill="#0a1525" stroke="#0f2035" strokeWidth="1" />

          {/* Road network (subtle) */}
          <polyline points="215,0 215,460" stroke="#0d1e30" strokeWidth="8" />
          <polyline points="0,270 700,270" stroke="#0d1e30" strokeWidth="8" />
          <polyline points="380,0 380,460" stroke="#0d1e30" strokeWidth="6" />
          <polyline points="0,130 700,130" stroke="#0d1e30" strokeWidth="6" />

          {/* === BLUE ROUTE (clean / low congestion) === */}
          {dest === "Mall" && (
            <g onClick={() => setSelected("blue")} style={{ cursor: "pointer" }}>
              {/* Shadow glow */}
              <polyline
                points={bluePoints}
                fill="none" stroke="#38bdf8" strokeWidth="10" strokeOpacity="0.15"
                strokeLinecap="round" strokeLinejoin="round"
                filter="url(#glow-blue)"
              />
              {/* Main line */}
              <polyline
                points={bluePoints}
                fill="none"
                stroke={selected === "blue" ? "#7dd3fc" : "#38bdf8"}
                strokeWidth={selected === "blue" ? 5 : 3.5}
                strokeLinecap="round" strokeLinejoin="round"
                strokeDasharray="12 6"
                markerEnd="url(#arrow-blue)"
                style={{
                  strokeDashoffset: 0,
                  animation: "dash-blue 2.5s linear infinite",
                }}
              />
              {/* Label */}
              <rect x="270" y="96" width="80" height="20" rx="4" fill="rgba(6,13,26,0.85)" />
              <text x="310" y="110" textAnchor="middle" fill="#38bdf8" fontSize="11" fontWeight="700" fontFamily="'Share Tech Mono',monospace">
                CLEAN ROUTE
              </text>
            </g>
          )}

          {/* === RED ROUTE (congested / high emission) === */}
          {dest === "Mall" && (
            <g onClick={() => setSelected("red")} style={{ cursor: "pointer" }}>
              {/* Shadow glow */}
              <polyline
                points={redPoints}
                fill="none" stroke="#ef4444" strokeWidth="10" strokeOpacity="0.15"
                strokeLinecap="round" strokeLinejoin="round"
                filter="url(#glow-red)"
              />
              {/* Main line */}
              <polyline
                points={redPoints}
                fill="none"
                stroke={selected === "red" ? "#fca5a5" : "#ef4444"}
                strokeWidth={selected === "red" ? 5 : 3.5}
                strokeLinecap="round" strokeLinejoin="round"
                strokeDasharray="8 5"
                markerEnd="url(#arrow-red)"
                style={{
                  strokeDashoffset: 0,
                  animation: "dash-red 1.2s linear infinite",
                }}
              />
              {/* Label */}
              <rect x="310" y="230" width="90" height="20" rx="4" fill="rgba(28,10,10,0.9)" />
              <text x="355" y="244" textAnchor="middle" fill="#ef4444" fontSize="11" fontWeight="700" fontFamily="'Share Tech Mono',monospace">
                CONGESTED
              </text>
            </g>
          )}

          {/* Generic route for non-mall destinations */}
          {dest !== "Mall" && (
            <g>
              <polyline
                points="215,270 300,230 390,195 450,165 490,130"
                fill="none" stroke="#38bdf8" strokeWidth="3.5"
                strokeLinecap="round" strokeLinejoin="round"
                strokeDasharray="12 6"
              />
              <rect x="315" y="192" width="80" height="20" rx="4" fill="rgba(6,13,26,0.85)" />
              <text x="355" y="206" textAnchor="middle" fill="#38bdf8" fontSize="11" fontWeight="700" fontFamily="'Share Tech Mono',monospace">
                ROUTE TO {dest.toUpperCase()}
              </text>
            </g>
          )}

          {/* Landmarks */}
          {landmarks.map((lm, i) => (
            <g key={i}>
              <circle cx={lm.x} cy={lm.y} r="14" fill={lm.x === 215 && lm.y === 270 ? "#071a0e" : "#0a1525"}
                stroke={lm.color} strokeWidth="2" />
              <text x={lm.x} y={lm.y + 5} textAnchor="middle" fontSize="12">{lm.icon}</text>
              {/* Label below pin */}
              <text
                x={lm.x} y={lm.y + 28}
                textAnchor="middle" fill={lm.color}
                fontSize={lm.label.includes("\n") ? 9 : 10}
                fontWeight="700" fontFamily="'Share Tech Mono',monospace"
              >
                {lm.label.split("\n").map((line, li) => (
                  <tspan key={li} x={lm.x} dy={li === 0 ? 0 : 11}>{line}</tspan>
                ))}
              </text>
            </g>
          ))}

          {/* Home pulse ring */}
          <circle cx="215" cy="270" r="18" fill="none" stroke={G.green} strokeWidth="1.5" strokeOpacity="0.5"
            style={{ animation: "pulse-pin 2s ease-in-out infinite" }} />

          {/* Congestion smoke clouds for red route area */}
          {dest === "Mall" && (
            <g opacity="0.4">
              <ellipse cx="350" cy="225" rx="22" ry="12" fill="#7f1d1d" />
              <ellipse cx="400" cy="200" rx="18" ry="9"  fill="#7f1d1d" />
              <ellipse cx="310" cy="235" rx="14" ry="7"  fill="#7f1d1d" />
              <text x="360" y="195" textAnchor="middle" fill="#fca5a5" fontSize="9" fontFamily="monospace">SMOKE</text>
            </g>
          )}

          {/* Legend */}
          <rect x="12" y="390" width="190" height="58" rx="8" fill="rgba(6,13,26,0.9)" stroke="#1e293b" strokeWidth="1" />
          <line x1="22" y1="408" x2="52" y2="408" stroke="#38bdf8" strokeWidth="2.5" strokeDasharray="6 3" />
          <text x="58" y="412" fill="#38bdf8" fontSize="10" fontFamily="'Share Tech Mono',monospace">Blue = Clean / Low Pollution</text>
          <line x1="22" y1="428" x2="52" y2="428" stroke="#ef4444" strokeWidth="2.5" strokeDasharray="4 3" />
          <text x="58" y="432" fill="#ef4444" fontSize="10" fontFamily="'Share Tech Mono',monospace">Red = Congested / Smoky</text>

          {/* Selected highlight ring */}
          {selected === "blue" && <polyline points={bluePoints} fill="none" stroke="#38bdf8" strokeWidth="8" strokeOpacity="0.18" strokeLinecap="round" />}
          {selected === "red"  && <polyline points={redPoints}  fill="none" stroke="#ef4444" strokeWidth="8" strokeOpacity="0.18" strokeLinecap="round" />}
        </svg>
      </div>

      {/* Route comparison cards (shown when going to Mall) */}
      {dest === "Mall" && (
        <div className="grid-2" style={{ gap: 12, marginBottom: 14 }}>
          {/* Blue route card */}
          <div
            className="route-blue map-route-card"
            style={{
              cursor: "pointer",
              boxShadow: selected === "blue" ? `0 0 24px #38bdf844` : "none",
              transform: selected === "blue" ? "scale(1.02)" : "scale(1)",
              transition: ".2s",
            }}
            onClick={() => setSelected("blue")}
          >
            <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 10 }}>
              <div style={{ width: 16, height: 4, background: G.blue, borderRadius: 2 }} />
              <span style={{ fontSize: 14, fontWeight: 800, color: G.blue }}>CLEAN ROUTE</span>
              {selected === "blue" && <span style={{ marginLeft: "auto", background: "#0d2318", color: G.green2, border: `1px solid ${G.green}`, borderRadius: 12, padding: "2px 8px", fontSize: 10 }}>SELECTED</span>}
            </div>
            <div style={{ color: "#7dd3fc", fontSize: 10, letterSpacing: 2, marginBottom: 12 }}>LOW EMISSIONS - RECOMMENDED</div>
            <div className="grid-2" style={{ gap: 6 }}>
              {[
                ["Congestion", blueStats.congestion, G.blue],
                ["Travel Time", blueStats.time, G.blue],
                ["CO2 Output", blueStats.co2, G.green2],
                ["Air Quality", blueStats.quality, G.green2],
              ].map(([l, v, c]) => (
                <div key={l} style={{ background: "#071a2e", borderRadius: 8, padding: 8 }}>
                  <div className="mono" style={{ fontSize: 16, fontWeight: 900, color: c }}>{v}</div>
                  <div style={{ color: "#64748b", fontSize: 9, letterSpacing: 1 }}>{l.toUpperCase()}</div>
                </div>
              ))}
            </div>
            <div style={{ marginTop: 10, background: "#071520", borderRadius: 8, padding: 8, fontSize: 12, color: "#7dd3fc" }}>
              Smooth flow · Less cars · Earn +15 Green Points
            </div>
          </div>

          {/* Red route card */}
          <div
            className="route-red map-route-card"
            style={{
              cursor: "pointer",
              boxShadow: selected === "red" ? `0 0 24px #ef444444` : "none",
              transform: selected === "red" ? "scale(1.02)" : "scale(1)",
              transition: ".2s",
            }}
            onClick={() => setSelected("red")}
          >
            <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 10 }}>
              <div style={{ width: 16, height: 4, background: G.red, borderRadius: 2 }} />
              <span style={{ fontSize: 14, fontWeight: 800, color: G.red }}>HIGH EMISSION ROUTE</span>
              {selected === "red" && <span style={{ marginLeft: "auto", background: "#1c0a0a", color: G.red, border: `1px solid ${G.red}`, borderRadius: 12, padding: "2px 8px", fontSize: 10 }}>SELECTED</span>}
            </div>
            <div style={{ color: "#fca5a5", fontSize: 10, letterSpacing: 2, marginBottom: 12 }}>HEAVY TRAFFIC - AVOID</div>
            <div className="grid-2" style={{ gap: 6 }}>
              {[
                ["Congestion", redStats.congestion, G.red],
                ["Travel Time", redStats.time, G.red],
                ["CO2 Output", redStats.co2, "#f87171"],
                ["Air Quality", redStats.quality, "#f87171"],
              ].map(([l, v, c]) => (
                <div key={l} style={{ background: "#1c0808", borderRadius: 8, padding: 8 }}>
                  <div className="mono" style={{ fontSize: 16, fontWeight: 900, color: c }}>{v}</div>
                  <div style={{ color: "#64748b", fontSize: 9, letterSpacing: 1 }}>{l.toUpperCase()}</div>
                </div>
              ))}
            </div>
            <div style={{ marginTop: 10, background: "#1c0808", borderRadius: 8, padding: 8, fontSize: 12, color: "#fca5a5" }}>
              Stop-and-go · Lots of cars · Smoke & pollution
            </div>
          </div>
        </div>
      )}

      {/* Decision advisor */}
      {dest === "Mall" && selected && (
        <div className={selected === "blue" ? "alert-green" : "alert-red"} style={{ marginBottom: 12 }}>
          {selected === "blue"
            ? <><b style={{ color: G.green }}>Smart Choice!</b><br /><span style={{ color: "#86efac", fontSize: 13 }}>The Clean Route saves 1.3 kg CO2 and ~14 minutes travel time. You'll earn +15 Green Points for taking the eco-friendly path.</span></>
            : <><b style={{ color: G.red }}>High Pollution Warning</b><br /><span style={{ color: "#fca5a5", fontSize: 13 }}>This route has heavy congestion, smoke exposure, and burns more fuel. Consider switching to the Blue Route for a healthier, faster trip.</span></>
          }
        </div>
      )}

      {/* Start trip button */}
      {dest === "Mall" && selected === "blue" && (
        <button
          className="btn-green"
          onClick={() => navigate("routes")}
          style={{ marginTop: 4 }}
        >
          Navigate - Start Clean Route to {dest}
        </button>
      )}

      {dest !== "Mall" && (
        <div className="alert-amber">
          <b style={{ color: G.amber }}>Route Preview</b><br />
          <span style={{ color: "#fde68a", fontSize: 13 }}>Showing estimated clean route to {dest}. Select Mall to see full dual-route comparison with emission data.</span>
        </div>
      )}
    </div>
  );
}

// --- PAGE: SMART ROUTES ---
function SmartRoutes({ state, setState }) {
  const [origin,  setOrigin]  = useState("Home");
  const [dest,    setDest]    = useState("Work");
  const [leaveHr, setLeaveHr] = useState(HOUR);
  const [tripMsg, setTripMsg] = useState("");

  const r     = seededRand(leaveHr + origin.charCodeAt(0) + dest.charCodeAt(0));
  const congA = Math.min(100, Math.floor(r() * 35) + 10);
  const congB = Math.min(100, Math.floor(r() * 40) + 50 + (IS_RUSH ? 25 : 0));
  const distA = +(r() * 14 + 4).toFixed(1);
  const distB = +(distA * (r() * 0.5 + 0.8)).toFixed(1);
  const timeA = Math.round(distA * 1.5 + congA * 0.3);
  const timeB = Math.round(distB * 1.5 + congB * 0.5);
  const fuelA = +(distA * 0.08).toFixed(2);
  const fuelB = +(distB * 0.08 + congB * 0.005).toFixed(2);
  const co2A  = +(fuelA * 2.31).toFixed(2);
  const co2B  = +(fuelB * 2.31).toFixed(2);

  function takeTrip() {
    setState(s => ({ ...s, greenPoints: s.greenPoints + 15, trips: s.trips + 1, ecoScore: Math.min(100, s.ecoScore + 1) }));
    setTripMsg("Trip started! +15 pts added.");
    setTimeout(() => setTripMsg(""), 3000);
  }

  return (
    <div>
      <PageHead emoji="📍" title="Smart Routes" sub="Choose cleaner routes -- reduce emissions, earn Green Points" />

      <div className="grid-2" style={{ gap: 10, marginBottom: 10 }}>
        <div>
          <div className="lbl">ORIGIN</div>
          <select className="sel" value={origin} onChange={e => setOrigin(e.target.value)}>
            {LOC_NAMES.map(l => <option key={l}>{l}</option>)}
          </select>
        </div>
        <div>
          <div className="lbl">DESTINATION</div>
          <select className="sel" value={dest} onChange={e => setDest(e.target.value)}>
            {LOC_NAMES.filter(l => l !== origin).map(l => <option key={l}>{l}</option>)}
          </select>
        </div>
      </div>

      <div style={{ marginBottom: 12 }}>
        <div className="lbl">DEPARTURE HOUR: {leaveHr}:00</div>
        <input type="range" min={0} max={23} value={leaveHr} onChange={e => setLeaveHr(+e.target.value)} />
      </div>

      <div className="grid-2" style={{ gap: 10, marginBottom: 14 }}>
        {/* Clean route */}
        <div className="route-blue">
          <div style={{ fontSize: 14, fontWeight: 800, color: G.blue }}>OK CLEAN ROUTE</div>
          <div style={{ color: "#7dd3fc", fontSize: 10, letterSpacing: 2, marginBottom: 10 }}>LOW EMISSIONS - RECOMMENDED</div>
          <div className="grid-2">
            {[["Congestion", `${congA}%`, G.blue], ["Time", `${timeA} min`, G.blue],
              ["Distance",   `${distA} km`, G.green2], ["CO2", `${co2A} kg`, G.green2]
            ].map(([l, v, c]) => (
              <div key={l}>
                <div className="mono" style={{ fontSize: 22, fontWeight: 900, color: c }}>{v}</div>
                <div style={{ color: "#64748b", fontSize: 10 }}>{l.toUpperCase()}</div>
              </div>
            ))}
          </div>
          <div style={{ marginTop: 10, background: "#0a1a2e", borderRadius: 8, padding: 8, fontSize: 12, color: "#7dd3fc" }}>
            Smooth flow - Earn +15 Green Points
          </div>
        </div>
        {/* High emission route */}
        <div className="route-red">
          <div style={{ fontSize: 14, fontWeight: 800, color: G.red }}>X HIGH EMISSION ROUTE</div>
          <div style={{ color: "#fca5a5", fontSize: 10, letterSpacing: 2, marginBottom: 10 }}>HEAVY TRAFFIC - AVOID</div>
          <div className="grid-2">
            {[["Congestion", `${congB}%`, G.red], ["Time", `${timeB} min`, G.red],
              ["Distance",   `${distB} km`, "#f87171"], ["CO2", `${co2B} kg`, "#f87171"]
            ].map(([l, v, c]) => (
              <div key={l}>
                <div className="mono" style={{ fontSize: 22, fontWeight: 900, color: c }}>{v}</div>
                <div style={{ color: "#64748b", fontSize: 10 }}>{l.toUpperCase()}</div>
              </div>
            ))}
          </div>
          <div style={{ marginTop: 10, background: "#1c0808", borderRadius: 8, padding: 8, fontSize: 12, color: "#fca5a5" }}>
            Stop-and-go - High idling - More fuel
          </div>
        </div>
      </div>

      <div className="alert-green">
        <b style={{ color: G.green }}>Smart Advisor</b><br />
        <span style={{ color: "#86efac", fontSize: 13 }}>
          Taking the Clean Route saves <b>{(co2B - co2A).toFixed(2)} kg CO2</b> and
          ~<b>R{((fuelB - fuelA) * 20).toFixed(2)}</b> in fuel. Earn <b>+15 Green Points</b>.
        </span>
      </div>

      <button className="btn-green" style={{ marginTop: 14 }} onClick={takeTrip}>
        Car Take Clean Route -- Start Trip
      </button>
      {tripMsg && <div className="alert-green" style={{ marginTop: 8 }}><b style={{ color: G.green }}>{tripMsg}</b> Total: {state.greenPoints + 15} pts</div>}
    </div>
  );
}

// --- PAGE: EMISSION ALERTS ---
function EmissionAlerts() {
  const r      = seededRand(HOUR * 3 + 7);
  const emPct  = IS_RUSH ? Math.floor(r() * 75) + 20 : Math.floor(r() * 45) + 10;
  const speed  = IS_RUSH ? Math.floor(r() * 30) + 15 : Math.floor(r() * 50) + 50;
  const idle   = Math.floor(r() * 8);
  const rpm    = Math.floor(r() * 3200) + 800;

  const speedData = [0,10,20,30,40,50,60,70,80,90,100,110,120].map((s, i) => ({
    speed: s, emission: [85,80,70,55,38,25,20,18,22,30,42,58,75][i],
  }));

  const actions = [
    { icon: "Tools", title: "Check Engine Diagnostics",  desc: "Run OBD scan or visit mechanic if emissions stay high.",         color: G.red   },
    { icon: "Fuel",  title: "Reduce Fuel Waste",          desc: "Avoid rapid acceleration, maintain 60-80 km/h, reduce RPM.",     color: G.amber },
    { icon: "Wrench",title: "Service Your Vehicle",       desc: "Oil change, air filter, fuel injector cleaning, exhaust check.", color: G.blue  },
    { icon: "Stop",  title: "Stop Unnecessary Idling",    desc: "Switch off engine after 1 minute of idling.",                    color: G.amber },
    { icon: "Map",   title: "Switch to a Cleaner Route",  desc: "Less traffic = less emissions. Open City Map for options.",      color: G.green },
  ];

  return (
    <div>
      <PageHead emoji="⚠️" title="Emission Alerts" sub="Live diagnostics and driving behaviour intelligence" />

      {emPct > 65
        ? <div className="alert-red">
            <b style={{ color: G.red, fontSize: 16 }}>HIGH EMISSION DETECTED</b><br />
            <span style={{ color: "#fca5a5", fontSize: 13 }}>Above-normal emissions. Reduce speed and check diagnostics.</span>
          </div>
        : emPct > 40
        ? <div className="alert-amber">
            <b style={{ color: G.amber, fontSize: 16 }}>MODERATE EMISSIONS</b><br />
            <span style={{ color: "#fde68a", fontSize: 13 }}>Slightly elevated -- maintain steady speed and avoid sudden braking.</span>
          </div>
        : <div className="alert-green">
            <b style={{ color: G.green, fontSize: 16 }}>LOW EMISSIONS -- CLEAN DRIVING</b><br />
            <span style={{ color: "#86efac", fontSize: 13 }}>Excellent! Keep it up and earn Green Points.</span>
          </div>
      }

      <div className="grid-4" style={{ margin: "12px 0" }}>
        <KpiCard value={`${emPct}%`}   label="EMISSION LEVEL"
          cls={emPct > 65 ? "card-red" : emPct > 40 ? "card-amber" : ""}
          kvcls={emPct > 65 ? "kv-red" : emPct > 40 ? "kv-amber" : "kv-green"} />
        <KpiCard value={`${speed} km/h`} label="SPEED"      cls="card-blue" kvcls="kv-blue" />
        <KpiCard value={`${idle} min`}   label="IDLE TIME"
          cls={idle > 2 ? "card-amber" : ""}  kvcls={idle > 2 ? "kv-amber" : "kv-green"} />
        <KpiCard value={rpm}             label="ENGINE RPM"
          cls={rpm > 3000 ? "card-red" : ""}  kvcls={rpm > 3000 ? "kv-red" : "kv-green"} />
      </div>

      <div className="sec-head">Speed and Emission Relationship</div>
      <div style={{ background: G.bg1, border: `1px solid ${G.border}`, borderRadius: 12, padding: 10 }}>
        <ResponsiveContainer width="100%" height={160}>
          <LineChart data={speedData}>
            <XAxis dataKey="speed" tick={{ fill: G.muted, fontSize: 10 }} />
            <YAxis tick={{ fill: G.muted, fontSize: 10 }} />
            <Tooltip contentStyle={{ background: G.bg2, border: `1px solid ${G.border}`, borderRadius: 8 }} />
            <Line type="monotone" dataKey="emission" stroke={G.green} strokeWidth={2} dot={false} />
          </LineChart>
        </ResponsiveContainer>
      </div>
      <div className="alert-green" style={{ marginTop: 8 }}>
        <b style={{ color: G.green }}>Key Insight</b>{" "}
        <span style={{ color: "#86efac", fontSize: 13 }}>Driving at a steady 60-80 km/h produces the least pollution. Stop-and-go and high speeds burn significantly more fuel.</span>
      </div>

      <div className="sec-head">Action Plan</div>
      {actions.map(a => (
        <div key={a.title} className="action-card" style={{ borderLeft: `3px solid ${a.color}` }}>
          <div style={{ color: a.color, fontWeight: 700, fontSize: 14 }}>{a.icon} - {a.title}</div>
          <div style={{ color: "#94a3b8", fontSize: 13, marginTop: 4 }}>{a.desc}</div>
        </div>
      ))}
    </div>
  );
}

// --- PAGE: ANALYTICS ---
function Analytics() {
  const [tab, setTab] = useState(0);
  const TABS = ["Hourly Trends", "Zone Emissions", "Cost Impact", "Heatmap"];

  const hourly = Array.from({ length: 24 }, (_, h) => {
    const r = seededRand(h * 5 + 3);
    let em = Math.floor(r() * 35) + 15;
    if ((h >= 7 && h <= 9) || (h >= 16 && h <= 18)) em = Math.min(100, em + 35);
    return { hour: `${h}:00`, emission: em, speed: Math.max(10, 85 - em / 2) };
  });

  const zones = LOC_NAMES.map((n, i) => {
    const c = congestionFor(i * 11 + 2, HOUR);
    return { name: n, congestion: c, ...emissionLevel(c) };
  });

  const DAYS = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"];
  const HRS  = [6,7,8,9,10,11,12,13,14,15,16,17,18,19,20];
  const heat = DAYS.map((d, di) => {
    const row = { day: d };
    HRS.forEach(h => {
      const r = seededRand(di * 100 + h);
      let v = Math.floor(r() * 70) + 10;
      if ([7,8,17,18].includes(h) && di < 5) v = Math.min(100, v + 35);
      row[`${h}:00`] = v;
    });
    return row;
  });
  const heatColor = v => v > 65 ? "#7f1d1d" : v > 40 ? "#78350f" : "#14532d";

  const [weeklyKm,   setWeeklyKm]   = useState(200);
  const [fuelPrice,  setFuelPrice]  = useState(22);
  const [driveStyle, setDriveStyle] = useState("Moderate");
  const cons    = { Aggressive: 12, Moderate: 8, Eco: 6 };
  const litres  = weeklyKm / 100 * cons[driveStyle];
  const costWk  = (litres * fuelPrice).toFixed(2);
  const co2Wk   = (litres * 2.31).toFixed(2);
  const ecoSave = Math.max(0, (litres - weeklyKm / 100 * 6) * fuelPrice).toFixed(2);

  return (
    <div>
      <PageHead emoji="📊" title="Analytics" sub="Traffic and emission trends, zone status, cost impact" />
      <div className="tabs">
        {TABS.map((t, i) => <div key={i} className={`tab ${tab === i ? "active" : ""}`} onClick={() => setTab(i)}>{t}</div>)}
      </div>

      {tab === 0 && (
        <div>
          <div className="sec-head">24-Hour Emission and Speed Trends</div>
          <div style={{ background: G.bg1, border: `1px solid ${G.border}`, borderRadius: 12, padding: 10 }}>
            <ResponsiveContainer width="100%" height={200}>
              <LineChart data={hourly}>
                <XAxis dataKey="hour" tick={{ fill: G.muted, fontSize: 9 }} interval={3} />
                <YAxis tick={{ fill: G.muted, fontSize: 9 }} />
                <Tooltip contentStyle={{ background: G.bg2, border: `1px solid ${G.border}`, borderRadius: 8 }} />
                <Line type="monotone" dataKey="emission" stroke={G.red}  strokeWidth={2} dot={false} name="Emission %" />
                <Line type="monotone" dataKey="speed"    stroke={G.blue} strokeWidth={2} dot={false} name="Speed km/h" />
              </LineChart>
            </ResponsiveContainer>
          </div>
          <div className="alert-amber" style={{ marginTop: 8 }}>
            <b style={{ color: G.amber }}>Peak:</b>{" "}
            <span style={{ color: "#fde68a", fontSize: 13 }}>Rush hours 07:00-09:00 and 16:00-18:00. Cleanest window: 10:00-15:00.</span>
          </div>
        </div>
      )}

      {tab === 1 && (
        <div>
          <div className="sec-head">Zone Emission Status</div>
          {zones.map(z => (
            <div key={z.name} style={{ background: "#0a0f1e", border: `1px solid ${G.border}`, borderRadius: 10, padding: 12, marginBottom: 8 }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <span style={{ fontWeight: 700, fontSize: 14 }}>{z.name}</span>
                <span style={{ background: z.color + "22", color: z.color, border: `1px solid ${z.color}55`, borderRadius: 20, padding: "2px 10px", fontSize: 11, fontWeight: 700 }}>{z.label}</span>
              </div>
              <div className="pbar-bg"><div className="pbar-fill" style={{ width: `${z.congestion}%`, background: z.color }} /></div>
              <div style={{ color: "#64748b", fontSize: 12 }}>{z.congestion}% congestion</div>
            </div>
          ))}
        </div>
      )}

      {tab === 2 && (
        <div>
          <div className="sec-head">Fuel Cost Impact Estimator</div>
          <div style={{ marginBottom: 10 }}>
            <div className="lbl">WEEKLY DRIVING: {weeklyKm} km</div>
            <input type="range" min={50} max={500} value={weeklyKm} onChange={e => setWeeklyKm(+e.target.value)} />
          </div>
          <div style={{ marginBottom: 10 }}>
            <div className="lbl">FUEL PRICE: R{fuelPrice}/L</div>
            <input type="range" min={18} max={30} value={fuelPrice} onChange={e => setFuelPrice(+e.target.value)} />
          </div>
          <div style={{ marginBottom: 14 }}>
            <div className="lbl">DRIVING STYLE</div>
            <select className="sel" value={driveStyle} onChange={e => setDriveStyle(e.target.value)}>
              {["Aggressive","Moderate","Eco"].map(s => <option key={s}>{s}</option>)}
            </select>
          </div>
          <div className="grid-2" style={{ gap: 10 }}>
            <KpiCard value={`R${costWk}`}                   label="WEEKLY FUEL COST"   cls="card-amber" kvcls="kv-amber" />
            <KpiCard value={`${co2Wk} kg`}                  label="CO2 PER WEEK"       cls="card-red"   kvcls="kv-red"   />
            <KpiCard value={`R${(+costWk * 4.3).toFixed(0)}`} label="MONTHLY COST"     cls="card-red"   kvcls="kv-red"   />
            <KpiCard value={`R${ecoSave}`}                  label="POTENTIAL SAVING/WK" />
          </div>
          {+ecoSave > 0 && (
            <div className="alert-amber" style={{ marginTop: 10 }}>
              <b style={{ color: G.amber }}>Tip:</b>{" "}
              <span style={{ color: "#fde68a", fontSize: 13 }}>Switch to Eco driving to save R{ecoSave}/week (R{(+ecoSave * 52).toFixed(0)}/year).</span>
            </div>
          )}
        </div>
      )}

      {tab === 3 && (
        <div>
          <div className="sec-head">Weekly Emission Heatmap</div>
          <div style={{ overflowX: "auto" }}>
            <table style={{ borderCollapse: "collapse", width: "100%", fontSize: 11 }}>
              <thead>
                <tr>
                  <th style={{ padding: "4px 8px", color: G.muted, textAlign: "left" }}>Day</th>
                  {HRS.map(h => <th key={h} style={{ padding: "4px 6px", color: G.muted }}>{h}:00</th>)}
                </tr>
              </thead>
              <tbody>
                {heat.map(row => (
                  <tr key={row.day}>
                    <td style={{ padding: "4px 8px", color: G.text, fontWeight: 700 }}>{row.day}</td>
                    {HRS.map(h => {
                      const v = row[`${h}:00`];
                      return (
                        <td key={h} style={{ padding: "4px 6px", background: heatColor(v), borderRadius: 4, textAlign: "center", color: "#ccc", fontFamily: "monospace" }}>{v}</td>
                      );
                    })}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <div style={{ color: G.muted, fontSize: 11, marginTop: 8 }}>Red = heavy congestion - Green = smooth flow</div>
        </div>
      )}
    </div>
  );
}

// --- PAGE: ECO SCORE ---
function EcoScore({ state }) {
  const s     = state.ecoScore;
  const grade = s >= 80 ? "A" : s >= 65 ? "B" : s >= 50 ? "C" : "D";
  const gCol  = s >= 80 ? G.green : s >= 65 ? G.green2 : s >= 50 ? G.amber : G.red;
  const label = s >= 80 ? "Excellent Eco Driver" : s >= 65 ? "Good Eco Driver" : s >= 50 ? "Average Driver" : "High Emission Driver";

  const weekLabels = ["6wk ago","5wk ago","4wk ago","3wk ago","2wk ago","Last wk","This wk"];
  const weekData   = weekLabels.map((w, i) => ({ week: w, score: state.weeklyScores[i] }));

  const factors = [
    ["Route Choices",     78, G.green],  ["Speed Consistency",  65, G.green2],
    ["Idle Management",   82, G.green],  ["Trip Efficiency",    70, G.amber],
    ["Emission Level",    55, G.amber],  ["Carpooling Bonus",   40, G.red],
  ];

  const leaderboard = [
    { rank: "1st", driver: "EcoDriver_01", score: 96, pts: 1240, co2: 148 },
    { rank: "2nd", driver: "GreenWheels",  score: 91, pts: 985,  co2: 118 },
    { rank: "3rd", driver: "CleanCommuter",score: 88, pts: 872,  co2: 104 },
    { rank: "4th", driver: state.username, score: s,  pts: state.greenPoints, co2: +(state.greenPoints * 0.12).toFixed(1) },
    { rank: "5th", driver: "QuickRacer",   score: 43, pts: 120,  co2: 14 },
  ];

  return (
    <div>
      <PageHead emoji="⭐" title="Eco Score" sub="Your environmental driving rating" />

      <div style={{ display: "flex", gap: 12, flexWrap: "wrap", marginBottom: 16 }}>
        <div className="card" style={{ textAlign: "center", padding: 24, minWidth: 140 }}>
          <div className="mono" style={{ fontSize: 64, fontWeight: 900, color: gCol }}>{grade}</div>
          <div className="mono" style={{ fontSize: 32, fontWeight: 900, color: gCol }}>{s}/100</div>
          <div style={{ color: "#64748b", fontSize: 10, letterSpacing: 2, marginTop: 8 }}>{label.toUpperCase()}</div>
        </div>
        <div style={{ flex: 1, minWidth: 200 }}>
          <div className="sec-head">Weekly Performance</div>
          <div style={{ background: G.bg1, border: `1px solid ${G.border}`, borderRadius: 12, padding: 10 }}>
            <ResponsiveContainer width="100%" height={130}>
              <LineChart data={weekData}>
                <XAxis dataKey="week" tick={{ fill: G.muted, fontSize: 9 }} />
                <YAxis domain={[40, 100]} tick={{ fill: G.muted, fontSize: 9 }} />
                <Tooltip contentStyle={{ background: G.bg2, border: `1px solid ${G.border}`, borderRadius: 8 }} />
                <Line type="monotone" dataKey="score" stroke={G.green} strokeWidth={2} dot={{ fill: G.green, r: 3 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      <div className="sec-head">Score Breakdown</div>
      {factors.map(([n, v, c]) => (
        <div key={n} style={{ marginBottom: 10 }}>
          <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 3 }}>
            <span style={{ fontSize: 13 }}>{n}</span>
            <span style={{ color: c, fontWeight: 700 }}>{v}/100</span>
          </div>
          <div className="pbar-bg"><div className="pbar-fill" style={{ width: `${v}%`, background: c }} /></div>
        </div>
      ))}

      <div className="sec-head">Driver Leaderboard</div>
      <div style={{ overflowX: "auto" }}>
        <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 13 }}>
          <thead>
            <tr style={{ borderBottom: `1px solid ${G.border}` }}>
              {["Rank","Driver","Eco Score","Green Pts","CO2 Saved"].map(h => (
                <th key={h} style={{ padding: "8px 10px", color: G.muted, textAlign: "left", fontSize: 11 }}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {leaderboard.map(row => (
              <tr key={row.rank} style={{ borderBottom: `1px solid ${G.border}`, background: row.driver === state.username ? "#0d2318" : "transparent" }}>
                <td style={{ padding: "8px 10px" }}>{row.rank}</td>
                <td style={{ padding: "8px 10px", color: row.driver === state.username ? G.green2 : G.text, fontWeight: row.driver === state.username ? 700 : 400 }}>{row.driver}</td>
                <td style={{ padding: "8px 10px", fontFamily: "monospace", color: G.green2 }}>{row.score}</td>
                <td style={{ padding: "8px 10px", fontFamily: "monospace", color: G.amber  }}>{row.pts}</td>
                <td style={{ padding: "8px 10px", fontFamily: "monospace", color: G.blue   }}>{row.co2} kg</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

// --- PAGE: REWARDS ---
function Rewards({ state }) {
  const pts = state.greenPoints;

  const rewardList = [
    { name: "Fuel Voucher",          cost: 50,  desc: "Save R10 at participating fuel stations",  color: G.amber   },
    { name: "Petrol Discount 10%",   cost: 120, desc: "10% off your next full tank",              color: G.amber   },
    { name: "Shopping Voucher R50",  cost: 100, desc: "Redeem at partner retailers",              color: G.blue    },
    { name: "Transport Credit",      cost: 80,  desc: "Bus or taxi credit for 5 trips",           color: G.green   },
    { name: "Free Vehicle Check",    cost: 200, desc: "Emission diagnostic + engine check",       color: "#a78bfa" },
    { name: "Tree Planting Credit",  cost: 30,  desc: "Sponsor a tree planted in your name",      color: G.green   },
    { name: "Partner Discounts",     cost: 60,  desc: "Discounts at eco-friendly stores",         color: G.blue    },
    { name: "Premium Eco Status",    cost: 500, desc: "Unlock premium leaderboard + extra pts",   color: G.amber   },
  ];

  const earnTips = [
    ["Clean Routes",      "+15 pts/trip"], ["Steady Speed",        "+5 pts/trip"],
    ["Public Transport",  "+20 pts/trip"], ["No Idling",           "+3 pts"      ],
    ["Carpool",           "+25 pts/trip"], ["Vehicle Service",     "+50 pts"     ],
  ];

  return (
    <div>
      <PageHead emoji="🎁" title="Rewards" sub="Convert your Green Points into real-world rewards" />

      <div style={{ background: "linear-gradient(135deg,#0f2a0a,#1a3a10)", border: "1px solid #166534", borderRadius: 16, padding: 24, marginBottom: 16 }}>
        <div style={{ fontFamily: "monospace", fontSize: 10, color: "#86efac", letterSpacing: 3 }}>MELLOWTECH REWARDS CARD</div>
        <div className="mono" style={{ fontSize: 36, fontWeight: 900, color: G.green2, margin: "6px 0" }}>{pts} pts</div>
        <div style={{ color: G.green, fontSize: 13 }}>{state.username}</div>
        <div style={{ color: "#64748b", fontSize: 11, marginTop: 4 }}>{DATE_STR} - ACTIVE</div>
      </div>

      <div className="grid-2">
        {rewardList.map(rw => {
          const can = pts >= rw.cost;
          return (
            <div key={rw.name} className="reward-card" style={{ borderColor: can ? rw.color + "55" : G.border }}>
              <div style={{ fontWeight: 700, fontSize: 14, color: can ? G.text : "#334155" }}>{rw.name}</div>
              <div style={{ color: "#64748b", fontSize: 12, margin: "4px 0" }}>{rw.desc}</div>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginTop: 8 }}>
                <span className="mono" style={{ fontSize: 18, fontWeight: 900, color: rw.color }}>{rw.cost} pts</span>
                <span style={{ fontSize: 11, fontWeight: 600, color: can ? rw.color : "#334155" }}>
                  {can ? "Tap to Redeem" : `Need ${rw.cost - pts} more`}
                </span>
              </div>
            </div>
          );
        })}
      </div>

      <div className="sec-head">How to Earn Green Points</div>
      <div className="grid-2">
        {earnTips.map(([tip, val]) => (
          <div key={tip} style={{ background: "#071a0e", border: "1px solid #14532d", borderRadius: 10, padding: 12, textAlign: "center", marginBottom: 8 }}>
            <div style={{ fontWeight: 700, fontSize: 13, color: G.green2 }}>{tip}</div>
            <div className="mono" style={{ color: G.green, fontSize: 15, fontWeight: 900, marginTop: 4 }}>{val}</div>
          </div>
        ))}
      </div>
    </div>
  );
}

// --- PAGE: PROFILE ---
function Profile({ state, setState }) {
  const [name,  setName]  = useState(state.username);
  const [home,  setHome]  = useState(state.home);
  const [mode,  setMode]  = useState(state.drivingMode);
  const [saved, setSaved] = useState(false);

  const s     = state.ecoScore;
  const grade = s >= 80 ? "A" : s >= 65 ? "B" : s >= 50 ? "C" : "D";
  const gCol  = s >= 80 ? G.green : s >= 65 ? G.green2 : s >= 50 ? G.amber : G.red;
  const co2   = +(state.greenPoints * 0.12).toFixed(2);
  const fuel  = +(state.greenPoints * 0.05).toFixed(2);

  function save() {
    setState(prev => ({ ...prev, username: name, home, drivingMode: mode }));
    setSaved(true);
    setTimeout(() => setSaved(false), 2500);
  }

  return (
    <div>
      <PageHead emoji="👤" title="Profile" sub="Your account and preferences" />

      <div style={{ display: "flex", gap: 12, flexWrap: "wrap", marginBottom: 16 }}>
        <div className="card" style={{ textAlign: "center", padding: 24, minWidth: 160 }}>
          <div style={{ fontSize: 44 }}>🌿</div>
          <div style={{ fontSize: 17, fontWeight: 900, color: G.green, marginTop: 8 }}>{state.username}</div>
          <span className="badge" style={{ marginTop: 6 }}>GRADE {grade}</span>
          <hr style={{ borderColor: G.border, margin: "12px 0" }} />
          <div style={{ color: "#64748b", fontSize: 11 }}>Member since {now.toLocaleDateString("en-ZA", { month: "short", year: "numeric" })}</div>
          <div className="mono" style={{ fontSize: 28, fontWeight: 900, color: gCol, marginTop: 10 }}>{s}/100</div>
          <div style={{ color: "#64748b", fontSize: 10, letterSpacing: 2 }}>ECO SCORE</div>
          <div className="mono" style={{ fontSize: 24, fontWeight: 900, color: G.green2, marginTop: 8 }}>{state.greenPoints}</div>
          <div style={{ color: "#64748b", fontSize: 10, letterSpacing: 2 }}>GREEN POINTS</div>
        </div>

        <div style={{ flex: 1, minWidth: 200 }}>
          <div className="sec-head">Preferences</div>
          <div style={{ marginBottom: 10 }}>
            <div className="lbl">DISPLAY NAME</div>
            <input className="inp" value={name} onChange={e => setName(e.target.value)} />
          </div>
          <div style={{ marginBottom: 10 }}>
            <div className="lbl">HOME LOCATION</div>
            <select className="sel" value={home} onChange={e => setHome(e.target.value)}>
              {LOC_NAMES.map(l => <option key={l}>{l}</option>)}
            </select>
          </div>
          <div style={{ marginBottom: 14 }}>
            <div className="lbl">DEFAULT DRIVING MODE</div>
            <select className="sel" value={mode} onChange={e => setMode(e.target.value)}>
              {["Eco Mode","Normal Mode","Fast Mode"].map(m => <option key={m}>{m}</option>)}
            </select>
          </div>
          <button className="btn-green" onClick={save}>Save Preferences</button>
          {saved && (
            <div className="alert-green" style={{ marginTop: 8 }}>
              <b style={{ color: G.green }}>Preferences saved!</b>
            </div>
          )}
        </div>
      </div>

      <div className="sec-head">My Environmental Impact</div>
      <div className="grid-4" style={{ gap: 10 }}>
        <KpiCard value={`${co2} kg`}          label="CO2 SAVED" />
        <KpiCard value={`${fuel} L`}           label="FUEL SAVED"   cls="card-amber" kvcls="kv-amber" />
        <KpiCard value={`R${(fuel*22).toFixed(2)}`} label="MONEY SAVED" cls="card-blue"  kvcls="kv-blue" />
        <KpiCard value={state.trips}           label="TRIPS DONE" />
      </div>

      <div className="alert-green" style={{ marginTop: 12 }}>
        <b style={{ color: G.green }}>Your Climate Contribution</b><br />
        <span style={{ color: "#86efac", fontSize: 13 }}>
          By using MellowTech you help reduce urban air pollution and contribute to South Africa's climate goals. Every clean trip counts.
        </span>
      </div>
    </div>
  );
}

// --- ROOT APP ---
export default function App() {
  const [loggedIn,  setLoggedIn]  = useState(false);
  const [username,  setUsername]  = useState("");
  const [password,  setPassword]  = useState("");
  const [loginErr,  setLoginErr]  = useState("");

  const [drawerOpen, setDrawerOpen] = useState(false);
  const [page,       setPage]       = useState("dashboard");

  const [appState, setAppState] = useState({
    username:     "",
    greenPoints:  0,
    ecoScore:     72,
    trips:        0,
    home:         "Home",
    drivingMode:  "Normal",
    weeklyScores: [55, 61, 58, 67, 70, 68, 72],
  });

  const touchStartX = useRef(null);
  function onTouchStart(e) { touchStartX.current = e.touches[0].clientX; }
  function onTouchEnd(e) {
    if (touchStartX.current === null) return;
    const dx = e.changedTouches[0].clientX - touchStartX.current;
    if (dx >  60) setDrawerOpen(true);
    if (dx < -60) setDrawerOpen(false);
    touchStartX.current = null;
  }

  function login() {
    if (!username.trim()) { setLoginErr("Please enter a username."); return; }
    if (!password)        { setLoginErr("Please enter a password."); return; }
    setAppState(s => ({ ...s, username: username.trim() }));
    setLoggedIn(true);
  }

  function navigate(id) { setPage(id); setDrawerOpen(false); }

  const PAGES = {
    dashboard: <Dashboard   state={appState} />,
    citymap:   <CityMap     navigate={navigate} />,
    routes:    <SmartRoutes state={appState} setState={setAppState} />,
    alerts:    <EmissionAlerts />,
    analytics: <Analytics />,
    ecoscore:  <EcoScore    state={appState} />,
    rewards:   <Rewards     state={appState} />,
    profile:   <Profile     state={appState} setState={setAppState} />,
  };

  return (
    <>
      <style>{css}</style>

      {!loggedIn ? (
        <div style={{ minHeight: "100vh", display: "flex", flexDirection: "column", justifyContent: "center" }}>
          <div style={{ textAlign: "center", marginBottom: 8 }}>
            <div style={{ fontSize: 40, fontWeight: 900, color: G.green2, letterSpacing: 4, fontFamily: "Share Tech Mono" }}>
              MELLOWTECH
            </div>
            <div style={{ color: G.muted, fontSize: 11, letterSpacing: 6, textTransform: "uppercase" }}>
              Smart Emission Intelligence System
            </div>
          </div>

          <div className="login-wrap">
            <h3 style={{ color: G.green, fontWeight: 900, marginBottom: 4 }}>Sign In</h3>
            <p style={{ color: G.muted, fontSize: 11, letterSpacing: 2, marginBottom: 20 }}>
              PROTECTING THE PLANET, ONE TRIP AT A TIME
            </p>
            <input
              className="inp" placeholder="Username"
              value={username} onChange={e => setUsername(e.target.value)}
              onKeyDown={e => e.key === "Enter" && login()}
            />
            <input
              className="inp" type="password" placeholder="Password"
              value={password} onChange={e => setPassword(e.target.value)}
              onKeyDown={e => e.key === "Enter" && login()}
            />
            {loginErr && <div style={{ color: G.red, fontSize: 13, marginBottom: 8 }}>{loginErr}</div>}
            <button className="btn-green" onClick={login}>Launch MellowTech</button>
            <p style={{ color: "#334155", fontSize: 11, marginTop: 14 }}>Demo: any username + any password</p>
          </div>
        </div>

      ) : (
        <div onTouchStart={onTouchStart} onTouchEnd={onTouchEnd} style={{ minHeight: "100vh" }}>

          <div
            className={`drawer-overlay ${drawerOpen ? "" : "hidden"}`}
            onClick={() => setDrawerOpen(false)}
          />

          <div className={`drawer ${drawerOpen ? "open" : ""}`}>
            <div style={{ padding: "20px 20px 14px", borderBottom: `1px solid ${G.border}` }}>
              <div style={{ color: G.green2, fontSize: 18, fontWeight: 900, letterSpacing: 3 }}>🌿 MELLOWTECH</div>
              <div style={{ color: "#334155", fontSize: 9, letterSpacing: 2, marginTop: 2 }}>EMISSION INTELLIGENCE</div>
            </div>

            <div style={{ padding: "12px 20px", borderBottom: `1px solid ${G.border}` }}>
              <div style={{ color: G.text, fontSize: 13, fontWeight: 600 }}>👤 {appState.username}</div>
              <div style={{ color: G.green, fontSize: 11, marginTop: 2 }}>{appState.greenPoints} Green Points</div>
            </div>

            <div style={{ flex: 1, overflowY: "auto", padding: "8px 0" }}>
              {NAV.map(n => (
                <div
                  key={n.id}
                  className={`nav-item ${page === n.id ? "active" : ""}`}
                  onClick={() => navigate(n.id)}
                >
                  <span className="nav-icon">{n.icon}</span>
                  <span>{n.label}</span>
                </div>
              ))}
            </div>

            <div style={{ padding: "12px 20px", borderTop: `1px solid ${G.border}` }}>
              <div style={{ color: G.muted, fontSize: 10, letterSpacing: 2, marginBottom: 4 }}>ECO SCORE</div>
              <div className="pbar-bg">
                <div className="pbar-fill" style={{ width: `${appState.ecoScore}%`, background: G.green }} />
              </div>
              <div style={{ color: G.green2, fontSize: 13, fontWeight: 700, marginTop: 4 }}>{appState.ecoScore}/100</div>
            </div>

            <div style={{ padding: "12px 20px", borderTop: `1px solid ${G.border}` }}>
              <button
                className="btn-sm"
                style={{ width: "100%" }}
                onClick={() => { setLoggedIn(false); setUsername(""); setPassword(""); setPage("dashboard"); }}
              >
                Sign Out
              </button>
            </div>
          </div>

          <div className="topbar">
            <button className="hamburger" onClick={() => setDrawerOpen(o => !o)} aria-label="Open menu">
              <span /><span /><span />
            </button>
            <span className="topbar-title">MELLOWTECH</span>
            <span style={{ marginLeft: "auto", color: IS_RUSH ? G.red : G.green, fontSize: 11, fontWeight: 700 }}>
              {IS_RUSH ? "RUSH HOUR" : "TRAFFIC CLEAR"}
            </span>
          </div>

          <main className="content" style={{ paddingTop: 16 }}>
            {PAGES[page]}
          </main>

        </div>
      )}
    </>
  );
}
