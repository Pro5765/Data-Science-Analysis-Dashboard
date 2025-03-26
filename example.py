from data_analyzer import DataAnalyzer
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set basic style for better visualizations
plt.rcParams['figure.figsize'] = [12, 6]
plt.rcParams['font.size'] = 12
sns.set_theme(style="whitegrid")

# Prevent displaying plots
plt.ioff()

# Initialize analyzer with the e-commerce dataset
analyzer = DataAnalyzer('Ecommerce_Delivery_Analytics_New.csv')

# Get basic information about the dataset
analyzer.get_basic_info()

# Clean the data (automatically handle missing values)
analyzer.clean_data()

print("\nGenerating visualizations...")

# 1. Distribution of delivery times
fig, ax = plt.subplots()
analyzer.plot_distribution('Delivery Time (Minutes)')
plt.title('Distribution of Delivery Times Across All Orders', fontsize=14, pad=20)
plt.xlabel('Delivery Time (Minutes)', fontsize=12)
plt.ylabel('Number of Orders', fontsize=12)
plt.savefig('delivery_time_distribution.png', bbox_inches='tight', dpi=300)
plt.close('all')

# 2. Correlation matrix of numerical features
fig, ax = plt.subplots(figsize=(10, 8))
analyzer.plot_correlation_matrix()
plt.title('Correlation Matrix: Relationship Between Numerical Features', fontsize=14, pad=20)
plt.savefig('correlation_matrix.png', bbox_inches='tight', dpi=300)
plt.close('all')

# 3. Scatter plot with platform comparison
fig, ax = plt.subplots()
analyzer.plot_scatter('Order Value (INR)', 'Delivery Time (Minutes)', 'Platform')
plt.title('Delivery Time vs Order Value by Platform', fontsize=14, pad=20)
plt.xlabel('Order Value (INR)', fontsize=12)
plt.ylabel('Delivery Time (Minutes)', fontsize=12)
plt.savefig('delivery_time_vs_value.png', bbox_inches='tight', dpi=300)
plt.close('all')

# 4. Box plot of delivery times by platform
fig, ax = plt.subplots()
analyzer.plot_boxplot('Delivery Time (Minutes)', 'Platform')
plt.title('Delivery Time Distribution by Platform', fontsize=14, pad=20)
plt.xlabel('Platform', fontsize=12)
plt.ylabel('Delivery Time (Minutes)', fontsize=12)
plt.savefig('delivery_time_boxplot.png', bbox_inches='tight', dpi=300)
plt.close('all')

# Get summary statistics by platform
summary = analyzer.get_summary_by_category('Platform', 'Delivery Time (Minutes)')
print("\nDelivery Time Summary Statistics by Platform:")
print(summary)

# Normalize delivery time for comparison
analyzer.normalize_column('Delivery Time (Minutes)')

# Additional analysis
print("\nAnalyzing order patterns...")
df = analyzer.df

# 5. Average delivery time by product category
fig, ax = plt.subplots()
category_stats = df.groupby('Product Category')['Delivery Time (Minutes)'].mean().sort_values(ascending=True)
category_stats.plot(kind='bar')
plt.title('Average Delivery Time by Product Category', fontsize=14, pad=20)
plt.xlabel('Product Category', fontsize=12)
plt.ylabel('Average Delivery Time (Minutes)', fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('category_delivery_times.png', bbox_inches='tight', dpi=300)
plt.close('all')

# 6. Platform order value distribution
fig, ax = plt.subplots()
sns.boxplot(data=df, x='Platform', y='Order Value (INR)')
plt.title('Order Value Distribution by Platform', fontsize=14, pad=20)
plt.xlabel('Platform', fontsize=12)
plt.ylabel('Order Value (INR)', fontsize=12)
plt.tight_layout()
plt.savefig('platform_order_values.png', bbox_inches='tight', dpi=300)
plt.close('all')

# Print analysis summary
print("\nVisualization Summary:")
print("1. delivery_time_distribution.png - Shows how delivery times are distributed across all orders")
print("2. correlation_matrix.png - Displays relationships between numerical features")
print("3. delivery_time_vs_value.png - Scatter plot showing relationship between order value and delivery time")
print("4. delivery_time_boxplot.png - Compares delivery time distributions across platforms")
print("5. category_delivery_times.png - Average delivery times for each product category")
print("6. platform_order_values.png - Distribution of order values across different platforms")

# Average delivery time by product category
category_stats = df.groupby('Product Category')['Delivery Time (Minutes)'].agg(['mean', 'count']).sort_values('mean', ascending=False)
print("\nAverage Delivery Time by Product Category:")
print(category_stats)

# Platform performance metrics
platform_stats = df.groupby('Platform').agg({
    'Order Value (INR)': 'mean',
    'Delivery Time (Minutes)': 'mean',
    'Order ID': 'count'
}).round(2)
platform_stats.columns = ['Avg Order Value', 'Avg Delivery Time', 'Total Orders']
print("\nPlatform Performance Metrics:")
print(platform_stats)
