import pandas as pd

def check_missing(df: pd.DataFrame):
    print("Missing values per column:")
    print(df.isna().sum())


def check_date_range(df: pd.DataFrame):
    print("Start:", df.index.min())
    print("End:", df.index.max())


def check_frequency(df: pd.DataFrame):
    inferred = pd.infer_freq(df.index)
    print("Detected frequency:", inferred)


def basic_summary(df: pd.DataFrame):
    print(df.describe())