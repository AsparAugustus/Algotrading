# %%
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates
import seaborn as sns
import datetime
import backtrader
import backtrader.feeds as btfeeds

from examplestrat import SmaCross

# %%


# %%
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = 30, 10

# %%
def quick_clean(df):
    """convert all columns to their proper dtype"""

    df['open_time'] = pd.to_datetime(df['open_time'], unit='ms')
    df = df.set_index('open_time', drop=True)

    df = df.astype(dtype={
        'open': 'float64',
        'high': 'float64',
        'low': 'float64',
        'close': 'float64',
        'volume': 'float64',
        'close_time': 'datetime64[ms]',
        'quote_asset_volume': 'float64',
        'number_of_trades': 'int64',
        'taker_buy_base_asset_volume': 'float64',
        'taker_buy_quote_asset_volume': 'float64',
        'ignore': 'float64'
    })
    
    return df

# %%
# _df = pd.read_parquet("ETH-USDT.parquet")

# # Write the DataFrame to a CSV file
# _df.to_csv('ETH-USDT.csv')

# %%
df = pd.read_csv('ETH-USDT.csv', parse_dates = True, index_col=0)

perid_from_2020 = 60 * 12

df = df.iloc[-perid_from_2020:]

df = df.drop(columns=['quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume'])


# window of minutes times hours times days
window = 60 * 12 * 3

print(df)


# %%
cerebro = backtrader.Cerebro()

cerebro.addsizer(backtrader.sizers.PercentSizer, percents=50)

class MyBuySell(backtrader.observers.BuySell):
    plotlines = dict(
        buy=dict(marker='$\u21E7$', markersize=12.0),
        sell=dict(marker='$\u21E9$', markersize=12.0)
    )
backtrader.observers.Observer

backtrader.observers.BuySell = MyBuySell
cerebro.addobserver(MyBuySell, barplot=True, bardist=0.006)

Trades = backtrader.observers.Trades
cerebro.addobserver(Trades)



data = btfeeds.PandasData(dataname=df)


cerebro.adddata(data)
cerebro.addstrategy(SmaCross)



# %%
df['moving_average'] = df['open'].rolling(window).mean()
df[['open', 'moving_average']].plot(title='ETHUSDT', color=['black', 'red', 'green'])

# print(df['open'].rolling(window).mean())

# %%
# ax = df['volume'].plot(title='ETHUSDT', color='black', legend=True)
# df['number_of_trades'].plot(title='ETHUSDT', color='gold', legend=True, ax=ax)

# %%
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

cerebro.addobserver(backtrader.observers.Value)


cerebro.run(stdstats=False)



print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

cerebro.plot(style='candlestick')  # and plot it with a single command


