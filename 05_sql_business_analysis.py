import duckdb
import pandas as pd

# using duckdb so we can write real SQL against the parquet files
# directly, no need to load everything into pandas first
con = duckdb.connect()

# revenue = units_sold * sell_price. only makes sense for rows that
# actually have a price (item was stocked), so this naturally
# excludes the item_not_stocked rows
con.execute("""
    CREATE VIEW sales AS
    SELECT *,
        units_sold * sell_price AS revenue
    FROM read_parquet('outputs/model_data.parquet')
    WHERE sell_price IS NOT NULL
""")

print("total rows in sales view:")
print(con.execute("SELECT COUNT(*) FROM sales").fetchdf())

# revenue and units by category
print("\nrevenue and units by category:")
print(con.execute("""
    SELECT cat_id,
        SUM(units_sold) AS total_units,
        ROUND(SUM(revenue), 2) AS total_revenue
    FROM sales
    GROUP BY cat_id
    ORDER BY total_revenue DESC
""").fetchdf())

# revenue by state
print("\nrevenue by state:")
print(con.execute("""
    SELECT state_id,
        SUM(units_sold) AS total_units,
        ROUND(SUM(revenue), 2) AS total_revenue
    FROM sales
    GROUP BY state_id
    ORDER BY total_revenue DESC
""").fetchdf())

# revenue by individual store, to see if a few stores dominate
print("\nrevenue by store:")
print(con.execute("""
    SELECT store_id,
        SUM(units_sold) AS total_units,
        ROUND(SUM(revenue), 2) AS total_revenue
    FROM sales
    GROUP BY store_id
    ORDER BY total_revenue DESC
""").fetchdf())

# top 10 items by revenue - useful to know which SKUs actually
# matter most for the business
print("\ntop 10 items by revenue:")
print(con.execute("""
    SELECT item_id, dept_id, cat_id,
        SUM(units_sold) AS total_units,
        ROUND(SUM(revenue), 2) AS total_revenue
    FROM sales
    GROUP BY item_id, dept_id, cat_id
    ORDER BY total_revenue DESC
    LIMIT 10
""").fetchdf())

# demand concentration - what share of total revenue comes from the
# top 20% of items? this is basically checking for a pareto pattern,
# common in retail and directly relevant to inventory prioritization
item_revenue = con.execute("""
    SELECT item_id, SUM(revenue) AS item_revenue
    FROM sales
    GROUP BY item_id
    ORDER BY item_revenue DESC
""").fetchdf()

total_revenue = item_revenue["item_revenue"].sum()
top_20_pct_count = int(len(item_revenue) * 0.2)
top_20_pct_revenue = item_revenue.head(top_20_pct_count)["item_revenue"].sum()

print(f"\ntop 20% of items ({top_20_pct_count} of {len(item_revenue)}) account for "
      f"{top_20_pct_revenue / total_revenue * 100:.1f}% of total revenue")

# average price and average units sold on SNAP vs non-SNAP days,
# by category - checking whether SNAP boosts some categories more
# than others
print("\nSNAP effect by category:")
print(con.execute("""
    SELECT cat_id,
        ROUND(AVG(CASE WHEN snap_today = 1 THEN units_sold END), 3) AS avg_units_snap,
        ROUND(AVG(CASE WHEN snap_today = 0 THEN units_sold END), 3) AS avg_units_non_snap
    FROM sales
    GROUP BY cat_id
    ORDER BY cat_id
""").fetchdf())

con.close()