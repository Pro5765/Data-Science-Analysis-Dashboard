from flask import Flask
import dash
from dash import html, dcc, Input, Output, State
import pandas as pd
import plotly.express as px
import base64
import io

server = Flask(__name__)
app = dash.Dash(__name__, server=server)

app.layout = html.Div([
    html.H1("Data Science Analysis Dashboard", style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': 30}),
    
    html.Div([
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select CSV File')
            ]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px'
            },
            multiple=False
        ),
    ], style={'margin': '20px'}),

    html.Div(id='output-data-upload'),
    
    html.Div([
        html.Div(id='data-summary', style={'margin': '20px'}),
        html.Div([
            html.H3("Visualization Options", style={'color': '#2c3e50'}),
            dcc.Dropdown(id='column-selector', multi=False, placeholder='Select column to visualize'),
            dcc.Graph(id='visualization')
        ], style={'margin': '20px'})
    ])
])

def parse_contents(contents):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
    return df

@app.callback(
    [Output('data-summary', 'children'),
     Output('column-selector', 'options')],
    Input('upload-data', 'contents')
)
def update_output(contents):
    if contents is None:
        return [], []
    
    df = parse_contents(contents)
    
    summary = [
        html.H3("Dataset Summary", style={'color': '#2c3e50'}),
        html.P(f"Number of rows: {len(df)}"),
        html.P(f"Number of columns: {len(df.columns)}"),
        html.H4("Data Types:"),
        html.Pre(df.dtypes.to_string())
    ]
    
    columns = [{'label': col, 'value': col} for col in df.columns]
    
    return summary, columns

@app.callback(
    Output('visualization', 'figure'),
    [Input('column-selector', 'value'),
     Input('upload-data', 'contents')]
)
def update_graph(selected_column, contents):
    if contents is None or selected_column is None:
        return {}
    
    df = parse_contents(contents)
    
    if pd.api.types.is_numeric_dtype(df[selected_column]):
        fig = px.histogram(df, x=selected_column, title=f'Distribution of {selected_column}')
    else:
        value_counts = df[selected_column].value_counts()
        fig = px.bar(x=value_counts.index, y=value_counts.values, 
                    title=f'Distribution of {selected_column}')
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
