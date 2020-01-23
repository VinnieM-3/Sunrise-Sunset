from sun_rise_set import sun_rise_set, dec_to_clk


def dc2(dec_time):
    return dec_to_clk(dec_time, 12, False)


# New York City
res_str_title = "NYC"
res_str = res_str_title + ": {0:}  Solar Noon = {1:}  Sunrise = {2:}  Sunset = {3:}  Daylight(hrs) = {4:5.3f}"
res_str += "  Sunrise Change (mins) = {5:5.3f}  Sunset Change (mins) = {6:5.3f}"
results = sun_rise_set(40.716, -74.017, 0, "20200105 07:48", "20191222 04:19", -5, -4, "20200308", "20201101")
for i in results:
    print(res_str.format(i.cal_date, dc2(i.solar_noon_dec), dc2(i.sunrise_dec), dc2(i.sunset_dec), i.daylight_hours,
                         i.sunrise_change_mins, i.sunset_change_mins))


# Sydney
res_str_title = "Sydney"
res_str = res_str_title + ": {0:}  Solar Noon = {1:}  Sunrise = {2:}  Sunset = {3:}  Daylight(hrs) = {4:5.3f}"
res_str += "  Sunrise Change (mins) = {5:5.3f}  Sunset Change (mins) = {6:5.3f}"
results = sun_rise_set(-33.867, 151.200, 0, "20200105 07:48", "20191222 04:19", 10, 11, "20201004", "20200405")
for i in results:
    print(res_str.format(i.cal_date, dc2(i.solar_noon_dec), dc2(i.sunrise_dec), dc2(i.sunset_dec), i.daylight_hours,
                         i.sunrise_change_mins, i.sunset_change_mins))


# Mexico City
res_str_title = "Mexico City"
res_str = res_str_title + ": {0:}  Solar Noon = {1:}  Sunrise = {2:}  Sunset = {3:}  Daylight(hrs) = {4:5.3f}"
res_str += "  Sunrise Change (mins) = {5:5.3f}  Sunset Change (mins) = {6:5.3f}"
results = sun_rise_set(19.4326, -99.1332, 0, "20200105 07:48", "20191222 04:19", -6, -5, "20200405", "20201025")
for i in results:
    print(res_str.format(i.cal_date, dc2(i.solar_noon_dec), dc2(i.sunrise_dec), dc2(i.sunset_dec), i.daylight_hours,
                         i.sunrise_change_mins, i.sunset_change_mins))


# Mumbai
res_str_title = "Mumbai"
res_str = res_str_title + ": {0:}  Solar Noon = {1:}  Sunrise = {2:}  Sunset = {3:}  Daylight(hrs) = {4:5.3f}"
res_str += "  Sunrise Change (mins) = {5:5.3f}  Sunset Change (mins) = {6:5.3f}"
results = sun_rise_set(18.95, 72.833, 0, "20200105 07:48", "20191222 04:19", 5.5)
for i in results:
    print(res_str.format(i.cal_date, dc2(i.solar_noon_dec), dc2(i.sunrise_dec), dc2(i.sunset_dec), i.daylight_hours,
                         i.sunrise_change_mins, i.sunset_change_mins))

