"""
Configuration for all data sources
"""

# ==========================================
# WORLD BANK INDICATORS (12 indicators)
# ==========================================
WORLD_BANK_INDICATORS = {
    # Monetary & Financial
    "reserves": "FI.RES.TOTL.CD",  # Foreign exchange reserves (USD)
    "inflation": "FP.CPI.TOTL.ZG",  # Inflation rate (%)

    # Debt & Fiscal
    "debt": "GC.DOD.TOTL.GD.ZS",  # Central government debt (% of GDP)
    "external_debt": "DT.DOD.DECT.GD.ZS",  # External debt (% of GNI)

    # Growth & Economic
    "gdp_growth": "NY.GDP.MKTP.KD.ZG",  # GDP growth (% annual)
    "gdp_per_capita": "NY.GDP.PCAP.CD",  # GDP per capita (USD)

    # Trade & Investment
    "trade_openness": "NE.TRD.GNRL.CD.ZS",  # Trade (% of GDP)
    "exports_pct_gdp": "NE.EXP.GNFS.CD.ZS",  # Exports (% of GDP)
    "imports_pct_gdp": "NE.IMP.GNFS.CD.ZS",  # Imports (% of GDP)
    "fdi_inflows": "BX.KLT.DINV.CD.WD",  # FDI inflows (USD)

    # Unemployment & Labor
    "unemployment_rate": "SL.UEM.TOTL.ZS",  # Unemployment (% of labor force)

    # Interest Rates
    "real_interest_rate": "FR.INR.RINR",  # Real interest rate (%)
}

# ==========================================
# ALTERNATIVE SOURCES (ADB, IMF proxies via WB)
# ==========================================
ALTERNATIVE_INDICATORS = {
    # Current account (as proxy from trade balance)
    "trade_balance": "NE.EXP.GNFS.CD",  # Exports (USD)

    # Tourism receipts
    "tourism_receipts": "ST.INT.RCPT.CD",  # International tourism receipts (USD)

    # Personal remittances
    "remittances_inflows": "BX.TRF.PWKR.CD.DT",  # Personal remittances received (USD)
}

# ==========================================
# MOCK CBSL INDICATORS
# (In production, these would connect to real CBSL APIs)
# ==========================================
CBSL_INDICATORS = {
    "exchange_rate_usd": "Exchange Rate USD/LKR",  # Mock data
    "money_supply_m2": "Money Supply M2 (LKR Bn)",  # Mock data
    "credit_private_sector": "Credit to Private Sector (LKR Bn)",  # Mock data
    "base_lending_rate": "Base Lending Rate (%)",  # Mock data
    "stock_index": "All Share Index (ASPI)",  # Mock data
}

# ==========================================
# COUNTRIES & COMPARATORS
# ==========================================
COUNTRIES = {
    "sri_lanka": "LKA",
    "india": "IND",
    "bangladesh": "BGD",
    "vietnam": "VNM",
    "turkey": "TUR",
    "argentina": "ARG",
    "ecuador": "ECU",
    "pakistan": "PAK",
    "indonesia": "IDN",
}