import pandas as pd

def profile_data(df):

    profile = {}

    # Total rows and columns
    profile["total_rows"] = df.shape[0]
    profile["total_columns"] = df.shape[1]

    # Duplicate rows
    profile["duplicate_rows"] = int(df.duplicated().sum())

    # Column analysis
    profile["columns"] = {}

    for col in df.columns:

        profile["columns"][col] = {

            "datatype": str(df[col].dtype),

            "null_count": int(df[col].isnull().sum()),

            "unique_values": int(df[col].nunique()),

            "sample_values": (
                df[col]
                .dropna()
                .astype(str)
                .head(5)
                .tolist()
            )
        }

    return profile