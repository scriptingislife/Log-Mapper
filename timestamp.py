def month_num(month_txt):
    month_txt = month_txt.upper()
    try:
        month_rt = {
        'JAN' : 1,
        'FEB' : 2,
        'MAR' : 3,
        'APR' : 4,
        'MAY' : 5,
        'JUN' : 6,
        'JUL' : 7,
        'AUG' : 8,
        'SEP' : 9,
        'OCT' : 10,
        'NOV' : 11,
        'DEC' : 12
        }[month_txt]
    except KeyError:
        month_rt = "UND"
    return month_rt

def month_txt(month_num):
    try:
        month_rt = {
        1 : "JAN",
        2 : "FEB",
        3 : "MAR",
        4 : "APR",
        5 : "MAY",
        6 : "JUN",
        7 : "JUL",
        8 : "AUG",
        9 : "SEP",
        10 : "OCT",
        11 : "NOV",
        12 : "DEC"
        }[month_txt]
    except KeyError:
        month_rt = 0
    return month_rt

def fill(num, length):
    return str(num).zfill(length)

class Timestamp(object):
    month = 1
    day = 1
    year = 2000
    hour = 0
    minute = 0
    second = 0

    def __init__(self, month, day, year, hour, minute, second):
        self.month = month
        self.day = day
        self.year = year
        self.hour = hour
        self.minute = minute
        self.second = second

    def hreadable(self):
        return "{} {}, {} {}:{}:{}".format(month_num(self.month), self.day, self.year, self.hour, self.minute, self.second)

    def stamp(self):
        return "{}-{}-{} {}:{}:{}".format(fill(self.year, 4), fill(self.month, 2), fill(self.day, 2), fill(self.hour, 2), fill(self.minute, 2), fill(self.second, 2))