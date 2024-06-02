import pandas as pd
from tabulate import tabulate
from datetime import datetime
import io
from utils.nbtb_strategy import BullMarketNowBetterThanBefore
from commands.base_command import BCBaseCommand
from utils.brainycore_dataproxy import BrainyCoreDataProxy

class NBTBSignalsCommand(BCBaseCommand):
    
    def run(self, profile,use_last_close=False):
        
        list_of_currencies_by_profile = self.bc_data_proxy.get_portfolio_currencies(profile)
        portfolio_currency = self.bc_data_proxy.get_portfolio_currency(profile)
        
        bcdp = BrainyCoreDataProxy.get_default_data_proxy()
        current_trades = bcdp.get_current_trades(profile)
        bases_in_current_trades = [idx['base'] for idx in current_trades if idx['base'] != idx['quote']]
     
        results = {'portfolio':profile}
        for base_currency in list_of_currencies_by_profile:
               strategy = BullMarketNowBetterThanBefore(base_currency,portfolio_currency,60)
               strategy_run_result = strategy.run(use_last_close)
               if strategy_run_result == None or \
                   (strategy_run_result==0 and base_currency not in bases_in_current_trades):
                   continue
               results.update({base_currency:strategy_run_result})
        return results
    
    def pretty_print(self,results):
        close_position = ':skull_crossbones: **CIERRE de posicion con NBTB** en: '
        open_position = ':money_mouth: **APERTURA de posicion con NBTB** en: '
        print_close = False
        print_open= False
        
        
        for key,value in results.items():
            if value==1:
                open_position += key+' '
                print_open = True
            if value==0:
                close_position += key+' '
                print_close = True
        data = ''
        if print_close:
            data += close_position
        if print_open:
            if data != '':
                data += '\n'
            data += open_position
        if data != '':
            data = f'Perfil {results["portfolio"]}:\n'+data
        return data