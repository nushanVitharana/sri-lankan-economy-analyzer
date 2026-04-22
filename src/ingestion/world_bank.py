import wbgapi as wb
import pandas as pd
import logging

logger = logging.getLogger(__name__)

class WorldBankClient:
    def __init__(self, start_year=2000, end_year=2025):
        self.start_year = start_year
        self.end_year = end_year
        self.failed_indicators = []

    def fetch_indicator(self, country: str, indicator: str, indicator_name: str = None) -> pd.DataFrame:
        """
        Fetch a single indicator for a country

        Args:
            country: Country code (e.g., 'LKA')
            indicator: World Bank indicator code (e.g., 'FI.RES.TOTL.CD')
            indicator_name: Human-readable name (defaults to indicator code)

        Returns:
            DataFrame with indicator values
        """
        try:
            df = wb.data.DataFrame(
                indicator,
                country,
                time=range(self.start_year, self.end_year)
            )

            df = df.T
            df.index = pd.to_datetime(df.index.str.replace('YR', ''), format="%Y")

            # Use human-readable name if provided
            col_name = indicator_name if indicator_name else indicator
            df.columns = [col_name]

            logger.info(f"✓ Successfully fetched {col_name} ({indicator})")
            return df

        except Exception as e:
            logger.warning(f"✗ Failed to fetch {indicator}: {str(e)}")
            self.failed_indicators.append(indicator)
            return None

    def fetch_multiple(self, country: str, indicators: dict) -> pd.DataFrame:
        """
        Fetch multiple indicators for a country

        Args:
            country: Country code (e.g., 'LKA')
            indicators: Dictionary of {indicator_name: indicator_code}

        Returns:
            DataFrame with all successfully fetched indicators
        """
        frames = []

        for name, code in indicators.items():
            df = self.fetch_indicator(country, code, name)
            if df is not None:
                frames.append(df)

        if not frames:
            raise ValueError(f"No indicators could be fetched for country {country}")

        result = pd.concat(frames, axis=1)
        result = result.sort_index()

        logger.info(f"✓ Fetched {len(frames)}/{len(indicators)} indicators successfully")

        return result

    def fetch_multiple_countries(self, countries: list, indicators: dict) -> dict:
        """
        Fetch same indicators for multiple countries

        Args:
            countries: List of country codes
            indicators: Dictionary of indicators

        Returns:
            Dictionary of {country_code: DataFrame}
        """
        results = {}

        for country in countries:
            try:
                results[country] = self.fetch_multiple(country, indicators)
                logger.info(f"✓ Successfully fetched data for {country}")
            except Exception as e:
                logger.error(f"✗ Failed to fetch data for {country}: {str(e)}")
                results[country] = None

        return results
