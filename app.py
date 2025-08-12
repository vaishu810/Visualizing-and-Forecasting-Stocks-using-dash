import pandas as pd
import numpy as np
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import io
import base64

# Function to load stock data
def load_data():
    try:
        print("Attempting to load CSV data...")
        portfolio_data = pd.read_csv('portfolio_data.csv')
        print("CSV data loaded successfully.")
        
        portfolio_data['Date'] = pd.to_datetime(portfolio_data['Date'], errors='coerce')
        portfolio_data.set_index('Date', inplace=True)

        portfolio_data = portfolio_data.apply(pd.to_numeric, errors='coerce')
        print("Data after processing:\n", portfolio_data.head())
        
        return portfolio_data.dropna()
    except Exception as e:
        print(f"Error loading data: {e}")
        print("Generating sample data...")
        dates = pd.date_range(start="2022-01-01", periods=100)
        return pd.DataFrame({
            'Date': dates,
            'BTC': np.random.normal(2800, 2800, size=100),
            'DPZ': np.random.normal(2800, 2800, size=100),
            'NFLX': np.random.normal(2800, 2800, size=100),
            'AMZN': np.random.normal(2800, 2800, size=100)
        }).set_index('Date')

# Load portfolio data
portfolio_data = load_data()
returns = portfolio_data.pct_change().dropna()

# Initialize Dash app
app = dash.Dash(__name__)

# Define app layout
app.layout = html.Div([
    html.H1("Stock Portfolio Analysis", style={'text-align': 'center'}),
    
    dcc.Dropdown(
        id='stock-code-dropdown',
        options=[{'label': col, 'value': col} for col in portfolio_data.columns],
        value=[portfolio_data.columns[0]] if portfolio_data.columns.size > 0 else [],
        multi=True,
        style={'width': '50%', 'margin': 'auto'}
    ),
    
    html.Div(id='graphs-container', children=[
        html.H3("Daily Returns"),
        dcc.Graph(id='daily-returns-graph'),

        html.H3("Correlation Matrix"),
        dcc.Graph(id='correlation-graph'),

        html.H3("Moving Averages"),
        dcc.Graph(id='moving-averages-graph'),

        html.H3("Stock Price Over Time"),
        dcc.Graph(id='stock-price-graph'),

        html.H3("Risk vs Expected Returns"),
        dcc.Graph(id='risk-vs-expected-returns-graph'),

        html.H3("Seaborn Heatmap"),
        html.Img(id='seaborn-plot-image'),

        html.H3("Prediction Graph"),
        dcc.Graph(id='prediction-graph'),
    ])
])

# Callback for daily returns graph
@app.callback(
    Output('daily-returns-graph', 'figure'),
    Input('stock-code-dropdown', 'value')
)
def update_daily_returns_graph(selected_stocks):
    fig = go.Figure()
    for stock in selected_stocks:
        if stock in returns.columns:
            fig.add_trace(go.Scatter(x=returns.index, y=returns[stock], mode='lines', name=stock))
    fig.update_layout(title="Daily Returns of Selected Stocks", xaxis_title="Date", yaxis_title="Daily Returns")
    return fig

# Callback for correlation matrix graph
@app.callback(
    Output('correlation-graph', 'figure'),
    Input('stock-code-dropdown', 'value')
)
def update_correlation_graph(selected_stocks):
    if not selected_stocks:
        return go.Figure()
    correlation_data = returns[selected_stocks].corr()
    fig = px.imshow(correlation_data, text_auto=True, aspect="auto", color_continuous_scale='Viridis')
    fig.update_layout(title="Correlation Matrix")
    return fig

# Callback for moving averages graph
@app.callback(
    Output('moving-averages-graph', 'figure'),
    Input('stock-code-dropdown', 'value')
)
def update_moving_averages_graph(selected_stocks):
    fig = go.Figure()
    for stock in selected_stocks:
        if stock in portfolio_data.columns:
            fig.add_trace(go.Scatter(x=portfolio_data.index, y=portfolio_data[stock].rolling(window=20).mean(), name=f"{stock} 20-day MA"))
            fig.add_trace(go.Scatter(x=portfolio_data.index, y=portfolio_data[stock].rolling(window=50).mean(), name=f"{stock} 50-day MA"))
    fig.update_layout(title="Moving Averages", xaxis_title="Date", yaxis_title="Price")
    return fig

# Callback for stock price over time graph
@app.callback(
    Output('stock-price-graph', 'figure'),
    Input('stock-code-dropdown', 'value')
)
def update_stock_price_graph(selected_stocks):
    fig = go.Figure()
    for stock in selected_stocks:
        if stock in portfolio_data.columns:
            fig.add_trace(go.Scatter(x=portfolio_data.index, y=portfolio_data[stock], mode='lines', name=stock))
    fig.update_layout(title="Stock Price Over Time", xaxis_title="Date", yaxis_title="Price")
    return fig

# Callback for risk vs expected returns graph
@app.callback(
    Output('risk-vs-expected-returns-graph', 'figure'),
    Input('stock-code-dropdown', 'value')
)
def update_risk_vs_expected_returns_graph(selected_stocks):
    if not selected_stocks:
        return go.Figure()
    risk = [returns[stock].std() for stock in selected_stocks if stock in returns.columns]
    expected_returns = [returns[stock].mean() for stock in selected_stocks if stock in returns.columns]
    
    fig = go.Figure(data=go.Scatter(
        x=risk,
        y=expected_returns,
        mode='markers+text',
        text=selected_stocks,
        textposition="bottom center"
    ))
    fig.update_layout(title="Risk vs Expected Returns", xaxis_title="Risk (Std Dev)", yaxis_title="Expected Returns (Mean)")
    return fig

# Callback for prediction graph
@app.callback(
    Output('prediction-graph', 'figure'),
    Input('stock-code-dropdown', 'value')
)
def update_prediction_graph(selected_stocks):
    fig = go.Figure()
    for stock in selected_stocks:
        if stock in portfolio_data.columns:
            fig.add_trace(go.Scatter(x=portfolio_data.index, y=portfolio_data[stock], mode='lines', name=f"{stock} Actual"))
            prediction = portfolio_data[stock].shift(-5).fillna(method='bfill')
            fig.add_trace(go.Scatter(x=portfolio_data.index, y=prediction, mode='lines', name=f"{stock} Predicted"))
    fig.update_layout(title="Stock Price Prediction", xaxis_title="Date", yaxis_title="Price")
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
