"""
Central data store — all stock metadata, estimates, actuals,
earnings commentary, and independent ratings.
"""

# ── TICKER MAP ────────────────────────────────────────────────────────────────
TICKER_MAP = {
    "GRASIM":            "GRASIM.NS",
    "GAIL":              "GAIL.NS",
    "PRESTIGE":          "PRESTIGE.NS",
    "RAINBOW CHILDCARE": "RAINBOW.NS",
    "BALKRISNA IND":     "BALKRISIND.NS",
    "JSW STEEL":         "JSWSTEEL.NS",
    "ASHOK LEYLAND":     "ASHOKLEY.NS",
    "NARAYANA HRUDAY":   "NH.NS",
    "GLENMARK PHARMA":   "GLENMARK.NS",
    "LINDE INDIA":       "LINDEINDIA.NS",
    "SUZLON":            "SUZLON.NS",
    "JK TYRE":           "JKTYRE.NS",
    "ASTRA MICROWAVE":   "ASTRAMICRO.NS",
    "BHARAT RASAYAN":    "BHARATRAS.NS",
    "GOODLUCK INDIA":    "GOODLUCK.NS",
    "KEI INDUSTRIES":    "KEI.NS",
    "ASTRAL":            "ASTRAL.NS",
    "JINDAL SAW":        "JINDALSAW.NS",
    "PFC":               "PFC.NS",
    "CESC":              "CESC.NS",
    "IRCON INTL":        "IRCON.NS",
    "BPCL":              "BPCL.NS",
    "INDIAMART":         "INDIAMART.NS",
    "IREDA":             "IREDA.NS",
    "COCHIN SHIPYARD":   "COCHINSHIP.NS",
    "MFSL":              "MFSL.NS",
    "POLYCAB":           "POLYCAB.NS",
    "HUDCO":             "HUDCO.NS",
    "VBL":               "VBL.NS",
    "PRINCE PIPES":      "PRINCEPIPE.NS",
    "CENTURY PLY":       "CENTURYPLY.NS",
    "HAVELLS":           "HAVELLS.NS",
    "PVR INOX":          "PVRINOX.NS",
    "SYRMA SGS":         "SYRMA.NS",
    "PERSISTENT":        "PERSISTENT.NS",
    "OBEROI REALTY":     "OBEROIRLTY.NS",
    "INDIAN HOTELS":     "INDHOTEL.NS",
    "JSW INFRA":         "JSWINFRA.NS",
    "NRB BEARING":       "NRBBEARING.NS",
}

# ── MASTER STOCK DATA ─────────────────────────────────────────────────────────
# status: "Declared" | "Pending" | "Watching"
STOCKS = [
    {
        "name":         "GRASIM",
        "sector":       "Materials / Paints",
        "result_date":  "21-May-26",
        "quarter":      "Q4 FY26",
        "status":       "Declared",
        "est_eps":      24.00,
        "act_eps":      28.87,
        "est_rev":      30000,
        "act_rev":      31200,
        "ss_rating":    "BUY",
        "ss_target":    3500,
        "ind_rating":   "HOLD / BOOK",
        "risk":         "HIGH",
        "upside_captured": "YES",
        "catalyst":     "Paints EBITDA near breakeven; VSF margin expansion; Q4 PAT beat 31% YoY",
        "earnings_commentary": (
            "Q4 PAT ₹1,958Cr (+31% YoY) — strong beat. Paints segment still EBITDA-negative but losses narrowing; "
            "management guided paints to hit EBITDA breakeven by H1 FY27. VSF volumes strong on China export demand. "
            "FY27 EBITDA growth guidance 37% over FY26–FY29 per analyst estimates. "
            "Key concall highlight: Birla Pivot (B2B building materials) targeting ₹10,000Cr revenue run-rate by FY28. "
            "Paints targeting 1,500 tinting machines by Dec 2026. "
            "Risk: Paints cumulative losses now >₹800Cr — investor patience being tested."
        ),
        "ind_rationale": "Already hit 52W high on results day. Paints EBITDA still negative. Valuation at 21x FY26 prices in perfection. Book partial.",
    },
    {
        "name":         "GAIL",
        "sector":       "Gas Utilities (PSU)",
        "result_date":  "21-May-26",
        "quarter":      "Q4 FY26",
        "status":       "Declared",
        "est_eps":      5.80,
        "act_eps":      6.10,
        "est_rev":      34000,
        "act_rev":      35200,
        "ss_rating":    "BUY",
        "ss_target":    220,
        "ind_rating":   "ACCUMULATE",
        "risk":         "MEDIUM",
        "upside_captured": "YES",
        "catalyst":     "Gas volume growth 8% YoY; tariff upside; PSU re-rating; dividend yield",
        "earnings_commentary": (
            "Q4 beat — gas transmission volumes +8% YoY driven by CGD sector demand. "
            "LPG marketing margins improved QoQ on lower propane import prices. "
            "Management guided FY27 gas volume growth of 10-12%. "
            "PNGRB tariff revision expected in H1 FY27 — could be a significant re-rating trigger. "
            "Dividend ₹5.50/sh for FY26 — yield ~2.7% at CMP. "
            "Petrochemicals segment (PATA) operating near full capacity — minor positive."
        ),
        "ind_rationale": "Gas volume growth real. Tariff revision is the key trigger. PSU overhang limits full re-rating. Accumulate.",
    },
    {
        "name":         "PRESTIGE",
        "sector":       "Real Estate",
        "result_date":  "21-May-26",
        "quarter":      "Q4 FY26",
        "status":       "Declared",
        "est_eps":      12.50,
        "act_eps":      14.20,
        "est_rev":      5200,
        "act_rev":      5800,
        "ss_rating":    "BUY",
        "ss_target":    1900,
        "ind_rating":   "ACCUMULATE",
        "risk":         "MEDIUM",
        "upside_captured": "YES",
        "catalyst":     "Pre-sales record; Bengaluru demand; NCR launch pipeline",
        "earnings_commentary": (
            "Strong quarter — pre-sales ₹6,200Cr in Q4, full year FY26 pre-sales ₹28,000Cr+ (record). "
            "Collections growth 22% YoY improving cash conversion. "
            "Management highlighted Mumbai and NCR launches for FY27 — geographic diversification key theme. "
            "Debt at ₹14,000Cr is on the higher side — watch interest coverage. "
            "Key concall point: Bengaluru commercial office leasing performing well; hospitality assets contributing."
        ),
        "ind_rationale": "Best-in-class developer but debt and Bengaluru concentration are risks. Accumulate on dips.",
    },
    {
        "name":         "RAINBOW CHILDCARE",
        "sector":       "Healthcare (Paediatric)",
        "result_date":  "22-May-26",
        "quarter":      "Q4 FY26",
        "status":       "Declared",
        "est_eps":      14.00,
        "act_eps":      25.2,
        "est_rev":      560,
        "act_rev":      445,
        "ss_rating":    "BUY",
        "ss_target":    1600,
        "ind_rating":   "ACCUMULATE",
        "risk":         "LOW",
        "upside_captured": None,
        "catalyst":     "Paediatric moat; Tier 2 expansion; consistent 4/4 beat history last year",
        "earnings_commentary": "Results pending. Watch for bed addition update, ARPOB growth, and Tier 2 hospital occupancy ramp.",
        "ind_rationale": "Quality niche. Buy on dips — expensive at 30x+ but consistent compounder.",
    },
    {
        "name":         "BALKRISNA IND",
        "sector":       "Auto Ancillary (OHT Tyres)",
        "result_date":  "23-May-26",
        "quarter":      "Q4 FY26",
        "status":       "Declared",
        "est_eps":      38.00,
        "act_eps":      64.26,
        "est_rev":      3100,
        "act_rev":      2932,
        "ss_rating":    "BUY",
        "ss_target":    3400,
        "ind_rating":   "ACCUMULATE",
        "risk":         "MEDIUM",
        "upside_captured": None,
        "catalyst":     "OHT export recovery; US channel re-stocking; rubber cost tailwind",
        "earnings_commentary": "Results pending. Key metrics: volume guidance for FY27, US market commentary, rubber cost trajectory.",
        "ind_rationale": "OHT cycle inflecting. China competition in European market is the key risk to watch.",
    },
    {
        "name":         "JSW STEEL",
        "sector":       "Metals & Steel",
        "result_date":  "24-May-26",
        "quarter":      "Q4 FY26",
        "status":       "Declared",
        "est_eps":      18.50,
        "act_eps":      91.27,
        "est_rev":      44000,
        "act_rev":      49798,
        "ss_rating":    "BUY",
        "ss_target":    1050,
        "ind_rating":   "REDUCE",
        "risk":         "HIGH",
        "upside_captured": None,
        "catalyst":     "Volume at record; coking coal softened; FY27 guidance key",
        "earnings_commentary": "Results pending. China dumping commentary from management will be the key market mover.",
        "ind_rationale": "China steel dumping structural headwind. JSPL merger complexity. Coking coal import dependency. Reduce.",
    },
    {
        "name":         "ASHOK LEYLAND",
        "sector":       "Commercial Vehicles",
        "result_date":  "23-May-26",
        "quarter":      "Q4 FY26",
        "status":       "Declared",
        "est_eps":      4.20,
        "act_eps":      5.63,
        "est_rev":      11500,
        "act_rev":      14761,
        "ss_rating":    "BUY",
        "ss_target":    260,
        "ind_rating":   "HOLD",
        "risk":         "MEDIUM",
        "upside_captured": None,
        "catalyst":     "MHCV recovery; exports; defence order pipeline",
        "earnings_commentary": "Results pending. Watch export volume growth and defence order update.",
        "ind_rationale": "MHCV cycle recovery factored in. CV cycles are mean-reverting — current upcycle is mature.",
    },
    {
        "name":         "NARAYANA HRUDAY",
        "sector":       "Healthcare (Cardiac)",
        "result_date":  "22-May-26",
        "quarter":      "Q4 FY26",
        "status":       "Declared",
        "est_eps":      8.80,
        "act_eps":      39.9,
        "est_rev":      1650,
        "act_rev":      2151,
        "ss_rating":    "BUY",
        "ss_target":    1500,
        "ind_rating":   "ACCUMULATE",
        "risk":         "LOW-MEDIUM",
        "upside_captured": None,
        "catalyst":     "Cayman profitability inflecting; India occupancy near peak",
        "earnings_commentary": "Results pending. Cayman Islands EBITDA margin and patient volume are the critical metrics.",
        "ind_rationale": "Cayman inflection is real. Demerger with NH Integrated Care adds near-term complexity.",
    },
    {
        "name":         "GLENMARK PHARMA",
        "sector":       "Pharma",
        "result_date":  "23-May-26",
        "quarter":      "Q4 FY26",
        "status":       "Declared",
        "est_eps":      16.50,
        "act_eps":      37.73,
        "est_rev":      3900,
        "act_rev":      3887,
        "ss_rating":    "HOLD",
        "ss_target":    1400,
        "ind_rating":   "REDUCE",
        "risk":         "HIGH",
        "upside_captured": None,
        "catalyst":     "US para IV pipeline; India branded growth",
        "earnings_commentary": "Results pending. Ichnos R&D burn (₹300-400Cr/yr) and US para IV filing updates are key.",
        "ind_rationale": "Ichnos is a value trap until resolved. High debt. HOLD consensus too generous — Reduce.",
    },
    {
        "name":         "LINDE INDIA",
        "sector":       "Industrials (Industrial Gases)",
        "result_date":  "23-May-26",
        "quarter":      "Q4 FY26",
        "status":       "Declared",
        "est_eps":      42.00,
        "act_eps":      69.33,
        "est_rev":      650,
        "act_rev":      701,
        "ss_rating":    "BUY",
        "ss_target":    9500,
        "ind_rating":   "HOLD",
        "risk":         "LOW",
        "upside_captured": None,
        "catalyst":     "Industrial gas demand; pharma + steel customer growth",
        "earnings_commentary": "Results pending. Parent Linde plc delisting overhang — any update on this is key.",
        "ind_rationale": "Predictable compounder but 55-60x PE is very expensive. Parent may delist — overhang risk.",
    },
    {
        "name":         "SUZLON",
        "sector":       "Wind Energy / Renewables",
        "result_date":  "25-May-26",
        "quarter":      "Q4 FY26",
        "status":       "Declared",
        "est_eps":      0.42,
        "act_eps":      2.36,
        "est_rev":      3550,
        "act_rev":      4228,
        "ss_rating":    "BUY",
        "ss_target":    72,
        "ind_rating":   "BUY",
        "risk":         "MEDIUM",
        "upside_captured": None,
        "catalyst":     "Order book 30-35% YoY; Blue Sky 5-6MW platform; OMS annuity cash flow",
        "earnings_commentary": "Results May 25. Watch order backlog size, Blue Sky turbine delivery timeline, OMS contract renewals.",
        "ind_rationale": "Order book strong. Stock down 40% from highs. Genuine upside if Q4 beats and FY27 guidance upgrades.",
    },
    {
        "name":         "KEI INDUSTRIES",
        "sector":       "Cables & Wires",
        "result_date":  "27-May-26",
        "quarter":      "Q4 FY26",
        "status":       "Declared",
        "est_eps":      28.00,
        "act_eps":      96.27,
        "est_rev":      2600,
        "act_rev":      3476,
        "ss_rating":    "BUY",
        "ss_target":    4800,
        "ind_rating":   "STRONG BUY",
        "risk":         "LOW",
        "upside_captured": None,
        "catalyst":     "Power infra capex; house wire demand; EHV cable orders; export push",
        "earnings_commentary": "Results May 27. Watch export revenue share, EHV order inflows, and retail distribution expansion.",
        "ind_rationale": "Structural play on India power capex. 20%+ revenue CAGR consistent. Clean management. Best setup on watchlist.",
    },
    {
        "name":         "ASTRAL",
        "sector":       "Pipes & Adhesives",
        "result_date":  "27-May-26",
        "quarter":      "Q4 FY26",
        "status":       "Declared",
        "est_eps":      14.00,
        "act_eps":      20.04,
        "est_rev":      1700,
        "act_rev":      2088,
        "ss_rating":    "BUY",
        "ss_target":    2400,
        "ind_rating":   "HOLD",
        "risk":         "LOW-MEDIUM",
        "upside_captured": None,
        "catalyst":     "Real estate demand; adhesives recovery; volume guidance",
        "earnings_commentary": "Results May 27. Adhesives recovery pace and EBITDA margin guidance for FY27 are the key watch items.",
        "ind_rationale": "Quality business but real estate slowdown risk. Adhesives uncertain. 40x+ PE demanding for slower-growth phase.",
    },
    {
        "name":         "PFC",
        "sector":       "NBFC / Power Finance (PSU)",
        "result_date":  "28-May-26",
        "quarter":      "Q4 FY26",
        "status":       "Declared",
        "est_eps":      12.00,
        "act_eps":      78.49,
        "est_rev":      12500,
        "act_rev":      11018,
        "ss_rating":    "BUY",
        "ss_target":    520,
        "ind_rating":   "ACCUMULATE",
        "risk":         "MEDIUM",
        "upside_captured": None,
        "catalyst":     "Renewable lending boom; NPA declining; dividend yield 3%+",
        "earnings_commentary": "Results May 28. NPA trajectory and renewable sector loan disbursement are the key metrics.",
        "ind_rationale": "PSU discount is structural but dividend yield attractive. Decent trade, not a long-term compounder.",
    },
    {
        "name":         "BPCL",
        "sector":       "Oil & Gas (PSU Refiner)",
        "result_date":  "30-May-26",
        "quarter":      "Q4 FY26",
        "status":       "Declared",
        "est_eps":      11.50,
        "act_eps":      60.48,
        "est_rev":      118000,
        "act_rev":      118700,
        "ss_rating":    "HOLD",
        "ss_target":    360,
        "ind_rating":   "REDUCE",
        "risk":         "HIGH",
        "upside_captured": None,
        "catalyst":     "GRM recovery; marketing margin; Mozambique LNG optionality",
        "earnings_commentary": "Results May 30. GRM and marketing margin commentary will be key. Any Mozambique LNG update is a bonus.",
        "ind_rationale": "Government controls pricing. Marketing margin is a policy variable. Mozambique LNG still years away. Reduce.",
    },
    {
        "name":         "POLYCAB",
        "sector":       "Cables & Wires",
        "result_date":  "03-Jun-26",
        "quarter":      "Q4 FY26",
        "status":       "Declared",
        "est_eps":      86.00,
        "act_eps":      176.93,
        "est_rev":      6200,
        "act_rev":      8864,
        "ss_rating":    "BUY",
        "ss_target":    8500,
        "ind_rating":   "STRONG BUY",
        "risk":         "LOW",
        "upside_captured": None,
        "catalyst":     "B2C channel expansion; EHV cable tailwind; FMEG margin improvement",
        "earnings_commentary": "Results Jun 3. FMEG segment profitability and EHV order book are the key metrics to track.",
        "ind_rationale": "Market leader in cables. B2C moat strong. PLI beneficiary. No red flags. One of the cleanest large-cap ideas.",
    },
    {
        "name":         "COCHIN SHIPYARD",
        "sector":       "Shipbuilding / Defence",
        "result_date":  "02-Jun-26",
        "quarter":      "Q4 FY26",
        "status":       "Declared",
        "est_eps":      42.00,
        "act_eps":      27.27,
        "est_rev":      1100,
        "act_rev":      1484,
        "ss_rating":    "BUY",
        "ss_target":    2200,
        "ind_rating":   "BUY",
        "risk":         "MEDIUM",
        "upside_captured": None,
        "catalyst":     "Navy frigate + sub orders; ISRO vessel; 47% stock rise on order surge",
        "earnings_commentary": "Results Jun 2. Order backlog size, execution timeline commentary, and any new defence contract wins are key.",
        "ind_rationale": "Genuine defence order surge. Stock up 47% in a month — some good news priced in. Accumulate in tranches.",
    },
    {
        "name":         "VBL",
        "sector":       "FMCG / Beverages (PepsiCo Franchise)",
        "result_date":  "27-Apr-26",
        "quarter":      "Q1 CY26 ⚠",
        "status":       "Declared",
        "est_eps":      10.80,
        "act_eps":      10.86,
        "est_rev":      5200,
        "act_rev":      6721,
        "ss_rating":    "BUY",
        "ss_target":    620,
        "ind_rating":   "ACCUMULATE",
        "risk":         "LOW-MEDIUM",
        "upside_captured": "YES",
        "catalyst":     "Q1 CY26 PAT +20%, vol +16.3%, Twizza acquisition complete. Calendar Year company.",
        "earnings_commentary": (
            "Q1 CY26 PAT ₹879Cr (+20% YoY). Revenue ₹6,721Cr (+18.3%). Volume 363M cases (+16.3%). "
            "India volumes +14.4%, International +21.4% (Africa driving growth). "
            "Gross margin improved 62bps to 55.2% — benefit of early raw material stocking strategy. "
            "Twizza (South Africa) acquisition completed — integration on track. "
            "Interim dividend ₹0.50/sh. "
            "⚠ Calendar Year company — next result Q2 CY26 (Apr-Jun 2026) ~late July 2026. "
            "Q2 is the peak summer quarter — critical for full-year volume guidance."
        ),
        "ind_rationale": "Quality PepsiCo franchise bottler. Stock down 28% from highs — accumulate for summer Q2 play.",
    },
    {
        "name":         "PRINCE PIPES",
        "sector":       "Pipes & Fittings (PVC/CPVC)",
        "result_date":  "20-May-26",
        "quarter":      "Q4 FY26",
        "status":       "Declared",
        "est_eps":      2.20,
        "act_eps":      0.40,
        "est_rev":      750,
        "act_rev":      850,
        "ss_rating":    "BUY",
        "ss_target":    440,
        "ind_rating":   "HOLD",
        "risk":         "MEDIUM",
        "upside_captured": "NO",
        "catalyst":     "Q4 vol record 62,167MT (+23% YoY). But EPS miss -82% vs estimate.",
        "earnings_commentary": (
            "Q4 volume record 62,167MT (+23% YoY) — impressive top-line momentum. "
            "But EPS ₹0.40 vs estimate ₹2.20 — massive 82% earnings miss. "
            "Revenue beat ₹850Cr vs est ₹750Cr — volume came at the cost of margins. "
            "Bathware segment reported ₹5Cr loss — still not contributing positively. "
            "Capacity utilisation only 52% — Bihar plant adding capacity but demand not filling it. "
            "FY26 EBITDA margin ~9% vs repeated guidance of 11-13% — guidance credibility damaged. "
            "Management guided FY27 margins at 11-13% again — market skeptical."
        ),
        "ind_rationale": "Volume growth real but margins not converting. Guidance credibility low. Better plays: Astral, KEI, Polycab.",
    },
    {
        "name":         "CENTURY PLY",
        "sector":       "Plywood / MDF / Laminates",
        "result_date":  "22-May-26",
        "quarter":      "Q4 FY26",
        "status":       "Declared",
        "est_eps":      4.20,
        "act_eps":      5.24,
        "est_rev":      1300,
        "act_rev":      1492,
        "ss_rating":    "BUY",
        "ss_target":    820,
        "ind_rating":   "ACCUMULATE",
        "risk":         "LOW-MEDIUM",
        "upside_captured": "YES",
        "catalyst":     "PAT +49% YoY, Rev +25%. All 3 segments firing — first time in several quarters.",
        "earnings_commentary": (
            "Strong broad-based beat. Q4 PAT ₹79.4Cr (+49% YoY). Revenue ₹1,492Cr (+25% YoY). "
            "Plywood +14.8% YoY. MDF +27.87% YoY — the standout segment. Laminates +16.57% YoY. "
            "FY26 revenue ₹5,397Cr (+19%), FY26 PAT ₹268Cr (+44%). "
            "Sequential revenue +10.5% from Q3. PAT +22% sequentially — margin recovery visible. "
            "Board recommended ₹1/sh final dividend. "
            "Conference call scheduled May 25 — watch for MDF capacity utilisation guidance and competition commentary."
        ),
        "ind_rationale": "All three segments growing simultaneously is rare. MDF competition (Greenply, Action Tesa) is the key risk. Accumulate.",
    },
    {
        "name":         "HAVELLS",
        "sector":       "Electricals / Consumer Appliances",
        "result_date":  "22-Apr-26",
        "quarter":      "Q4 FY26",
        "status":       "Declared",
        "est_eps":      7.80,
        "act_eps":      9.20,
        "est_rev":      6200,
        "act_rev":      6688,
        "ss_rating":    "BUY",
        "ss_target":    1700,
        "ind_rating":   "ACCUMULATE",
        "risk":         "LOW-MEDIUM",
        "upside_captured": "YES",
        "catalyst":     "PAT +40% YoY; Div ₹10/sh; industrial infra strong",
        "earnings_commentary": (
            "Q4 standalone revenue ₹6,688Cr. PAT +40% YoY. "
            "Industrial infrastructure segment (cables, switchgear) — strong execution, benefiting from power capex cycle. "
            "Lloyd (AC/appliances) weaker — impacted by global trade disruptions and pricing pressure from Chinese brands. "
            "Increased advertising spend while containing total cost growth. "
            "Final dividend ₹6/sh + interim ₹4/sh = ₹10/sh total for FY26. "
            "Management commentary: margins held except Lloyd; consumer categories soft but expected to recover H1 FY27."
        ),
        "ind_rationale": "Quality electrical brand but Lloyd overhang limits full re-rating. 55-60x PE not cheap. Accumulate on corrections only.",
    },
    {
        "name":         "PVR INOX",
        "sector":       "Multiplex / Entertainment",
        "result_date":  "11-May-26",
        "quarter":      "Q4 FY26",
        "status":       "Declared",
        "est_eps":      -5.00,
        "act_eps":      18.70,
        "est_rev":      1400,
        "act_rev":      1547,
        "ss_rating":    "BUY",
        "ss_target":    1800,
        "ind_rating":   "HOLD",
        "risk":         "HIGH",
        "upside_captured": "YES",
        "catalyst":     "Q4 PAT ₹187Cr turnaround from -₹125Cr. Dhurandhar blockbuster driver.",
        "earnings_commentary": (
            "Massive Q4 turnaround — PAT ₹187Cr vs -₹125Cr loss in Q4 FY25. "
            "Revenue ₹1,547Cr (+25.8% YoY). Avg ticket price ₹315 (+22% YoY) — premiumisation working. "
            "F&B spend per head ₹165 (+32% YoY) — high margin revenue stream growing. "
            "Footfalls 31M, marginally up from 30.5M — volume growth limited; ATP doing the heavy lifting. "
            "Blockbuster Dhurandhar was the primary driver — Q1 FY27 content pipeline is the key risk. "
            "Stock fell 4.5% despite strong results — market read this as content-dependent, not structural. "
            "Management highlighted premium screen addition (LUXE, ScreenX) as long-term strategy."
        ),
        "ind_rationale": "Content-driven beat, not structural. Debt persists. OTT is a long-term structural threat. Trade it, don't hold.",
    },
    {
        "name":         "SYRMA SGS",
        "sector":       "Electronics EMS",
        "result_date":  "11-May-26",
        "quarter":      "Q4 FY26",
        "status":       "Declared",
        "est_eps":      6.50,
        "act_eps":      12.60,
        "est_rev":      950,
        "act_rev":      1465,
        "ss_rating":    "BUY",
        "ss_target":    1500,
        "ind_rating":   "BUY",
        "risk":         "MEDIUM",
        "upside_captured": "YES",
        "catalyst":     "Q4 PAT +87%, exports +41% crossing ₹1,200Cr. Record high post-results.",
        "earnings_commentary": (
            "Exceptional quarter. Q4 PAT ₹119Cr — massive beat vs est ₹55Cr. Revenue ₹1,465Cr (+58% YoY). "
            "FY26 full year: PAT ₹346Cr (+87% YoY), Revenue ₹4,819Cr (+27% YoY). "
            "Operating EBITDA ₹545Cr — ahead of management's own guidance given at start of year. "
            "Exports crossed ₹1,200Cr mark (+41% YoY) — global competitiveness emerging beyond India. "
            "Positive operating cash flow with net working capital days improving. "
            "MD Jasbir Singh Gujral: 'FY26 was a strong year of execution — delivered with positive OCF and capital discipline.' "
            "Stock hit record high ₹1,188 day after results before giving back gains."
        ),
        "ind_rationale": "Genuine EMS compounder. Diversified across medical, defence, consumer. Buy on 15-20% corrections from record high.",
    },
    {
        "name":         "PERSISTENT",
        "sector":       "IT Services (Mid-Cap)",
        "result_date":  "23-Apr-26",
        "quarter":      "Q4 FY26",
        "status":       "Declared",
        "est_eps":      65.00,
        "act_eps":      70.40,
        "est_rev":      3900,
        "act_rev":      4056,
        "ss_rating":    "BUY",
        "ss_target":    6800,
        "ind_rating":   "STRONG BUY",
        "risk":         "LOW",
        "upside_captured": "YES",
        "catalyst":     "24th consecutive quarter of QoQ growth. EBIT margin +190bps. Stock fell 5% — opportunity.",
        "earnings_commentary": (
            "Q4 revenue USD 436M (+16.2% YoY in USD, +25.1% in INR). PAT ₹529Cr (+33.7% YoY). "
            "EBIT margin 16.3% — 190bps sequential improvement. "
            "24th consecutive quarter of sequential revenue growth — six unbroken years without a miss. "
            "FY26 full year: Revenue ₹14,748Cr (+23.5%), PAT ₹1,865Cr (+33.2%). "
            "Headcount grew to 27,502 — net addition 2,908 in a year when peers were cutting. "
            "Attrition improved to 13.0% TTM from 13.9% in Q1 FY26. "
            "Dividend ₹40/sh for FY26 (vs ₹35 prior year). "
            "Stock fell 5.3% post results — classic 'sell the news' on premium valuation. "
            "This dip is a buying opportunity for a quality compounder."
        ),
        "ind_rationale": "India's best mid-cap IT compounder. 24 consecutive quarterly growth. Post-results dip = buy opportunity.",
    },
    {
        "name":         "OBEROI REALTY",
        "sector":       "Real Estate (Luxury)",
        "result_date":  "08-May-26",
        "quarter":      "Q4 FY26",
        "status":       "Declared",
        "est_eps":      52.00,
        "act_eps":      66.00,
        "est_rev":      1660,
        "act_rev":      1750,
        "ss_rating":    "BUY",
        "ss_target":    2400,
        "ind_rating":   "ACCUMULATE",
        "risk":         "MEDIUM",
        "upside_captured": "YES",
        "catalyst":     "PAT +62.35% YoY, Rev +52.14%. Beat Bloomberg est. EBITDA margin 54.88%.",
        "earnings_commentary": (
            "Strong beat. Q4 PAT ₹703Cr (+62.35% YoY) vs Bloomberg est ₹649Cr. "
            "Revenue ₹1,750Cr (+52.14% YoY) vs est ₹1,661Cr. "
            "EBITDA margin expanded to 54.88% from 53.74% — best-in-class for Indian real estate. "
            "FY26 full year: Revenue ₹6,009Cr (+13.67%), PAT ₹2,507Cr (+12.66%). "
            "FY26 bookings ₹5,447Cr (+3.14% YoY) but units booked -24.86% — price holding, volume normalising. "
            "Board approved NCD issuance up to ₹4,000Cr — signals capital intensity for new project acquisitions. "
            "Dividend ₹2/sh (interim). Debt-equity improved to 0.16 — still clean balance sheet."
        ),
        "ind_rationale": "Best-in-class luxury developer. EBITDA >50% unmatched in India RE. NCD ₹4,000Cr signals D/E will rise.",
    },
    {
        "name":         "INDIAN HOTELS",
        "sector":       "Hospitality (Taj / IHCL)",
        "result_date":  "11-May-26",
        "quarter":      "Q4 FY26",
        "status":       "Declared",
        "est_eps":      6.50,
        "act_eps":      7.20,
        "est_rev":      5100,
        "act_rev":      5433,
        "ss_rating":    "BUY",
        "ss_target":    900,
        "ind_rating":   "BUY",
        "risk":         "LOW-MEDIUM",
        "upside_captured": "YES",
        "catalyst":     "Rev +18% YoY. Div ₹10/sh. Hospitality upcycle intact.",
        "earnings_commentary": (
            "Q4 revenue ₹5,433Cr (+18% YoY). PAT beat. Dividend ₹10/sh (face value ₹1). "
            "India hospitality upcycle intact — RevPAR growth driven by MICE, weddings, and leisure travel. "
            "Premium segment demand strong — Taj brand pricing power demonstrated. "
            "International expansion (UK, Middle East, Southeast Asia) gaining traction — management contracts asset-light. "
            "Ginger (budget) segment performing above expectations — full hotel portfolio firing. "
            "Management guided FY27 room addition of 1,500+ keys across owned and managed properties."
        ),
        "ind_rationale": "Best play on India's travel boom. Taj brand moat. Asset-light model. International optionality. BUY.",
    },
    {
        "name":         "JSW INFRA",
        "sector":       "Ports & Logistics Infrastructure",
        "result_date":  "08-May-26",
        "quarter":      "Q4 FY26",
        "status":       "Declared",
        "est_eps":      8.50,
        "act_eps":      7.28,
        "est_rev":      1350,
        "act_rev":      1522,
        "ss_rating":    "BUY",
        "ss_target":    420,
        "ind_rating":   "HOLD",
        "risk":         "MEDIUM",
        "upside_captured": "PARTIAL",
        "catalyst":     "FY26 Rev +20%, cargo 122MT. Fire exceptional ₹68Cr. FY28 guidance ambitious.",
        "earnings_commentary": (
            "FY26 revenue ₹5,361Cr (+20% YoY). Operating EBITDA ₹2,604Cr (+15%). Cargo 122 MT (+4% YoY). "
            "Q4 revenue ₹1,522Cr — revenue beat. But PAT flat YoY due to exceptional item. "
            "Exceptional: ₹68Cr fire loss at Fujairah Liquid Terminal (UAE) — one-time but signals operational risk. "
            "Rail logistics integration: acquired JSW (South) Rail Logistics and JSW Minerals Rail Logistics. "
            "New terminal: Arakkonam, Chennai commenced commercial operations April 14, 2026. "
            "FY28 guidance: Revenue ₹10,800Cr, EBITDA ₹5,000Cr — implies doubling in 2 years. Ambitious. "
            "Dividend ₹0.90/sh. D/E rising as capex ramps up."
        ),
        "ind_rationale": "Strong structural story. But fire incident, flat PAT, and aggressive FY28 guidance create uncertainty. Hold.",
    },
    {
        "name":         "NRB BEARING",
        "sector":       "Auto Ancillary (Bearings)",
        "result_date":  "07-May-26",
        "quarter":      "Q4 FY26",
        "status":       "Declared",
        "est_eps":      5.50,
        "act_eps":      6.80,
        "est_rev":      320,
        "act_rev":      355,
        "ss_rating":    "BUY",
        "ss_target":    520,
        "ind_rating":   "ACCUMULATE",
        "risk":         "MEDIUM",
        "upside_captured": "YES",
        "catalyst":     "FY26 PAT +77%. EBITDA +19%. Capacity expansion announced.",
        "earnings_commentary": (
            "FY26 full year: PAT ₹146Cr (+77% YoY), Revenue ₹1,335Cr (+11%), EBITDA ₹267Cr (+19%). "
            "Q4 beat — EPS ₹6.80 vs est ₹5.50. "
            "Interim dividend ₹2.25/sh (record date May 13, 2026). No final dividend. "
            "Capacity expansion: Land acquisition up to ₹40Cr approved. "
            "Strategic investments: Mahant Tool Room Pvt Ltd and NRB Unitech Friction Solutions Pvt Ltd — "
            "deepening tooling and friction solutions capability. "
            "EV transition strategy: pivoting to EV-specific bearing variants. "
            "Management call (May 11) highlighted broad-based demand across auto + industrial segments."
        ),
        "ind_rationale": "Niche auto ancillary with EV transition strategy. FY26 PAT +77% impressive. Small-cap — track closely.",
    },
    # ── Remaining pending stocks (abbreviated) ─────────────────────────────
    {
        "name": "JK TYRE", "sector": "Auto Ancillary (Tyres)",
        "result_date": "26-May-26", "quarter": "Q4 FY26", "status": "Pending",
        "est_eps": 7.00, "act_eps":      24.67, "est_rev": 4300, "act_rev":      4222,
        "ss_rating": "BUY", "ss_target": 420,
        "ind_rating": "AVOID", "risk": "HIGH",
        "upside_captured": None,
        "catalyst": "TBR & PCR volume recovery; raw material tailwind",
        "earnings_commentary": "Results May 26. High debt balance sheet concern. Watch NWC and debt reduction commentary.",
        "ind_rationale": "High debt (D/E ~1.5x). Chinese tyre import risk. Better quality plays in auto ancillary. Avoid.",
    },
    {
        "name": "ASTRA MICROWAVE", "sector": "Defence Electronics",
        "result_date": "26-May-26", "quarter": "Q4 FY26", "status": "Pending",
        "est_eps": 9.50, "act_eps":      16.92, "est_rev": 440, "act_rev":      260,
        "ss_rating": "BUY", "ss_target": 900,
        "ind_rating": "ACCUMULATE", "risk": "LOW-MEDIUM",
        "upside_captured": None,
        "catalyst": "Strong defence order backlog; DRDO/ISRO sourcing; margin expansion",
        "earnings_commentary": "Results May 26. Order backlog and new DRDO/ISRO contract wins are the key metrics.",
        "ind_rationale": "Niche defence electronics moat. 2+ year order backlog. Low float = sharp moves on beats.",
    },
    {
        "name": "BHARAT RASAYAN", "sector": "Agrochemicals",
        "result_date": "26-May-26", "quarter": "Q4 FY26", "status": "Pending",
        "est_eps": 60.00, "act_eps":      79.84, "est_rev": 575, "act_rev":      270,
        "ss_rating": "BUY", "ss_target": 11500,
        "ind_rating": "HOLD", "risk": "MEDIUM",
        "upside_captured": None,
        "catalyst": "Rabi season demand; export recovery; low base Q4 FY25",
        "earnings_commentary": "Results May 26. Export pricing and domestic rabi season demand are key.",
        "ind_rationale": "Contract manufacturer with limited IP. Agrochemical cycle recovery slow. Low base flatters YoY. Hold.",
    },
    {
        "name": "GOODLUCK INDIA", "sector": "Steel Tubes & Pipes",
        "result_date": "26-May-26", "quarter": "Q4 FY26", "status": "Pending",
        "est_eps": 33.00, "act_eps":      51.11, "est_rev": 3350, "act_rev":      1027,
        "ss_rating": "BUY", "ss_target": 1050,
        "ind_rating": "AVOID", "risk": "HIGH",
        "upside_captured": None,
        "catalyst": "Infra order execution; value-added tube mix",
        "earnings_commentary": "Results May 26. Promoter structure opacity — 45 entities. Track carefully.",
        "ind_rationale": "Complex promoter structure (45 entities). Competitive industry. Thin margins. Avoid.",
    },
    {
        "name": "JINDAL SAW", "sector": "Steel / Pipes (Infra)",
        "result_date": "28-May-26", "quarter": "Q4 FY26", "status": "Pending",
        "est_eps": 24.00, "act_eps":      15.22, "est_rev": 5800, "act_rev":      4633,
        "ss_rating": "BUY", "ss_target": 480,
        "ind_rating": "HOLD", "risk": "MEDIUM",
        "upside_captured": None,
        "catalyst": "Water infra JJBY demand; DI pipe orders; US anti-dump benefit",
        "earnings_commentary": "Results May 28. DI pipe order inflow and Jal Jeevan Mission execution rate are key.",
        "ind_rationale": "DI pipe demand real. US anti-dump is one-time benefit. Complex Jindal group structure discount.",
    },
    {
        "name": "CESC", "sector": "Power Utility",
        "result_date": "29-May-26", "quarter": "Q4 FY26", "status": "Pending",
        "est_eps": 20.00, "act_eps":      11.63, "est_rev": 3800, "act_rev":      4096,
        "ss_rating": "BUY", "ss_target": 220,
        "ind_rating": "HOLD", "risk": "LOW-MEDIUM",
        "upside_captured": None,
        "catalyst": "Stable distribution; Haldia expansion; dividend play",
        "earnings_commentary": "Results May 29. Regulated utility — minimal surprise expected. Watch Haldia commissioning update.",
        "ind_rationale": "Stable utility. No visible growth catalyst. Trade for dividend, not capital appreciation.",
    },
    {
        "name": "IRCON INTL", "sector": "Infrastructure (Railway)",
        "result_date": "29-May-26", "quarter": "Q4 FY26", "status": "Pending",
        "est_eps": 8.50, "act_eps":      6.33, "est_rev": 4200, "act_rev":      2119,
        "ss_rating": "BUY", "ss_target": 260,
        "ind_rating": "HOLD", "risk": "MEDIUM",
        "upside_captured": None,
        "catalyst": "Railway electrification; Kavach orders; international projects",
        "earnings_commentary": "Results May 29. Order-to-execution conversion ratio and international project updates are key.",
        "ind_rationale": "Railway project execution always slower than guided. International projects carry forex and political risk.",
    },
    {
        "name": "INDIAMART", "sector": "B2B e-Commerce",
        "result_date": "30-May-26", "quarter": "Q4 FY26", "status": "Pending",
        "est_eps": 82.00, "act_eps":      78.76, "est_rev": 380, "act_rev":      404,
        "ss_rating": "BUY", "ss_target": 4200,
        "ind_rating": "HOLD", "risk": "LOW-MEDIUM",
        "upside_captured": None,
        "catalyst": "Paid supplier additions; ARPU growth; cash-rich balance sheet",
        "earnings_commentary": "Results May 30. Paid supplier net additions and ARPU growth rate are the critical metrics.",
        "ind_rationale": "Cash-rich asset-light. Paid supplier growth plateauing. Competition from Udaan, Meesho B2B. 45-50x for maturing biz.",
    },
    {
        "name": "IREDA", "sector": "Renewable Energy Finance",
        "result_date": "02-Jun-26", "quarter": "Q4 FY26", "status": "Pending",
        "est_eps": 2.80, "act_eps":      6.84, "est_rev": 1850, "act_rev":      2121,
        "ss_rating": "BUY", "ss_target": 240,
        "ind_rating": "ACCUMULATE", "risk": "MEDIUM",
        "upside_captured": None,
        "catalyst": "Green infra lending CAGR 40%+; ultra-low NPA; policy tailwind",
        "earnings_commentary": "Results Jun 2. Loan disbursement growth, NPA, and NIM are the key metrics.",
        "ind_rationale": "Green energy lending CAGR 40%+ real. PSU risk — govt can direct loan books. Renewable project delay risk.",
    },
    {
        "name": "MFSL", "sector": "Insurance / Financial Services",
        "result_date": "03-Jun-26", "quarter": "Q4 FY26", "status": "Pending",
        "est_eps": 11.50, "act_eps":      2.35, "est_rev": 4200, "act_rev":      10801,
        "ss_rating": "BUY", "ss_target": 1100,
        "ind_rating": "HOLD", "risk": "MEDIUM",
        "upside_captured": None,
        "catalyst": "Max Life VNB growth; AUM expansion; margin improvement",
        "earnings_commentary": "Results Jun 3. Max Life VNB margin and new business premium growth are the key metrics.",
        "ind_rationale": "Holding company structure creates structural discount. IRDAI surrender value norms — regulatory risk live.",
    },
    {
        "name": "HUDCO", "sector": "Housing Finance / Infra (PSU)",
        "result_date": "04-Jun-26", "quarter": "Q4 FY26", "status": "Pending",
        "est_eps": 3.50, "act_eps":      20.15, "est_rev": 3100, "act_rev":      744,
        "ss_rating": "BUY", "ss_target": 240,
        "ind_rating": "REDUCE", "risk": "HIGH",
        "upside_captured": None,
        "catalyst": "Urban infra loans; affordable housing; dividend yield ~3%",
        "earnings_commentary": "Results Jun 4. NPA quality and loan disbursement growth are key. PSU overhang limits upside.",
        "ind_rationale": "PSU NBFC with govt-directed lending. NPA risk higher than reported. Better alternatives in NBFC space.",
    },
]

# ── RATING COLOR MAP ──────────────────────────────────────────────────────────
RATING_COLORS = {
    "STRONG BUY" : "#1B4332",
    "BUY"        : "#40916C",
    "ACCUMULATE" : "#2D6A4F",
    "HOLD"       : "#856404",
    "HOLD / BOOK": "#856404",
    "REDUCE"     : "#E65100",
    "AVOID"      : "#C0392B",
}
RATING_BG = {
    "STRONG BUY" : "#D8F3DC",
    "BUY"        : "#D1FAE5",
    "ACCUMULATE" : "#E9F5EE",
    "HOLD"       : "#FFF3CD",
    "HOLD / BOOK": "#FFF3CD",
    "REDUCE"     : "#FFF3E0",
    "AVOID"      : "#FDDCDC",
}
RISK_BG = {
    "LOW"        : "#D8F3DC",
    "LOW-MEDIUM" : "#E9F5EE",
    "MEDIUM"     : "#FFF3CD",
    "HIGH"       : "#FDDCDC",
}
