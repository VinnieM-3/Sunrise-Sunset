from sun_rise_set import sun_rise_set, dec_to_clk
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import matplotlib.ticker as tick


# Sydney, 2020
year = 2020
plot_title = "Sydney, 2020"
results = sun_rise_set(-33.8688, -151.2093, 0, "20200105 07:48", "20191222 04:19", 10, 11, "20201004", "20200405")


# no need to change anything past this point:

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
y_rise = [i.sunrise_dec for i in results]
y_set = [i.sunset_dec for i in results]
y_solar_noon = [i.solar_noon_dec for i in results]
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
day_length = [i.daylight_hours for i in results]
ax_1_0 = plt.subplot(gs.new_subplotspec((16, 0), colspan=12, rowspan=12))
ax_1_0.set_title("Length of Day ")
ax_1_0.grid(which='major', linestyle='-', linewidth=0.5, color='grey')
ax_1_0.set_xlabel('Day of Year')
ax_1_0.xaxis.set_major_locator(mdates.MonthLocator())
ax_1_0.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
ax_1_0.set_ylabel('Time (hours)')
ax_1_0.plot(date_list, day_length, 'k')


# Sunrise Sunset Data
sunrise_roc = [i.sunrise_change_mins for i in results]
sunset_roc = [i.sunset_change_mins for i in results]
total_roc = [i.change_total_mins for i in results]
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
