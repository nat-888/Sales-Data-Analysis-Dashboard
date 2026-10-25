import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#--------------------------------

try:
    df = pd.read_csv("sales.csv")
except FileNotFoundError:
    print("orders.csvが見つかりません")

print(df.head())
print(df.info())
print(df.columns)
print("重複行数:", df.duplicated().sum())
print("欠損数:", df.isnull().sum())


df["order_date"] = pd.to_datetime(df["order_date"])
df["month"] = df["order_date"].dt.to_period("M").astype(str)

#重複行だけ表示
orders_duplicated = df[df.duplicated(keep=False)]
print(orders_duplicated)
print(f"削除前の重複数:{df.duplicated().sum()}")


print(f'order_idの重複数: {df["order_id"].duplicated().sum()}')

#重複を削除
df = df.drop_duplicates()

print(f"削除後の重複数:{df.duplicated().sum()}")

#欠損値がある行を探す
#any(axis=1)：各行について、1つでも True があるか調べる
print(df[df.isnull().any(axis=1)])

# 数量が欠損している行を確認
print(df[df["quantity"].isna()])


# 商品名の前後にある余分な空白を削除
df["product"] = df["product"].str.strip()

# カテゴリにも同じ処理を適用
df["category"] = df["category"].str.strip()

# 集計用データを作り直す
df_clean = df.dropna(subset=["quantity"]).copy()

# 売上金額を計算
df_clean["sales"] = (
    df_clean["quantity"] * df_clean["unit_price"]
)


print(df_clean[["order_id", "product", "quantity", "sales"]])

print("元データの行数:", len(df))
print("集計対象の行数:", len(df_clean))
print("除外した行数:", len(df) - len(df_clean))

product_sales = (
    df_clean.groupby("product")["sales"]
    .sum()
    .reset_index()
)

print(product_sales)

monthly_sales = (
    df_clean.groupby("month")["sales"]
    .sum()
    .reset_index()
)

print(monthly_sales)


# 月別 × 商品別の売上ピボット表
sales_pivot = pd.pivot_table(
    df_clean,
    index="month",
    columns="product",
    values="sales",
    aggfunc="sum",
    fill_value=0
)

print(sales_pivot)

#CSVで保存
sales_pivot.to_csv(
    "/monthly_product_sales.csv",
    encoding="utf-8-sig"
)

print("CSVファイルを保存しました！")

# 月別売上を集計
monthly_sales = (
    df_clean.groupby("month")["sales"]
    .sum()
    .reset_index()
)

# グラフを作成
plt.figure(figsize=(6, 4))

plt.bar(
    monthly_sales["month"],
    monthly_sales["sales"]
)

plt.title("Monthly Sales")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.tight_layout()

# 画像を保存
plt.savefig("monthly_sales.png", dpi=300)

# グラフを表示
plt.show()

# 商品別売上を集計
product_sales = (
    df_clean.groupby("product")["sales"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(8, 5))

plt.bar(
    product_sales.index,
    product_sales.values
)

plt.title("Sales by Product")
plt.xlabel("Product")
plt.ylabel("Sales")
plt.tight_layout()

plt.savefig("product_sales.png", dpi=300)
plt.show()


from pathlib import Path

# 月別・商品別に売上を集計する
monthly_product_sales_long = (
    df_clean
    .groupby(["month", "product"], as_index=False)["sales"]
    .sum()
)

# 出力フォルダを作成する
Path("output").mkdir(parents=True, exist_ok=True)

# CSVファイルに保存する
monthly_product_sales_long.to_csv(
    "monthly_product_sales_long.csv",
    index=False,
    encoding="utf-8-sig"
)

# 結果を確認する
print(monthly_product_sales_long)
