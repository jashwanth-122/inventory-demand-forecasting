# -------------------------------------------------------------
# 02 - Full Melt and Exploratory Data Analysis
# Supply Chain Demand Forecasting & Inventory Optimization
# M5 Forecasting (Walmart) dataset
# -------------------------------------------------------------
# Goal of this script: melt the FULL sales file into long format,
# join in calendar and price data, then explore demand patterns
# by category, by SNAP days, by events, and by item sparsity.
#
# This will take a little while to run since we are now working
# with the full ~30,490 x 1913 grid, which becomes about 58
# million rows once melted.

import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------------------------------------
# Step 1: Load the raw files
# -------------------------------------------------------------

calendar = pd.read_csv("data/calendar.csv")
prices = pd.read_csv("data/sell_prices.csv")
sales = pd.read_csv("data/sales_train_validation.csv")

id_columns = ["id", "item_id", "dept_id", "cat_id", "store_id", "state_id"]
day_columns = [col for col in sales.columns if col.startswith("d_")]

# -------------------------------------------------------------
# Step 2: Reduce memory before melting
# -------------------------------------------------------------
# The day columns are stored as int64 by default, which wastes
# memory. Sales values are small non-negative integers, so we
# can safely downcast to a smaller integer type before melting.
# This matters a lot once we have 58 million rows.

sales[day_columns] = sales[day_columns].astype("int16")

# -------------------------------------------------------------
# Step 3: Melt the full sales file into long format
# -------------------------------------------------------------

sales_long = sales.melt(
    id_vars=id_columns,
    value_vars=day_columns,
    var_name="d",
    value_name="units_sold"
)

print("full melted shape:", sales_long.shape)

# -------------------------------------------------------------
# Step 4: Join with calendar to get real dates and event flags
# -------------------------------------------------------------

calendar_columns_needed = [
    "d", "date", "wm_yr_wk", "weekday", "wday", "month", "year",
    "event_name_1", "event_type_1", "snap_CA", "snap_TX", "snap_WI"
]

sales_long = sales_long.merge(
    calendar[calendar_columns_needed],
    on="d",
    how="left"
)

sales_long["date"] = pd.to_datetime(sales_long["date"])

# -------------------------------------------------------------
# Step 5: Join with prices
# -------------------------------------------------------------

sales_long = sales_long.merge(
    prices,
    on=["store_id", "item_id", "wm_yr_wk"],
    how="left"
)

print("after all joins, shape:", sales_long.shape)
print("missing prices after full join:", sales_long["sell_price"].isnull().sum())

# Note: rows with a missing price mean that item was not being
# sold/stocked at that store during that week. We keep these
# rows for now since they still carry a units_sold value of 0
# in most cases, but we will need a clear rule for how to treat
# them before modeling. That decision happens in the next script.

# -------------------------------------------------------------
# Step 6: Overall demand trend over time
# -------------------------------------------------------------
# This gives a first look at whether total demand is trending
# up, down, or staying flat over the ~5 years of history.

daily_total = sales_long.groupby("date")["units_sold"].sum()

plt.figure(figsize=(14, 5))
daily_total.plot()
plt.title("Total Daily Units Sold Across All Stores")
plt.xlabel("Date")
plt.ylabel("Units Sold")
plt.tight_layout()
plt.savefig("outputs/01_daily_total_demand.png")
plt.close()

print("saved: outputs/01_daily_total_demand.png")

# -------------------------------------------------------------
# Step 7: Demand by category
# -------------------------------------------------------------
# This shows whether FOODS, HOBBIES, and HOUSEHOLD behave
# differently in scale and seasonality.

category_daily = sales_long.groupby(["date", "cat_id"])["units_sold"].sum().unstack()

plt.figure(figsize=(14, 5))
category_daily.plot(ax=plt.gca())
plt.title("Daily Units Sold by Category")
plt.xlabel("Date")
plt.ylabel("Units Sold")
plt.tight_layout()
plt.savefig("outputs/02_demand_by_category.png")
plt.close()

print("saved: outputs/02_demand_by_category.png")

# -------------------------------------------------------------
# Step 8: Effect of SNAP days on demand
# -------------------------------------------------------------
# SNAP (Supplemental Nutrition Assistance Program) days are when
# SNAP benefits can be used, which tends to boost sales. Each
# state has its own snap flag column, so we check each state's
# stores against that state's snap column.

snap_effect = []

for state, snap_col in [("CA", "snap_CA"), ("TX", "snap_TX"), ("WI", "snap_WI")]:
    state_data = sales_long[sales_long["state_id"] == state]
    avg_on_snap = state_data.loc[state_data[snap_col] == 1, "units_sold"].mean()
    avg_off_snap = state_data.loc[state_data[snap_col] == 0, "units_sold"].mean()
    snap_effect.append({
        "state": state,
        "avg_units_snap_day": avg_on_snap,
        "avg_units_non_snap_day": avg_off_snap
    })

snap_effect_df = pd.DataFrame(snap_effect)
print("\nSNAP day effect on average units sold per row:")
print(snap_effect_df)

# -------------------------------------------------------------
# Step 9: Effect of named events on demand
# -------------------------------------------------------------
# This checks whether days with a named event (Christmas,
# Thanksgiving, Super Bowl, etc.) show higher average demand
# than ordinary days.

avg_on_event = sales_long.loc[sales_long["event_name_1"].notnull(), "units_sold"].mean()
avg_no_event = sales_long.loc[sales_long["event_name_1"].isnull(), "units_sold"].mean()

print("\naverage units sold on event days:", avg_on_event)
print("average units sold on non-event days:", avg_no_event)

# -------------------------------------------------------------
# Step 10: Identify intermittent (sparse) demand items
# -------------------------------------------------------------
# Some items sell almost every day, others sell rarely. This
# matters a lot for modeling, since sparse items are much harder
# to forecast with standard methods. We measure sparsity as the
# percentage of days with zero sales, per item-store series.

zero_pct_by_series = sales_long.groupby("id")["units_sold"].apply(
    lambda x: (x == 0).mean()
)

print("\nsparsity (percent of zero-sales days) summary across all series:")
print(zero_pct_by_series.describe())

high_sparsity_count = (zero_pct_by_series > 0.5).sum()
print("\nnumber of series with more than 50 percent zero-sales days:", high_sparsity_count)
print("out of total series:", zero_pct_by_series.shape[0])

# -------------------------------------------------------------
# Step 11: Save the full long-format table for the next step
# -------------------------------------------------------------
# We save this so the next script (feature engineering) does not
# need to redo the melt and joins from scratch.

sales_long.to_parquet("outputs/sales_long.parquet", index=False)
print("\nsaved: outputs/sales_long.parquet")

# -------------------------------------------------------------
# What this script confirmed
# -------------------------------------------------------------
# 1. The full sales file melts and joins cleanly at scale.
# 2. We have an overall demand trend and a category-level trend
#    saved as charts to review.
# 3. SNAP days and event days both appear to shift average
#    demand, which we will turn into real features next.
# 4. A meaningful share of series are sparse (many zero-sales
#    days), which tells us we cannot treat every item the same
#    way when building features and choosing models later.
# 5. The full long-format, joined table is saved to
#    outputs/sales_long.parquet so we do not repeat this work.