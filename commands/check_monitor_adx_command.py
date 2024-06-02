import pandas as pd
import numpy as np
from tabulate import tabulate
from datetime import datetime
import io
from utils.check_monitor_indicator import CheckMonitor
from utils.check_adx_indicator import CheckADX
from indicators.ma_indicator import MovingAverageIndicator
from commands.base_command import BCBaseCommand
from utils.check_ma_indicator import CheckMA
from utils.candlestick import CandlestickRepository, BinancePricesRepository

class CheckMonitorADXCommand(BCBaseCommand):

    def run(self, profile, currencies):
        
        list_of_currencies_by_profile = self.bc_data_proxy.get_portfolio_currencies(profile)
        portfolio_currency = self.bc_data_proxy.get_portfolio_currency(profile)
        
        list_of_currencies = list_of_currencies_by_profile
        if len(currencies) !=0:
            list_of_currencies = currencies

        data = self.processing_indicators_data(portfolio_currency, list_of_currencies, ['4h', '1d', '1w'])
        data = self.info_gral(data)

        return data 


    def processing_indicators_data(self, portfolio_currency, list_currencies, list_timeframes):
        
        dict_candles = {}
        df_all = pd.DataFrame()
        
        for base in list_currencies:
            for tf in list_timeframes:      
                
                #obtener los precios 
                repo=BinancePricesRepository()
                candles = repo.get_candles(base, portfolio_currency, tf, 100)    
                dict_candles[f'{tf}'] = candles
            
            #calculo ma
            ma = CheckMA() 
            ma_ = [ma.get_ma_info(dict_candles[f'{tf}']) for tf in list_timeframes]
            df_ma = pd.DataFrame(ma_, columns = [base], index = list_timeframes).T

            #calculo adx
            adx = CheckADX()
            adx_ = [adx.get_adx_info(dict_candles[f'{tf}']) for tf in list_timeframes]
            df_adx = pd.DataFrame(adx_, columns = [base], index = list_timeframes).T

            #calculo monitor
            monitor = CheckMonitor()    
            mo_ = [monitor.get_monitor_state(dict_candles[f'{tf}']) for tf in list_timeframes]
            df_mo = pd.DataFrame(mo_, columns = [base], index = list_timeframes).T

            #concatenando data
            df_temp = pd.concat([df_mo, df_adx], axis=1)
            df_temp = pd.concat([df_temp, df_ma], axis=1)
            df_all = pd.concat([df_all, df_temp], axis=0)
        return df_all
     

    def info_gral(self, data):
        
        df_Data = pd.DataFrame()
        monitor = CheckMonitor()
        
        data_mon = data.iloc[:,:3]
        data_mon = monitor.assing_rank_and_order(data_mon)

        data['rank'] = data_mon['rank']
    
        for tf in ['4h', '1d', '1w']:
            
            df_temp = data[f'{tf}']
            df_temp.columns = ['Mon', 'ADX', 'MAs']
            df_Data = pd.concat([df_Data, df_temp], axis=1)
        
        df_Data['rank'] = data_mon['rank']
        
        return df_Data


    def pretty_print(self, s, df :pd.DataFrame):

        try:
            data = "```"
            filtered_df = df[df.iloc[:,0] == s]
            if len(filtered_df) > 0:
                data += f"""

Pares {s} en 4hs
""" 
                data += f"""
            4hs                   1d                   1w
---------------------------------------------------------------------------
"""

                filtered_df.sort_values(by=['rank'], inplace=True, ascending=False)
                data += f'{tabulate(filtered_df, tablefmt="simple" , headers="keys", showindex=True, colalign=("centre",))}'
            data += "```"
        except:
            data = 'Algo anda mal'
        return data
