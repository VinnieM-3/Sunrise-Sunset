from sun_rise_set import sun_rise_set, dec_to_clk
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import matplotlib.ticker as tick
import argparse

# example
# -lat 40.716 -long -74 -elev 0 -peri "20200105 07:48" -sols "20191222 04:19" -std_tz -5 -dst_tz -4 -dst_start 20200308 -dst_end 20201101 -title "Sunrise / Sunset NYC, 2020"


parser = argparse.ArgumentParser()

parser.add_argument('-lat', '--latitude', help='latitude as a decimal value', required=True)
parser.add_argument('-long', '--longitude', help='longitude as a decimal value', required=True)
parser.add_argument('-elev', '--elevation', help='elevation in meters', required=True)
parser.add_argument('-peri', '--perihelion_date', help='date of perihelion in London YYYYMMDD HH:MM',
                    required=True)
parser.add_argument('-sols', '--solstice_date', help='date of previous solstice in London YYYYMMDD HH:MM',
                    required=True)
parser.add_argument('-std_tz', '--std_tz', help='Standard Timezone', required=True)
parser.add_argument('-dst_tz', '--dst_tz', help='DST Timezone', required=False, default=999)
parser.add_argument('-dst_start', '--dst_start_date', help='DST Start Date YYYYMMDD', required=False, default='')
parser.add_argument('-dst_end', '--dst_end_date', help='DST End Date YYYYMMDD', required=False, default='')
parser.add_argument('-title', '--title', help='Title of Plot', required=False, default='No Title')

args = parser.parse_args()
latitude = float(args.latitude)
longitude = float(args.longitude)
elevation = float(args.elevation)
peri_date = args.perihelion_date
sols_date = args.solstice_date
std_tz = float(args.std_tz)
dst_tz = float(args.dst_tz)
dst_start_date = args.dst_start_date
dst_end_date = args.dst_end_date
plot_title = args.title

data_dst = sun_rise_set(latitude, longitude, elevation, peri_date, sols_date, std_tz, dst_tz,
                        dst_start_date, dst_end_date)

year = datetime.strptime(peri_date, '%Y%m%d %H:%M').timetuple().tm_year
first_day = datetime.strptime(str(year) + '0101', '%Y%m%d').timetuple().tm_yday
last_day = datetime.strptime(str(year) + '1231', '%Y%m%d').timetuple().tm_yday
num_days = last_day - first_day + 1


# convert a time in decimal to 24-hour time
def dec_to_clk_ff(time_dec, i):
    return dec_to_clk(time_dec)


fig = plt.figure(figsize=(10, 6), num='Sunrise / Sunset')
plt.subplots_adjust(top=.925, left=0.100, right=.950, wspace=0.1)
gs = GridSpec(28, 28, figure=fig)

# date list for x axis of all plots
base = datetime.strptime(str(year) + '0101', '%Y%m%d')
date_list = [base + timedelta(days=x) for x in range(0, num_days)]

# main plot
y_rise = [i.sunrise_dec for i in data_dst]
y_set = [i.sunset_dec for i in data_dst]
y_solar_noon = [i.solar_noon_dec for i in data_dst]
ax_0_0 = plt.subplot(gs.new_subplotspec((0, 2), colspan=25, rowspan=10))
ax_0_0.set_title(plot_title)
ax_0_0.grid(which='major', linestyle='-', linewidth=0.5, color='grey')
ax_0_0.set_xlabel('Day of Year')
ax_0_0.xaxis.set_major_locator(mdates.MonthLocator())
ax_0_0.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
ax_0_0.xaxis.set_minor_locator(mdates.DayLocator())
ax_0_0.set_ylabel('Time (24-hour)')
ax_0_0.yaxis.set_major_formatter(tick.FuncFormatter(dec_to_clk_ff))
ax_0_0.set_ylim(0, 24)
ax_0_0.plot(date_list, y_rise, 'b')
ax_0_0.plot(date_list, y_set, 'r')
ax_0_0.plot(date_list, y_solar_noon, 'k-.', label='Solar Noon')
ax_0_0.legend(loc='best', fontsize='small')


# Day Length
day_length = [i.daylight_hours for i in data_dst]
ax_1_0 = plt.subplot(gs.new_subplotspec((16, 0), colspan=12, rowspan=12))
ax_1_0.set_title("Length of Day ")
ax_1_0.grid(which='major', linestyle='-', linewidth=0.5, color='grey')
ax_1_0.set_xlabel('Day of Year')
ax_1_0.xaxis.set_major_locator(mdates.MonthLocator())
ax_1_0.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
ax_1_0.set_ylabel('Time (hours)')
ax_1_0.plot(date_list, day_length, 'k')


# Sunrise Sunset Data
sunrise_roc = [i.sunrise_change_mins for i in data_dst]
sunset_roc = [i.sunset_change_mins for i in data_dst]
total_roc = [i.change_total_mins for i in data_dst]
ax_1_1 = plt.subplot(gs.new_subplotspec((16, 16), colspan=12, rowspan=12))
ax_1_1.set_title("Sunrise / Sunset Rate of Change\n- days getting shorter, + days getting longer")
ax_1_1.grid(which='major', linestyle='-', linewidth=0.5, color='grey')
ax_1_1.set_xlabel('Day of Year')
ax_1_1.xaxis.set_major_locator(mdates.MonthLocator())
ax_1_1.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
ax_1_1.set_ylabel('Time (mins)')
ax_1_1.plot(date_list, sunrise_roc, 'b--', label='Sunrise')
ax_1_1.plot(date_list, sunset_roc, 'r-.', label='Sunset')
ax_1_1.plot(date_list, total_roc, 'k', label='Total')
ax_1_1.legend(loc='best', fontsize='small')

plt.show()
