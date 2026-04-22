from src.ingestion.world_bank import WorldBankClient
from src.ingestion.config import WORLD_BANK_INDICATORS, COUNTRIES

client = WorldBankClient()

df = client.fetch_multiple(
    country=COUNTRIES["sri_lanka"],
    indicators=WORLD_BANK_INDICATORS
)

print(df.head())