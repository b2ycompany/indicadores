import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Read the CSV file
df = pd.read_csv('data/Pasta13 - Planilha1.csv', thousands='.', decimal=',')

# Clean and preprocess the data
# Remove any non-breaking spaces (\xa0) and replace commas with dots
df['QTD_FATURADA'] = df['QTD FATURADA'].str.replace('\xa0', ' ')  # Remove non-breaking spaces
df['QTD_FATURADA'] = df['QTD_FATURADA'].str.replace(' ', '')  # Remove spaces
df['QTD_FATURADA'] = df['QTD_FATURADA'].str.replace(',', '.')  # Replace commas with dots
df['QTD_FATURADA'] = pd.to_numeric(df['QTD_FATURADA'], errors='coerce')  # Convert to numeric, coerce errors to NaN

# Sort the dataframe by quantity sold in descending order
df_sorted = df.sort_values('QTD_FATURADA', ascending=False)

# Calculate total sales
total_sales = df['QTD_FATURADA'].sum()

# Calculate cumulative percentage and ABC classification
df_sorted['CUMULATIVE_PERCENTAGE'] = df_sorted['QTD_FATURADA'].cumsum() / total_sales * 100
df_sorted['ABC_CLASSIFICATION'] = pd.cut(
    df_sorted['CUMULATIVE_PERCENTAGE'], 
    bins=[0, 80, 95, 100], 
    labels=['A', 'B', 'C']
)

# Top 10 products
top_10_products = df_sorted.head(10)

# ABC Analysis Summary
abc_summary = df_sorted.groupby('ABC_CLASSIFICATION').agg({
    'QTD_FATURADA': ['count', 'sum', 'mean'],
    'CUMULATIVE_PERCENTAGE': 'max'
}).reset_index()
abc_summary.columns = ['Category', 'Product Count', 'Total Sales', 'Average Sales', 'Cumulative Percentage']

# Visualization 1: Top 10 Products Bar Chart
plt.figure(figsize=(15, 6))
plt.bar(top_10_products['DESCR'], top_10_products['QTD_FATURADA'])
plt.title('Top 10 Products by Sales Volume', fontsize=15)
plt.xlabel('Product Description', fontsize=12)
plt.ylabel('Sales Volume', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('top_10_products.png')
plt.close()

# Visualization 2: ABC Analysis Pie Chart
plt.figure(figsize=(10, 7))
abc_sales = df_sorted.groupby('ABC_CLASSIFICATION')['QTD_FATURADA'].sum()
plt.pie(abc_sales, labels=abc_sales.index, autopct='%1.1f%%', colors=['#FF6B6B', '#4ECDC4', '#45B7D1'])
plt.title('Sales Distribution by ABC Classification', fontsize=15)
plt.tight_layout()
plt.savefig('abc_distribution.png')
plt.close()

# Export detailed analysis
top_10_products[['DESCR', 'SKU', 'QTD_FATURADA']].to_csv('top_10_products.csv', index=False)
abc_summary.to_csv('abc_analysis_summary.csv', index=False)

# Strategic Insights
print("Strategic Insights:")
print("\nABC Analysis Summary:")
print(abc_summary)

print("\nTop 10 Products:")
print(top_10_products[['DESCR', 'SKU', 'QTD_FATURADA']])

# Calculate additional KPIs
print("\nAdditional KPIs:")
print(f"Total Products: {len(df)}")
print(f"Total Sales Volume: {total_sales:,.2f}")
print(f"Average Sales per Product: {df['QTD_FATURADA'].mean():,.2f}")
print(f"Median Sales per Product: {df['QTD_FATURADA'].median():,.2f}")
print(f"Standard Deviation of Sales: {df['QTD_FATURADA'].std():,.2f}")
