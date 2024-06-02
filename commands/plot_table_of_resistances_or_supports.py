import pandas as pd
from settings import USDT_PAIRS, BTC_PAIRS
from tabulate import tabulate

from commands.plot_resistance import PlotLastResistanceCommand
from commands.plot_support import PlotLastSupportCommand

class PlotMagicTable():
    
    def run(self, supports_or_resistances, quote): 
        pairs = USDT_PAIRS if quote == 'USDT' else BTC_PAIRS 
        timeframes = [1, 2, 4, 6, 12, 24]
        table = pd.DataFrame(columns=timeframes)
        for pair in pairs:
            signals = []
            for timeframe_in_hours in timeframes:  
                if supports_or_resistances == 'resistances':
                    signals = self.resistance_processor(timeframe_in_hours, pair, signals)
                elif supports_or_resistances == 'supports':
                    signals = self.support_processor(timeframe_in_hours, pair, signals)
                        
            name_of_row = pair.split('/')[0]
            table.loc[name_of_row] = pd.Series(signals, index=timeframes)
        table['Total'] = table[list(table.columns)].sum(axis=1)
        table = table.sort_values(by=['Total'], ascending=False)
        table.index.name = 'Pairs'
        return table
    
    def resistance_processor(self, timeframe_in_hours, pair, list_to_put_signals):
        processor = PlotLastResistanceCommand()
        processor = processor.create_processor_and_process_last_resistance(timeframe_in_hours, pair)
        try:
            price_state = 1 if processor.open_is_above_resistance() else 0
        except:
            price_state = -1
        list_to_put_signals.append(price_state)

        return list_to_put_signals
    
    def support_processor(self, timeframe_in_hours, pair, list_to_put_signals):
        processor = PlotLastSupportCommand()
        processor = processor.create_processor_and_process_last_support(timeframe_in_hours, pair)
        try:    
            price_state = 1 if processor.open_is_below_support() else 0
        except:
            price_state = -1
        list_to_put_signals.append(price_state)
        return list_to_put_signals
            
    def pretty_print(self, table: pd.DataFrame):
        data = f'```{tabulate(table, tablefmt="simple" , headers="keys", showindex=True, colalign=("centre",))}```'
        return data

        
