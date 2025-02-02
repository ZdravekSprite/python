from datetime import datetime as dt
from datetime import timedelta as td
import time

def toYearFraction(date):
    def sinceEpoch(date): # returns seconds since epoch
        return time.mktime(date.timetuple())
    s = sinceEpoch

    year = date.year
    startOfThisYear = dt(year=year, month=1, day=1)
    startOfNextYear = dt(year=year+1, month=1, day=1)

    yearElapsed = s(date) - s(startOfThisYear)
    yearDuration = s(startOfNextYear) - s(startOfThisYear)
    fraction = yearElapsed/yearDuration

    return date.year + fraction

def diffYearFraction(date1,date2):
    start_date = date1 if date2 > date1 else date2
    end_date = (date2 + td(days=1)) if date2 > date1 else (date1 + td(days=1))
    return toYearFraction(end_date)-toYearFraction(start_date)

def strptimeDiffYearFraction(date_str1,date_str2,date_format):
    date1 = dt.strptime(date_str1,date_format)
    date2 = dt.strptime(date_str2,date_format)
    start_date = date1 if date2 > date1 else date2
    end_date = (date2 + td(days=1)) if date2 > date1 else (date1 + td(days=1))
    return toYearFraction(end_date)-toYearFraction(start_date)

def main():
    # decimalna dio godine od početka te godine
    #print(toYearFraction(dt.now()))

    date_format = '%d.%m.%Y.'
    start_date_str = '1.12.2003.'
    end_date_str = '19.3.2020.'
    date_list = [
        ('1.12.2003.','19.3.2020.'),
        ('11.11.2020.','28.2.2022.'),
        ('1.3.2022.','31.5.2022.'),
        ('1.6.2022.','2.2.2025.'),
        ]
    date_list_out = [
        ('1.12.2003.','19.3.2020.'),
        ('11.11.2020.','28.2.2022.')
        ]
    date_list_in = [
        ('1.3.2022.','31.5.2022.'),
        ('1.6.2022.','2.2.2025.')
        ]
    #start_date = dt.strptime(start_date_str,date_format)
    #end_date = dt.strptime(end_date_str,date_format) + td(days=1)
    #print(start_date,end_date)
    #print(toYearFraction(end_date)-toYearFraction(start_date))
    #print(strptimeDiffYearFraction(start_date_str,end_date_str,date_format))

    #for t in date_list:
    #    print(strptimeDiffYearFraction(t[0],t[1],date_format))

    y_out = 0
    for t in date_list_out:
        y_out += strptimeDiffYearFraction(t[0],t[1],date_format)
    
    y_in = 0
    for t in date_list_in:
        y_in += strptimeDiffYearFraction(t[0],t[1],date_format)

    print(y_out,y_in)
    print((y_out/2+y_in)/3)
    
if __name__ == "__main__":
    main()
