from src.ingestion.world_bank import WorldBankClient
from src.ingestion.config import WORLD_BANK_INDICATORS, COUNTRIES
from src.processing.pipeline import build_master_dataset
from src.models.cross_correlation import compute_cross_correlation
from src.models.lag_detector import find_best_lag, interpret_lag

# Load and process data
client = WorldBankClient()
df_raw = client.fetch_multiple(
    country=COUNTRIES["sri_lanka"],
    indicators=WORLD_BANK_INDICATORS
)

series_dict = {col: df_raw[[col]] for col in df_raw.columns}
df = build_master_dataset(series_dict)

# Test cross-correlation between reserves and inflation
corr = compute_cross_correlation(
    df["reserves"],
    df["inflation"]
)

best = find_best_lag(corr)

print("Cross-correlation analysis:")
print(f"Best lag result: {best}")
print(interpret_lag(best, "reserves", "inflation"))
