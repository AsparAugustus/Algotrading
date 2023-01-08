import backtrader as bt


class SmaCross(bt.Strategy):
    # list of parameters which are configurable for the strategy
    params = dict(
        pfast=30,  # period for the fast moving average
        pslow=200,   # period for the slow moving average
        stop_loss=0.02,  # price is 2% less than the entry point
    )

    def __init__(self):
        sma1 = bt.ind.SMA(period=self.p.pfast)  # fast moving average
        sma2 = bt.ind.SMA(period=self.p.pslow)  # slow moving average
        self.crossover = bt.ind.CrossOver(sma1, sma2)  # crossover signal
        self.order = None

    def log(self, txt, dt=None, doprint=False):
        ''' Logging function for this strategy'''
        dt = dt or self.data.datetime[0]
        if isinstance(dt, float):
            dt = bt.num2date(dt)
        print("%s, %s" % (dt.date(), txt))

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            # order_details = f"{order.excecuted.price}, Cost: {order.executed.value}, Comm {order.executed.comm}"

            # print("hah", order)

            

            if order.isbuy():
                self.log('BUY EXECUTED {}'.format(order.executed))
                # self.log('{}'.format(order.executed.price, order.executed.value, order.executed.comm))
                dir(order.executed)

            elif order.issell():
                self.log('SELL EXECUTED {}'.format(order.executed.price))

            self.bar_executed = len(self)
        self.order = None

    def next(self):
        if not self.position:  # not in the market
            if self.crossover > 0:  # if fast crosses slow to the upside
                limit_price = self.datas[0].low
                self.buy(exectype=bt.Order.Stop,
                         price=limit_price * 0.99)  # enter long
                # self.log(f'BUY LIMIT, price {limit_price}')

                self.sell(exectype=bt.Order.Stop, price=limit_price * 0.97)
                self.sell(exectype=bt.Order.Limit, price=limit_price * 1.03)

        elif self.crossover < -0:  # in the market & cross to the downside
            self.close()  # close long position
