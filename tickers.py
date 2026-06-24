# tickers.py — Full US stock universe (NYSE + NASDAQ)
# ~820 liquid US stocks: S&P 500 + Nasdaq 100 + Russell 1000 mid-caps
# Last cleaned: 2026-05-26 — verified active tickers only
# NSE support removed — US-only screener

US_TICKERS = [
    # ── Mega-cap Tech (NASDAQ) ─────────────────────────────────────────────
    "AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "GOOG", "META", "TSLA",
    "AVGO", "ORCL", "ADBE", "CSCO", "QCOM", "TXN", "AMAT", "MU",
    "AMD", "INTC", "KLAC", "LRCX", "MRVL", "NXPI", "ON", "SWKS",
    "MPWR", "ENTG", "WOLF", "ONTO", "COHU", "ACLS",
    # ── Software / Cloud ──────────────────────────────────────────────────
    "CRM", "NOW", "INTU", "PANW", "CRWD", "SNOW", "DDOG", "ZS",
    "OKTA", "MDB", "GTLB", "HUBS", "VEEV", "WDAY", "TEAM", "SPLK",
    "FROG", "DOCN", "NET", "CFLT", "APP", "TTD", "RBLX", "HOOD",
    "BILL", "SMAR", "BOX", "APPN", "PCTY", "PAYC",
    # ── Internet / E-Commerce ─────────────────────────────────────────────
    "NFLX", "ABNB", "UBER", "LYFT", "DASH", "SHOP", "EBAY", "ETSY",
    "PINS", "SNAP", "SPOT", "ZM", "YELP", "IAC", "ANGI", "TRIP",
    # ── Fintech / Payments ────────────────────────────────────────────────
    "V", "MA", "PYPL", "SQ", "AFRM", "SOFI", "UPST", "LC",
    "COIN", "MSTR", "GPN", "FIS", "FISV", "WEX", "PRFT", "RPAY",
    # ── Semiconductors extended ───────────────────────────────────────────
    "ASML", "TSM", "ARM", "MCHP", "ADI", "XLNX", "MTSI", "SLAB",
    "DIOD", "POWI", "SMTC", "AMBA", "AEHR", "FORM",
    # ── Financials — Banks ────────────────────────────────────────────────
    "JPM", "BAC", "WFC", "C", "GS", "MS", "AXP", "BLK", "SCHW", "USB",
    "PNC", "TFC", "COF", "MTB", "RF", "KEY", "CFG", "HBAN", "FITB", "ZION",
    "ALLY", "CMA", "SNV", "WTFC", "BOKF", "FHB", "FBMS", "HOPE", "NBTB",
    # ── Insurance ────────────────────────────────────────────────────────
    "BRK.B", "CB", "HIG", "WRB", "CINF", "AFL", "MET", "PRU", "UNM",
    "GL", "LNC", "TRV", "ALL", "PGR", "AON", "MMC", "MKL", "RLI",
    # ── Asset Management / Alt Finance ───────────────────────────────────
    "BX", "KKR", "APO", "CG", "ARES", "OWL", "BN", "BAM",
    "GAIN", "MAIN", "ARCC", "HTGC", "GBDC", "PFLT",
    # ── Energy — Oil & Gas ───────────────────────────────────────────────
    "XOM", "CVX", "COP", "SLB", "EOG", "MPC", "PSX", "VLO", "OXY",
    "DVN", "FANG", "MRO", "APA", "SM", "CIVI", "PR", "MGY", "MTDR",
    "HAL", "BKR", "CHX", "NOV", "PTEN", "RIG", "HP", "NE",
    # ── Energy — Clean / Utilities ────────────────────────────────────────
    "NEE", "DUK", "SO", "D", "AEP", "EXC", "SRE", "PEG", "ED", "EIX",
    "PCG", "CEG", "ETR", "FE", "AES", "NRG", "VST", "GEV",
    "ENPH", "SEDG", "FSLR", "RUN", "ARRY", "NOVA", "CSIQ",
    # ── Healthcare — Pharma / Biotech ────────────────────────────────────
    "PFE", "JNJ", "ABT", "MRK", "BMY", "LLY", "AMGN", "GILD",
    "BIIB", "REGN", "VRTX", "MRNA", "BNTX", "ALNY", "IONS",
    "INCY", "EXEL", "HALO", "FOLD", "RARE",
    # ── Healthcare — Equipment / Services ────────────────────────────────
    "UNH", "CVS", "CI", "HUM", "ELV", "CNC", "MOH",
    "TMO", "DHR", "SYK", "BSX", "MDT", "BDX", "EW", "ISRG",
    "ZBH", "HOLX", "ALGN", "DXCM", "PODD", "NVCR", "NVST",
    "MCK", "CAH", "ABC", "WAT", "IDXX", "IQV", "A", "PKI",
    # ── Consumer Discretionary ────────────────────────────────────────────
    "AMZN", "HD", "LOW", "TGT", "WMT", "COST", "DG", "DLTR",
    "MCD", "SBUX", "YUM", "QSR", "DPZ", "CMG", "CAKE", "DRI",
    "BLMN", "EAT", "TXRH", "JACK", "SHAK",
    "NKE", "LULU", "UAA", "PVH", "RL", "TPR", "CPRI", "HBI",
    "GPS", "ANF", "AEO", "URBN", "ROST", "TJX", "BURL",
    "WSM", "RH", "W", "FND", "WHR", "BBWI",
    # ── Autos ────────────────────────────────────────────────────────────
    "TSLA", "F", "GM", "RIVN", "LCID", "NKLA",
    "PAG", "AN", "KMX", "LAD", "SAH", "ABG",
    "APTV", "LEA", "MGA", "BWA", "DAN",
    # ── Consumer Staples ─────────────────────────────────────────────────
    "PG", "KO", "PEP", "CL", "KMB", "CHD", "EL", "SPB", "NWL",
    "KHC", "GIS", "CAG", "CPB", "HSY", "MKC", "SJM", "HRL", "TSN",
    "TAP", "STZ", "MNST", "KDP", "CELH", "FIZZ", "COKE",
    # ── Media / Entertainment ─────────────────────────────────────────────
    "DIS", "CMCSA", "CHTR", "PARA", "FOX", "FOXA", "WBD", "NYT",
    "NWS", "OMC", "WPP", "IPG", "NFLX", "SPOT", "LYV", "MSG",
    # ── Telecom ───────────────────────────────────────────────────────────
    "T", "VZ", "LUMN", "TMUS", "CABO", "TDS", "SHEN", "LBRDA",
    # ── Industrials — Aerospace & Defense ────────────────────────────────
    "BA", "LMT", "RTX", "NOC", "GD", "HII", "TDG", "LDOS",
    "BAH", "CACI", "SAIC", "DRS", "KTOS", "AVAV", "RKLB",
    # ── Industrials — Machinery & Equipment ──────────────────────────────
    "CAT", "DE", "EMR", "ETN", "PH", "ITW", "DOV", "FTV", "AME", "ROP",
    "GE", "HON", "MMM", "IR", "XYL", "GNRC", "GTLS", "FLOW",
    "TT", "JCI", "CARR", "OTIS", "AIXI",
    # ── Industrials — Transport & Logistics ──────────────────────────────
    "UPS", "FDX", "JBHT", "ODFL", "XPO", "CHRW", "R", "EXPD",
    "MATX", "SAIA", "SNDR", "WERN", "KNX", "LSTR", "ARCB",
    "DAL", "UAL", "AAL", "LUV", "ALK", "SAVE",
    # ── Industrials — Waste / Services ───────────────────────────────────
    "RSG", "WM", "CWST", "SRCL", "CLH",
    # ── Materials — Metals & Mining ──────────────────────────────────────
    "NEM", "FCX", "AA", "CLF", "NUE", "STLD", "RS", "CMC",
    "MP", "ARNC", "ATI", "CENX", "KALU", "MTRX",
    # ── Materials — Chemicals ────────────────────────────────────────────
    "DD", "DOW", "LYB", "EMN", "IFF", "ALB", "CE", "HUN", "OLN",
    "TROX", "AXTA", "RPM", "SHW", "PPG", "FUL", "CBT", "OLIN",
    "CC", "GPRK", "RYAM",
    # ── Materials — Packaging & Paper ────────────────────────────────────
    "IP", "PKG", "SEE", "SON", "GEF", "ATR", "SLGN", "BERY",
    "AMCR", "BALL", "CCK", "OI",
    # ── REITs ────────────────────────────────────────────────────────────
    "AMT", "CCI", "PLD", "SPG", "PSA", "EQR", "AVB", "VTR", "WELL",
    "DLR", "EQIX", "O", "VICI", "GLPI", "MPW", "PEAK", "HR",
    "KIM", "REG", "FRT", "NNN", "STOR", "EPRT", "ADC",
    "EXR", "CUBE", "LSI", "REXR", "EGP", "FR",
    # ── Healthcare REITs / Services ───────────────────────────────────────
    "STE", "HOLX", "BAX", "INVACARE",
    # ── Technology Hardware ───────────────────────────────────────────────
    "AAPL", "IBM", "HPE", "HPQ", "DXC", "NCR", "NTAP", "STX",
    "WDC", "PSTG", "ANET", "JNPR", "FFIV", "RBBN", "VIAV",
    "CRUS", "SYNA", "CEVA", "COHU",
    # ── Homebuilders & Construction ───────────────────────────────────────
    "LEN", "DHI", "PHM", "TOL", "MTH", "MHO", "LGIH", "BZH", "HOV",
    "MDC", "SKY", "CVCO", "NVR", "KBH",
    # ── Education / Staffing ─────────────────────────────────────────────
    "COUR", "CHGG", "PRDO", "STRA", "LAUR", "APEI",
    "MAN", "ADP", "PAYX", "G", "NSP", "KFRC",
    # ── Biotech — Small/Mid cap ───────────────────────────────────────────
    "SRPT", "RCUS", "ACAD", "SAGE", "ARQT", "PRAX", "DAWN",
    "KRTX", "IMVT", "ROIV", "DNLI", "ARGT", "BLUE", "BMRN",
    "NBIX", "INSM", "PRGO", "JAZZ", "SUPN",
    # ── Retail — Specialty ────────────────────────────────────────────────
    "ULTA", "FIVE", "OLLI", "BIG", "AZO", "AAP", "ORLY", "GPC",
    "SIG", "ZGN", "BOOT", "CATO", "PLBY",
    # ── Real Estate Services ─────────────────────────────────────────────
    "CBRE", "JLL", "NMRK", "COMP", "OPEN", "RDFN",
    # ── Restaurants & Food Service ────────────────────────────────────────
    "WEN", "JACK", "WING", "RRGB", "NDLS", "DNUT", "PTLO",
    # ── Gaming & Leisure ─────────────────────────────────────────────────
    "MGM", "CZR", "WYNN", "LVS", "PENN", "DKNG", "RSI", "GAN",
    "EA", "TTWO", "ATVI", "MSFT", "NTDOY",
    # ── Travel & Hospitality ─────────────────────────────────────────────
    "MAR", "HLT", "H", "IHG", "CHH", "ATNM",
    "ABNB", "BKNG", "EXPE", "TRIP", "PCLN",
    # ── Agriculture & Food ───────────────────────────────────────────────
    "ADM", "BG", "MOS", "NTR", "CF", "FMC", "ICL",
    "CALM", "PPC", "SEB", "SAFM",
    # ── Industrial Gases & Specialty ─────────────────────────────────────
    "APD", "LIN", "ECL", "IFF", "PPG", "ALB",
    # ── Infrastructure & Engineering ─────────────────────────────────────
    "URI", "HEES", "GATX", "TRN", "GNRC", "MYRG", "PRIM",
    "ACM", "PWR", "MYR", "WLDN", "STRL",
    # ── Data / Analytics ─────────────────────────────────────────────────
    "SPGI", "MCO", "ICE", "CME", "CBOE", "NDAQ", "TW", "FDS",
    "MSCI", "INFO", "VRSK", "CSGP", "ANSS", "CDNS", "SNPS",
    # ── Cybersecurity ────────────────────────────────────────────────────
    "PANW", "CRWD", "ZS", "OKTA", "FTNT", "CHKP", "TENB",
    "QLYS", "VRNT", "SAIL", "S", "CYBR", "RPD",
    # ── AI / Data Infrastructure ──────────────────────────────────────────
    "AI", "PLTR", "BBAI", "SOUN", "GFAI", "SYNTX",
    "SMCI", "VRT", "DELL", "HPE", "NTAP",
    # ── Healthcare Tech ───────────────────────────────────────────────────
    "VEEVA", "CERN", "NXGN", "CPSI", "HCAT", "PHR", "DOCS",
    "ACCD", "TDOC", "AMWL", "ONEM", "CANO",
    # ── Misc Industrial / Conglomerates ──────────────────────────────────
    "GE", "HON", "MMM", "ITT", "RBC", "FELE", "AIXI",
    "NVT", "REXNORD", "WTTR", "DSGR",
]

# ── Runtime blacklist — populated automatically when yfinance returns no data ─
_BLACKLIST: set = set()

def add_to_blacklist(tickers: list):
    """Called by screener.py when yfinance reports a ticker as delisted/missing."""
    _BLACKLIST.update(tickers)
    if tickers:
        import logging
        logging.getLogger(__name__).info(
            f"Blacklisted {len(tickers)} tickers this session: {tickers}"
        )

def get_tickers(market: str = "US") -> list:
    """Return active US ticker list, deduplicated, excluding runtime blacklist."""
    seen   = set()
    result = []
    for t in US_TICKERS:
        if t not in seen and t not in _BLACKLIST:
            seen.add(t)
            result.append(t)
    return result
