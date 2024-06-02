from tabulate import tabulate
import pandas as pd
from datetime import datetime, timedelta, timezone

from commands.base_command import BCBaseCommand

class OKRPortfolioPerformanceCommand(BCBaseCommand):

    def process_portfolio_performance_for_okr(self, portfolio_name, shift_period):
        start_period, end_period = self.bc_data_proxy.get_dates_for_okr(shift_period)

        processed_recommmendations, prices = self.bc_data_proxy.get_processed_recommendations_and_prices(portfolio_name, start_period, end_period)

        result = pd.DataFrame(
            [{'Nombre': portfolio_name.capitalize(),
              'Desde': processed_recommmendations.index[0],
              'Hasta': processed_recommmendations.index[-1],
              'Variacion': round(processed_recommmendations.performance[-1]-1, 4)  } ])

        return result

    def run(self, profiles, shift_period): 
        shift_period = int(shift_period)
        dfs = []
        for profile in profiles:
            dfs.append(self.process_portfolio_performance_for_okr(profile, shift_period))       
        performances = pd.concat(dfs)
        return performances

    def pretty_print(self, performances: pd.DataFrame):
        pretty_dates = lambda x: x.strftime("%d/%m/%Y, %H:%M")
        performances['Desde'] = performances['Desde'].apply(pretty_dates) 
        performances['Hasta'] = performances['Hasta'].apply(pretty_dates)         
        data = f'```{tabulate(performances, tablefmt="simple" , headers="keys", showindex=False, colalign=("centre",))}```'
        return data

