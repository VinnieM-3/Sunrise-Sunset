from sun_rise_set import sun_rise_set

# NYC
res_str_title = "NYC"
res_str = res_str_title + ": {0:}  Solar Noon = {1:}  Sunrise = {2:}  Sunset = {3:}  daylight_hours = {4:5.3f}"
res_str += "  sunrise_change_mins = {5:5.3f}   sunset_change_mins = {6:5.3f}"
results = sun_rise_set(40.716, -74.017, 0, "20200105 07:48", "20191222 04:19", -5, -4, "20200308", "20201101")
for i in results:
    print(res_str.format(i.cal_date, i.solar_noon_hrs, i.sunrise_hrs, i.sunset_hrs, i.daylight_hours,
                         i.sunrise_change_mins, i.sunset_change_mins))


# Sydney
res_str_title = "Sydney"
res_str = res_str_title + ": {0:}  Solar Noon = {1:}  Sunrise = {2:}  Sunset = {3:}  daylight_hours = {4:5.3f}"
res_str += "  sunrise_change_mins = {5:5.3f}   sunset_change_mins = {6:5.3f}"
results = sun_rise_set(-33.867, 151.200, 0, "20200105 07:48", "20191222 04:19", 10, 11, "20201004", "20200405")
for i in results:
    print(res_str.format(i.cal_date, i.solar_noon_hrs, i.sunrise_hrs, i.sunset_hrs, i.daylight_hours,
                         i.sunrise_change_mins, i.sunset_change_mins))


# Mexico City
res_str_title = "Mexico City"
res_str = res_str_title + ": {0:}  Solar Noon = {1:}  Sunrise = {2:}  Sunset = {3:}  daylight_hours = {4:5.3f}"
res_str += "  sunrise_change_mins = {5:5.3f}   sunset_change_mins = {6:5.3f}"
results = sun_rise_set(19.4326, -99.1332, 0, "20200105 07:48", "20191222 04:19", -6, -5, "20200405", "20201025")
for i in results:
    print(res_str.format(i.cal_date, i.solar_noon_hrs, i.sunrise_hrs, i.sunset_hrs, i.daylight_hours,
                         i.sunrise_change_mins, i.sunset_change_mins))
