"""
NSE Watchlist — Alert System
=============================
Sends WhatsApp + Email alerts when:
  1. New stocks are auto-discovered and added
  2. Pending stocks get actuals updated (declared)
  3. Daily summary after each auto-update run

WhatsApp: via CallMeBot API (free, no account needed)
Email:    via Gmail SMTP (free with App Password)

Setup: See README_ALERTS.txt
"""

import os
import smtplib
import urllib.request
import urllib.parse
import json
import logging
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ── Config from environment variables (GitHub Secrets) ────────────────────────
WHATSAPP_PHONE   = os.environ.get("WHATSAPP_PHONE",   "")   # 918097674445
WHATSAPP_API_KEY = os.environ.get("WHATSAPP_API_KEY", "")   # from CallMeBot
GMAIL_ADDRESS    = os.environ.get("GMAIL_ADDRESS",    "")   # jamesp7189@gmail.com
GMAIL_APP_PASS   = os.environ.get("GMAIL_APP_PASS",   "")   # Gmail App Password
ALERT_EMAIL_TO   = os.environ.get("ALERT_EMAIL_TO",   "jamesp7189@gmail.com")

# ── WhatsApp via CallMeBot ─────────────────────────────────────────────────────
def send_whatsapp(message: str) -> bool:
    """
    Sends WhatsApp message via CallMeBot free API.
    Requires one-time setup — see README_ALERTS.txt Step 1.
    """
    if not WHATSAPP_PHONE or not WHATSAPP_API_KEY:
        logging.warning("WhatsApp not configured — skipping.")
        return False

    try:
        encoded_msg = urllib.parse.quote(message)
        url = (f"https://api.callmebot.com/whatsapp.php"
               f"?phone={WHATSAPP_PHONE}"
               f"&text={encoded_msg}"
               f"&apikey={WHATSAPP_API_KEY}")

        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            status = resp.status
            if status == 200:
                logging.info("✅ WhatsApp alert sent")
                return True
            else:
                logging.warning(f"WhatsApp API returned {status}")
                return False

    except Exception as e:
        logging.warning(f"WhatsApp alert failed: {e}")
        return False


# ── Email via Gmail SMTP ───────────────────────────────────────────────────────
def send_email(subject: str, body_html: str) -> bool:
    """
    Sends HTML email via Gmail SMTP using App Password.
    Requires Gmail App Password — see README_ALERTS.txt Step 2.
    """
    if not GMAIL_ADDRESS or not GMAIL_APP_PASS:
        logging.warning("Email not configured — skipping.")
        return False

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"]    = f"NSE Watchlist Bot <{GMAIL_ADDRESS}>"
        msg["To"]      = ALERT_EMAIL_TO

        # Plain text fallback
        plain = body_html.replace("<br>", "\n").replace("</p>", "\n")
        import re
        plain = re.sub(r"<[^>]+>", "", plain)
        msg.attach(MIMEText(plain,    "plain"))
        msg.attach(MIMEText(body_html, "html"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=15) as server:
            server.login(GMAIL_ADDRESS, GMAIL_APP_PASS)
            server.sendmail(GMAIL_ADDRESS, ALERT_EMAIL_TO, msg.as_string())

        logging.info(f"✅ Email sent: {subject}")
        return True

    except Exception as e:
        logging.warning(f"Email alert failed: {e}")
        return False


# ── Alert Templates ────────────────────────────────────────────────────────────
def alert_new_stocks(new_stocks: list):
    """
    Alert when new stocks are auto-discovered and added to watchlist.
    new_stocks: list of dicts with name, sector, result_date
    """
    if not new_stocks:
        return

    count = len(new_stocks)
    date_str = datetime.now().strftime("%d-%b-%Y")

    # WhatsApp message (keep concise)
    wa_lines = [f"📊 *NSE Watchlist Update — {date_str}*",
                f"",
                f"🆕 *{count} new stock(s) added to Q4 FY26 watchlist:*",
                f""]
    for s in new_stocks:
        wa_lines.append(f"• *{s['name']}* ({s['sector']})")
        wa_lines.append(f"  Results: {s.get('result_date','TBD')}")
        wa_lines.append(f"  Rating: {s.get('ind_rating','HOLD')} | Risk: {s.get('risk','MEDIUM')}")
        wa_lines.append("")

    wa_lines.append("➡ Open dashboard: https://nse-watchlist-james.streamlit.app")
    wa_lines.append("")
    wa_lines.append("⚠ Add your commentary + rating on GitHub data.py")

    send_whatsapp("\n".join(wa_lines))

    # Email (rich HTML)
    rows_html = ""
    for s in new_stocks:
        rating = s.get("ind_rating", "HOLD")
        color = {"STRONG BUY":"#1B4332","BUY":"#40916C","ACCUMULATE":"#2D6A4F",
                 "HOLD":"#856404","REDUCE":"#E65100","AVOID":"#C0392B"}.get(rating, "#333")
        bg    = {"STRONG BUY":"#D8F3DC","BUY":"#D1FAE5","ACCUMULATE":"#E9F5EE",
                 "HOLD":"#FFF3CD","REDUCE":"#FFF3E0","AVOID":"#FDDCDC"}.get(rating, "#F3F4F6")
        rows_html += f"""
        <tr>
          <td style="padding:10px;border-bottom:1px solid #eee;font-weight:600">{s['name']}</td>
          <td style="padding:10px;border-bottom:1px solid #eee;color:#555">{s['sector']}</td>
          <td style="padding:10px;border-bottom:1px solid #eee">{s.get('result_date','TBD')}</td>
          <td style="padding:10px;border-bottom:1px solid #eee">
            <span style="background:{bg};color:{color};padding:3px 10px;border-radius:999px;
                         font-weight:700;font-size:12px">{rating}</span>
          </td>
          <td style="padding:10px;border-bottom:1px solid #eee;font-size:12px;color:#555">
            {s.get('catalyst','Auto-added — update commentary manually.')}
          </td>
        </tr>"""

    body = f"""
    <div style="font-family:Arial,sans-serif;max-width:700px;margin:0 auto">
      <div style="background:#0D1B2A;padding:20px;border-radius:8px 8px 0 0">
        <h2 style="color:white;margin:0">📊 NSE Watchlist — New Stocks Added</h2>
        <p style="color:#aaa;margin:4px 0 0">{date_str} | Auto-discovery by GitHub Actions</p>
      </div>
      <div style="background:#F8FAFC;padding:20px">
        <p style="color:#1A3A5C;font-size:15px">
          <strong>{count} new stock(s)</strong> have been auto-added to your Q4 FY26 watchlist
          based on the NSE earnings calendar.
        </p>
        <table style="width:100%;border-collapse:collapse;background:white;border-radius:8px;
                      overflow:hidden;box-shadow:0 1px 4px rgba(0,0,0,0.08)">
          <thead>
            <tr style="background:#2E5F8A;color:white">
              <th style="padding:12px;text-align:left">Stock</th>
              <th style="padding:12px;text-align:left">Sector</th>
              <th style="padding:12px;text-align:left">Result Date</th>
              <th style="padding:12px;text-align:left">My Rating</th>
              <th style="padding:12px;text-align:left">Catalyst</th>
            </tr>
          </thead>
          <tbody>{rows_html}</tbody>
        </table>
        <div style="margin-top:16px;background:#FFF3CD;border-left:4px solid #F59E0B;
                    padding:12px;border-radius:0 8px 8px 0">
          <strong>⚠ Action needed:</strong> Open GitHub → data.py → find these stocks
          → update <code>earnings_commentary</code>, <code>ind_rating</code>,
          and <code>ind_rationale</code> after reviewing.
        </div>
        <div style="margin-top:12px;text-align:center">
          <a href="https://nse-watchlist-james.streamlit.app"
             style="background:#1A3A5C;color:white;padding:10px 24px;border-radius:6px;
                    text-decoration:none;font-weight:600">Open Dashboard →</a>
          &nbsp;&nbsp;
          <a href="https://github.com/james7189/nse-watchlist/blob/main/data.py"
             style="background:#40916C;color:white;padding:10px 24px;border-radius:6px;
                    text-decoration:none;font-weight:600">Edit data.py →</a>
        </div>
      </div>
      <div style="background:#eee;padding:10px;text-align:center;font-size:11px;color:#888">
        NSE Watchlist Bot | Personal tracker — not SEBI-registered advice
      </div>
    </div>"""

    send_email(f"📊 {count} New Stock(s) Added — NSE Watchlist {date_str}", body)


def alert_results_declared(updated_stocks: list):
    """
    Alert when pending stocks get actuals updated.
    updated_stocks: list of dicts with name, act_eps, act_rev, est_eps, est_rev
    """
    if not updated_stocks:
        return

    count    = len(updated_stocks)
    date_str = datetime.now().strftime("%d-%b-%Y")

    # WhatsApp
    wa_lines = [f"🎯 *Results Declared — {date_str}*",
                f"",
                f"*{count} stock(s) updated with actuals:*",
                f""]

    for s in updated_stocks:
        name    = s['name']
        act_eps = s.get('act_eps')
        est_eps = s.get('est_eps')
        act_rev = s.get('act_rev')

        beat_str = ""
        if act_eps and est_eps and est_eps != 0:
            beat = (act_eps - est_eps) / abs(est_eps) * 100
            beat_str = f" ({beat:+.1f}% {'✅ BEAT' if beat > 0 else '❌ MISS'})"

        wa_lines.append(f"• *{name}*")
        wa_lines.append(f"  EPS: ₹{act_eps}{beat_str}")
        if act_rev:
            wa_lines.append(f"  Revenue: ₹{act_rev:,}Cr")
        wa_lines.append("")

    wa_lines.append("➡ https://nse-watchlist-james.streamlit.app")
    wa_lines.append("⚠ Add earnings commentary on GitHub")

    send_whatsapp("\n".join(wa_lines))

    # Email
    rows_html = ""
    for s in updated_stocks:
        act_eps = s.get('act_eps')
        est_eps = s.get('est_eps')
        act_rev = s.get('act_rev')
        est_rev = s.get('est_rev')

        beat_pct = ""
        beat_bg  = "#F8F8F8"
        beat_col = "#333"
        if act_eps and est_eps and est_eps != 0:
            beat = (act_eps - est_eps) / abs(est_eps) * 100
            beat_pct = f"{beat:+.1f}%"
            beat_bg  = "#D8F3DC" if beat > 0 else "#FDDCDC"
            beat_col = "#1B4332" if beat > 0 else "#C0392B"

        rev_beat = ""
        if act_rev and est_rev and est_rev != 0:
            rb = (act_rev - est_rev) / abs(est_rev) * 100
            rev_beat = f"<br><small style='color:{'#40916C' if rb>0 else '#C0392B'}'>{rb:+.1f}%</small>"

        act_rev_str = f"₹{act_rev:,}Cr" if act_rev else "—"
        est_rev_str = f"₹{est_rev:,}Cr" if est_rev else "—"
        act_eps_str = f"₹{act_eps}" if act_eps else "—"
        est_eps_str = f"₹{est_eps}" if est_eps else "—"

        rows_html += f"""
        <tr>
          <td style="padding:10px;border-bottom:1px solid #eee;font-weight:600">{s['name']}</td>
          <td style="padding:10px;border-bottom:1px solid #eee;color:#555">{est_eps_str}</td>
          <td style="padding:10px;border-bottom:1px solid #eee;font-weight:700">{act_eps_str}</td>
          <td style="padding:10px;border-bottom:1px solid #eee">
            <span style="background:{beat_bg};color:{beat_col};padding:3px 8px;
                         border-radius:4px;font-weight:700">{beat_pct}</span>
          </td>
          <td style="padding:10px;border-bottom:1px solid #eee">
            {act_rev_str}{rev_beat} vs est {est_rev_str}
          </td>
        </tr>"""

    body = f"""
    <div style="font-family:Arial,sans-serif;max-width:700px;margin:0 auto">
      <div style="background:#1B4332;padding:20px;border-radius:8px 8px 0 0">
        <h2 style="color:white;margin:0">🎯 Results Declared — Actuals Updated</h2>
        <p style="color:#aaa;margin:4px 0 0">{date_str} | Auto-fetched from Yahoo Finance</p>
      </div>
      <div style="background:#F8FAFC;padding:20px">
        <table style="width:100%;border-collapse:collapse;background:white;border-radius:8px;
                      overflow:hidden;box-shadow:0 1px 4px rgba(0,0,0,0.08)">
          <thead>
            <tr style="background:#2E5F8A;color:white">
              <th style="padding:12px;text-align:left">Stock</th>
              <th style="padding:12px;text-align:left">Est. EPS</th>
              <th style="padding:12px;text-align:left">Actual EPS</th>
              <th style="padding:12px;text-align:left">Beat/Miss</th>
              <th style="padding:12px;text-align:left">Revenue</th>
            </tr>
          </thead>
          <tbody>{rows_html}</tbody>
        </table>
        <div style="margin-top:16px;background:#FFF3CD;border-left:4px solid #F59E0B;
                    padding:12px;border-radius:0 8px 8px 0">
          <strong>⚠ Action needed:</strong> Add <code>earnings_commentary</code>,
          update <code>ind_rating</code> and <code>upside_captured</code> on GitHub.
        </div>
        <div style="margin-top:12px;text-align:center">
          <a href="https://nse-watchlist-james.streamlit.app"
             style="background:#1B4332;color:white;padding:10px 24px;border-radius:6px;
                    text-decoration:none;font-weight:600">View Results →</a>
          &nbsp;&nbsp;
          <a href="https://github.com/james7189/nse-watchlist/blob/main/data.py"
             style="background:#2E5F8A;color:white;padding:10px 24px;border-radius:6px;
                    text-decoration:none;font-weight:600">Edit data.py →</a>
        </div>
      </div>
    </div>"""

    send_email(f"🎯 {count} Result(s) Declared — NSE Watchlist {date_str}", body)


def alert_daily_summary(actuals_updated: int, stocks_added: int,
                        pending_count: int, declared_count: int):
    """
    Daily summary alert after each auto-update run.
    Only sends if something actually changed.
    """
    if actuals_updated == 0 and stocks_added == 0:
        return  # Nothing changed — don't spam

    date_str = datetime.now().strftime("%d-%b-%Y %H:%M")

    wa_msg = (
        f"📊 *NSE Watchlist Daily Update*\n"
        f"_{date_str}_\n\n"
        f"{'🆕 ' + str(stocks_added) + ' new stock(s) added' if stocks_added else ''}"
        f"{chr(10) if stocks_added and actuals_updated else ''}"
        f"{'✅ ' + str(actuals_updated) + ' result(s) declared & updated' if actuals_updated else ''}\n\n"
        f"📋 Status: {declared_count} declared | {pending_count} pending\n\n"
        f"➡ https://nse-watchlist-james.streamlit.app"
    )
    send_whatsapp(wa_msg)
