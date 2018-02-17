def lineup(text, length):
    line_len = length
    text = str(text)
    while len(text) <= line_len:
        text += " "
    return text[:(line_len - 1)] + " "

def print_header():
    header = lineup("IP ADDRESS", 20)
    header += lineup("TIMESTAMP", 25)
    header += lineup("SUCCESS", 10)
    header += lineup("COUNTRY", 10)
    header += lineup("CONTINENT", 10)
    #header += lineup("DIVISION", 10) 
    header += lineup("LATITUDE", 10) 
    header += lineup("LONGITUDE", 10)
    return header


class Attempt(object):
    ip = ""
    timestamp = None
    success = 0
    #country = "UD"
    #continent = "UD"
    #latitude = 0.0
    #longitude = 0.0
    lookup = None

    def __init__(self):
        pass

    def summary(self):
        if self.lookup == None:
            print("Uhhhh...")
            return
        if self.timestamp == None:
            print("Uhhhh....")
            return
        success_hr = ""
        if self.success == 0:
            success_hr = "FAIL"
        else:
            success_hr = "SUCCESS"
        #print(success_hr + " from {} at {}".format(self.ip, self.timestamp.stamp()))
        str_sum = lineup(self.ip, 20) 
        str_sum += lineup(self.timestamp.stamp(), 25)
        str_sum += lineup(success_hr, 10)
        str_sum += lineup(self.lookup.country, 10)
        str_sum += lineup(self.lookup.continent, 10)
        #str_sum += lineup(iter(self.lookup.subdivisions).next(), 10) 
        str_sum += lineup(self.lookup.location[0], 10) 
        str_sum += lineup(self.lookup.location[1], 10)
        return str_sum