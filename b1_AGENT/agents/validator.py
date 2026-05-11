VALID_STATES = [
    "AC", "AL", "AP", "AM", "BA",
    "CE", "DF", "ES", "GO", "MA",
    "MT", "MS", "MG", "PA", "PB",
    "PR", "PE", "PI", "RJ", "RN",
    "RS", "RO", "RR", "SC", "SP",
    "SE", "TO"
]

def validate_data(df):

    errors = []

    # =========================================
    # DUPLICATE CHECKS
    # =========================================

    if "customer_id" in df.columns:

        duplicate_ids = df[df.duplicated("customer_id")]

        for idx in duplicate_ids.index:

            errors.append({
                "row": idx,
                "column": "customer_id",
                "issue": "Duplicate customer_id"
            })

    if "order_id" in df.columns:

        duplicate_orders = df[
            df.duplicated("order_id")
        ]

        for idx in duplicate_orders.index:

            errors.append(
                {
                    "row": idx,
                    "column": "order_id",
                    "issue": "Duplicate order_id"
                }
            )

    # =========================================
    # NULL CHECKS
    # =========================================

    for column in df.columns:

        null_rows = df[
            df[column].isnull()
        ]

        for idx in null_rows.index:

            errors.append(
                {
                    "row": idx,
                    "column": column,
                    "issue": "Null value"
                }
            )

    # =========================================
    # STATE VALIDATION
    # =========================================

    if "customer_state" in df.columns:

        invalid_states = df[
            ~df["customer_state"].isin(VALID_STATES)
        ]

        for idx in invalid_states.index:

            errors.append({
                "row": idx,
                "column": "customer_state",
                "issue": "Invalid state code"
            })

    return errors