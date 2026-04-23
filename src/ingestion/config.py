"""
Configuration for all data sources
"""

# ==========================================
# WORLD BANK INDICATORS
# ==========================================
WORLD_BANK_INDICATORS = {
    # External and balance-of-payments
    "reserves": "FI.RES.TOTL.CD",
    "current_account_pct_gdp": "BN.CAB.XOKA.GD.ZS",
    "exports_usd": "NE.EXP.GNFS.CD",
    "imports_usd": "NE.IMP.GNFS.CD",
    "exports_pct_gdp": "NE.EXP.GNFS.CD.ZS",
    "imports_pct_gdp": "NE.IMP.GNFS.CD.ZS",
    "trade_openness": "NE.TRD.GNFS.ZS",
    "fdi_inflows": "BX.KLT.DINV.CD.WD",
    "remittances_pct_gdp": "BX.TRF.PWKR.DT.GD.ZS",
    "tourism_receipts_pct_exports": "ST.INT.RCPT.XP.ZS",

    # Debt and fiscal
    "debt": "GC.DOD.TOTL.GD.ZS",
    "external_debt": "DT.DOD.DECT.GN.ZS",
    "debt_service_pct_exports": "DT.TDS.DECT.EX.ZS",
    "short_term_debt_pct_reserves": "DT.DOD.DSTC.IR.ZS",
    "revenue_pct_gdp": "GC.REV.XGRT.GD.ZS",
    "expense_pct_gdp": "GC.XPN.TOTL.GD.ZS",

    # Growth and social
    "gdp_growth": "NY.GDP.MKTP.KD.ZG",
    "gdp_per_capita": "NY.GDP.PCAP.CD",
    "unemployment_rate": "SL.UEM.TOTL.ZS",
    "poverty_headcount": "SI.POV.NAHC",

    # Monetary and inflation
    "inflation": "FP.CPI.TOTL.ZG",
    "food_inflation_proxy": "FP.CPI.FOOD.ZG",
    "real_interest_rate": "FR.INR.RINR",
    "broad_money_pct_gdp": "FM.LBL.BMNY.GD.ZS",
}

# ==========================================
# ALTERNATIVE SOURCES
# ==========================================
ALTERNATIVE_INDICATORS = {
    "trade_balance_proxy": "NE.RSB.GNFS.CD",
    "tourism_receipts": "ST.INT.RCPT.CD",
    "remittances_inflows": "BX.TRF.PWKR.CD.DT",
    "net_oda": "DT.ODA.ALLD.CD",
    "portfolio_inflows": "CM.MKT.PORT.CD.WD",
}

# ==========================================
# SYNTHETIC / CBSL-LIKE INDICATORS
# ==========================================
CBSL_INDICATORS = {
    "exchange_rate_usd": "Exchange Rate USD/LKR",
    "money_supply_m2": "Money Supply M2 (LKR Bn)",
    "credit_private_sector": "Credit to Private Sector (LKR Bn)",
    "policy_rate": "Policy Rate (%)",
    "base_lending_rate": "Base Lending Rate (%)",
    "treasury_bill_rate": "Treasury Bill Rate (%)",
    "bank_npl_ratio": "Bank NPL Ratio (%)",
    "stock_index": "All Share Index (ASPI)",
}

# ==========================================
# INDICATOR METADATA
# ==========================================
INDICATOR_METADATA = {
    "reserves": {"label": "FX Reserves", "unit": "USD", "category": "External"},
    "current_account_pct_gdp": {"label": "Current Account", "unit": "% GDP", "category": "External"},
    "exports_usd": {"label": "Exports", "unit": "USD", "category": "External"},
    "imports_usd": {"label": "Imports", "unit": "USD", "category": "External"},
    "exports_pct_gdp": {"label": "Exports Share", "unit": "% GDP", "category": "External"},
    "imports_pct_gdp": {"label": "Imports Share", "unit": "% GDP", "category": "External"},
    "trade_openness": {"label": "Trade Openness", "unit": "% GDP", "category": "External"},
    "fdi_inflows": {"label": "FDI Inflows", "unit": "USD", "category": "Capital Flows"},
    "remittances_pct_gdp": {"label": "Remittances", "unit": "% GDP", "category": "Capital Flows"},
    "tourism_receipts_pct_exports": {"label": "Tourism Receipts", "unit": "% Exports", "category": "Capital Flows"},
    "debt": {"label": "Government Debt", "unit": "% GDP", "category": "Fiscal"},
    "external_debt": {"label": "External Debt", "unit": "% GNI", "category": "Fiscal"},
    "debt_service_pct_exports": {"label": "Debt Service", "unit": "% Exports", "category": "Fiscal"},
    "short_term_debt_pct_reserves": {"label": "Short-term Debt / Reserves", "unit": "%", "category": "Fiscal"},
    "revenue_pct_gdp": {"label": "Revenue", "unit": "% GDP", "category": "Fiscal"},
    "expense_pct_gdp": {"label": "Expenditure", "unit": "% GDP", "category": "Fiscal"},
    "gdp_growth": {"label": "GDP Growth", "unit": "%", "category": "Real Economy"},
    "gdp_per_capita": {"label": "GDP Per Capita", "unit": "USD", "category": "Real Economy"},
    "unemployment_rate": {"label": "Unemployment", "unit": "%", "category": "Real Economy"},
    "poverty_headcount": {"label": "Poverty Headcount", "unit": "%", "category": "Households"},
    "inflation": {"label": "Inflation", "unit": "%", "category": "Prices"},
    "food_inflation_proxy": {"label": "Food Inflation", "unit": "%", "category": "Prices"},
    "real_interest_rate": {"label": "Real Interest Rate", "unit": "%", "category": "Monetary"},
    "broad_money_pct_gdp": {"label": "Broad Money", "unit": "% GDP", "category": "Monetary"},
    "tourism_receipts": {"label": "Tourism Receipts", "unit": "USD", "category": "Capital Flows"},
    "remittances_inflows": {"label": "Remittances Inflows", "unit": "USD", "category": "Capital Flows"},
    "net_oda": {"label": "Net ODA", "unit": "USD", "category": "Capital Flows"},
    "portfolio_inflows": {"label": "Portfolio Inflows", "unit": "USD", "category": "Capital Flows"},
    "exchange_rate_usd": {"label": "LKR per USD", "unit": "LKR", "category": "Monetary"},
    "money_supply_m2": {"label": "Money Supply M2", "unit": "LKR bn", "category": "Monetary"},
    "credit_private_sector": {"label": "Private Credit", "unit": "LKR bn", "category": "Monetary"},
    "policy_rate": {"label": "Policy Rate", "unit": "%", "category": "Monetary"},
    "base_lending_rate": {"label": "Base Lending Rate", "unit": "%", "category": "Monetary"},
    "treasury_bill_rate": {"label": "Treasury Bill Rate", "unit": "%", "category": "Monetary"},
    "bank_npl_ratio": {"label": "Bank NPL Ratio", "unit": "%", "category": "Banking"},
    "stock_index": {"label": "All Share Index", "unit": "index", "category": "Market"},
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

COMPARATOR_COUNTRIES = ["PAK", "BGD", "IND", "EGY", "GHA"]
