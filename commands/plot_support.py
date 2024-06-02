import pandas as pd
from datetime import datetime
import io
import matplotlib.pyplot as plt

from commands.base_command import BCBaseCommand

from utils.candlestick import CandlestickRepository
from utils.supports import SupportsProcessor
from settings import ORCA_PATH, USDT_PAIRS, BTC_PAIRS, INFLUX_DB_NAME, INFLUX_HOST, INFLUX_PORT
import plotly
plotly.io.orca.config.executable = ORCA_PATH
from datetime import datetime


class PlotLastSupportCommand(BCBaseCommand):

    def create_processor_and_process_last_support(self, timeframe_in_hours, pair):
        s_processor = SupportsProcessor(short_pp_pct=0.02, long_pp_pct=0.05)
        start_date = s_processor.get_start_date_based_on_timeframe(timeframe_in_hours)
        repo = CandlestickRepository(INFLUX_DB_NAME, INFLUX_HOST, INFLUX_PORT)
        candles = repo.get_candlestick(pair, "binance", 60 * timeframe_in_hours, start_date, datetime.utcnow())

        if len(candles) == 0:
            raise ValueError(f"No hay datos para {pair}. Si te parece importante el par, hablá con I+D y lo agregamos.")

        s_processor.process_last_support(candles)
        return s_processor

    def generate_plot_as_file(self, s_processor, timeframe_in_hours, pair):
        fig = s_processor._plot_support_for_BCC_core(f"Último Soporte detectado para {pair}", pair, timeframe_in_hours=timeframe_in_hours)
        binary_image_string = fig.to_image(format='png')
        plot_as_file = io.BytesIO(binary_image_string)
        plot_as_file.seek(0)

        return plot_as_file

    def run(self, timeframe_in_hours, pair): 
        s_processor = self.create_processor_and_process_last_support(timeframe_in_hours, pair)
        plot_as_file = self.generate_plot_as_file(s_processor, timeframe_in_hours, pair)

        return self.generate_embed_and_plot(plot_as_file)


class PlotSupportAllTimeframesCommand(PlotLastSupportCommand):

    def run(self, pair): 
        for timeframe_in_hours in [1, 2, 4, 6, 12, 24]:
            s_processor = self.create_processor_and_process_last_support(timeframe_in_hours, pair)
            plot_as_file = self.generate_plot_as_file(s_processor, timeframe_in_hours, pair)
            yield self.generate_embed_and_plot(plot_as_file)
    

class PlotSupportAllPairs(PlotLastSupportCommand):

    def run(self, quote, timeframe_in_hours): 
        pairs = USDT_PAIRS if quote == 'USDT' else BTC_PAIRS 
        for pair in pairs:
            s_processor = self.create_processor_and_process_last_support(timeframe_in_hours, pair)
            plot_as_file = self.generate_plot_as_file(s_processor, timeframe_in_hours, pair)
            yield self.generate_embed_and_plot(plot_as_file)
