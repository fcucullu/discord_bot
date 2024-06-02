import pandas as pd
from datetime import datetime, timedelta, date
import io
import matplotlib.pyplot as plt


from commands.base_command import BCBaseCommand

class PlotPairsPerformanceCommand(BCBaseCommand):
    def generate_list_of_plots(self, portfolio_name, start_date, end_date):
        plots = []
        pair_perfomances_list = self.bc_data_proxy.process_pair_performances_for_period(portfolio_name, start_date, end_date)

        for pair_name, df in pair_perfomances_list:
            pair_performance = (df.open.pct_change().fillna(0) + 1).cumprod()
            strategy_performance = df.performance

            data_stream = io.BytesIO()
    
            plt.figure(figsize=(15,8))
            plt.plot(pair_performance, label=pair_name, linewidth=1)
            plt.plot(strategy_performance, label=f"Performance over the pair", linewidth=2)            
            plt.legend(prop={'size': 10})
            plt.savefig(data_stream, format='png', bbox_inches="tight", dpi = 80)
            plt.close()
            data_stream.seek(0)
            plots.append(data_stream)
        
        return plots 
    
    def run(self, portfolio_name, n_days): 
        start_date, end_date = self.get_datetime_interval_for_requesting_recommendations(n_days)
        plots = self.generate_list_of_plots(portfolio_name, start_date, end_date)
        plots = [self.generate_embed_and_plot(plot_as_file) for plot_as_file in plots]

        return plots
