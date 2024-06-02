import pandas as pd
from datetime import datetime, timedelta

from commands.period_performances import PortfolioPeriodPerformanceCommand

class LastNDaysPortfolioPerformanceCommand(PortfolioPeriodPerformanceCommand):
    def run(self, profiles, n_days): 
        start_date, end_date = self.get_datetime_interval_for_requesting_recommendations(n_days)        
        dfs = []
        for profile in profiles:
                dfs.append(self.process_portfolio_performance(profile, start_date, end_date))       
        performances = pd.concat(dfs)
        return performances
