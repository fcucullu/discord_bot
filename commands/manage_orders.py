from tabulate import tabulate
import pandas as pd
import numpy as np
import pytz
from datetime import datetime

from commands.base_command import BCBaseCommand


class BaseOrdersCommand(BCBaseCommand):

    def get_orders(self, portfolio_name, order_id):
        dfs = []
        open_trades = self.get_open_trades(portfolio_name)
        if len(open_trades) > 0:
            dfs.append(open_trades)
        
        pending_orders = self.get_pending_orders(portfolio_name)
        if len(pending_orders) > 0:
            dfs.append(pending_orders)

        df = pd.DataFrame()
        if len(dfs) > 0:     
            df = pd.concat(dfs)
            ordered_cols = ['pair', 'entry_price', 'last_close', 'perf', 'buy_limit', 'SL', 'TP', 'R/R', 'start_time', 'trade_duration', 'order_state']
            cols = [c for c in ordered_cols if c in df.columns]
            df = df[cols].fillna(0)
            df = df.T

        return df

    def get_open_trades(self, portfolio_name):
        current_trades = self.bc_data_proxy.get_current_trades(portfolio_name)
        current_trades = [trade for trade in current_trades if trade['base']!=trade['quote']]

        if len(current_trades) == 0:
            return pd.DataFrame()

        df = pd.DataFrame(current_trades) 
        df.start_time = pd.to_datetime(df.start_time)

        candlestick_repository = self.bc_data_proxy.candlestick_repository
        
        get_open_price = lambda row: candlestick_repository.get_open_price(f"{row['base']}/{row['quote']}", row['start_time']) 
        df['entry_price'] = df.apply(get_open_price, axis=1)
        
        get_last_close = lambda row: candlestick_repository.get_current_close_price(f"{row['base']}/{row['quote']}")
        df['last_close'] = df.apply(get_last_close, axis=1)

        df['pair'] = df.apply(lambda row: f"{row['base']}/{row['quote']}", axis=1)

        df['perf'] = ((df.last_close / df.entry_price) - 1).apply(lambda x: round(x,4))
                
        reward = ((df['sell_limit'] / df['entry_price']) - 1)  
        risk = ((df['stop_loss'] / df['entry_price']) - 1) * (-1) 
        df['R/R'] = (reward / risk).apply(lambda x: round(x,2))
        df['R/R'] = np.where(df['R/R'] < 0, 0, df['R/R'])

        df['trade_duration'] = datetime.utcnow().replace(tzinfo=pytz.utc) - df.start_time
        format_timedelta = lambda x: str(x).split(':')[0] + 'hs'
        df.trade_duration = df.trade_duration.apply(format_timedelta)

        df.start_time = df.start_time.apply(lambda x: x.strftime("%d/%m %H:%M"))
        
        df['order_state'] = 'buy_executed'

        df = df.rename(columns={'strategy_conf_pk': 'pk', 'stop_loss': 'SL', 'sell_limit': 'TP'})
        df = df[['pk', 'pair',   'entry_price', 'last_close', 'perf', 'SL', 'TP', 'R/R', 'start_time', 'trade_duration', 'order_state']]
        df.set_index('pk', inplace=True)


        return df
    

    def get_pending_orders(self, portfolio_name):
        portfolio_id = self.bc_data_proxy.SUPPORTED_PORTFOLIOS[portfolio_name]['id']
        pending_orders = self.bc_data_proxy.get_peding_orders(portfolio_id)
        pending_orders = pd.DataFrame(pending_orders)

        if len(pending_orders) > 0:
            candlestick_repository = self.bc_data_proxy.candlestick_repository
            pending_orders['pair'] = pending_orders.apply(lambda row: f"{row['base']}/{row['quote']}", axis=1)
            
            get_last_close = lambda row: candlestick_repository.get_current_close_price(f"{row['pair']}")
            pending_orders['last_close'] = pending_orders.apply(get_last_close, axis=1)

            reward = ((pending_orders['sell_limit'] / pending_orders['buy_limit']) - 1)  
            risk = ((pending_orders['stop_loss'] / pending_orders['buy_limit']) - 1) * (-1) 
            pending_orders['R/R'] =  (reward / risk).apply(lambda x: round(x,2))

            pending_orders.rename(columns={'strategy_conf_pk': 'pk', 'stop_loss': 'SL', 'sell_limit': 'TP'}, inplace=True)
            cols = ['pk', 'pair', 'buy_limit', 'SL', 'TP', 'R/R', 'last_close', 'order_state']
            pending_orders = pending_orders[cols]
            pending_orders.set_index('pk', inplace=True)

        return pending_orders
            
    def pretty_print(self, trades: pd.DataFrame):
        data = 'No hay trades abiertos'
        if len(trades):
            data = f'```{tabulate(trades, tablefmt="simple" , headers="keys", showindex=True, colalign=("centre",))}```'
            
        return data
    
class GetOrders(BaseOrdersCommand):
    def run(self, portfolio_name, order_id=None):
        orders = self.get_orders(portfolio_name, order_id)
        return self.pretty_print(orders)
            
class UpdateOrders(BaseOrdersCommand):
    def run(self, portfolio_name, order_id, buy_limit_price, sl_price, tp_price):
        portfolio_id = self.bc_data_proxy.SUPPORTED_PORTFOLIOS[portfolio_name]['id']
        response = self.bc_data_proxy.update_order(portfolio_id, order_id, buy_limit_price, sl_price, tp_price)                
        return self.pretty_print(response)
    
class NewOrder(BaseOrdersCommand):
    def run(self, portfolio_name, coin, buy_limit_price, sl_price, tp_price):
        portfolio_id = self.bc_data_proxy.SUPPORTED_PORTFOLIOS[portfolio_name]['id']
        response = self.bc_data_proxy.new_order(portfolio_id, coin, buy_limit_price, sl_price, tp_price)                
        return self.pretty_print(response)
        
class CancelOrder(BaseOrdersCommand):
    def run(self, portfolio_name, order_id):
        portfolio_id = self.bc_data_proxy.SUPPORTED_PORTFOLIOS[portfolio_name]['id']
        response = self.bc_data_proxy.cancel_order(portfolio_id, order_id)                
        return self.pretty_print(response)
        