import pandas as pd
import sys
sys.path.append('../financial_utils')
import performance as per


price_table = pd.read_csv('../history_files/SPX.csv', parse_dates=[0])

# Build Tick Table
tick_table = price_table[["Date","Close","Open","High"]]
tick_table.columns = ["Date", "Tick","Open","High"]

returns, other_returns = per.tick2ret_pivoted(tick_table)
per.maxdrawdown(tick_table)
per.sharpeR(tick_table)

print("Returns:")
print(returns)

print("Other Returns:")
print(other_returns)