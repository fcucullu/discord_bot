import pandas as pd
from tabulate import tabulate
from datetime import datetime
import io

from utils.tracking_market_cap import *
from commands.base_command import BCBaseCommand


class CheckMarketCapCommand(BCBaseCommand):

    def run(self):

        mc = GetMarketCapitalization()
        df_marketcap = mc.get_market_cap_for_a_period()

        tcmc = TrackingCoinsByMarketCap(df_marketcap, 100, 5)
        df_ranking = tcmc.get_ranking_of_all_coins()
        df_summary = tcmc.track_last_changes_in_ranking_by_market_cap_for_all_coins(df_ranking)

        tcmc_ = TrackingCoinsByMarketCap(df_marketcap, 20, 2)
        df_ranking_ = tcmc_.get_ranking_of_all_coins()
        df_summary_ = tcmc_.track_last_changes_in_ranking_by_market_cap_for_all_coins(df_ranking)

        return df_summary, df_summary_
    
    def pretty_print(self,
                     df :pd.DataFrame):

        try:
            data = f'```{tabulate(df, tablefmt="simple" , headers="keys", showindex=False, colalign=("centre",))}```' #show index false
        except:
            data = 'No hay cambios significativos en el ranking según MCap'
        return data