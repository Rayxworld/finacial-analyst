import yfinance as yf
import pandas as pd

ticker = "TSLA"
t = yf.Ticker(ticker)
holders = t.institutional_holders
print(f"--- Holders for {ticker} ---")
print(holders)
if holders is not None:
    print(f"Columns: {holders.columns.tolist()}")
    print(holders.head(2))

insiders = t.insider_transactions
print(f"\n--- Insiders for {ticker} ---")
print(insiders)
if insiders is not None:
    print(f"Columns: {insiders.columns.tolist()}")
