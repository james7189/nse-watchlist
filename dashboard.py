"""
NSE Results Watchlist — Streamlit Web Dashboard
================================================
Run locally:  streamlit run dashboard.py
Deploy free:  push to GitHub → streamlit.io/cloud → connect repo
"""

import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime
import time
from data import STOCKS, TICKER_MAP, RATING_COLORS, RATING_BG, RISK_BG

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NSE Results Watchlist | Q4 FY26",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
  .main { background-color: #F8FAFC; }
  .stMetric { background: white; border-radius: 12px; padding: 16px; box-shadow: 0 1px 4px rgba(0,0,0,0.08); }
  .stMetric label { font-size: 12px !important; color: #6B7280; }
  h1 { color: #0D1B2A; font-weight: 700; }
  h2 { color: #1A3A5C; font-weight: 600; border-bottom: 2px solid #E5E7EB; padding-bottom: 6px; }
  h3 { color: #374151; font-weight: 600; }
  .badge { display: inline-block; padding: 2px 10px; border-radius: 999px; font-size: 12px; font-weight: 600; }
  .card { background: white; border-radius: 12px; padding: 20px; margin-bottom: 16px;
          box-shadow: 0 1px 4px rgba(0,0,0,0.08); border-left: 4px solid #1A3A5C; }
  .card-green { border-left-color: #40916C; }
  .card-amber { border-left-color: #F59E0B; }
  .card-red   { border-left-color: #C0392B; }
  .tag { display: inline-block; padding: 1px 8px; border-radius: 4px;
         font-size: 11px; font-weight: 600; margin-right: 4px; }
  .commentary-box { background: #F0F9FF; border-left: 3px solid #0EA5E9;
                    padding: 12px 16px; border-radius: 0 8px 8px 0;
                    font-size: 13px; color: #1E3A5F; line-height: 1.6; }
  div[data-testid="stExpander"] { border: 1px solid #E5E7EB; border-radius: 8px; }
  .stDataFrame { border-radius: 8px; overflow: hidden; }
  footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/fluency/48/combo-chart.png", width=48)
    st.markdown("## 📊 NSE Watchlist\n**Q4 FY26 Results Tracker**")
    st.caption(f"James | Updated {datetime.now().strftime('%d %b %Y')}")
    st.divider()

    page = st.radio("Navigate", [
        "🏠 Dashboard",
        "🗓 Results Calendar",
        "📈 Pre-Result Setup",
        "🎯 Post-Result Tracker",
        "🔬 Stock Deep Dive",
        "⚙️ Live Prices",
    ])
    st.divider()

    st.markdown("**Filters**")
    status_filter = st.multiselect("Status", ["Declared", "Pending"], default=["Declared", "Pending"])
    rating_filter = st.multiselect("My Rating", ["STRONG BUY","BUY","ACCUMULATE","HOLD","HOLD / BOOK","REDUCE","AVOID"],
                                    default=["STRONG BUY","BUY","ACCUMULATE","HOLD","HOLD / BOOK","REDUCE","AVOID"])
    st.divider()
    st.caption("⚠️ Personal tracking tool. Not SEBI-registered investment advice.")

# ── Helper: filter stocks ─────────────────────────────────────────────────────
def filtered_stocks():
    return [s for s in STOCKS
            if s["status"] in status_filter
            and s["ind_rating"] in rating_filter]

# ── Helper: rating badge HTML ─────────────────────────────────────────────────
def rating_badge(rating, size=12):
    bg  = RATING_BG.get(rating, "#F3F4F6")
    col = RATING_COLORS.get(rating, "#374151")
    return f'<span class="badge" style="background:{bg};color:{col};font-size:{size}px">{rating}</span>'

def status_badge(status):
    if status == "Declared":
        return '<span class="badge" style="background:#D8F3DC;color:#1B4332">✅ Declared</span>'
    return '<span class="badge" style="background:#FFF3CD;color:#856404">⏳ Pending</span>'

def upside_badge(captured):
    if captured == "YES":
        return '<span class="badge" style="background:#D8F3DC;color:#1B4332">YES ✅</span>'
    elif captured == "PARTIAL":
        return '<span class="badge" style="background:#FFF3CD;color:#856404">PARTIAL ⚠</span>'
    elif captured == "NO":
        return '<span class="badge" style="background:#FDDCDC;color:#C0392B">NO ❌</span>'
    return "—"

# ─────────────────────────────────────────────────────────────────────────────
# PAGE: DASHBOARD
# ─────────────────────────────────────────────────────────────────────────────
if page == "🏠 Dashboard":
    st.markdown("# 📊 NSE Results Watchlist — Q4 FY26")
    st.caption(f"James's personal tracker | {len(STOCKS)} stocks | {datetime.now().strftime('%d %b %Y %H:%M')}")

    # KPI row
    declared  = [s for s in STOCKS if s["status"] == "Declared"]
    pending   = [s for s in STOCKS if s["status"] == "Pending"]
    beats     = [s for s in declared if s["act_eps"] and s["est_eps"] and s["act_eps"] > s["est_eps"]]
    misses    = [s for s in declared if s["act_eps"] and s["est_eps"] and s["act_eps"] < s["est_eps"]]
    captured  = [s for s in declared if s.get("upside_captured") == "YES"]
    strong    = [s for s in STOCKS if s["ind_rating"] in ("STRONG BUY","BUY")]

    c1,c2,c3,c4,c5,c6 = st.columns(6)
    c1.metric("Total Tracked",    f"{len(STOCKS)}")
    c2.metric("Declared",         f"{len(declared)}")
    c3.metric("Pending",          f"{len(pending)}")
    c4.metric("Beats / Misses",   f"{len(beats)} / {len(misses)}")
    c5.metric("Upside Captured",  f"{len(captured)}")
    c6.metric("BUY / STRONG BUY", f"{len(strong)}")

    st.markdown("---")

    # Rating distribution
    col_a, col_b = st.columns([1, 1])
    with col_a:
        st.markdown("### ⚖️ Independent Rating Distribution")
        from collections import Counter
        dist = Counter(s["ind_rating"] for s in STOCKS)
        order = ["STRONG BUY","BUY","ACCUMULATE","HOLD","HOLD / BOOK","REDUCE","AVOID"]
        rows = []
        for r in order:
            if r in dist:
                stocks_in = [s["name"] for s in STOCKS if s["ind_rating"] == r]
                rows.append({"Rating": r, "Count": dist[r], "Stocks": ", ".join(stocks_in)})
        df_dist = pd.DataFrame(rows)

        def color_rating(val):
            bg  = RATING_BG.get(val, "#F3F4F6")
            col = RATING_COLORS.get(val, "#374151")
            return f"background-color:{bg};color:{col};font-weight:600"

        st.dataframe(
            df_dist.style.map(color_rating, subset=["Rating"]),
            use_container_width=True, hide_index=True, height=280
        )

    with col_b:
        st.markdown("### 📅 15-Day Results Radar")
        radar = [
            ("May 21 ✅", "GRASIM, GAIL, PRESTIGE", "3 Declared"),
            ("May 22 ✅", "CENTURY PLY, NH, RAINBOW CHILDCARE", "3"),
            ("May 23 ⏳", "BALKRISNA, ASHOK LEYLAND, GLENMARK, LINDE", "4"),
            ("May 24 ⏳", "JSW STEEL", "1"),
            ("May 25 ⏳", "SUZLON", "1"),
            ("May 26 ⏳", "JK TYRE, ASTRA MICROWAVE, BHARAT RASAYAN, GOODLUCK", "4"),
            ("May 27 ⏳", "KEI INDUSTRIES, ASTRAL", "2"),
            ("May 28 ⏳", "JINDAL SAW, PFC", "2"),
            ("May 29 ⏳", "CESC, IRCON INTL", "2"),
            ("May 30 ⏳", "BPCL, INDIAMART", "2"),
            ("Jun 2 ⏳",  "IREDA, COCHIN SHIPYARD", "2"),
            ("Jun 3 ⏳",  "MFSL, POLYCAB", "2"),
            ("Jun 4 ⏳",  "HUDCO", "1"),
        ]
        df_radar = pd.DataFrame(radar, columns=["Date", "Companies", "Count"])
        st.dataframe(df_radar, use_container_width=True, hide_index=True, height=480)

    # Disclaimer
    st.info("⚠️ Independent ratings are personal assessments for tracking purposes only — not SEBI-registered research. "
            "Sell-side consensus ratings are shown separately. Always consult a registered advisor before investing.")

# ─────────────────────────────────────────────────────────────────────────────
# PAGE: RESULTS CALENDAR
# ─────────────────────────────────────────────────────────────────────────────
elif page == "🗓 Results Calendar":
    st.markdown("## 🗓 Results Calendar — Q4 FY26")
    fs = filtered_stocks()

    rows = []
    for s in fs:
        eps_beat = None
        if s["act_eps"] and s["est_eps"] and s["est_eps"] != 0:
            eps_beat = (s["act_eps"] - s["est_eps"]) / abs(s["est_eps"]) * 100
        rows.append({
            "Company":       s["name"],
            "Sector":        s["sector"],
            "Result Date":   s["result_date"],
            "Quarter":       s["quarter"],
            "Status":        s["status"],
            "Est. EPS (₹)":  s["est_eps"],
            "Act. EPS (₹)":  s["act_eps"] if s["act_eps"] else "Pending",
            "EPS Beat %":    f"{eps_beat:+.1f}%" if eps_beat is not None else "—",
            "Est. Rev (₹Cr)":s["est_rev"],
            "Sell-Side":     s["ss_rating"],
            "Target (₹)":    s["ss_target"],
            "My Rating":     s["ind_rating"],
            "Risk":          s["risk"],
        })

    df = pd.DataFrame(rows)

    def color_status(val):
        if val == "Declared": return "background-color:#D8F3DC;color:#1B4332;font-weight:600"
        return "background-color:#FFF3CD;color:#856404;font-weight:600"

    def color_rating(val):
        return f"background-color:{RATING_BG.get(val,'#F3F4F6')};color:{RATING_COLORS.get(val,'#374151')};font-weight:600"

    def color_beat(val):
        if val == "—": return ""
        try:
            n = float(val.replace("%","").replace("+",""))
            return "background-color:#D8F3DC;color:#1B4332" if n > 0 else "background-color:#FDDCDC;color:#C0392B"
        except: return ""

    def color_risk(val):
        return f"background-color:{RISK_BG.get(val,'#F3F4F6')}"

    styled = df.style \
        .map(color_status, subset=["Status"]) \
        .map(color_rating, subset=["My Rating"]) \
        .map(color_beat,   subset=["EPS Beat %"]) \
        .map(color_risk,   subset=["Risk"])

    st.dataframe(styled, use_container_width=True, hide_index=True, height=700)
    st.caption(f"Showing {len(fs)} stocks | Filters applied via sidebar")

# ─────────────────────────────────────────────────────────────────────────────
# PAGE: PRE-RESULT SETUP
# ─────────────────────────────────────────────────────────────────────────────
elif page == "📈 Pre-Result Setup":
    st.markdown("## 📈 Pre-Result Setup Sheet")
    fs = [s for s in filtered_stocks() if s["status"] == "Pending"]
    st.caption(f"{len(fs)} pending results | Live prices via sidebar → ⚙️ Live Prices")

    if not fs:
        st.info("No pending results matching current filters.")
    else:
        for s in fs:
            rat_bg  = RATING_BG.get(s["ind_rating"], "#F3F4F6")
            rat_col = RATING_COLORS.get(s["ind_rating"], "#374151")
            card_class = "card-green" if "BUY" in s["ind_rating"] else \
                         "card-amber" if "HOLD" in s["ind_rating"] else "card-red"

            with st.expander(f"**{s['name']}** — {s['sector']} | 📅 {s['result_date']}", expanded=False):
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Est. EPS (₹)",   f"₹{s['est_eps']}")
                col2.metric("Est. Rev (₹Cr)", f"₹{s['est_rev']:,}")
                col3.metric("SS Target (₹)",  f"₹{s['ss_target']}")
                col4.metric("SS Rating",       s["ss_rating"])

                st.markdown(f"""
                <div style="margin-top:8px">
                  <span style="background:{rat_bg};color:{rat_col};font-weight:700;padding:4px 14px;
                        border-radius:999px;font-size:13px">
                    MY RATING: {s['ind_rating']}
                  </span>
                  <span style="margin-left:8px;background:{RISK_BG.get(s['risk'],'#F3F4F6')};
                        padding:4px 12px;border-radius:999px;font-size:12px;font-weight:600">
                    Risk: {s['risk']}
                  </span>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("**📌 Catalyst**")
                st.markdown(f'<div class="commentary-box">{s["catalyst"]}</div>', unsafe_allow_html=True)

                st.markdown("**🔍 Independent Rationale**")
                st.markdown(f'<div class="commentary-box" style="background:#FFF9F0;border-color:#F59E0B">'
                            f'{s["ind_rationale"]}</div>', unsafe_allow_html=True)

                st.markdown("**📋 What to Watch**")
                st.markdown(f'<div class="commentary-box" style="background:#F8F0FF;border-color:#8B5CF6">'
                            f'{s["earnings_commentary"]}</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# PAGE: POST-RESULT TRACKER
# ─────────────────────────────────────────────────────────────────────────────
elif page == "🎯 Post-Result Tracker":
    st.markdown("## 🎯 Post-Result Tracker")
    declared = [s for s in filtered_stocks() if s["status"] == "Declared"]
    st.caption(f"{len(declared)} results declared")

    for s in declared:
        eps_beat_pct = None
        if s["act_eps"] and s["est_eps"] and s["est_eps"] != 0:
            eps_beat_pct = (s["act_eps"] - s["est_eps"]) / abs(s["est_eps"]) * 100
        rev_beat_pct = None
        if s["act_rev"] and s["est_rev"] and s["est_rev"] != 0:
            rev_beat_pct = (s["act_rev"] - s["est_rev"]) / abs(s["est_rev"]) * 100

        beat_color   = "#40916C" if eps_beat_pct and eps_beat_pct > 0 else "#C0392B"
        card_accent  = "#40916C" if eps_beat_pct and eps_beat_pct > 0 else "#C0392B"

        with st.expander(
            f"**{s['name']}** | {s['result_date']} | "
            f"EPS: ₹{s['act_eps']} ({'**BEAT**' if eps_beat_pct and eps_beat_pct>0 else '**MISS**'} "
            f"{f'{eps_beat_pct:+.1f}%' if eps_beat_pct else ''})",
            expanded=False
        ):
            c1,c2,c3,c4,c5 = st.columns(5)
            c1.metric("Est. EPS",     f"₹{s['est_eps']}")
            c2.metric("Actual EPS",   f"₹{s['act_eps']}", f"{eps_beat_pct:+.1f}%" if eps_beat_pct else None)
            c3.metric("Est. Rev",     f"₹{s['est_rev']:,}Cr")
            c4.metric("Actual Rev",   f"₹{s['act_rev']:,}Cr" if s["act_rev"] else "—",
                      f"{rev_beat_pct:+.1f}%" if rev_beat_pct else None)
            c5.metric("Upside Captured", s.get("upside_captured","—") or "—")

            st.markdown(f"""
            <div style="margin:8px 0">
              {rating_badge(s['ind_rating'], 13)}
              <span style="margin-left:8px;font-size:12px;color:#6B7280">
                Sell-side: <b>{s['ss_rating']}</b> | Target: ₹{s['ss_target']}
              </span>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("**📢 Earnings Commentary**")
            st.markdown(
                f'<div class="commentary-box">{s["earnings_commentary"]}</div>',
                unsafe_allow_html=True
            )

            st.markdown("**⚖️ Independent View**")
            st.markdown(
                f'<div class="commentary-box" style="background:#FFF9F0;border-color:#F59E0B">'
                f'{s["ind_rationale"]}</div>',
                unsafe_allow_html=True
            )

# ─────────────────────────────────────────────────────────────────────────────
# PAGE: STOCK DEEP DIVE
# ─────────────────────────────────────────────────────────────────────────────
elif page == "🔬 Stock Deep Dive":
    st.markdown("## 🔬 Stock Deep Dive")
    stock_names = [s["name"] for s in STOCKS]
    selected    = st.selectbox("Select Stock", stock_names)
    s = next(x for x in STOCKS if x["name"] == selected)

    # Header
    rat_bg  = RATING_BG.get(s["ind_rating"], "#F3F4F6")
    rat_col = RATING_COLORS.get(s["ind_rating"], "#374151")

    col1, col2 = st.columns([2,1])
    with col1:
        st.markdown(f"### {s['name']}")
        st.caption(f"{s['sector']}  |  📅 {s['result_date']}  |  {s['quarter']}")
        st.markdown(f"""
        <div>
          {status_badge(s['status'])}
          <span style="background:{rat_bg};color:{rat_col};font-weight:700;padding:4px 14px;
                border-radius:999px;font-size:13px;margin-left:8px">
            {s['ind_rating']}
          </span>
          <span style="background:{RISK_BG.get(s['risk'],'#F3F4F6')};padding:4px 12px;
                border-radius:999px;font-size:12px;font-weight:600;margin-left:8px">
            Risk: {s['risk']}
          </span>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        ticker = TICKER_MAP.get(s["name"])
        if ticker and st.button("🔄 Fetch Live Price", type="primary"):
            with st.spinner("Fetching..."):
                try:
                    info  = yf.Ticker(ticker).info
                    price = info.get("currentPrice") or info.get("regularMarketPrice")
                    chg   = info.get("regularMarketChangePercent", 0)
                    w52h  = info.get("fiftyTwoWeekHigh")
                    w52l  = info.get("fiftyTwoWeekLow")
                    pe    = info.get("trailingPE")
                    st.metric("Live CMP", f"₹{price:,.2f}" if price else "N/A",
                              f"{chg:+.2f}%" if chg else None)
                    if w52h: st.caption(f"52W H: ₹{w52h:,}  |  52W L: ₹{w52l:,}")
                    if pe:   st.caption(f"P/E: {pe:.1f}x")
                except Exception as e:
                    st.error(f"Fetch failed: {e}")

    st.divider()

    # Estimates vs Actuals
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("#### 📊 Estimates vs Actuals")
        rows = [
            ("Est. EPS (₹)",     f"₹{s['est_eps']}"),
            ("Actual EPS (₹)",   f"₹{s['act_eps']}" if s['act_eps'] else "Pending"),
            ("Est. Revenue",     f"₹{s['est_rev']:,}Cr"),
            ("Actual Revenue",   f"₹{s['act_rev']:,}Cr" if s['act_rev'] else "Pending"),
            ("Sell-Side Target", f"₹{s['ss_target']}"),
            ("Sell-Side Rating", s["ss_rating"]),
        ]
        if s["act_eps"] and s["est_eps"]:
            beat = (s["act_eps"] - s["est_eps"]) / abs(s["est_eps"]) * 100
            rows.insert(2, ("EPS Beat/Miss", f"{beat:+.1f}%"))
        df_est = pd.DataFrame(rows, columns=["Metric","Value"])
        st.dataframe(df_est, use_container_width=True, hide_index=True)

    with col_b:
        st.markdown("#### 🎯 My Assessment")
        st.markdown(f"""
        | Field | Value |
        |-------|-------|
        | Independent Rating | **{s['ind_rating']}** |
        | Risk Level | **{s['risk']}** |
        | Upside Captured | **{s.get('upside_captured') or '—'}** |
        """)

    st.markdown("#### 📢 Earnings Commentary")
    st.markdown(f'<div class="commentary-box">{s["earnings_commentary"]}</div>', unsafe_allow_html=True)

    st.markdown("#### 🔍 Independent Rationale")
    st.markdown(
        f'<div class="commentary-box" style="background:#FFF9F0;border-color:#F59E0B">'
        f'{s["ind_rationale"]}</div>', unsafe_allow_html=True
    )

    st.markdown("#### 💡 Key Catalyst")
    st.markdown(
        f'<div class="commentary-box" style="background:#F0FDF4;border-color:#22C55E">'
        f'{s["catalyst"]}</div>', unsafe_allow_html=True
    )

# ─────────────────────────────────────────────────────────────────────────────
# PAGE: LIVE PRICES
# ─────────────────────────────────────────────────────────────────────────────
elif page == "⚙️ Live Prices":
    st.markdown("## ⚙️ Live Prices — All Tracked Stocks")
    st.caption("Prices sourced from Yahoo Finance (NSE). May have ~15 min delay.")

    auto_refresh = st.toggle("Auto-refresh every 5 minutes", value=False)
    if st.button("🔄 Refresh All Prices Now", type="primary") or auto_refresh:
        progress = st.progress(0, text="Fetching prices...")
        rows = []
        stocks_list = filtered_stocks()

        for i, s in enumerate(stocks_list):
            ticker = TICKER_MAP.get(s["name"])
            progress.progress((i+1)/len(stocks_list), text=f"Fetching {s['name']}...")
            row = {
                "Company":   s["name"],
                "Sector":    s["sector"],
                "My Rating": s["ind_rating"],
                "CMP (₹)":   "—",
                "Change %":  "—",
                "52W High":  "—",
                "52W Low":   "—",
                "P/E":       "—",
                "Status":    s["status"],
            }
            if ticker:
                try:
                    info = yf.Ticker(ticker).info
                    price = info.get("currentPrice") or info.get("regularMarketPrice")
                    chg   = info.get("regularMarketChangePercent")
                    row.update({
                        "CMP (₹)":  f"₹{price:,.2f}" if price else "—",
                        "Change %": f"{chg:+.2f}%" if chg else "—",
                        "52W High": f"₹{info.get('fiftyTwoWeekHigh'):,.0f}" if info.get('fiftyTwoWeekHigh') else "—",
                        "52W Low":  f"₹{info.get('fiftyTwoWeekLow'):,.0f}" if info.get('fiftyTwoWeekLow') else "—",
                        "P/E":      f"{info.get('trailingPE'):.1f}x" if info.get('trailingPE') else "—",
                    })
                    time.sleep(0.3)
                except:
                    pass
            rows.append(row)

        progress.empty()
        df_live = pd.DataFrame(rows)

        def color_chg(val):
            if val == "—": return ""
            try:
                n = float(val.replace("%","").replace("+",""))
                return "color:#1B4332;font-weight:600" if n >= 0 else "color:#C0392B;font-weight:600"
            except: return ""

        def color_rating(val):
            return f"background-color:{RATING_BG.get(val,'#F3F4F6')};color:{RATING_COLORS.get(val,'#374151')};font-weight:600"

        styled = df_live.style \
            .map(color_chg, subset=["Change %"]) \
            .map(color_rating, subset=["My Rating"])

        st.dataframe(styled, use_container_width=True, hide_index=True, height=800)
        st.success(f"✅ {len(rows)} stocks refreshed at {datetime.now().strftime('%H:%M:%S')}")

        if auto_refresh:
            time.sleep(300)
            st.rerun()
    else:
        st.info("Click **Refresh All Prices Now** to fetch live NSE prices for all tracked stocks.")
        st.markdown("""
        **What you'll see:**
        - Live CMP from Yahoo Finance (NSE feed, ~15 min delay)
        - Day's change %
        - 52-week High / Low
        - Trailing P/E
        - My independent rating colour-coded
        """)
