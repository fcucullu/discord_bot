from tabulate import tabulate
import pandas as pd
from datetime import datetime

from commands.base_command import BCBaseCommand

class PortfolioPeriodMetricsCommand(BCBaseCommand):
    def process_portfolio_metrics(self, portfolio_name, start_date, end_date):
        metrics = self.bc_data_proxy.process_portfolio_metrics_for_period(portfolio_name, start_date, end_date)
        return metrics

    def run(self, start_date, end_date, profiles): 
        start_date = datetime.strptime(start_date, '%d/%m/%Y')
        end_date = datetime.strptime(end_date, '%d/%m/%Y')
        dfs = []
        for profile in profiles:
            dfs.append(self.process_portfolio_metrics(profile, start_date, end_date))       
        metrics = pd.concat(dfs, axis=1)
        return metrics

    def pretty_print(self, metrics: pd.DataFrame):
        data = f'```{tabulate(metrics, tablefmt="simple" , headers="keys", showindex=True, colalign=("centre",))}```'
        return data
