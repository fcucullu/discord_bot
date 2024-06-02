from commands.trades_percentiles import PortfolioTradesPercentilesCommand

class OKRPortfolioTradesPercentilesCommand(PortfolioTradesPercentilesCommand):

    def run_okr(self, profiles, shift_period): 
        shift_period = int(shift_period)
        start_period, end_period = self.bc_data_proxy.get_dates_for_okr(shift_period)
        
        results = self.run(start_period.strftime("%d/%m/%Y"),
                           end_period.strftime("%d/%m/%Y"), 
                           profiles)
        return results
