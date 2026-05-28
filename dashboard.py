"""
NSE Results Watchlist — Streamlit Web Dashboard v2
====================================================
Improvements: Returns Tracker, Action Required, Sector Beat Rate,
Share Button, Mobile-optimised sidebar
"""

import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime, date
from collections import Counter
import time
import urllib.parse
from data import STOCKS, TICKER_MAP, RATING_COLORS, RATING_BG, RISK_BG

st.set_page_config(
    page_title="NSE Watchlist | Q4 FY26",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",   # #7 mobile-friendly: collapsed by default
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
  .main { background-color: #F8FAFC; }

  /* Metrics */
  .stMetric { background: white; border-radius: 12px; padding: 16px;
              box-shadow: 0 1px 4px rgba(0,0,0,0.08); }
  .stMetric label { font-size: 12px !important; color: #6B7280; }

  /* Typography */
  h1 { color: #0D1B2A; font-weight: 700; }
  h2 { color: #1A3A5C; font-weight: 600; border-bottom: 2px solid #E5E7EB; padding-bottom: 6px; }
  h3 { color: #374151; font-weight: 600; }

  /* Cards */
  .commentary-box { background: #F0F9FF; border-left: 3px solid #0EA5E9;
                    padding: 12px 16px; border-radius: 0 8px 8px 0;
                    font-size: 13px; color: #1E3A5F; line-height: 1.6; }
  .action-card    { background: #FFF9F0; border-left: 4px solid #F59E0B;
                    padding: 14px 18px; border-radius: 0 10px 10px 0;
                    margin-bottom: 10px; }
  .share-box      { background: #F0FDF4; border: 1px solid #BBF7D0;
                    border-radius: 8px; padding: 10px 14px; font-size: 12px;
                    font-family: monospace; white-space: pre-wrap; color: #166534; }
  .win-badge      { display:inline-block; padding:2px 10px; border-radius:999px;
                    font-size:12px; font-weight:700; }

  /* Mobile sidebar */
  @media (max-width: 768px) {
    section[data-testid="stSidebar"] { width: 85vw !important; }
    .stMetric { padding: 10px; }
  }

  div[data-testid="stExpander"] { border: 1px solid #E5E7EB; border-radius: 8px; }
  .stDataFrame { border-radius: 8px; overflow: hidden; }
  footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📊 NSE Watchlist\n**Q4 FY26 Results Tracker**")
    st.caption(f"James | {datetime.now().strftime('%d %b %Y')}")
    st.divider()

    page = st.radio("Navigate", [
        "🏠 Dashboard",
        "🗓 Results Calendar",
        "📈 Pre-Result Setup",
        "🎯 Post-Result Tracker",
        "💰 Returns Tracker",
        "🔬 Stock Deep Dive",
        "⚙️ Live Prices",
    ])
    st.divider()
    st.markdown("**Filters**")
    status_filter = st.multiselect("Status", ["Declared","Pending"],
                                    default=["Declared","Pending"])
    rating_filter = st.multiselect("My Rating",
                                    ["STRONG BUY","BUY","ACCUMULATE","HOLD",
                                     "HOLD / BOOK","REDUCE","AVOID"],
                                    default=["STRONG BUY","BUY","ACCUMULATE",
                                             "HOLD","HOLD / BOOK","REDUCE","AVOID"])
    st.divider()
    st.caption("⚠️ Personal tracking tool. Not SEBI-registered investment advice.")

# ── Helpers ───────────────────────────────────────────────────────────────────
def fs():
    return [s for s in STOCKS
            if s["status"] in status_filter and s["ind_rating"] in rating_filter]

def rating_badge(r, sz=12):
    bg  = RATING_BG.get(r, "#F3F4F6")
    col = RATING_COLORS.get(r, "#374151")
    return f'<span style="background:{bg};color:{col};font-weight:700;padding:2px 10px;border-radius:999px;font-size:{sz}px">{r}</span>'

def share_text(s):
    """Build WhatsApp-ready share text for a stock."""
    eps_line = ""
    if s.get("act_eps") and s.get("est_eps"):
        beat = (s["act_eps"] - s["est_eps"]) / abs(s["est_eps"]) * 100
        eps_line = f"EPS: ₹{s['act_eps']} ({beat:+.1f}% {'✅ BEAT' if beat>0 else '❌ MISS'})\n"
    return (
        f"📊 *{s['name']}* | {s.get('quarter','Q4 FY26')}\n"
        f"Sector: {s['sector']}\n"
        f"Result: {s['result_date']} | Status: {s['status']}\n"
        f"{eps_line}"
        f"My Rating: *{s['ind_rating']}* | Risk: {s['risk']}\n"
        f"Rationale: {s['ind_rationale'][:120]}...\n"
        f"📌 {s.get('catalyst','')[:100]}\n\n"
        f"View: https://nse-watchlist-james.streamlit.app"
    )

# ── Parse result dates ────────────────────────────────────────────────────────
def parse_date(date_str):
    if not date_str:
        return None
    clean = str(date_str).replace(" ✅","").replace(" ⏳","").strip()
    for fmt in ["%d-%b-%y", "%d-%b-%Y", "%d-%m-%Y"]:
        try:
            return datetime.strptime(clean, fmt).date()
        except:
            continue
    return None

TODAY = date.today()

# ─────────────────────────────────────────────────────────────────────────────
# PAGE: DASHBOARD
# ─────────────────────────────────────────────────────────────────────────────
if page == "🏠 Dashboard":
    st.markdown("# 📊 NSE Results Watchlist — Q4 FY26")
    st.caption(f"James's personal tracker | {len(STOCKS)} stocks | {datetime.now().strftime('%d %b %Y %H:%M')}")

    declared  = [s for s in STOCKS if s["status"] == "Declared"]
    pending   = [s for s in STOCKS if s["status"] == "Pending"]
    beats     = [s for s in declared if s.get("act_eps") and s.get("est_eps") and s["act_eps"] > s["est_eps"]]
    misses    = [s for s in declared if s.get("act_eps") and s.get("est_eps") and s["act_eps"] < s["est_eps"]]
    captured  = [s for s in declared if s.get("upside_captured") == "YES"]
    strong    = [s for s in STOCKS if s["ind_rating"] in ("STRONG BUY","BUY")]

    c1,c2,c3,c4,c5,c6 = st.columns(6)
    c1.metric("Total Tracked",   f"{len(STOCKS)}")
    c2.metric("Declared",        f"{len(declared)}")
    c3.metric("Pending",         f"{len(pending)}")
    c4.metric("Beats / Misses",  f"{len(beats)} / {len(misses)}")
    c5.metric("Upside Captured", f"{len(captured)}")
    c6.metric("BUY / STRONG BUY",f"{len(strong)}")

    st.markdown("---")

    # ── #2 ACTION REQUIRED ────────────────────────────────────────────────────
    recent_declared = []
    for s in declared:
        d = parse_date(s.get("result_date",""))
        if d and (TODAY - d).days <= 2:
            needs_action = (
                "Auto-added" in str(s.get("earnings_commentary","")) or
                "Results pending" in str(s.get("earnings_commentary","")) or
                s.get("upside_captured") is None
            )
            if needs_action:
                recent_declared.append(s)

    if recent_declared:
        st.markdown("### 🚨 Action Required — Update These Now")
        for s in recent_declared:
            col = RATING_COLORS.get(s["ind_rating"],"#856404")
            bg  = RATING_BG.get(s["ind_rating"],"#FFF3CD")
            eps_beat = ""
            if s.get("act_eps") and s.get("est_eps") and s["est_eps"] != 0:
                b = (s["act_eps"] - s["est_eps"]) / abs(s["est_eps"]) * 100
                eps_beat = f"  |  EPS {'✅ +' if b>0 else '❌ '}{abs(b):.1f}%"
            st.markdown(f"""
            <div class="action-card">
              <b>{s['name']}</b> — {s['result_date']}{eps_beat}<br>
              <span style="background:{bg};color:{col};padding:2px 10px;border-radius:999px;
                           font-size:12px;font-weight:700">{s['ind_rating']}</span>
              <span style="font-size:12px;color:#6B7280;margin-left:8px">
                ⚠ Add earnings_commentary + upside_captured on GitHub
              </span>
            </div>""", unsafe_allow_html=True)
        st.markdown("---")
    else:
        st.success("✅ All recently declared stocks have been updated.")

    # ── Rating distribution + Radar ───────────────────────────────────────────
    col_a, col_b = st.columns([1,1])
    with col_a:
        st.markdown("### ⚖️ Independent Rating Distribution")
        dist = Counter(s["ind_rating"] for s in STOCKS)
        order = ["STRONG BUY","BUY","ACCUMULATE","HOLD","HOLD / BOOK","REDUCE","AVOID"]
        rows = [{"Rating":r,"Count":dist[r],"Stocks":", ".join(s["name"] for s in STOCKS if s["ind_rating"]==r)}
                for r in order if r in dist]
        df_dist = pd.DataFrame(rows)
        def color_r(val):
            return f"background-color:{RATING_BG.get(val,'#F3F4F6')};color:{RATING_COLORS.get(val,'#374151')};font-weight:600"
        st.dataframe(df_dist.style.map(color_r, subset=["Rating"]),
                     use_container_width=True, hide_index=True, height=280)

    with col_b:
        st.markdown("### 📅 15-Day Results Radar")
        radar = [
            ("May 21 ✅","GRASIM, GAIL, PRESTIGE","3 Declared"),
            ("May 22 ✅","CENTURY PLY, NH, RAINBOW CHILDCARE","3"),
            ("May 23 ✅","BALKRISNA, ASHOK LEYLAND, GLENMARK, LINDE","4"),
            ("May 25 ✅","SUZLON","1"),
            ("May 26 ✅","ASTRA MICROWAVE, JK TYRE, BHARAT RASAYAN","3"),
            ("May 27 ⏳","KEI INDUSTRIES, ASTRAL","2"),
            ("May 28 ⏳","JINDAL SAW, PFC, CUMMINS","3"),
            ("May 29 ⏳","ASIAN PAINTS, PREMIER EXPLOSIVES, SAIL, GLENMARK, ONGC, IPCA","6"),
            ("May 30 ⏳","BPCL, INDIAMART, LINDE","3"),
            ("Jun 2 ⏳","IREDA, COCHIN SHIPYARD","2"),
            ("Jun 3 ⏳","MFSL, POLYCAB","2"),
            ("Jun 4 ⏳","HUDCO","1"),
        ]
        df_r = pd.DataFrame(radar, columns=["Date","Companies","Count"])
        st.dataframe(df_r, use_container_width=True, hide_index=True, height=460)

    st.markdown("---")

    # ── #3 BEAT RATE BY SECTOR ────────────────────────────────────────────────
    st.markdown("### 📊 Beat Rate by Sector")
    sector_beats = {}
    for s in declared:
        if s.get("act_eps") and s.get("est_eps"):
            sec = s["sector"].split("(")[0].strip().split("/")[0].strip()[:25]
            if sec not in sector_beats:
                sector_beats[sec] = {"beats":0,"total":0,"stocks":[]}
            sector_beats[sec]["total"] += 1
            sector_beats[sec]["stocks"].append(s["name"])
            if s["act_eps"] > s["est_eps"]:
                sector_beats[sec]["beats"] += 1

    sector_rows = []
    for sec, data in sorted(sector_beats.items(), key=lambda x: -x[1]["beats"]/max(x[1]["total"],1)):
        rate = data["beats"] / data["total"] * 100
        sector_rows.append({
            "Sector":       sec,
            "Stocks":       data["total"],
            "Beats":        data["beats"],
            "Misses":       data["total"] - data["beats"],
            "Beat Rate":    f"{rate:.0f}%",
            "Companies":    ", ".join(data["stocks"]),
        })

    if sector_rows:
        df_sec = pd.DataFrame(sector_rows)
        def color_beat_rate(val):
            try:
                n = float(val.replace("%",""))
                if n >= 80: return "background-color:#D8F3DC;color:#1B4332;font-weight:700"
                elif n >= 50: return "background-color:#FFF3CD;color:#856404;font-weight:700"
                else: return "background-color:#FDDCDC;color:#C0392B;font-weight:700"
            except: return ""
        st.dataframe(df_sec.style.map(color_beat_rate, subset=["Beat Rate"]),
                     use_container_width=True, hide_index=True)

    st.info("⚠️ Independent ratings are personal assessments — not SEBI-registered research.")

# ─────────────────────────────────────────────────────────────────────────────
# PAGE: RESULTS CALENDAR
# ─────────────────────────────────────────────────────────────────────────────
elif page == "🗓 Results Calendar":
    st.markdown("## 🗓 Results Calendar — Q4 FY26")
    fstocks = fs()
    rows = []
    for s in fstocks:
        eps_beat = None
        if s.get("act_eps") and s.get("est_eps") and s["est_eps"] != 0:
            eps_beat = (s["act_eps"] - s["est_eps"]) / abs(s["est_eps"]) * 100
        rows.append({
            "Company":        s["name"],
            "Sector":         s["sector"],
            "Result Date":    s["result_date"],
            "Status":         s["status"],
            "Est. EPS (₹)":   s.get("est_eps"),
            "Act. EPS (₹)":   s.get("act_eps") if s.get("act_eps") else "Pending",
            "EPS Beat %":     f"{eps_beat:+.1f}%" if eps_beat is not None else "—",
            "Est. Rev (₹Cr)": s.get("est_rev"),
            "Sell-Side":      s.get("ss_rating"),
            "Target (₹)":     s.get("ss_target"),
            "My Rating":      s["ind_rating"],
            "Risk":           s["risk"],
        })
    df = pd.DataFrame(rows)
    def cs(val):
        if val=="Declared": return "background-color:#D8F3DC;color:#1B4332;font-weight:600"
        return "background-color:#FFF3CD;color:#856404;font-weight:600"
    def cr(val):
        return f"background-color:{RATING_BG.get(val,'#F3F4F6')};color:{RATING_COLORS.get(val,'#374151')};font-weight:600"
    def cb(val):
        if val=="—": return ""
        try:
            n=float(val.replace("%","").replace("+",""))
            return "background-color:#D8F3DC;color:#1B4332" if n>0 else "background-color:#FDDCDC;color:#C0392B"
        except: return ""
    def crisk(val):
        return f"background-color:{RISK_BG.get(val,'#F3F4F6')}"
    st.dataframe(df.style.map(cs,subset=["Status"]).map(cr,subset=["My Rating"])
                 .map(cb,subset=["EPS Beat %"]).map(crisk,subset=["Risk"]),
                 use_container_width=True, hide_index=True, height=700)
    st.caption(f"Showing {len(fstocks)} stocks")

# ─────────────────────────────────────────────────────────────────────────────
# PAGE: PRE-RESULT SETUP
# ─────────────────────────────────────────────────────────────────────────────
elif page == "📈 Pre-Result Setup":
    st.markdown("## 📈 Pre-Result Setup")
    pending_s = [s for s in fs() if s["status"]=="Pending"]
    st.caption(f"{len(pending_s)} pending results")
    if not pending_s:
        st.info("No pending results matching filters.")
    else:
        for s in pending_s:
            rat_bg  = RATING_BG.get(s["ind_rating"],"#F3F4F6")
            rat_col = RATING_COLORS.get(s["ind_rating"],"#374151")
            with st.expander(f"**{s['name']}** — {s['sector']} | 📅 {s['result_date']}"):
                c1,c2,c3,c4 = st.columns(4)
                c1.metric("Est. EPS",f"₹{s.get('est_eps','—')}")
                c2.metric("Est. Rev",f"₹{s.get('est_rev','—'):,}Cr" if s.get('est_rev') else "—")
                c3.metric("SS Target",f"₹{s.get('ss_target','—')}")
                c4.metric("SS Rating",s.get("ss_rating","—"))
                st.markdown(f'<span style="background:{rat_bg};color:{rat_col};font-weight:700;padding:4px 14px;border-radius:999px;font-size:13px">MY RATING: {s["ind_rating"]}</span>', unsafe_allow_html=True)
                st.markdown("**📌 Catalyst**")
                st.markdown(f'<div class="commentary-box">{s.get("catalyst","—")}</div>', unsafe_allow_html=True)
                st.markdown("**🔍 Independent Rationale**")
                st.markdown(f'<div class="commentary-box" style="background:#FFF9F0;border-color:#F59E0B">{s.get("ind_rationale","—")}</div>', unsafe_allow_html=True)
                st.markdown("**📋 What to Watch**")
                st.markdown(f'<div class="commentary-box" style="background:#F8F0FF;border-color:#8B5CF6">{s.get("earnings_commentary","—")}</div>', unsafe_allow_html=True)

                # ── #8 SHARE BUTTON ───────────────────────────────────────────
                share_msg = share_text(s)
                wa_url    = "https://wa.me/?text=" + urllib.parse.quote(share_msg)
                st.markdown(f'<a href="{wa_url}" target="_blank" style="background:#25D366;color:white;padding:7px 18px;border-radius:6px;text-decoration:none;font-size:13px;font-weight:600">📲 Share on WhatsApp</a>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# PAGE: POST-RESULT TRACKER
# ─────────────────────────────────────────────────────────────────────────────
elif page == "🎯 Post-Result Tracker":
    st.markdown("## 🎯 Post-Result Tracker")
    dec = [s for s in fs() if s["status"]=="Declared"]
    st.caption(f"{len(dec)} results declared")

    for s in dec:
        eps_beat_pct = None
        if s.get("act_eps") and s.get("est_eps") and s["est_eps"]!=0:
            eps_beat_pct = (s["act_eps"] - s["est_eps"]) / abs(s["est_eps"]) * 100
        rev_beat_pct = None
        if s.get("act_rev") and s.get("est_rev") and s["est_rev"]!=0:
            rev_beat_pct = (s["act_rev"] - s["est_rev"]) / abs(s["est_rev"]) * 100

        label = (f"**{s['name']}** | {s['result_date']} | "
                 f"EPS: ₹{s.get('act_eps','—')} "
                 f"({'BEAT ✅' if eps_beat_pct and eps_beat_pct>0 else 'MISS ❌'} "
                 f"{f'{eps_beat_pct:+.1f}%' if eps_beat_pct else ''})")

        with st.expander(label):
            c1,c2,c3,c4,c5 = st.columns(5)
            c1.metric("Est. EPS",  f"₹{s.get('est_eps','—')}")
            c2.metric("Actual EPS",f"₹{s.get('act_eps','—')}",
                      f"{eps_beat_pct:+.1f}%" if eps_beat_pct else None)
            c3.metric("Est. Rev",  f"₹{s.get('est_rev','—'):,}Cr" if s.get('est_rev') else "—")
            c4.metric("Actual Rev",f"₹{s.get('act_rev','—'):,}Cr" if s.get('act_rev') else "—",
                      f"{rev_beat_pct:+.1f}%" if rev_beat_pct else None)
            c5.metric("Upside Captured", s.get("upside_captured") or "—")

            st.markdown(rating_badge(s["ind_rating"],13), unsafe_allow_html=True)
            st.markdown("**📢 Earnings Commentary**")
            st.markdown(f'<div class="commentary-box">{s.get("earnings_commentary","—")}</div>', unsafe_allow_html=True)
            st.markdown("**⚖️ Independent View**")
            st.markdown(f'<div class="commentary-box" style="background:#FFF9F0;border-color:#F59E0B">{s.get("ind_rationale","—")}</div>', unsafe_allow_html=True)

            # ── #8 SHARE BUTTON ───────────────────────────────────────────────
            share_msg = share_text(s)
            wa_url    = "https://wa.me/?text=" + urllib.parse.quote(share_msg)
            st.markdown(f'<a href="{wa_url}" target="_blank" style="background:#25D366;color:white;padding:7px 18px;border-radius:6px;text-decoration:none;font-size:13px;font-weight:600">📲 Share on WhatsApp</a>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# PAGE: 💰 RETURNS TRACKER  (#1)
# ─────────────────────────────────────────────────────────────────────────────
elif page == "💰 Returns Tracker":
    st.markdown("## 💰 Returns Tracker — ₹1 Lakh per BUY Call")
    st.caption("Recommendation date = date stock was first discussed. ₹1,00,000 invested at rec price.")

    INV = 100000
    RETURNS_DATA = [
        ("PERSISTENT",        "STRONG BUY", "23-Apr-26", 5300,  5600),
        ("KEI INDUSTRIES",    "STRONG BUY", "04-May-26", 4250,  4548),
        ("POLYCAB",           "STRONG BUY", "06-May-26", 8800,  9465),
        ("BHARTI AIRTEL",     "BUY",        "13-May-26", 1720,  1902),
        ("CIPLA",             "BUY",        "13-May-26", 1480,  1590),
        ("INDIAN HOTELS",     "BUY",        "11-May-26", 630,   675),
        ("TATA POWER",        "BUY",        "12-May-26", 385,   415),
        ("SOLAR INDUSTRIES",  "BUY",        "15-May-26", 10200, 17900),
        ("SYRMA SGS",         "BUY",        "11-May-26", 1100,  1188),
        ("COCHIN SHIPYARD",   "BUY",        "21-May-26", 1532,  1548),
        ("PREMIER ENERGIES",  "BUY",        "15-May-26", 740,   820),
        ("UNO MINDA",         "BUY",        "16-May-26", 860,   950),
        ("PREMIER EXPLOSIVES","BUY",        "25-May-26", 595,   714),
        ("PIDILITE",          "BUY",        "07-May-26", 2800,  3050),
        ("SUN PHARMA",        "BUY",        "22-May-26", 1750,  1890),
        ("MARICO",            "BUY",        "07-May-26", 620,   668),
        ("DIVI'S LABS",       "BUY",        "23-May-26", 4800,  5200),
        ("CUMMINS INDIA",     "BUY",        "22-May-26", 3100,  3350),
        ("GAIL",              "ACCUMULATE", "21-May-26", 175,   192),
        ("PRESTIGE",          "ACCUMULATE", "21-May-26", 1420,  1620),
        ("NARAYANA HRUDAY",   "ACCUMULATE", "22-May-26", 1180,  1250),
        ("BALKRISNA IND",     "ACCUMULATE", "23-May-26", 2200,  2208),
        ("PFC",               "ACCUMULATE", "21-May-26", 370,   412),
        ("IREDA",             "ACCUMULATE", "21-May-26", 168,   188),
        ("VBL",               "ACCUMULATE", "27-Apr-26", 460,   485),
        ("CENTURY PLY",       "ACCUMULATE", "22-May-26", 640,   720),
        ("HAVELLS",           "ACCUMULATE", "22-Apr-26", 1350,  1510),
        ("OBEROI REALTY",     "ACCUMULATE", "08-May-26", 1700,  1850),
        ("NRB BEARING",       "ACCUMULATE", "07-May-26", 360,   390),
        ("TATA MOTORS",       "ACCUMULATE", "13-May-26", 680,   730),
        ("DR REDDY'S",        "ACCUMULATE", "12-May-26", 1260,  1380),
        ("DIXON TECHNOLOGIES","ACCUMULATE", "12-May-26", 10200, 11200),
        ("HAL",               "ACCUMULATE", "14-May-26", 4700,  5100),
        ("DLF",               "ACCUMULATE", "13-May-26", 790,   875),
        ("POWER GRID",        "ACCUMULATE", "15-May-26", 295,   318),
        ("KEC INTERNATIONAL", "ACCUMULATE", "16-May-26", 940,   1020),
        ("TORRENT POWER",     "ACCUMULATE", "13-May-26", 1640,  1780),
        ("MTAR TECHNOLOGIES", "ACCUMULATE", "12-May-26", 1800,  2100),
        ("TITAN",             "ACCUMULATE", "08-May-26", 4219,  4600),
        ("GODREJ CONSUMER",   "ACCUMULATE", "06-May-26", 1300,  1390),
        ("BERGER PAINTS",     "ACCUMULATE", "06-May-26", 460,   495),
        ("BRITANNIA",         "ACCUMULATE", "07-May-26", 5200,  5450),
        ("GODREJ PROPERTIES", "ACCUMULATE", "06-May-26", 2400,  2620),
        ("DABUR",             "ACCUMULATE", "07-May-26", 540,   575),
        ("INFO EDGE",         "ACCUMULATE", "22-May-26", 7200,  7650),
        ("FORTIS HEALTHCARE", "ACCUMULATE", "22-May-26", 580,   610),
        ("PAGE INDUSTRIES",   "ACCUMULATE", "21-May-26", 43000, 46000),
        ("EICHER MOTORS",     "ACCUMULATE", "22-May-26", 4700,  5050),
        # Reduce/Avoid for comparison
        ("GLENMARK PHARMA",   "REDUCE",     "21-May-26", 1350,  1320),
        ("JSW STEEL",         "REDUCE",     "21-May-26", 950,   980),
        ("BPCL",              "REDUCE",     "21-May-26", 295,   308),
        ("JK TYRE",           "AVOID",      "21-May-26", 330,   318),
        ("GOODLUCK INDIA",    "AVOID",      "21-May-26", 820,   798),
        ("PRINCE PIPES",      "HOLD",       "20-May-26", 280,   265),
        ("HPCL",              "REDUCE",     "13-May-26", 340,   318),
        ("PVR INOX",          "HOLD",       "11-May-26", 1380,  1290),
    ]

    # Deduplicate
    seen_r = set(); unique_r = []
    for row in RETURNS_DATA:
        if row[0] not in seen_r:
            seen_r.add(row[0]); unique_r.append(row)

    today_d = date.today()
    rows_r  = []
    total_inv = total_val = 0
    buy_inv   = buy_val   = 0

    for name, rating, rec_date_str, rec_price, today_price in unique_r:
        try:
            rec_d = datetime.strptime(rec_date_str, "%d-%b-%y").date()
        except:
            rec_d = datetime.strptime(rec_date_str, "%d-%b-%Y").date()
        days    = max((today_d - rec_d).days, 1)
        ret_pct = (today_price - rec_price) / rec_price
        curr_val= INV * (1 + ret_pct)
        pnl     = curr_val - INV

        rows_r.append({
            "Stock":        name,
            "Rating":       rating,
            "Rec. Date":    rec_date_str,
            "Rec. Price":   f"₹{rec_price:,}",
            "Today":        f"₹{today_price:,}",
            "Return %":     f"{ret_pct*100:+.1f}%",
            "Value of ₹1L": f"₹{curr_val:,.0f}",
            "P&L":          f"₹{pnl:+,.0f}",
            "Days Held":    days,
        })

        total_inv += INV; total_val += curr_val
        if rating in ("STRONG BUY","BUY","ACCUMULATE"):
            buy_inv += INV; buy_val += curr_val

    # Sort by return descending
    rows_r.sort(key=lambda x: float(x["Return %"].replace("%","").replace("+","")), reverse=True)
    df_ret = pd.DataFrame(rows_r)

    # Summary KPIs
    total_ret = (total_val - total_inv) / total_inv
    buy_ret   = (buy_val  - buy_inv)   / buy_inv

    k1,k2,k3,k4,k5 = st.columns(5)
    k1.metric("Stocks Tracked",    f"{len(unique_r)}")
    k2.metric("Total Deployed",    f"₹{total_inv/100000:.0f}L")
    k3.metric("Portfolio Value",   f"₹{total_val/100000:.1f}L")
    k4.metric("Total P&L",         f"₹{(total_val-total_inv)/100000:.1f}L",
              f"{total_ret*100:+.1f}%")
    k5.metric("BUY/ACCUM Return",  f"{buy_ret*100:+.1f}%")

    st.markdown("---")

    winners = sum(1 for r in rows_r if "+" in r["Return %"] and r["Rating"] in ("STRONG BUY","BUY","ACCUMULATE"))
    losers  = sum(1 for r in rows_r if "-" in r["Return %"] and r["Rating"] in ("STRONG BUY","BUY","ACCUMULATE"))
    buy_count = sum(1 for r in rows_r if r["Rating"] in ("STRONG BUY","BUY","ACCUMULATE"))
    hit_rate  = winners / buy_count * 100 if buy_count else 0

    st.markdown(f"""
    <div style="background:#D8F3DC;border-radius:10px;padding:14px 20px;margin-bottom:16px">
      <b>🏆 Hit Rate: {hit_rate:.0f}%</b> &nbsp;|&nbsp;
      Winners: <b>{winners}</b> &nbsp;|&nbsp;
      Losers: <b>{losers}</b> &nbsp;|&nbsp;
      Avg holding: <b>{sum(r['Days Held'] for r in rows_r)//len(rows_r)} days</b> &nbsp;|&nbsp;
      ⚠ XIRR not shown — holding period too short to be meaningful
    </div>""", unsafe_allow_html=True)

    def color_ret(val):
        if "+" in str(val): return "background-color:#D8F3DC;color:#1B4332;font-weight:700"
        elif "-" in str(val): return "background-color:#FDDCDC;color:#C0392B;font-weight:700"
        return ""
    def color_rat(val):
        return f"background-color:{RATING_BG.get(val,'#F3F4F6')};color:{RATING_COLORS.get(val,'#374151')};font-weight:600"

    st.dataframe(
        df_ret.style.map(color_ret, subset=["Return %","P&L"]).map(color_rat, subset=["Rating"]),
        use_container_width=True, hide_index=True, height=650
    )
    st.caption("⚠ Prices are approx CMP on recommendation date. Today's prices as of 27-May-2026. Not SEBI advice.")

# ─────────────────────────────────────────────────────────────────────────────
# PAGE: STOCK DEEP DIVE
# ─────────────────────────────────────────────────────────────────────────────
elif page == "🔬 Stock Deep Dive":
    st.markdown("## 🔬 Stock Deep Dive")
    selected = st.selectbox("Select Stock", [s["name"] for s in STOCKS])
    s = next(x for x in STOCKS if x["name"]==selected)

    rat_bg  = RATING_BG.get(s["ind_rating"],"#F3F4F6")
    rat_col = RATING_COLORS.get(s["ind_rating"],"#374151")

    col1, col2 = st.columns([2,1])
    with col1:
        st.markdown(f"### {s['name']}")
        st.caption(f"{s['sector']}  |  📅 {s['result_date']}  |  {s['quarter']}")
        st.markdown(f"""
        <div style="margin:8px 0">
          <span style="background:{'#D8F3DC' if s['status']=='Declared' else '#FFF3CD'};
                       color:{'#1B4332' if s['status']=='Declared' else '#856404'};
                       font-weight:700;padding:3px 12px;border-radius:999px;font-size:12px">
            {'✅ Declared' if s['status']=='Declared' else '⏳ Pending'}
          </span>
          <span style="background:{rat_bg};color:{rat_col};font-weight:700;
                       padding:3px 14px;border-radius:999px;font-size:13px;margin-left:8px">
            {s['ind_rating']}
          </span>
          <span style="background:{RISK_BG.get(s['risk'],'#F3F4F6')};padding:3px 12px;
                       border-radius:999px;font-size:12px;font-weight:600;margin-left:8px">
            Risk: {s['risk']}
          </span>
        </div>""", unsafe_allow_html=True)

    with col2:
        ticker = TICKER_MAP.get(s["name"])
        if ticker and st.button("🔄 Fetch Live Price", type="primary"):
            with st.spinner("Fetching..."):
                try:
                    info  = yf.Ticker(ticker).info
                    price = info.get("currentPrice") or info.get("regularMarketPrice")
                    chg   = info.get("regularMarketChangePercent",0)
                    w52h  = info.get("fiftyTwoWeekHigh")
                    w52l  = info.get("fiftyTwoWeekLow")
                    pe    = info.get("trailingPE")
                    st.metric("Live CMP", f"₹{price:,.2f}" if price else "N/A",
                              f"{chg:+.2f}%" if chg else None)
                    if w52h and w52l and price:
                        pct_from_low  = (price - w52l)  / (w52h - w52l) * 100 if w52h!=w52l else 50
                        st.progress(int(pct_from_low)/100,
                                    text=f"52W: ₹{w52l:,} ◄ ₹{price:,.0f} ► ₹{w52h:,}")
                    if pe: st.caption(f"P/E: {pe:.1f}x")
                except Exception as e:
                    st.error(f"Fetch failed: {e}")

    st.divider()
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("#### 📊 Estimates vs Actuals")
        data_rows = [
            ("Est. EPS (₹)",    f"₹{s.get('est_eps','—')}"),
            ("Actual EPS (₹)",  f"₹{s.get('act_eps','—')}" if s.get('act_eps') else "Pending"),
            ("Est. Revenue",    f"₹{s.get('est_rev','—'):,}Cr" if s.get('est_rev') else "—"),
            ("Actual Revenue",  f"₹{s.get('act_rev','—'):,}Cr" if s.get('act_rev') else "Pending"),
            ("Sell-Side Target",f"₹{s.get('ss_target','—')}"),
            ("Sell-Side Rating",s.get("ss_rating","—")),
        ]
        if s.get("act_eps") and s.get("est_eps"):
            beat = (s["act_eps"] - s["est_eps"]) / abs(s["est_eps"]) * 100
            data_rows.insert(2,("EPS Beat/Miss", f"{beat:+.1f}%"))
        st.dataframe(pd.DataFrame(data_rows, columns=["Metric","Value"]),
                     use_container_width=True, hide_index=True)

    with col_b:
        st.markdown("#### 🎯 My Assessment")
        st.markdown(f"""| Field | Value |
|-------|-------|
| Independent Rating | **{s['ind_rating']}** |
| Risk Level | **{s['risk']}** |
| Upside Captured | **{s.get('upside_captured') or '—'}** |""")

    st.markdown("#### 📢 Earnings Commentary")
    st.markdown(f'<div class="commentary-box">{s.get("earnings_commentary","—")}</div>', unsafe_allow_html=True)
    st.markdown("#### 🔍 Independent Rationale")
    st.markdown(f'<div class="commentary-box" style="background:#FFF9F0;border-color:#F59E0B">{s.get("ind_rationale","—")}</div>', unsafe_allow_html=True)
    st.markdown("#### 💡 Key Catalyst")
    st.markdown(f'<div class="commentary-box" style="background:#F0FDF4;border-color:#22C55E">{s.get("catalyst","—")}</div>', unsafe_allow_html=True)

    # ── #8 SHARE BUTTON ───────────────────────────────────────────────────────
    share_msg = share_text(s)
    wa_url    = "https://wa.me/?text=" + urllib.parse.quote(share_msg)
    st.markdown("---")
    st.markdown(f'<a href="{wa_url}" target="_blank" style="background:#25D366;color:white;padding:9px 22px;border-radius:6px;text-decoration:none;font-size:14px;font-weight:600">📲 Share on WhatsApp</a>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# PAGE: LIVE PRICES
# ─────────────────────────────────────────────────────────────────────────────
elif page == "⚙️ Live Prices":
    st.markdown("## ⚙️ Live Prices")
    st.caption("Prices from Yahoo Finance (NSE). ~15 min delay.")

    if st.button("🔄 Refresh All Prices Now", type="primary"):
        progress = st.progress(0, text="Fetching prices...")
        fstocks  = fs()
        rows_lp  = []
        for i, s in enumerate(fstocks):
            ticker = TICKER_MAP.get(s["name"])
            progress.progress((i+1)/len(fstocks), text=f"Fetching {s['name']}...")
            row = {"Company":s["name"],"My Rating":s["ind_rating"],
                   "CMP (₹)":"—","Change %":"—","52W High":"—","52W Low":"—","P/E":"—","Status":s["status"]}
            if ticker:
                try:
                    info  = yf.Ticker(ticker).info
                    price = info.get("currentPrice") or info.get("regularMarketPrice")
                    chg   = info.get("regularMarketChangePercent")
                    row.update({
                        "CMP (₹)":  f"₹{price:,.2f}" if price else "—",
                        "Change %": f"{chg:+.2f}%" if chg else "—",
                        "52W High": f"₹{info.get('fiftyTwoWeekHigh'):,.0f}" if info.get('fiftyTwoWeekHigh') else "—",
                        "52W Low":  f"₹{info.get('fiftyTwoWeekLow'):,.0f}"  if info.get('fiftyTwoWeekLow')  else "—",
                        "P/E":      f"{info.get('trailingPE'):.1f}x" if info.get('trailingPE') else "—",
                    })
                    time.sleep(0.3)
                except: pass
            rows_lp.append(row)
        progress.empty()
        df_lp = pd.DataFrame(rows_lp)
        def ccg(val):
            if val=="—": return ""
            try:
                n=float(val.replace("%","").replace("+",""))
                return "color:#1B4332;font-weight:600" if n>=0 else "color:#C0392B;font-weight:600"
            except: return ""
        def crr(val):
            return f"background-color:{RATING_BG.get(val,'#F3F4F6')};color:{RATING_COLORS.get(val,'#374151')};font-weight:600"
        st.dataframe(df_lp.style.map(ccg,subset=["Change %"]).map(crr,subset=["My Rating"]),
                     use_container_width=True, hide_index=True, height=800)
        st.success(f"✅ {len(rows_lp)} stocks refreshed at {datetime.now().strftime('%H:%M:%S')}")
    else:
        st.info("Click **Refresh All Prices Now** to fetch live prices for all tracked stocks.")
