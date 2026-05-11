import pandas as pd

VALID_STATES = [
    "AC", "AL", "AP", "AM", "BA",
    "CE", "Distrito Federal", "Espírito Santo", "GO", "MA",
    "MT", "MS", "MG", "PA", "PB",
    "PR", "PE", "PI", "RJ", "RN",
    "RS", "RO", "RR", "SC", "SP",
    "SE", "TO"
]

STATE_MAPPING = {
    "SAOPAULO": "SP",
    "S": "SP",
    "sp": "SP",
    "rj": "RJ",
    "mg": "MG"
}


def self_heal(df):

    df = df.copy()

    # =========================================
    # REMOVE DUPLICATES
    # =========================================

    if "customer_id" in df.columns:

        df = df.drop_duplicates(
            subset=["customer_id"]
        )

    elif "order_id" in df.columns:

        df = df.drop_duplicates(
            subset=["order_id"]
        )

    elif "product_id" in df.columns:

        df = df.drop_duplicates(
            subset=["product_id"]
        )

    # =========================================
    # HANDLE NULL VALUES
    # =========================================

    for column in df.columns:

        if df[column].dtype == "object":

            df[column] = df[column].fillna("UNKNOWN")

        else:

            df[column] = df[column].fillna(0)

    # =========================================
    # FIX CUSTOMER STATE VALUES
    # =========================================

    if "customer_state" in df.columns:

        df["customer_state"] = (
            df["customer_state"]
            .astype(str)
            .str.upper()
        )

        df["customer_state"] = (
            df["customer_state"]
            .replace(STATE_MAPPING)
        )

        df.loc[
            ~df["customer_state"].isin(VALID_STATES),
            "customer_state"
        ] = "UNKNOWN"

    # =========================================
    # STANDARDIZE CITY NAMES
    # =========================================

    if "customer_city" in df.columns:

        df["customer_city"] = (
            df["customer_city"]
            .astype(str)
            .str.lower()
            .str.strip()
        )

    # =========================================
    # CLEAN PAYMENT VALUES
    # =========================================

    if "payment_value" in df.columns:

        df["payment_value"] = (
            pd.to_numeric(
                df["payment_value"],
                errors="coerce"
            )
            .fillna(0)
        )

    return df