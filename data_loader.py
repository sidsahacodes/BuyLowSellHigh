import yfinance as yf

equities_tickers = ['AAPL', 'MSFT', 'TSLA', 'AMZN', 'PLTR']

equities_data = yf.download(
    equities_tickers, 
    start='2024-01-01', 
    end='2025-01-01',
    interval='1h',
    group_by='ticker'
)

# Save to CSV
equities_data.to_csv('equities_intraday_1h_1year.csv')
