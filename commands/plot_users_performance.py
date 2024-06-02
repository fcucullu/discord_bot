import io
from datetime import datetime
import matplotlib.pyplot as plt

from commands.base_command import BCBaseCommand

class PlotUsersPerformanceCommand(BCBaseCommand):

    def run(self, start_date, original_end_date, acceptance_percentage, profiles): 
        start_date = datetime.strptime(start_date, '%d/%m/%Y')
        end_date = datetime.strptime(original_end_date, '%d/%m/%Y')
        histograms, alert_messages, quantity_messages = [], [], []
        for profile in profiles:
            users_performance, funds_quantity = self.influx_data_proxy.get_funds_performance_for_period(profile, start_date, end_date)
            users_performance = users_performance.real_performance
            theoric_performance = self.bc_data_proxy.process_portfolio_performance_for_period(profile, start_date, end_date).performance[-1]-1
            alert = self.check_dispersion_in_users_performance(acceptance_percentage, profile, users_performance, theoric_performance)
            if alert is not None:
                alert_messages.append(alert)
            quantity_messages.append(self.build_funds_quantity_message(profile, funds_quantity, original_end_date, users_performance))
            plot = self.generate_histogram(acceptance_percentage, profile, users_performance, theoric_performance)
            histograms.append(plot)
        histograms = [self.generate_embed_and_plot(plot_as_file) for plot_as_file in histograms]
        return histograms, alert_messages, quantity_messages

    def generate_histogram(self, acceptance_percentage, profile, users_performance, theoric_performance):  
        xlimits = self.get_acceptance_interval(acceptance_percentage, theoric_performance)
        
        data_stream = io.BytesIO()
        plt.figure(figsize=(10,8))
        plt.title(f'{profile.capitalize()}', fontsize= 15)
        plt.hist(users_performance, bins=100, label='Real Funds')
        plt.axvline(theoric_performance, color='k', linestyle='dashed', linewidth=2, label='Theoric')
        plt.axvline(users_performance.mean(), color='b', linestyle='dotted', linewidth=2, label='Real Mean')        
        plt.xlim(xmin=xlimits[0], xmax=xlimits[1])
        plt.legend(prop={'size': 15})
        plt.savefig(data_stream, format='png', bbox_inches="tight", dpi = 80)
        plt.close()
        data_stream.seek(0)
        return data_stream
    
    def check_dispersion_in_users_performance(self, acceptance_percentage, profile, users_performance, theoric_performance):
        acceptance_interval = self.get_acceptance_interval(acceptance_percentage, theoric_performance)
        outlier_condition = (users_performance < acceptance_interval[0]) | (users_performance > acceptance_interval[1])
        number_of_outliers = len(outlier_condition.loc[outlier_condition == True])
        if number_of_outliers > 0:
            msg = f':warning: ALERTA: Hay {number_of_outliers} fondos de los {len(outlier_condition)} en {profile.capitalize()} cuya performance difiere más de un {acceptance_percentage}% respecto del teórico.'
            return msg
        
    def build_funds_quantity_message(self, profile, funds_quantity, end_date, users_performance):
        return f'Al {end_date} había {funds_quantity} fondos activos en el perfil {profile}, pero sólo {len(users_performance)} estuvieron activos en todo el período seleccionado.'
        
    def get_acceptance_interval(self, acceptance_percentage, centre):
        return [centre - acceptance_percentage/100, centre + acceptance_percentage/100]
