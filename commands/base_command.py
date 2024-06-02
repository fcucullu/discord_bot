from utils.brainycore_dataproxy import BrainyCoreDataProxy
from utils.influx_dataproxy import InfluxDataProxy
import discord
from datetime import datetime, timedelta

class BCBaseCommand:
    def __init__(self, bc_data_proxy=None, influx_data_proxy=None):
        if bc_data_proxy is None:
            self.bc_data_proxy = BrainyCoreDataProxy.get_default_data_proxy()
        else:
            self.bc_data_proxy = bc_data_proxy
        
        if influx_data_proxy is None:
            self.influx_data_proxy = InfluxDataProxy.get_default_data_proxy()
        else:
            self.influx_data_proxy = influx_data_proxy
            
    def generate_embed_and_plot(self, plot_as_file):
        plot = discord.File(plot_as_file, filename="plot.png")
        embed = discord.Embed()
        embed.set_image(url="attachment://plot.png")
        return embed, plot
    
    def get_datetime_interval_for_requesting_recommendations(self, n_days_ending_today):
        end_date = datetime.today() +  timedelta(days=1)
        start_date = datetime.today() -  timedelta(days=n_days_ending_today)
        return start_date, end_date



