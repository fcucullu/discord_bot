import pandas as pd
from utils.check_coin_behaviors import CheckCorrelations, CheckVolumeGrowth
from commands.base_command import BCBaseCommand

class CheckCorrelationsCommand(BCBaseCommand):

    def run(self,list_of_currencies):
        list_of_currencies = list(list_of_currencies)
        cc = CheckCorrelations(list_of_currencies)
        price = cc.get_prices_info()
        returns = price.pct_change().fillna(0)
        correlation_alert = cc.check_correlation(returns)
        return correlation_alert[correlation_alert]
    
    def pretty_print(self,
                     correlation_alert:pd.DataFrame):
        coin_with_correlation_alerts = correlation_alert[correlation_alert].index
        data = ''
        if not coin_with_correlation_alerts.empty:
            data+= f'Perdida de correlacion en: `{coin_with_correlation_alerts.to_list()}`'
        return data

class CheckVolumeGrowthCommand(BCBaseCommand):

    def run(self,list_of_currencies):
        list_of_currencies = list(list_of_currencies)
        cvg = CheckVolumeGrowth(list_of_currencies)
        volume = cvg.get_volume_info()
        volume_alert = cvg.check_volume(volume)
        return volume_alert[volume_alert]
    
    def pretty_print(self,
                     volume_alert:pd.DataFrame):
        coin_with_volume_alerts = volume_alert[volume_alert].index
        data = ''
        if not coin_with_volume_alerts.empty:
            data+= f'Gran volumen de intercambio en: `{coin_with_volume_alerts.to_list()}`'
        return data
