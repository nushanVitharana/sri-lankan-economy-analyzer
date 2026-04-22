from src.ingestion.world_bank import WorldBankClient
from src.ingestion.config import WORLD_BANK_INDICATORS, COUNTRIES
from src.processing.pipeline import build_master_dataset

# Step 1: fetch data
client = WorldBankClient()

df_raw = client.fetch_multiple(
    country=COUNTRIES["sri_lanka"],
    indicators=WORLD_BANK_INDICATORS
)

# Step 2: split into series
series_dict = {
    col: df_raw[[col]] for col in df_raw.columns
}

# Step 3: build master dataset
master = build_master_dataset(series_dict)

print(master.head())