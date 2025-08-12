# Visualizing-and-Forecasting-Stocks-using-dash
Interactive stock analysis and prediction web application built with Python Dash, Plotly, and Scikit-learn. Visualizes historical data, trends, and forecasts future stock prices using machine learning models.

# Introduction
This project is a web application designed for visualizing historical stock data and forecasting future stock prices.
It provides interactive dashboards with multiple financial visualizations and uses a machine learning model to predict stock prices based on historical trends.

The application is built using Dash, Plotly, and Scikit-learn, fetching real-time data via the yfinance library.
# Features
Visualize various stock metrics, including:

- Daily returns
- Daily returns over time
- Correlation graphs
- Closing returns vs sales volume
- Moving averages
- Stock price over time
- Seaborn heatmaps, pairplots, and pair grids
- Risk vs expected returns
- Predict future stock prices using a machine learning model.
- Responsive horizontal dashboard layout for better visualization.
- User inputs for: Stock code, Forecast days
# Requirements
- Python 3.x
- Dash
- Plotly
- Pandas
- NumPy
- Scikit-learn
- yfinance
- Seaborn
## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/vaishu810/Visualizing-and-Forecasting-Stocks-using-dash.git
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```
    ## Usage

1. Run the Dash application:

    ```bash
    python app.py
    ```

2. Open your web browser and navigate to:  
   [http://localhost:8050](http://localhost:8050)

---

## File Structure

- **app.py** : Main Dash application file.
- **assets/** : Contains CSS stylesheets and static assets for the app.
- **data/** : Dataset files (e.g., `stock_data.csv`).
- **requirements.txt** : List of dependencies required to run the project.
- **README.md** : This file.


  
