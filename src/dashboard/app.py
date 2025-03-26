"""
E-commerce Delivery Analytics Dashboard
Created by: Vijeta Thakur (2025)
A comprehensive analytics dashboard for e-commerce delivery performance monitoring.
"""

import sys
import os

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from src.reports.report_generator import ReportGenerator
import os
from datetime import datetime

# Initialize the Dash app with external stylesheets
app = Dash(__name__)

# Define color scheme
COLORS = {
    'primary': '#2c3e50',
    'secondary': '#34495e',
    'accent': '#3498db',
    'success': '#2ecc71',
    'warning': '#f1c40f',
    'danger': '#e74c3c',
    'light': '#ecf0f1',
    'dark': '#2c3e50',
    'white': '#ffffff',
    'border': '#bdc3c7'
}

# Define styles
STYLES = {
    'card': {
        'backgroundColor': COLORS['white'],
        'borderRadius': '8px',
        'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
        'padding': '20px',
        'margin': '10px',
        'transition': 'transform 0.2s ease-in-out',
    },
    'section': {
        'backgroundColor': COLORS['white'],
        'borderRadius': '8px',
        'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
        'padding': '25px',
        'margin': '20px 0',
    },
    'header': {
        'color': COLORS['primary'],
        'marginBottom': '20px',
        'fontWeight': 'bold',
        'borderBottom': f'2px solid {COLORS["border"]}',
        'paddingBottom': '10px',
    },
    'subheader': {
        'color': COLORS['secondary'],
        'marginBottom': '15px',
        'fontWeight': '500',
    },
    'table': {
        'width': '100%',
        'borderCollapse': 'separate',
        'borderSpacing': '0',
        'backgroundColor': COLORS['white'],
        'borderRadius': '8px',
        'overflow': 'hidden',
    },
    'th': {
        'backgroundColor': COLORS['primary'],
        'color': COLORS['white'],
        'padding': '12px 15px',
        'textAlign': 'left',
        'fontWeight': '500',
    },
    'td': {
        'padding': '12px 15px',
        'borderBottom': f'1px solid {COLORS["border"]}',
    },
    'button': {
        'padding': '12px 24px',
        'borderRadius': '6px',
        'border': 'none',
        'fontWeight': '500',
        'cursor': 'pointer',
        'transition': 'all 0.2s ease-in-out',
        'margin': '0 10px',
    }
}

# Load and prepare the data
df = pd.read_csv('data/delivery_data.csv')
report_gen = ReportGenerator(df)

# Calculate detailed statistics
detailed_stats = {
    'delivery_time': {
        'max': df['Delivery Time (Minutes)'].max(),
        'min': df['Delivery Time (Minutes)'].min(),
        'avg': df['Delivery Time (Minutes)'].mean(),
        'fastest_platform': df.groupby('Platform')['Delivery Time (Minutes)'].mean().idxmin(),
        'slowest_platform': df.groupby('Platform')['Delivery Time (Minutes)'].mean().idxmax(),
    },
    'order_value': {
        'max': df['Order Value (INR)'].max(),
        'min': df['Order Value (INR)'].min(),
        'avg': df['Order Value (INR)'].mean(),
        'highest_value_platform': df.groupby('Platform')['Order Value (INR)'].mean().idxmax(),
        'lowest_value_platform': df.groupby('Platform')['Order Value (INR)'].mean().idxmin(),
    },
    'service_rating': {
        'max': df['Service Rating'].max(),
        'min': df['Service Rating'].min(),
        'avg': df['Service Rating'].mean(),
        'best_rated_platform': df.groupby('Platform')['Service Rating'].mean().idxmax(),
        'worst_rated_platform': df.groupby('Platform')['Service Rating'].mean().idxmin(),
    }
}

# Create detailed platform metrics
platform_detailed_stats = df.groupby('Platform').agg({
    'Order Value (INR)': ['mean', 'min', 'max', 'count'],
    'Delivery Time (Minutes)': ['mean', 'min', 'max'],
    'Service Rating': ['mean', 'min', 'max']
}).round(2)

# Create category performance metrics
category_stats = df.groupby('Product Category').agg({
    'Order Value (INR)': ['mean', 'count'],
    'Delivery Time (Minutes)': ['mean', 'min', 'max'],
    'Service Rating': ['mean']
}).round(2)

# Create visualizations
def create_delivery_time_dist():
    fig = px.histogram(df, x='Delivery Time (Minutes)',
                      title='Distribution of Delivery Times',
                      labels={'Delivery Time (Minutes)': 'Delivery Time (Minutes)',
                             'count': 'Number of Orders'})
    fig.update_layout(
        plot_bgcolor=COLORS['white'],
        paper_bgcolor=COLORS['white'],
        font={'color': COLORS['primary']},
        title={'font': {'size': 24, 'color': COLORS['primary']}},
        title_x=0.5,
        margin=dict(t=50, l=50, r=30, b=50)
    )
    return fig

def create_correlation_matrix():
    numeric_cols = ['Delivery Time (Minutes)', 'Order Value (INR)', 'Service Rating']
    corr_matrix = df[numeric_cols].corr()
    fig = px.imshow(corr_matrix,
                    labels=dict(color="Correlation"),
                    title='Correlation Matrix')
    fig.update_layout(
        plot_bgcolor=COLORS['white'],
        paper_bgcolor=COLORS['white'],
        font={'color': COLORS['primary']},
        title={'font': {'size': 24, 'color': COLORS['primary']}},
        title_x=0.5
    )
    return fig

def create_scatter_plot():
    return px.scatter(df, x='Order Value (INR)', y='Delivery Time (Minutes)',
                    color='Platform', title='Delivery Time vs Order Value by Platform')

def create_boxplot():
    return px.box(df, x='Platform', y='Delivery Time (Minutes)',
                 title='Delivery Time Distribution by Platform')

def create_category_times():
    category_stats = df.groupby('Product Category')['Delivery Time (Minutes)'].mean().sort_values(ascending=True)
    return px.bar(x=category_stats.index, y=category_stats.values,
                 title='Average Delivery Time by Product Category',
                 labels={'x': 'Product Category', 'y': 'Average Delivery Time (Minutes)'})

def create_platform_values():
    return px.box(df, x='Platform', y='Order Value (INR)',
                 title='Order Value Distribution by Platform')

# Calculate summary statistics
platform_stats = df.groupby('Platform').agg({
    'Order Value (INR)': 'mean',
    'Delivery Time (Minutes)': 'mean',
    'Order ID': 'count'
}).round(2)
platform_stats.columns = ['Avg Order Value', 'Avg Delivery Time', 'Total Orders']

# Define the layout with improved styling
app.layout = html.Div([
    # Header
    html.Div([
        html.H1('E-commerce Analytics Dashboard',
                style={'color': COLORS['primary'], 'textAlign': 'center', 'padding': '30px 0',
                       'fontSize': '36px', 'fontWeight': 'bold', 'letterSpacing': '0.5px'}),
        html.P('Created by: Vijeta Thakur',
               style={'color': COLORS['secondary'], 'textAlign': 'center', 'padding': '0 0 10px 0',
                      'fontSize': '16px', 'fontStyle': 'italic'}),
    ], style={'borderBottom': f'3px solid {COLORS["border"]}', 'marginBottom': '30px'}),
    
    # Report Generation Section
    html.Div([
        html.H2('Generate Reports', style=STYLES['header']),
        html.Div([
            html.Button(
                'Download PDF Report',
                id='btn-pdf',
                style={
                    **STYLES['button'],
                    'backgroundColor': COLORS['danger'],
                    'color': COLORS['white'],
                    'fontSize': '16px',
                }
            ),
            html.Button(
                'Download Word Report',
                id='btn-word',
                style={
                    **STYLES['button'],
                    'backgroundColor': COLORS['accent'],
                    'color': COLORS['white'],
                    'fontSize': '16px',
                }
            ),
            dcc.Download(id="download-pdf"),
            dcc.Download(id="download-word"),
        ], style={'textAlign': 'center', 'padding': '20px 0'}),
    ], style=STYLES['section']),
    
    # Key Metrics Section
    html.Div([
        html.H2('Key Performance Metrics', style=STYLES['header']),
        html.Div([
            # Delivery Time Card
            html.Div([
                html.H3('Delivery Time Metrics', style=STYLES['subheader']),
                html.Div([
                    html.P([
                        html.Strong('Fastest Delivery: '),
                        f"{detailed_stats['delivery_time']['min']:.0f} minutes"
                    ], style={'margin': '10px 0'}),
                    html.P([
                        html.Strong('Slowest Delivery: '),
                        f"{detailed_stats['delivery_time']['max']:.0f} minutes"
                    ], style={'margin': '10px 0'}),
                    html.P([
                        html.Strong('Average Time: '),
                        f"{detailed_stats['delivery_time']['avg']:.0f} minutes"
                    ], style={'margin': '10px 0'}),
                    html.P([
                        html.Strong('Best Platform: '),
                        detailed_stats['delivery_time']['fastest_platform']
                    ], style={'margin': '10px 0', 'color': COLORS['success']}),
                    html.P([
                        html.Strong('Needs Improvement: '),
                        detailed_stats['delivery_time']['slowest_platform']
                    ], style={'margin': '10px 0', 'color': COLORS['danger']}),
                ], style={'padding': '10px'})
            ], style={**STYLES['card'], 'flex': '1'}),
            
            # Order Value Card
            html.Div([
                html.H3('Order Value Metrics', style=STYLES['subheader']),
                html.Div([
                    html.P([
                        html.Strong('Highest Order: '),
                        f"₹{detailed_stats['order_value']['max']:,.0f}"
                    ], style={'margin': '10px 0', 'color': COLORS['success']}),
                    html.P([
                        html.Strong('Lowest Order: '),
                        f"₹{detailed_stats['order_value']['min']:,.0f}"
                    ], style={'margin': '10px 0', 'color': COLORS['danger']}),
                    html.P([
                        html.Strong('Average Value: '),
                        f"₹{detailed_stats['order_value']['avg']:,.0f}"
                    ], style={'margin': '10px 0'}),
                    html.P([
                        html.Strong('Best Platform: '),
                        detailed_stats['order_value']['highest_value_platform']
                    ], style={'margin': '10px 0', 'color': COLORS['success']}),
                ], style={'padding': '10px'})
            ], style={**STYLES['card'], 'flex': '1'}),
            
            # Rating Card
            html.Div([
                html.H3('Service Rating Metrics', style=STYLES['subheader']),
                html.Div([
                    html.P([
                        html.Strong('Highest Rating: '),
                        f"{detailed_stats['service_rating']['max']:.1f}"
                    ], style={'margin': '10px 0', 'color': COLORS['success']}),
                    html.P([
                        html.Strong('Lowest Rating: '),
                        f"{detailed_stats['service_rating']['min']:.1f}"
                    ], style={'margin': '10px 0', 'color': COLORS['danger']}),
                    html.P([
                        html.Strong('Average Rating: '),
                        f"{detailed_stats['service_rating']['avg']:.1f}"
                    ], style={'margin': '10px 0'}),
                    html.P([
                        html.Strong('Best Platform: '),
                        detailed_stats['service_rating']['best_rated_platform']
                    ], style={'margin': '10px 0', 'color': COLORS['success']}),
                ], style={'padding': '10px'})
            ], style={**STYLES['card'], 'flex': '1'}),
        ], style={'display': 'flex', 'gap': '20px', 'marginTop': '20px'}),
    ], style=STYLES['section']),
    
    # Overview Section
    html.Div([
        html.H2('Dataset Overview', style=STYLES['header']),
        html.Div([
            html.Div([
                html.Div([
                    html.Strong('Total Orders'),
                    html.H3(f"{len(df):,}", style={'color': COLORS['accent'], 'margin': '10px 0'})
                ], style={**STYLES['card'], 'textAlign': 'center'}),
                html.Div([
                    html.Strong('Total Revenue'),
                    html.H3(f"₹{df['Order Value (INR)'].sum():,.0f}", 
                           style={'color': COLORS['success'], 'margin': '10px 0'})
                ], style={**STYLES['card'], 'textAlign': 'center'}),
            ], style={'flex': '1', 'display': 'flex', 'gap': '20px'}),
            html.Div([
                html.Div([
                    html.Strong('Average Rating'),
                    html.H3(f"{df['Service Rating'].mean():.2f}", 
                           style={'color': COLORS['warning'], 'margin': '10px 0'})
                ], style={**STYLES['card'], 'textAlign': 'center'}),
                html.Div([
                    html.Strong('High Value Orders'),
                    html.H3(f"{(df['Order Value (INR)'] > df['Order Value (INR)'].mean()).sum():,}",
                           style={'color': COLORS['accent'], 'margin': '10px 0'})
                ], style={**STYLES['card'], 'textAlign': 'center'}),
            ], style={'flex': '1', 'display': 'flex', 'gap': '20px'}),
        ], style={'display': 'flex', 'gap': '20px', 'marginTop': '20px'}),
    ], style=STYLES['section']),
    
    # Visualizations Section
    html.Div([
        html.H2('Data Visualizations', style=STYLES['header']),
        html.Div([
            dcc.Graph(figure=create_delivery_time_dist(), 
                     style={**STYLES['card'], 'height': '400px'}),
            dcc.Graph(figure=create_correlation_matrix(),
                     style={**STYLES['card'], 'height': '400px'}),
        ], style={'display': 'flex', 'gap': '20px', 'marginBottom': '20px'}),
        html.Div([
            dcc.Graph(figure=create_scatter_plot(),
                     style={**STYLES['card'], 'height': '400px'}),
            dcc.Graph(figure=create_boxplot(),
                     style={**STYLES['card'], 'height': '400px'}),
        ], style={'display': 'flex', 'gap': '20px', 'marginBottom': '20px'}),
    ], style=STYLES['section']),
    
    # Detailed Analysis Tables
    html.Div([
        html.H2('Detailed Platform Analysis', style=STYLES['header']),
        html.Div(style={'overflowX': 'auto'}),
        html.Table([
            html.Thead(
                html.Tr([
                    html.Th(col, style=STYLES['th']) for col in [
                        'Platform', 'Total Orders', 'Avg Order Value', 'Min Order',
                        'Max Order', 'Avg Delivery Time', 'Fastest Delivery',
                        'Slowest Delivery', 'Avg Rating'
                    ]
                ])
            ),
            html.Tbody([
                html.Tr([
                    html.Td(platform, style=STYLES['td']),
                    html.Td(f"{stats[('Order Value (INR)', 'count')]:.0f}", style=STYLES['td']),
                    html.Td(f"₹{stats[('Order Value (INR)', 'mean')]:,.2f}", style=STYLES['td']),
                    html.Td(f"₹{stats[('Order Value (INR)', 'min')]:,.2f}", style=STYLES['td']),
                    html.Td(f"₹{stats[('Order Value (INR)', 'max')]:,.2f}", style=STYLES['td']),
                    html.Td(f"{stats[('Delivery Time (Minutes)', 'mean')]:.0f} min", style=STYLES['td']),
                    html.Td(f"{stats[('Delivery Time (Minutes)', 'min')]:.0f} min", style=STYLES['td']),
                    html.Td(f"{stats[('Delivery Time (Minutes)', 'max')]:.0f} min", style=STYLES['td']),
                    html.Td(f"{stats[('Service Rating', 'mean')]:.2f}", style=STYLES['td']),
                ]) for platform, stats in platform_detailed_stats.iterrows()
            ])
        ], style=STYLES['table']),
    ], style=STYLES['section']),
    
], style={'maxWidth': '1400px', 'margin': 'auto', 'padding': '20px', 'backgroundColor': COLORS['light']})

# Callbacks for report generation
@app.callback(
    Output('download-pdf', 'data'),
    Input('btn-pdf', 'n_clicks'),
    prevent_initial_call=True
)
def generate_pdf_report(n_clicks):
    if n_clicks:
        # Create all figures
        figures = {
            'delivery_time_dist': create_delivery_time_dist(),
            'correlation_matrix': create_correlation_matrix(),
            'scatter_plot': create_scatter_plot(),
            'boxplot': create_boxplot(),
            'category_times': create_category_times(),
            'platform_values': create_platform_values()
        }
        
        # Generate report with figures
        filename = report_gen.generate_pdf(figures)
        
        return dcc.send_file(filename)

@app.callback(
    Output('download-word', 'data'),
    Input('btn-word', 'n_clicks'),
    prevent_initial_call=True
)
def generate_word_report(n_clicks):
    if n_clicks:
        # Create all figures
        figures = {
            'delivery_time_dist': create_delivery_time_dist(),
            'correlation_matrix': create_correlation_matrix(),
            'scatter_plot': create_scatter_plot(),
            'boxplot': create_boxplot(),
            'category_times': create_category_times(),
            'platform_values': create_platform_values()
        }
        
        # Generate report with figures
        filename = report_gen.generate_word(figures)
        
        return dcc.send_file(filename)

if __name__ == '__main__':
    # Create output directories
    os.makedirs('output/reports', exist_ok=True)
    os.makedirs('output/temp', exist_ok=True)
    app.run_server(debug=True)
