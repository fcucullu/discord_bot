from tabulate import tabulate
import pandas as pd
from datetime import datetime

from commands.base_command import BCBaseCommand

class PairsPeriodMetricsCommand(BCBaseCommand):
    def process_pair_metrics(self, portfolio_name, start_date, end_date):
        metrics = self.bc_data_proxy.process_pair_metrics_for_period(portfolio_name, start_date, end_date)
        return metrics

    def run(self, start_date, end_date, portfolio_name): 
        start_date = datetime.strptime(start_date, '%d/%m/%Y')
        end_date = datetime.strptime(end_date, '%d/%m/%Y')
        metrics = self.process_pair_metrics(portfolio_name, start_date, end_date)
        return metrics

    def pretty_print(self, metrics: pd.DataFrame):
        max_columns = 5
        split_in = metrics.shape[1] // max_columns + 1
        dfs = []
        for split in range(0, split_in):
            rang = [n+max_columns*split for n in range(0,max_columns) if n+max_columns*split<metrics.shape[1]] 
            data = metrics.iloc[:, rang]
            data = f'```{tabulate(data, tablefmt="simple" , headers="keys", showindex=True, colalign=("centre",))}```'
            dfs.append(data)       
        return dfs

