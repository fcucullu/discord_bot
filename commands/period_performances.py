from tabulate import tabulate
import pandas as pd
from datetime import datetime

from commands.base_command import BCBaseCommand

class PortfolioPeriodPerformanceCommand(BCBaseCommand):
    def process_portfolio_performance(self, portfolio_name, start_date, end_date):
        performance = self.bc_data_proxy.process_portfolio_performance_for_period(portfolio_name, start_date, end_date)
        
        result = pd.DataFrame(
            [{'Nombre': portfolio_name.capitalize(),
              'Desde': performance.index[0],
              'Hasta': performance.index[-1],
              'Performance': performance.performance[-1]}])
        return result

    def run(self, start_date, end_date, profiles): 
        start_date = datetime.strptime(start_date, '%d/%m/%Y')
        end_date = datetime.strptime(end_date, '%d/%m/%Y')
        dfs = []
        for profile in profiles:
                dfs.append(self.process_portfolio_performance(profile, start_date, end_date))       
        performances = pd.concat(dfs)
        return performances

    def pretty_print(self, performances: pd.DataFrame):
        pretty_dates = lambda x: x.strftime("%d/%m/%Y, %H:%M")
        performances['Desde'] = performances['Desde'].apply(pretty_dates) 
        performances['Hasta'] = performances['Hasta'].apply(pretty_dates)         
        data = f'```{tabulate(performances, tablefmt="simple" , headers="keys", showindex=False, colalign=("centre",))}```'
        return data
