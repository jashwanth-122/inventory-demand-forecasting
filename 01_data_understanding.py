import pandas as pd

# Quick look at the three M5 files before we do anything real with them.
# calendar tells us the actual date for each d_1, d_2... column in sales.
# sell_prices has weekly prices per store/item. sales is wide format,
# one row per item-store, one column per day.

calendar = pd.read_csv("data/calendar.csv")
prices = pd.read_csv("data/sell_prices.csv")
sales = pd.read_csv("data/sales_train_validation.csv")

print("calendar shape:", calendar.shape)
print("prices shape:", prices.shape)
print("sales shape:", sales.shape)

print("\ncalendar columns:", list(calendar.columns))
print("prices columns:", list(prices.columns))

id_columns = ["id", "item_id", "dept_id", "cat_id", "store_id", "state_id"]
day_columns = [col for col in sales.columns if col.startswith("d_")]

print("\nday columns:", len(day_columns), "from", day_columns[0], "to", day_columns[-1])

print("\ncalendar head:")
print(calendar.head())

print("\nprices head:")
print(prices.head())

print("\nsales head:")
print(sales[id_columns + day_columns[:5]].head())

# how big is this thing, hierarchy-wise
print("\nstates:", sales["state_id"].nunique())
print("stores:", sales["store_id"].nunique())
print("categories:", sales["cat_id"].nunique())
print("departments:", sales["dept_id"].nunique())
print("items:", sales["item_id"].nunique())
print("rows (item-store combos):", sales.shape[0])

# missing values check - calendar has some (event columns are mostly
# blank since most days aren't holidays), sales/prices should be clean
print("\ncalendar nulls:")
print(calendar.isnull().sum()[calendar.isnull().sum() > 0])

print("\nprices nulls:", prices.isnull().sum().sum())
print("sales id column nulls:", sales[id_columns].isnull().sum().sum())
print("sales day column nulls:", sales[day_columns].isnull().sum().sum())

# sales is wide format (1913 day columns) which is useless for time
# series work directly. need to melt it to long format: one row per
# item, store, day. testing that on a small sample first before doing
# the full ~30M row melt in the next script.
sample = sales.head(100)

sample_long = sample.melt(
    id_vars=id_columns,
    value_vars=day_columns,
    var_name="d",
    value_name="units_sold"
)

print("\nmelted sample shape:", sample_long.shape)

# join calendar to get real dates + wm_yr_wk (needed to join prices,
# since prices are keyed by week not by exact date)
sample_long = sample_long.merge(
    calendar[["d", "date", "wm_yr_wk", "event_name_1", "event_type_1"]],
    on="d",
    how="left"
)

sample_long = sample_long.merge(
    prices,
    on=["store_id", "item_id", "wm_yr_wk"],
    how="left"
)

print("\nafter joining calendar + prices:")
print(sample_long.head())

# this sample is all d_1 (jan 2011), which is before the prices file's
# earliest week (11325), so basically everything will show missing
# price here - that's expected for this sample, not a bug
print("\nmissing prices in sample:", sample_long["sell_price"].isnull().sum())