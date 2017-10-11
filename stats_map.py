import attempt
import timestamp
import re
import datetime
import sqlite3
from geoip import geolite2
#import geoip2

LOGFILE = "auth.log"
DATE = datetime.datetime.now()


#Create an Attempt object from a single line of the log file
def getLineInfo(line):
    atm = attempt.Attempt()

    line_ips = re.findall(r'[0-9]+(?:\.[0-9]+){3}',line)
    if len(line_ips) != 0:
        spline = line.split()
        
        month_hr = spline[0]
        day = spline[1]
        time = spline[2].split(":")
        
        stamp = timestamp.Timestamp(timestamp.month_num(month_hr), day, DATE.year, time[0], time[1], time[2])

        atm.ip = line_ips[0]
        atm.timestamp = stamp
    else:
        return None

    #Determine if a failure or successful login
    if "fail" in line.lower():
        atm.success = 0
    elif "accept" in line.lower():
        atm.success = 1
    else:
        return None
    
    #GeoIP Lookup
    atm.lookup = geolite2.lookup(line_ips[0])

    return atm


def getAttempts(filename, lst_attempts):
    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            atm = getLineInfo(line)
            if atm == None:
                continue
            lst_attempts.append(atm)
            #print(atm.summary())


def insertAttempt(db, atm):
    db.execute("INSERT INTO MARKERS (IP, STAMP, SUCCESS, COUNTRY, CONTINENT, LATITUDE, LONGITUDE) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}');".format(atm.ip, atm.timestamp.stamp(), atm.success, atm.lookup.country, atm.lookup.continent, atm.lookup.location[0], atm.lookup.location[1]))

def getColumn(db, col):
    return db.execute("SELECT {} from MARKERS".format(col))

def getIPs(db):
    ips = set(getColumn(db, "IP"))
    for ip in ips:
        print(ip[0])
    print("{} Unique IP Addresses".format(len(ips)))


def isUnique(stamps, atm):
    for stamp in stamps:
        if atm.timestamp.stamp() == stamp[0]:
            return False
    return True


def makeDB(db):
        db.execute('''CREATE TABLE MARKERS
                (IP CHAR(15) NOT NULL,
                STAMP DATETIME,
                SUCCESS INT,
                COUNTRY CHAR(2),
                CONTINENT CHAR(2),
                LATITUDE DOUBLE,
				LONGITUDE DOUBLE
                );''')


def main():
    db = sqlite3.connect("test.db")
    try:
        makeDB(db)
    except:
        pass

    #Get a list of timestamps to deduplicate
    stamps = list(getColumn(db, "STAMP"))

    #Insert unique attempts only
    print(attempt.print_header())
    attempts = list()
    getAttempts(LOGFILE, attempts)
    for atm in attempts:
        if isUnique(stamps, atm):
            try:
                insertAttempt(db, atm)
                print(atm.summary())
            except AttributeError as (errno, strerror):
                print("AttributeError ({}): {}".format(errno, strerror))
                continue
            except:
                print("Unexpected Error:")
                continue

    uniq_ips = len(set(getColumn(db, "IP")))
    print("{} Unique IP Addresses".format(uniq_ips))

    #Write changes to db
    db.commit()


    db.close()

if __name__ == "__main__":
    main()