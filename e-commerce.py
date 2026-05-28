# ============================================================
# E-COMMERCE SALES ANALYSIS
# Author: Chirag Parhawk
# Dataset: UCI E-Commerce Dataset (541,909 transactions)
# Tools: Python, Pandas, Matplotlib, Seaborn
# ============================================================

# ---- STEP 1: IMPORT LIBRARIES ----
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---- STEP 2: LOAD DATASET ----
df = pd.read_csv('data.csv', encoding='latin1')
print("Shape before cleaning:", df.shape)
print("\nColumn names:")
print(df.columns.tolist())
print("\nDataset info:")
print(df.info())

# ---- STEP 3: CLEAN DATA ----

# Add TotalPrice column
df['TotalPrice'] = df['Quantity'] * df['UnitPrice']

# Drop rows with missing Description or CustomerID
df = df.dropna(subset=['Description', 'CustomerID'])

# Remove cancelled orders (InvoiceNo starts with 'C')
df = df[~df['InvoiceNo'].str.startswith('C')]

# Remove rows with negative or zero Quantity and UnitPrice
df = df[df['Quantity'] > 0]
df = df[df['UnitPrice'] > 0]

# Convert InvoiceDate to datetime format
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# Extract Month and Year
df['Month'] = df['InvoiceDate'].dt.month
df['Year'] = df['InvoiceDate'].dt.year

print("\nShape after cleaning:", df.shape)
print("\nMissing values after cleaning:")
print(df.isnull().sum())

# ---- STEP 4: ANALYSIS ----

# Total Revenue
total_revenue = df['TotalPrice'].sum()
print(f"\nTotal Revenue: £{total_revenue:,.2f}")

# Revenue by Month
print("\nRevenue by Month:")
monthly_revenue = df.groupby(['Year', 'Month'])['TotalPrice'].sum().reset_index()
print(monthly_revenue)

# Top 10 Best Selling Products by Quantity
print("\nTop 10 Best Selling Products:")
top_products = df.groupby('Description')['Quantity'].sum().sort_values(ascending=False).head(10)
print(top_products)

# Top 10 Products by Revenue
print("\nTop 10 Products by Revenue:")
top_revenue_products = df.groupby('Description')['TotalPrice'].sum().sort_values(ascending=False).head(10)
print(top_revenue_products)

# Top 10 Countries by Revenue
print("\nTop 10 Countries by Revenue:")
top_countries = df.groupby('Country')['TotalPrice'].sum().sort_values(ascending=False).head(10)
print(top_countries)

# ---- STEP 5: VISUALIZATIONS ----

sns.set_style("whitegrid")
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('E-Commerce Sales Analysis', fontsize=20, fontweight='bold', y=1.02)

# 1. Monthly Revenue Trend
monthly_revenue['Period'] = monthly_revenue['Month'].astype(str) + '/' + monthly_revenue['Year'].astype(str)
axes[0, 0].plot(monthly_revenue['Period'], monthly_revenue['TotalPrice'],
                marker='o', color='steelblue', linewidth=2, markersize=5)
axes[0, 0].set_title('Monthly Revenue Trend', fontsize=14, fontweight='bold')
axes[0, 0].set_xlabel('Month/Year')
axes[0, 0].set_ylabel('Revenue (£)')
axes[0, 0].tick_params(axis='x', rotation=45)
axes[0, 0].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'£{x:,.0f}'))

# 2. Top 10 Products by Revenue
top_revenue_products = df.groupby('Description')['TotalPrice'].sum().sort_values(ascending=False).head(10)
axes[0, 1].barh(top_revenue_products.index, top_revenue_products.values, color='coral')
axes[0, 1].set_title('Top 10 Products by Revenue', fontsize=14, fontweight='bold')
axes[0, 1].set_xlabel('Revenue (£)')
axes[0, 1].xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'£{x:,.0f}'))
axes[0, 1].invert_yaxis()

# 3. Top 10 Countries by Revenue
top_countries = df.groupby('Country')['TotalPrice'].sum().sort_values(ascending=False).head(10)
axes[1, 0].bar(top_countries.index, top_countries.values, color='seagreen')
axes[1, 0].set_title('Top 10 Countries by Revenue', fontsize=14, fontweight='bold')
axes[1, 0].set_xlabel('Country')
axes[1, 0].set_ylabel('Revenue (£)')
axes[1, 0].tick_params(axis='x', rotation=45)
axes[1, 0].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'£{x:,.0f}'))

# 4. Top 10 Products by Quantity Sold
top_quantity = df.groupby('Description')['Quantity'].sum().sort_values(ascending=False).head(10)
axes[1, 1].barh(top_quantity.index, top_quantity.values, color='mediumpurple')
axes[1, 1].set_title('Top 10 Products by Quantity Sold', fontsize=14, fontweight='bold')
axes[1, 1].set_xlabel('Quantity Sold')
axes[1, 1].invert_yaxis()

plt.tight_layout()
plt.savefig('ecommerce_analysis.png', dpi=150, bbox_inches='tight')
plt.show()
print("\n✅ Analysis complete! Chart saved as ecommerce_analysis.png")