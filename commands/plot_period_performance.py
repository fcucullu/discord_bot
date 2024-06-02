import pandas as pd
from datetime import datetime
import io
import matplotlib.pyplot as plt

from commands.base_command import BCBaseCommand

class PlotPortfolioPeriodPerformanceCommand(BCBaseCommand):
    def process_portfolio_performance(self, portfolio_name, start_date, end_date):
        performance = self.bc_data_proxy.process_portfolio_performance_for_period(portfolio_name, start_date, end_date)
        
        result = pd.DataFrame({
            f'{portfolio_name.capitalize()}': performance.performance
            })
        return result

    def generate_plot(self, data_to_plot):
        data_stream = io.BytesIO()
    
        plt.figure(figsize=(15,8))
        for column in data_to_plot.columns:
            plt.plot(data_to_plot[column], label= column, linewidth=2)
        plt.legend(prop={'size': 10})
        plt.savefig(data_stream, format='png', bbox_inches="tight", dpi = 80)
        plt.close()
        data_stream.seek(0)
        return data_stream
    
    def run(self, start_date, end_date, profiles): 
        start_date = datetime.strptime(start_date, '%d/%m/%Y')
        end_date = datetime.strptime(end_date, '%d/%m/%Y')
        dfs = []
        for profile in profiles:
                dfs.append(self.process_portfolio_performance(profile, start_date, end_date))       
        performances = pd.concat(dfs)
        plot_as_file = self.generate_plot(performances)
        return self.generate_embed_and_plot(plot_as_file)

class PlotNDaysPerformanceCommand(PlotPortfolioPeriodPerformanceCommand):

    def run(self, n_days, profiles): 
        start_date, end_date = self.get_datetime_interval_for_requesting_recommendations(n_days)
        dfs = []
        for profile in profiles:
                dfs.append(self.process_portfolio_performance(profile, start_date, end_date))       
        performances = pd.concat(dfs)
        plot_as_file = self.generate_plot(performances)
        return self.generate_embed_and_plot(plot_as_file)
