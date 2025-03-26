"""
E-commerce Analytics Data Analyzer
Created by: Vijeta Thakur (2025)
Advanced analytics and data processing utilities for e-commerce metrics.
"""

import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from typing import List, Optional

class DataAnalyzer:
    """
    Data analysis utilities for e-commerce delivery metrics.
    Created by: Vijeta Thakur
    """
    
    def __init__(self, file_path: str):
        """Initialize DataAnalyzer with a CSV file."""
        self.df = pd.read_csv(file_path)
        self.original_df = self.df.copy()
        self.process_data()
    
    def process_data(self):
        """Process and clean the dataset"""
        # Convert timestamps if present
        if 'Timestamp' in self.df.columns:
            self.df['Timestamp'] = pd.to_datetime(self.df['Timestamp'])
        
        # Calculate additional metrics
        self.calculate_metrics()
    
    def calculate_metrics(self):
        """Calculate key performance metrics"""
        # Platform performance
        self.platform_metrics = self.df.groupby('Platform').agg({
            'Order Value (INR)': ['mean', 'std', 'count'],
            'Delivery Time (Minutes)': ['mean', 'std', 'min', 'max'],
            'Service Rating': ['mean', 'count']
        }).round(2)
        
        # Category analysis
        self.category_metrics = self.df.groupby('Product Category').agg({
            'Order Value (INR)': ['mean', 'count'],
            'Delivery Time (Minutes)': ['mean', 'std'],
            'Service Rating': 'mean'
        }).round(2)
    
    def get_platform_performance(self):
        """Get platform-wise performance metrics"""
        return self.platform_metrics
    
    def get_category_insights(self):
        """Get category-wise performance insights"""
        return self.category_metrics
    
    def get_correlation_matrix(self):
        """Calculate correlation matrix for numerical metrics"""
        numeric_cols = ['Order Value (INR)', 'Delivery Time (Minutes)', 'Service Rating']
        return self.df[numeric_cols].corr().round(3)
    
    def get_time_based_analysis(self):
        """Analyze metrics over time periods"""
        if 'Timestamp' not in self.df.columns:
            return None
            
        return self.df.groupby(self.df['Timestamp'].dt.date).agg({
            'Order Value (INR)': 'mean',
            'Delivery Time (Minutes)': 'mean',
            'Service Rating': 'mean'
        }).round(2)
    
    def get_summary_stats(self):
        """Get summary statistics for key metrics"""
        return {
            'total_orders': len(self.df),
            'total_platforms': len(self.df['Platform'].unique()),
            'total_categories': len(self.df['Product Category'].unique()),
            'avg_delivery_time': self.df['Delivery Time (Minutes)'].mean(),
            'avg_order_value': self.df['Order Value (INR)'].mean(),
            'avg_rating': self.df['Service Rating'].mean()
        }
    
    def get_basic_info(self) -> None:
        """Display basic information about the dataset."""
        print("\n=== Dataset Info ===")
        print(f"Number of rows: {len(self.df)}")
        print(f"Number of columns: {len(self.df.columns)}")
        print("\n=== Data Types ===")
        print(self.df.dtypes)
        print("\n=== Missing Values ===")
        print(self.df.isnull().sum())
        print("\n=== Basic Statistics ===")
        print(self.df.describe())
    
    def clean_data(self, drop_na: bool = False) -> None:
        """Clean the dataset by handling missing values."""
        if drop_na:
            self.df = self.df.dropna()
        else:
            # Fill numeric columns with mean
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns
            self.df[numeric_cols] = self.df[numeric_cols].fillna(self.df[numeric_cols].mean())
            
            # Fill categorical columns with mode
            categorical_cols = self.df.select_dtypes(exclude=[np.number]).columns
            self.df[categorical_cols] = self.df[categorical_cols].fillna(self.df[categorical_cols].mode().iloc[0])
    
    def plot_distribution(self, column: str) -> None:
        """Plot distribution of a numerical column."""
        plt.figure(figsize=(10, 6))
        sns.histplot(data=self.df, x=column, kde=True)
        plt.title(f'Distribution of {column}')
        plt.show()
    
    def plot_correlation_matrix(self) -> None:
        """Plot correlation matrix for numerical columns."""
        numeric_df = self.df.select_dtypes(include=[np.number])
        plt.figure(figsize=(12, 8))
        sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', center=0)
        plt.title('Correlation Matrix')
        plt.show()
    
    def plot_scatter(self, x_col: str, y_col: str, color_col: Optional[str] = None) -> None:
        """Create an interactive scatter plot using plotly."""
        fig = px.scatter(self.df, x=x_col, y=y_col, color=color_col,
                        title=f'{y_col} vs {x_col}')
        fig.show()
    
    def plot_boxplot(self, numeric_col: str, category_col: Optional[str] = None) -> None:
        """Create a boxplot to show distribution across categories."""
        plt.figure(figsize=(10, 6))
        sns.boxplot(data=self.df, x=category_col, y=numeric_col)
        plt.title(f'Distribution of {numeric_col} by {category_col}')
        plt.xticks(rotation=45)
        plt.show()
    
    def get_summary_by_category(self, category_col: str, value_col: str) -> pd.DataFrame:
        """Get summary statistics grouped by a category."""
        return self.df.groupby(category_col)[value_col].agg(['mean', 'median', 'std', 'count'])
    
    def normalize_column(self, column: str) -> None:
        """Normalize a numerical column using StandardScaler."""
        if column in self.df.select_dtypes(include=[np.number]).columns:
            scaler = StandardScaler()
            self.df[f'{column}_normalized'] = scaler.fit_transform(self.df[[column]])
        else:
            print(f"Error: {column} is not a numerical column")
    
    def reset_data(self) -> None:
        """Reset the dataframe to its original state."""
        self.df = self.original_df.copy()
