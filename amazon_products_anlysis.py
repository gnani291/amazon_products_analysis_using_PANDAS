import pandas as pd
from google.colab import files
uploaded=files.upload()
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv("amazon.csv")

# ---- Clean numeric columns ----
for col in ['discounted_price', 'actual_price', 'discount_percentage', 'rating', 'rating_count']:
    df[col] = (df[col].astype(str)
                         .str.replace('₹','', regex=True)
                         .str.replace(',','', regex=True)
                         .str.replace('%','', regex=True)
                         .str.strip())
    df[col] = pd.to_numeric(df[col], errors='coerce')

#Top 10 products by number of ratings
top_products = df.groupby("product_name")['rating_count'].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(10,5))
sns.barplot(x=top_products.values, y=top_products.index, palette="viridis")
plt.title("Top 10 Products by Number of Ratings")
plt.xlabel("Rating Count")
plt.ylabel("Product")
plt.show()

# ---- Sales (rating_count) by category ----
category_sales = df.groupby("category")['rating_count'].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(10,5))
category_sales.plot(kind='bar', color="orange")
plt.title("Top 10 Categories by Rating Count (Sales Proxy)")
plt.ylabel("Rating Count")
plt.show()

# ---- Average discount per category ----
avg_discount = df.groupby("category")['discount_percentage'].mean().sort_values(ascending=False).head(10)

plt.figure(figsize=(10,5))
avg_discount.plot(kind='barh', color="green")
plt.title("Average Discount by Category")
plt.xlabel("Discount %")
plt.show()

# ---- Pivot: Category vs Average Rating ----
pivot = pd.pivot_table(df, index='category', values='rating', aggfunc='mean')
print(pivot.head())

