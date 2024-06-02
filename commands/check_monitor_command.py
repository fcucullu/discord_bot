import pandas as pd
from tabulate import tabulate
from utils.check_monitor_indicator import CheckMonitor
from commands.base_command import BCBaseCommand


class CheckMonitorCommand(BCBaseCommand):
    def run(self, profile, currencies):

        list_of_currencies_by_profile = self.bc_data_proxy.get_portfolio_currencies(profile)
        portfolio_currency = self.bc_data_proxy.get_portfolio_currency(profile)

        list_of_currencies = list_of_currencies_by_profile
        if len(currencies) !=0:
            list_of_currencies = currencies

        monitor = CheckMonitor()
        info_monitor = monitor.get_monitor_info_for_all_timeframes(list_of_currencies, portfolio_currency)
        return info_monitor

    def pretty_print(self, df :pd.DataFrame):

        states = [
            CheckMonitor.RED_DOWN,
            CheckMonitor.RED_UP,
            CheckMonitor.GREEN_UP,
            CheckMonitor.GREEN_DOWN,
        ]
        try:
            data = "```"
            for s in states:
                filtered_df = df[df['4h'] == s]
                if len(filtered_df) > 0:
                    data += f"""

Pares {s} en 4hs
#################
"""
                    data += f'{tabulate(filtered_df, tablefmt="simple" , headers="keys", showindex=True, colalign=("centre",))}'
            data += "```"
        except:
            data = 'Algo anda mal, revisar cálculo de Monitor'
        return data

