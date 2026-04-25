import pandas as pd

# Load the Titanic data
df = pd.read_csv("C:/Users/daveg/OneDrive/Desktop/titanic_cleaned.csv")

# Basic exploration
print("Shape:", df.shape)
print()
print("Columns:", df.columns.tolist())
print()
print(df.head())

# Info and missing values
print(df.info())
print()
print("Missingvalues:")
print(df.isnull().sum())

# FILTTERING
first_class = df[df["Pclass"] == 1]
print("First class passengers:", len(first_class))

survivors = df[(df["Pclass"] == 1) & (df["Survived"] == 1)]
print("First class survivaors:", len(survivors))

# SORTING
top_fares = df.sort_values("Fare", ascending=False).head(5)
print(top_fares[["Name", "Pclass", "Fare"]])

# GROUPBY
survival_by_class = df.groupby("Pclass")["Survived"].mean().round(2)
print("Survival rate by class:")
print(survival_by_class)
print()

# NAME AGGREGATIONS
stats = df.groupby("Pclass").agg(
    passengers=("PassengerId", "count"),
    ave_age=("Age", "mean"),
    avg_fare=("Fare", "mean")
).round(2)
print("Stats by class:")
print(stats)

#FILLNA
print("Cabin nulls before:", df["Cabin"].isnull().sum())

df["Cabin"] = df["Cabin"].fillna("Unknown")

print("Cabin nulls after:", df["Cabin"].isnull().sum())

# APPLY WITH LAMBDA
df["fare_grade"] = df["Fare"].apply(lambda x: "High" if x > 50 else "Low")
print(df["fare_grade"].value_counts())

# SORT BY MULTIPLE COLUMNS
sorted_df = df.sort_values(["Pclass", "Fare"], ascending=[True, False])
print(sorted_df[["Name", "Pclass", "Fare"]].head(10))

# PD.CUT - BINNING
df["age_group"] = pd.cut(df["Age"],
                         bins=[0, 12, 18, 35, 60, 100],
                         labels=["Child", "Teen", "Young Adult", "Adult", "Senior"])
                                 
print(df["age_group"].value_counts())

# ASTYPE - DATA TYPE CONVERSION
print("Survived dtype before:", df["Survived"].dtype)

df["Survived"] = df["Survived"].astype(str)
print("Survived dtype after:", df["Survived"].dtype)
print(df["Survived"].head())
