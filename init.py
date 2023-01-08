import pandas as pd
import matplotlib.pyplot as plt
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mpl_dates
from IPython.display import display

import seaborn as sns

import traceback

plt.style.use('ggplot')

sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = 30, 10



# Print the DataFrame to the screen
try:
    # Read the contents of a .parquet file into a DataFrame
    df = pd.read_parquet("ETH-USDT.parquet")
    df_last_1000 = df.iloc[-10000:]

    
    # window of minutes times hours times days
    window = 60 * 24 * 50
    df_last_1000['moving_average'] = df['open'].rolling(window).mean()

    df_last_1000[['open', 'moving_average']].plot(title='ETH BTC', color=['black', 'red', 'green'])


    pass
except Exception as e:
    print(e)
    traceback.print_exc()

