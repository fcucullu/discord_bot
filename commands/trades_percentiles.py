from tabulate import tabulate
import pandas as pd
from datetime import datetime
import io
import matplotlib.pyplot as plt

from commands.base_command import BCBaseCommand

class PortfolioTradesPercentilesCommand(BCBaseCommand):
    
    def run(self, start_date, end_date, profiles): 
        start_date = datetime.strptime(start_date, '%d/%m/%Y')
        end_date = datetime.strptime(end_date, '%d/%m/%Y')
        dfs_for_describe, dfs_for_histogram = [], []
        for profile in profiles:
            result_original = self.bc_data_proxy.process_portfolio_trades(profile, start_date, end_date).Trades
            result_original = result_original.rename(f'{profile.capitalize()}')
            result_original = pd.DataFrame(result_original)
            
            dfs_for_describe.append(result_original.describe())       
            dfs_for_histogram.append(result_original.reset_index(drop=True))       
        dfs_for_describe = pd.concat(dfs_for_describe, axis=1)
        dfs_for_histogram = pd.concat(dfs_for_histogram, axis=1)
        
        plots = self.generate_list_of_plots(dfs_for_histogram)
        plots = [self.generate_embed_and_plot(plot_as_file) for plot_as_file in plots]
                
        return dfs_for_describe, plots
    
    def pretty_print(self, df):
        data = f'```{tabulate(df, tablefmt="simple" , headers="keys", showindex=True, colalign=("centre",))}```'
        return data

    def generate_list_of_plots(self, data_to_plot):
        plots = []
        
        for column in data_to_plot.columns:
            data_stream = io.BytesIO()
            
            plt.figure(figsize=(15,8))
            plt.title(f'{column}')
            plt.hist(data_to_plot[column], bins=20)
            plt.savefig(data_stream, format='png', bbox_inches="tight", dpi = 80)
            plt.close()
            data_stream.seek(0)
            plots.append(data_stream)
        return plots
    