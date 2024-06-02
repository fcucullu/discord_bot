from commands.base_command import BCBaseCommand
from tabulate import tabulate
import pandas as pd

class BaseThresholdCommand(BCBaseCommand):
    def get_thresholds(self, portfolio_name):
        portfolio_id = self.bc_data_proxy.SUPPORTED_PORTFOLIOS[portfolio_name]['id']
        return self.bc_data_proxy.get_thresholds(portfolio_id)
          
    
class GetThresholds(BaseThresholdCommand):
    def run(self, portfolio_name):
        thresholds = self.get_thresholds(portfolio_name)
        return self.pretty_print(thresholds)
    
    def pretty_print(self, thresholds):
        data = pd.DataFrame.from_dict(thresholds, orient='index')
        msg = f'```{tabulate(data)}```'
        return msg
    
    
class UpdateThresholds(BaseThresholdCommand):
    def run(self, profile, coin, new_th):
        portfolio_id = self.bc_data_proxy.SUPPORTED_PORTFOLIOS[profile]['id']
        thresholds = self.get_thresholds(profile)
        
        coin = coin.upper()
        new_thresholds = thresholds.copy()
        new_thresholds.update({coin: float(new_th)})
        new_thresholds = self.bc_data_proxy.update_threshold(portfolio_id, new_thresholds)
        
        old_th = thresholds[coin]
        new_th = new_thresholds[coin]
        return old_th, new_th
        
        