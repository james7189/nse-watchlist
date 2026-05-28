"""
NSE Watchlist — Master Auto-Update Script
==========================================
Runs daily via GitHub Actions (cloud) at 7 PM IST.
Does two things:
  1. DISCOVERY  — finds new upcoming result dates, adds new stocks to data.py
  2. ACTUALS    — fetches declared results, updates act_eps/act_rev in data.py

No manual input needed. Fully automated.
"""

import re
import time
import json
import logging
import sys
import os
from datetime import datetime, timedelta
from pathlib import Path

try:
    import yfinance as yf
    import requests
    import pandas as pd
except ImportError:
    print("pip install yfinance requests pandas")
    sys.exit(1)

try:
    from alerts import alert_new_stocks, alert_results_declared, alert_daily_summary
except ImportError:
    def alert_new_stocks(*a): pass
    def alert_results_declared(*a): pass
    def alert_daily_summary(*a): pass

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(message)s",
    datefmt="%d-%b-%Y %H:%M",
    handlers=[logging.StreamHandler(sys.stdout)]
)

# ── CONFIG ────────────────────────────────────────────────────────────────────
# When running via GitHub Actions these come from environment automatically.
# When running locally, set GITHUB_TOKEN in auto_scraper.py instead.
GITHUB_TOKEN    = os.environ.get("GITHUB_TOKEN", "")
GITHUB_REPO     = os.environ.get("GITHUB_REPOSITORY", "james7189/nse-watchlist")
GITHUB_BRANCH   = "main"
DATA_FILE       = "data.py"
DISCOVERY_DAYS  = 15        # look ahead this many days for new results
MIN_MARKET_CAP  = 500e7     # ignore companies below ₹500Cr market cap

# ── KNOWN TICKER MAP (existing stocks — won't be re-added) ───────────────────
EXISTING_TICKERS = {
    "GRASIM.NS","GAIL.NS","PRESTIGE.NS","RAINBOW.NS","BALKRISIND.NS",
    "JSWSTEEL.NS","ASHOKLEY.NS","NH.NS","GLENMARK.NS","LINDEINDIA.NS",
    "SUZLON.NS","JKTYRE.NS","ASTRAMICRO.NS","BHARATRAS.NS","GOODLUCK.NS",
    "KEI.NS","ASTRAL.NS","JINDALSAW.NS","PFC.NS","CESC.NS","IRCON.NS",
    "BPCL.NS","INDIAMART.NS","IREDA.NS","COCHINSHIP.NS","MFSL.NS",
    "POLYCAB.NS","HUDCO.NS","VBL.NS","PRINCEPIPE.NS","CENTURYPLY.NS",
    "HAVELLS.NS","PVRINOX.NS","SYRMA.NS","PERSISTENT.NS","OBEROIRLTY.NS",
    "INDHOTEL.NS","JSWINFRA.NS","NRBBEARING.NS",
}

# ── SECTOR MAP — Yahoo Finance industry → readable sector ────────────────────
SECTOR_MAP = {
    "Technology":                   "IT Services",
    "Consumer Cyclical":            "Consumer Discretionary",
    "Consumer Defensive":           "FMCG / Consumer Staples",
    "Healthcare":                   "Healthcare / Pharma",
    "Financial Services":           "Banking / Financial Services",
    "Basic Materials":              "Materials / Chemicals",
    "Industrials":                  "Industrials / Capital Goods",
    "Energy":                       "Oil & Gas / Energy",
    "Real Estate":                  "Real Estate",
    "Utilities":                    "Power / Utilities",
    "Communication Services":       "Media / Telecom",
}

# ── GITHUB HELPERS ────────────────────────────────────────────────────────────
def gh_headers():
    return {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }

def get_data_py():
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{DATA_FILE}"
    r = requests.get(url, headers=gh_headers())
    if r.status_code == 200:
        import base64
        d = r.json()
        return base64.b64decode(d["content"]).decode("utf-8"), d["sha"]
    logging.error(f"Failed to fetch data.py: {r.status_code}")
    return None, None

def push_data_py(content, sha, msg):
    import base64
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{DATA_FILE}"
    payload = {
        "message": msg,
        "content": base64.b64encode(content.encode()).decode(),
        "sha": sha,
        "branch": GITHUB_BRANCH,
    }
    r = requests.put(url, headers=gh_headers(), json=payload)
    if r.status_code in (200, 201):
        logging.info(f"✅ Pushed: {msg}")
        return True
    logging.error(f"Push failed: {r.status_code} {r.text[:200]}")
    return False

# ── NSE EARNINGS CALENDAR ─────────────────────────────────────────────────────
def fetch_upcoming_results_nse():
    """
    Fetches upcoming board meeting / result dates from NSE India event calendar.
    Returns list of dicts: {symbol, company_name, result_date}
    """
    upcoming = []
    today = datetime.now()
    end_date = today + timedelta(days=DISCOVERY_DAYS)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.nseindia.com/",
        "X-Requested-With": "XMLHttpRequest",
    }

    # First get cookies
    session = requests.Session()
    try:
        session.get("https://www.nseindia.com", headers=headers, timeout=10)
        time.sleep(1)

        url = "https://www.nseindia.com/api/event-calendar"
        r = session.get(url, headers=headers, timeout=15)

        if r.status_code == 200:
            events = r.json()
            for event in events:
                try:
                    # Filter for board meetings / results
                    purpose = str(event.get("purpose","")).lower()
                    if not any(k in purpose for k in
                               ["financial result","quarterly result","board meeting"]):
                        continue

                    # Parse date
                    date_str = event.get("date","") or event.get("bfMtngDt","")
                    if not date_str:
                        continue

                    try:
                        evt_date = datetime.strptime(date_str[:10], "%d-%b-%Y")
                    except:
                        try:
                            evt_date = datetime.strptime(date_str[:10], "%Y-%m-%d")
                        except:
                            continue

                    if not (today <= evt_date <= end_date):
                        continue

                    symbol  = event.get("symbol","").strip()
                    company = event.get("company","") or event.get("companyName","")

                    if symbol:
                        upcoming.append({
                            "symbol":      symbol,
                            "yahoo_ticker": f"{symbol}.NS",
                            "company":     company,
                            "result_date": evt_date.strftime("%d-%b-%y"),
                        })
                except Exception:
                    continue

        logging.info(f"📅 NSE calendar: {len(upcoming)} upcoming result events found")

    except Exception as e:
        logging.warning(f"NSE calendar fetch failed: {e}. Trying Yahoo fallback.")

    return upcoming

def fetch_upcoming_results_yahoo():
    """
    Fallback: Yahoo Finance earnings calendar for Indian stocks.
    """
    upcoming = []
    today = datetime.now()
    end_date = today + timedelta(days=DISCOVERY_DAYS)

    # Yahoo Finance earnings calendar API
    for delta in range(DISCOVERY_DAYS):
        date = today + timedelta(days=delta)
        date_str = date.strftime("%Y-%m-%d")
        url = f"https://query1.finance.yahoo.com/v1/finance/eodhistoricaldata/earnings?date={date_str}&region=IN"
        try:
            r = requests.get(url, timeout=10,
                             headers={"User-Agent": "Mozilla/5.0"})
            if r.status_code == 200:
                data = r.json()
                earnings = (data.get("earnings",{})
                               .get("earningsDate",{})
                               .get("earningsDateList",[]))
                for item in earnings:
                    ticker = item.get("ticker","")
                    if ticker.endswith(".NS"):
                        upcoming.append({
                            "symbol":      ticker.replace(".NS",""),
                            "yahoo_ticker": ticker,
                            "company":     item.get("companyshortName",""),
                            "result_date": date.strftime("%d-%b-%y"),
                        })
            time.sleep(0.3)
        except Exception:
            continue

    logging.info(f"📅 Yahoo calendar: {len(upcoming)} events found")
    return upcoming

# ── FETCH STOCK DETAILS FROM YAHOO FINANCE ───────────────────────────────────
def fetch_stock_details(yahoo_ticker: str) -> dict:
    """
    Fetches sector, market cap, prior EPS, revenue for a new stock.
    """
    details = {
        "sector":    "Unknown",
        "market_cap": 0,
        "est_eps":   None,
        "est_rev":   None,
        "ss_target": None,
        "w52h":      None,
        "w52l":      None,
        "pe":        None,
    }
    try:
        t = yf.Ticker(yahoo_ticker)
        info = t.info

        details["market_cap"] = info.get("marketCap", 0) or 0
        raw_sector = info.get("sector","") or info.get("industry","")
        details["sector"]  = SECTOR_MAP.get(raw_sector, raw_sector or "Unknown")
        details["w52h"]    = info.get("fiftyTwoWeekHigh")
        details["w52l"]    = info.get("fiftyTwoWeekLow")
        details["pe"]      = info.get("trailingPE")

        # Use prior year same quarter EPS as estimate proxy
        try:
            qe = t.quarterly_earnings
            if qe is not None and not qe.empty and len(qe) >= 4:
                # Same quarter last year
                prior_eps = float(qe["EPS"].iloc[3])
                details["est_eps"] = round(prior_eps * 1.15, 2)  # assume 15% growth
        except Exception:
            pass

        # Use trailing 12M revenue / 4 as quarterly estimate
        try:
            rev = info.get("totalRevenue")
            if rev:
                details["est_rev"] = int(rev / 4 / 1e7)  # convert to ₹Cr quarterly
        except Exception:
            pass

        # Analyst target price
        details["ss_target"] = info.get("targetMeanPrice")
        if details["ss_target"]:
            details["ss_target"] = int(details["ss_target"])

        logging.info(f"  ✅ {yahoo_ticker}: {details['sector']} | "
                     f"MCap ₹{details['market_cap']/1e9:.0f}Bn")
    except Exception as e:
        logging.warning(f"  ⚠ {yahoo_ticker}: {e}")

    time.sleep(0.5)
    return details

# ── BUILD NEW STOCK ENTRY FOR data.py ────────────────────────────────────────
def build_stock_entry(symbol, company, result_date, details) -> str:
    """
    Generates a new stock dict entry in the same format as data.py STOCKS list.
    """
    sector   = details.get("sector", "Unknown")
    est_eps  = details.get("est_eps")
    est_rev  = details.get("est_rev")
    target   = details.get("ss_target")
    est_eps_str = str(est_eps) if est_eps else "None"
    est_rev_str = str(est_rev) if est_rev else "None"
    target_str  = str(target)  if target  else "None"

    entry = f'''    {{
        "name":         "{symbol}",
        "sector":       "{sector}",
        "result_date":  "{result_date}",
        "quarter":      "Q4 FY26",
        "status":       "Pending",
        "est_eps":      {est_eps_str},
        "act_eps":      None,
        "est_rev":      {est_rev_str},
        "act_rev":      None,
        "ss_rating":    "BUY",
        "ss_target":    {target_str},
        "ind_rating":   "HOLD",
        "risk":         "MEDIUM",
        "upside_captured": None,
        "catalyst":     "Q4 FY26 results due {result_date}. Auto-added — update commentary manually.",
        "earnings_commentary": "Results pending. Auto-added by scraper — add earnings commentary after declaration.",
        "ind_rationale": "Auto-added. Update independent rating and rationale manually after reviewing results.",
    }},'''
    return entry

# ── UPDATE ACTUALS IN data.py ─────────────────────────────────────────────────
def update_actuals(content: str) -> tuple:
    """
    For all Pending stocks, try to fetch latest quarterly results from Yahoo.
    Updates act_eps, act_rev, status in content.
    Returns (updated_content, num_changes).
    """
    changes = 0

    # Find all pending stock names
    pending = re.findall(
        r'"name"\s*:\s*"([^"]+)"[^}]{0,400}"status"\s*:\s*"Pending"',
        content, re.DOTALL
    )

    # Build ticker map from existing TICKER_MAP in data.py
    ticker_matches = re.findall(r'"([^"]+)"\s*:\s*"([A-Z0-9]+\.NS)"', content)
    ticker_map = {k: v for k, v in ticker_matches}

    for name in set(pending):
        ticker = ticker_map.get(name)
        if not ticker:
            continue

        logging.info(f"🔍 Checking actuals: {name} ({ticker})")
        try:
            t = yf.Ticker(ticker)
            qf = t.quarterly_financials
            qi = t.quarterly_income_stmt

            act_eps = None
            act_rev = None

            # Revenue
            for df in [qf, qi]:
                if df is not None and not df.empty:
                    for row in ["Total Revenue", "TotalRevenue", "Revenue"]:
                        if row in df.index:
                            val = df.loc[row].iloc[0]
                            if val and val > 0:
                                act_rev = int(val / 1e7)
                                break
                if act_rev:
                    break

            # EPS
            try:
                qe = t.quarterly_earnings
                if qe is not None and not qe.empty:
                    act_eps = round(float(qe["EPS"].iloc[0]), 2)
            except Exception:
                pass

            if not act_eps:
                info = t.info
                act_eps = info.get("trailingEps")
                if act_eps:
                    act_eps = round(float(act_eps), 2)

            if act_eps or act_rev:
                # Find and update this stock's block
                name_pat = rf'"name"\s*:\s*"{re.escape(name)}"'
                m = re.search(name_pat, content)
                if m:
                    bs = m.start()
                    be = content.find('\n    {', bs + 1)
                    if be == -1:
                        be = content.find('\n]', bs)
                    block = content[bs:be]
                    orig  = block

                    if act_eps:
                        block = re.sub(
                            r'"act_eps"\s*:\s*None',
                            f'"act_eps":      {act_eps}', block)
                    if act_rev:
                        block = re.sub(
                            r'"act_rev"\s*:\s*None',
                            f'"act_rev":      {act_rev}', block)
                    if block != orig:
                        block = block.replace(
                            '"status":       "Pending"',
                            '"status":       "Declared"')
                        content = content[:bs] + block + content[be:]
                        changes += 1
                        logging.info(f"  ✅ {name}: EPS={act_eps}, Rev=₹{act_rev}Cr")

            time.sleep(0.5)

        except Exception as e:
            logging.warning(f"  ⚠ {name}: {e}")

    return content, changes

# ── ADD NEW STOCKS TO data.py ─────────────────────────────────────────────────
def add_new_stocks(content: str, upcoming: list) -> tuple:
    """
    For each upcoming stock not already in data.py, fetches details and adds it.
    Returns (updated_content, num_added).
    """
    added = 0

    # Get existing names from content
    existing_names = set(re.findall(r'"name"\s*:\s*"([^"]+)"', content))
    existing_tickers_in_content = set(re.findall(r'"([A-Z0-9]+\.NS)"', content))
    all_existing = EXISTING_TICKERS | existing_tickers_in_content

    # Find insertion point — just before the closing ] of STOCKS list
    # Look for the last },\n] pattern
    insert_match = list(re.finditer(r'\},\s*\n\]', content))
    if not insert_match:
        logging.warning("Could not find STOCKS list end in data.py")
        return content, 0

    insert_pos = insert_match[-1].start() + 2  # after },

    new_entries = []

    for stock in upcoming:
        ticker   = stock["yahoo_ticker"]
        symbol   = stock["symbol"]
        company  = stock["company"]
        res_date = stock["result_date"]

        # Skip if already tracked
        if ticker in all_existing or symbol in existing_names:
            continue

        logging.info(f"\n🆕 New stock found: {symbol} ({company}) — {res_date}")

        # Fetch details
        details = fetch_stock_details(ticker)

        # Skip tiny companies
        if details["market_cap"] < MIN_MARKET_CAP:
            logging.info(f"  ⏭ Skipping {symbol} — market cap too small")
            continue

        # Build entry
        entry = build_stock_entry(symbol, company, res_date, details)
        new_entries.append(entry)

        # Add to ticker map in content
        ticker_map_pattern = r'(TICKER_MAP\s*=\s*\{[^}]+)'
        ticker_line = f'\n    "{symbol}":{" " * max(1, 20-len(symbol))}"{ticker}",'
        content = re.sub(
            ticker_map_pattern,
            lambda m: m.group(0) + ticker_line,
            content, count=1
        )

        all_existing.add(ticker)
        existing_names.add(symbol)
        added += 1

    if new_entries:
        insertion = "\n" + "\n".join(new_entries)
        content = content[:insert_pos] + insertion + content[insert_pos:]
        logging.info(f"\n✅ Added {added} new stocks to data.py")

    return content, added

# ── MAIN ──────────────────────────────────────────────────────────────────────
def main():
    logging.info(f"\n{'='*55}")
    logging.info(f"🚀 NSE Watchlist Auto-Update — {datetime.now().strftime('%d-%b-%Y %H:%M IST')}")

    # Fetch current data.py from GitHub
    content, sha = get_data_py()
    if not content:
        logging.error("Could not fetch data.py from GitHub")
        sys.exit(1)

    total_changes = 0

    # ── PART 1: Update actuals for pending stocks ─────────────────────────────
    logging.info("\n📊 PART 1: Updating actuals for pending stocks...")
    content, actuals_changed = update_actuals(content)
    total_changes += actuals_changed
    logging.info(f"   {actuals_changed} stocks updated with actuals")

    # ── PART 2: Discover new upcoming stocks ─────────────────────────────────
    logging.info(f"\n🔍 PART 2: Discovering new stocks (next {DISCOVERY_DAYS} days)...")

    # Try NSE first, fall back to Yahoo
    upcoming = fetch_upcoming_results_nse()
    if len(upcoming) < 3:
        logging.info("NSE calendar returned few results — trying Yahoo Finance...")
        upcoming += fetch_upcoming_results_yahoo()

    # Deduplicate
    seen = set()
    unique_upcoming = []
    for s in upcoming:
        if s["symbol"] not in seen:
            seen.add(s["symbol"])
            unique_upcoming.append(s)

    logging.info(f"   {len(unique_upcoming)} unique upcoming events found")

    content, stocks_added = add_new_stocks(content, unique_upcoming)
    total_changes += stocks_added
    logging.info(f"   {stocks_added} new stocks added")

    # ── PUSH IF CHANGES ───────────────────────────────────────────────────────
    # Send alerts first
    pending_count  = content.count('"status":       "Pending"')
    declared_count = content.count('"status":       "Declared"')

    if actuals_changed > 0:
        updated_list = [{"name": n, "act_eps": None, "est_eps": None,
                         "act_rev": None, "est_rev": None}
                        for n in re.findall(r'"name"\s*:\s*"([^"]+)"', content)[:actuals_changed]]
        alert_results_declared(updated_list)

    if stocks_added > 0:
        new_list = []
        for sym in list(seen)[-stocks_added:]:
            new_list.append({"name": sym, "sector": "Auto-discovered",
                             "result_date": "See watchlist",
                             "ind_rating": "HOLD", "risk": "MEDIUM",
                             "catalyst": "Auto-added — update commentary manually."})
        alert_new_stocks(new_list)

    alert_daily_summary(actuals_changed, stocks_added, pending_count, declared_count)

    if total_changes > 0:
        commit_msg = (
            f"Auto-update {datetime.now().strftime('%d-%b-%Y')}: "
            f"{actuals_changed} actuals updated, {stocks_added} new stocks added"
        )
        success = push_data_py(content, sha, commit_msg)
        if success:
            logging.info(f"\n🎉 Done! {total_changes} total changes pushed.")
            logging.info("📊 Dashboard refreshes within 60 seconds.")
        else:
            Path(DATA_FILE).write_text(content, encoding="utf-8")
            logging.info(f"\n✅ data.py updated locally — git will commit via workflow.")
    else:
        logging.info("\n✅ No changes needed — everything up to date.")

if __name__ == "__main__":
    main()

# ── ALERT INTEGRATION (add to bottom of main()) ──────────────────────────────
# This is called from main() after updates are complete.
# Already wired in — see updated main() below.
