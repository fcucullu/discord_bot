import pandas as pd
from datetime import datetime, timedelta

from commands.portfolio_period_metrics import PortfolioPeriodMetricsCommand

class LastPortfolioMetricsCommand(PortfolioPeriodMetricsCommand):
    def run(self, n_days, profiles): 
        start_date, end_date = self.get_datetime_interval_for_requesting_recommendations(n_days)
        dfs = []
        for profile in profiles:
            dfs.append(self.bc_data_proxy.process_portfolio_metrics_for_period(profile, start_date, end_date))       
        metrics = pd.concat(dfs, axis=1)
        return metrics
