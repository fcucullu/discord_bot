import pandas as pd
from tabulate import tabulate
from datetime import datetime
import io
from utils.check_market_cap_changes import MarketCapRanking
from commands.base_command import BCBaseCommand

class CheckMarketCapCommand(BCBaseCommand):

    def run(self):

        mcr = MarketCapRanking(100, 5)
        df_ranking = mcr.get_filter_rank()

        mcr_ = MarketCapRanking(20, 2)
        df_ranking_ = mcr_.get_filter_rank()

        return df_ranking, df_ranking_
    
    def pretty_print(self,
                     df :pd.DataFrame):

        try:
            data = f'```{tabulate(df, tablefmt="simple" , headers="keys", showindex=False, colalign=("centre",))}```' #show index false
        except:
            data = 'No hay cambios significativos en el ranking según MCap'
        return data