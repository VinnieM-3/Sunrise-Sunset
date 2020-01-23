from __future__ import division
from math import pi, radians, pow, sin, asin, cos, acos, sqrt
from datetime import datetime, timedelta

e = 0.01671022              # earth orbit eccentricity
orb_per = 365.25696         # earth orbital period
axis_norm_degs = 23.4367    # angle between the earth's axis and the norm of the orbit
p_deg_factor = 1.032        # approx factor to multiply days between solstice and perihelion to calc p angle in deg


# Sources of formulas:
# [1]   Position of the Sun
#           https://en.wikipedia.org/wiki/Position_of_the_Sun
#           Declination of the Sun as seen from Earth
#           Calculations, 3rd "more accurate" formula
#
# [2]   EQUATION OF TIME - PROBLEM IN ASTRONOMY
#           M. Muller
#           Gymnasium Munchenstein Grellingerstrasse 5,
#           4142 Munchenstein, Switzerland
# [3]   Sunrise Equation
#           https://en.wikipedia.org/wiki/Sunrise_equation
#           Generalized equation
#           with "observations on a sea horizon needing an elevation-of-observer correction"


# Equation of time, based on source [2]
# inputs:
#   day_of_year     day of the year
#   p_degs          projection of the axis of the earth onto the plane of the orbit in degrees [2]
#   peri_day        calendar day in January of perihelion ( typically 3-5) (decimal/fractional format)
# outputs:
#   equation of time in minutes for the day of the year input
def _eot_mins(day_of_year, p_degs, peri_day):
    time_mins = (24*60) / (2*pi)
    p = radians(p_degs)
    axis_norm_rads = radians(axis_norm_degs)
    t1 = (axis_norm_rads/2)*(1 - 4*pow(e, 2))
    tan2_1_4e2 = (1 - cos(2*t1)) / (1 + cos(2*t1))
    tan2 = (1-cos(axis_norm_rads)) / (1 + cos(axis_norm_rads))
    e2 = 2*e
    tan2_2e = 2*e*tan2
    tan4_1_2 = (1/2)*pow(tan2, 2)
    e2_5_4 = (5/4)*(pow(e, 2))
    tan4_2e = 2*e*pow(tan2, 2)
    tan2_2e_13_4 = (13/4)*(pow(e, 2))*tan2
    tan6_1_3 = (1/3)*pow(tan2, 3)
    m = 2*pi*((day_of_year - peri_day)/orb_per)
    return -(tan2_1_4e2*sin(2*(m+p)) + e2*sin(m) -
             tan2_2e*sin(m + 2*p) + tan2_2e*sin(3*m + 2*p) +
             tan4_1_2*sin(4*(m+p)) + e2_5_4*sin(2*m) - tan4_2e*sin(3*m + 4*p) +
             tan4_2e*sin((5*m) + (4*p)) + tan2_2e_13_4*sin(4*m + 2*p) +
             tan6_1_3*sin(6*(m+p)))*time_mins


# Sun's declination, based on source [1]
# inputs:
#   day_of_year     day of the year
# outputs:
#   declination in radians for the day of the year input
def _declination(day_of_year):
    sin_axis_norm = sin(radians(axis_norm_degs))
    ratio360 = 360/orb_per
    ratio_pi_e = (360/pi)*e
    d_offset = day_of_year - 1
    return -(asin(sin_axis_norm *
                  cos(radians(ratio360*(d_offset+10) +
                              ratio_pi_e*sin(radians(ratio360*(d_offset-2)))))))


class Record(object):
    """ Used similar to a C struct """
    __slots__ = ['_cal_date', '_solar_noon_dec', '_sunrise_dec', '_sunset_dec', '_daylight_hours',
                 '_sunrise_change_mins', '_sunset_change_mins']

    def __init__(self, cal_date, solar_noon_dec, sunrise_dec, sunset_dec, daylight_hours,
                 sunrise_change_mins, sunset_change_mins):
        self._cal_date = cal_date
        self._solar_noon_dec = solar_noon_dec
        self._sunrise_dec = sunrise_dec
        self._sunset_dec = sunset_dec
        self._daylight_hours = daylight_hours
        self._sunrise_change_mins = sunrise_change_mins
        self._sunset_change_mins = sunset_change_mins

    @property
    def cal_date(self):
        return self._cal_date

    @property
    def solar_noon_dec(self):
        return self._solar_noon_dec

    @property
    def solar_noon_hrs(self):
        return dec_to_clk(self._solar_noon_dec)

    @property
    def sunrise_dec(self):
        return self._sunrise_dec

    @property
    def sunrise_hrs(self):
        return dec_to_clk(self._sunrise_dec)

    @property
    def sunset_dec(self):
        return self._sunset_dec

    @property
    def sunset_hrs(self):
        return dec_to_clk(self._sunset_dec)

    @property
    def daylight_hours(self):
        return self._daylight_hours

    @property
    def sunrise_change_mins(self):
        return self._sunrise_change_mins

    @property
    def sunset_change_mins(self):
        return self._sunset_change_mins

    @property
    def change_total_mins(self):
        return self._sunrise_change_mins + self._sunset_change_mins


# Sunrise Sunset Data, based on source [3]
# inputs:
#   latitude            your latitude in decimal format
#   longitude           your longitude in decimal format
#   elevation           your elevation in meters
#   peri_date           date of perihelion in London YYYYMMDD HH:MM'
#   sols_date           date of previous solstice in London YYYYMMDD HH:MM'
#   std_tz              standard timezone
#   dst_tz              DST timezone
#   dst_start_date      DST start date YYYYMMDD
#   dst_end_date        DST End Date YYYYMMDD
# outputs:
#   Records             see Record object
def sun_rise_set(latitude, longitude, elevation, peri_date, sols_date, std_tz, dst_tz=999,
                 dst_start_date='', dst_end_date=''):

    results = []

    year = datetime.strptime(peri_date, '%Y%m%d %H:%M').timetuple().tm_year
    first_day = datetime.strptime(str(year)+'0101', '%Y%m%d').timetuple().tm_yday
    last_day = datetime.strptime(str(year)+'1231', '%Y%m%d').timetuple().tm_yday
    num_days = last_day - first_day + 1

    peri_day_part = datetime.strptime(peri_date, '%Y%m%d %H:%M').timetuple().tm_yday  # or tm_mday, same ans for Jan
    peri_min_part = datetime.strptime(peri_date, '%Y%m%d %H:%M').timetuple().tm_min

    peri_day = peri_day_part + peri_min_part/1440
    peri_datetime = datetime.strptime(peri_date, '%Y%m%d %H:%M')
    sols_datetime = datetime.strptime(sols_date, '%Y%m%d %H:%M')
    diff = peri_datetime - sols_datetime
    p_degs = (diff.total_seconds()/(60*60*24))*p_deg_factor

    tz_list = []
    if dst_start_date == '':
        for i in range(1, num_days+1):
            tz_list.append(std_tz)
    else:
        dst_start_day = datetime.strptime(dst_start_date, '%Y%m%d').timetuple().tm_yday
        dst_end_day = datetime.strptime(dst_end_date, '%Y%m%d').timetuple().tm_yday
        if dst_end_day >= dst_start_day:
            for i in range(1, num_days+1):
                if i < dst_start_day or i >= dst_end_day:
                    tz_list.append(std_tz)
                else:
                    tz_list.append(dst_tz)
        else:
            for i in range(1, num_days+1):
                if i < dst_end_day or i >= dst_start_day:
                    tz_list.append(dst_tz)
                else:
                    tz_list.append(std_tz)

    # correction for refraction
    center_solar_disc = -0.83
    elevation_correction = -2.076*sqrt(elevation/60)
    a = radians(center_solar_disc + elevation_correction)

    b = radians(latitude)

    # correction for specific longitude (i.e. not being directly on the timezone meridian)
    longitude_correction_hrs = (std_tz * 15 - longitude) / 15

    prev_sunrise_dec_no_dst = 0
    prev_sunset_dec_no_dst = 0
    day_num = 1
    for tz in tz_list:

        if day_num == 1:  # set initial values for previous sunrise, sunset, and tz change
            c = _declination(0 + 0.5 - (longitude / 360))
            w = acos((sin(a) - sin(b) * sin(c)) / (cos(b) * cos(c)))
            w_degs = w * 360 / (2 * pi)
            w_hrs = w_degs / 15
            eot_correction_hrs = _eot_mins(0 + 0.5 - (longitude / 360), p_degs, peri_day) / 60
            solar_noon_dec_no_dst = 12 - eot_correction_hrs + longitude_correction_hrs
            prev_sunrise_dec_no_dst = solar_noon_dec_no_dst - w_hrs
            prev_sunset_dec_no_dst = solar_noon_dec_no_dst + w_hrs

        c = _declination(day_num + 0.5 - (longitude / 360))
        w = acos((sin(a) - sin(b) * sin(c)) / (cos(b) * cos(c)))
        w_degs = w*360/(2*pi)
        w_hrs = w_degs/15
        eot_correction_hrs = _eot_mins(day_num + 0.5 - (longitude / 360), p_degs, peri_day) / 60
        dst_correction = tz - std_tz

        cal_date = (datetime(year, 1, 1) + timedelta(day_num-1)).strftime("%b %d %Y")
        solar_noon_dec_no_dst = 12 - eot_correction_hrs + longitude_correction_hrs
        solar_noon_dec = solar_noon_dec_no_dst + dst_correction

        sunrise_dec = solar_noon_dec - w_hrs
        sunset_dec = solar_noon_dec + w_hrs
        daylight_hours = sunset_dec - sunrise_dec

        sunrise_change = (prev_sunrise_dec_no_dst - (solar_noon_dec_no_dst - w_hrs))*60
        sunset_change = ((solar_noon_dec_no_dst + w_hrs) - prev_sunset_dec_no_dst)*60
        prev_sunrise_dec_no_dst = solar_noon_dec_no_dst - w_hrs
        prev_sunset_dec_no_dst = solar_noon_dec_no_dst + w_hrs

        rec = Record(cal_date, solar_noon_dec, sunrise_dec, sunset_dec, daylight_hours, sunrise_change, sunset_change)
        results.append(rec)

        day_num += 1

    return results


# Converts decimal time to clock time (e.g. 11.5 -> 11:30AM)
# inputs:
#   decimal time
# outputs:
#   clock time
def dec_to_clk(time_dec, format_12_24=24, secs_on=True, fixed_width=True):
    int_hours = int(time_dec)//1
    int_mins = int(time_dec % 1 * 60)//1
    int_secs = int((time_dec % 1 * 60) % 1 * 60) // 1

    if not secs_on:
        if int_secs >= 30:
            int_mins += 1
            if int_mins == 60:
                int_mins = 0
                int_hours += 1

    if int_hours < 12:
        str_am_pm = 'AM'
    else:
        str_am_pm = 'PM'

    str_secs = str(int_secs)
    if (len(str_secs)) == 1:
        str_secs = "0" + str_secs

    str_mins = str(int_mins)
    if (len(str_mins)) == 1:
        str_mins = "0" + str_mins

    str_hours = str(int_hours)
    if format_12_24 == 24:
        if (len(str_hours)) == 1:
            str_hours = "0" + str_hours
    else:
        if int_hours < 1:
            str_hours = '12'
        elif int_hours >= 13:
            str_hours = str(int_hours - 12)

        if fixed_width:
            if (len(str_hours)) == 1:
                str_hours = " " + str_hours

    time_clk = str_hours + ":" + str_mins
    if secs_on:
        time_clk = time_clk + ':' + str_secs

    if format_12_24 == 12:
        time_clk += str_am_pm

    return time_clk
