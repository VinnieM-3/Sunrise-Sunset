import argparse
from sun_rise_set import sun_rise_set, dec_to_clk

# example
# -lat 40.716 -long -74 -elev 0 -peri "20200105 07:48" -sols "20191222 04:19" -std_tz -5 -dst_tz -4 -dst_start 20200308 -dst_end 20201101 -title "NYC"

parser = argparse.ArgumentParser()

parser.add_argument('-lat', '--latitude', help='latitude, decimal value, North is positive', required=True)
parser.add_argument('-long', '--longitude', help='longitude, decimal value, West is positive', required=True)
parser.add_argument('-elev', '--elevation', help='elevation in meters', required=True)
parser.add_argument('-peri', '--perihelion_date', help='date/time of perihelion YYYYMMDD HH:MM', required=True)
parser.add_argument('-sols', '--solstice_date', help='date/time of previous solstice YYYYMMDD HH:MM', required=True)
parser.add_argument('-std_tz', '--std_tz', help='Standard Timezone', required=True)
parser.add_argument('-dst_tz', '--dst_tz', help='DST Timezone', required=False, default=999)
parser.add_argument('-dst_start', '--dst_start_date', help='DST Start Date YYYYMMDD',  required=False, default='')
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
res_str_title = args.title


def dc2(dec_time):
    return dec_to_clk(dec_time, 12, False)


results = sun_rise_set(latitude, longitude, elevation, peri_date, sols_date, std_tz, dst_tz,
                       dst_start_date, dst_end_date)

res_str = res_str_title + ": {0:}  Solar Noon = {1:}  Sunrise = {2:}  Sunset = {3:}  Daylight(hrs) = {4:5.3f}"
res_str += "  Sunrise Change (mins) = {5:5.3f}  Sunset Change (mins) = {6:5.3f}"
for i in results:
    print(res_str.format(i.cal_date, dc2(i.solar_noon_dec), dc2(i.sunrise_dec), dc2(i.sunset_dec), i.daylight_hours,
                         i.sunrise_change_mins, i.sunset_change_mins))
