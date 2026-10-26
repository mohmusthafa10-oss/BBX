import pandas as pd
import numpy as np

# 1. Load data
df = pd.read_csv("messy_sales.csv")

# 2. Standardise missing values
df = df.replace(["unknown", "not available", ""], pd.NA)
df["age_was_missing"] = df["age"].isna()

# 3. Missingness profile
profile = pd.DataFrame({
    "count": df.isna().sum(),
    "percent": df.isna().mean() * 100
})
print("Missingness profile:\n", profile)

# 4. Find duplicates
print("Exact duplicates:", df.duplicated().sum())
print("Repeated order IDs:",
      df.duplicated(subset="order_id", keep=False).sum())

df = df.drop_duplicates().copy()

# 5. Fix data types and inspect failures
df["age"] = pd.to_numeric(df["age"], errors="coerce")

amount_text = df["amount"].astype("string").str.replace(
    r"[₹,\s]", "", regex=True
)
df["amount"] = pd.to_numeric(amount_text, errors="coerce")

df["order_date"] = pd.to_datetime(
    df["order_date"], errors="coerce"
)

print("Invalid/missing ages:\n", df.loc[df["age"].isna(), "age"])
print("Missing amounts:", df["amount"].isna().sum())
print("Missing dates:", df["order_date"].isna().sum())

# 6. Normalise city names
before = df["city"].nunique()
df["city"] = df["city"].str.strip().str.title()
after = df["city"].nunique()
print("Distinct cities before/after:", before, after)

# 7. Detect outliers using IQR and z-score
for col in ["age", "amount"]:
    s = df[col]
    q1, q3 = s.quantile([0.25, 0.75])
    iqr = q3 - q1
    iqr_outliers = (s < q1 - 1.5 * iqr) | (s > q3 + 1.5 * iqr)

    z = (s - s.mean()) / s.std()
    z_outliers = z.abs() > 3

    print(f"\n{col} outliers:")
    print(df.loc[iqr_outliers | z_outliers, ["order_id", col]])
    print("IQR only:", (iqr_outliers & ~z_outliers).sum())
    print("Z-score only:", (~iqr_outliers & z_outliers).sum())

# 8. Handle impossible age and missing values
df.loc[df["age"] > 120, "age"] = np.nan

df["age"] = df["age"].fillna(df["age"].median())
df["amount"] = df["amount"].fillna(df["amount"].median())

# 9. Pivot table
pivot = df.pivot_table(
    index="city", columns="category",
    values="amount", aggfunc="sum"
)
print("\nSales summary:\n", pivot)

# 10. Melt to long format
long_df = df.melt(
    id_vars=["order_id", "city", "category"],
    value_vars=["age", "amount"],
    var_name="metric", value_name="value"
)

# Save results
df.to_csv("cleaned_sales.csv", index=False)
long_df.to_csv("sales_long.csv", index=False)

print("\nFinal shape:", df.shape)
print("Cleaning completed.")
