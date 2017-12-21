######
#Parse log file and write data to database
######
import os
import re
import datetime
import sqlite3
from geoip import geolite2
import plotter
import attempt
import timestamp
import get_stats as gs
import draw_map
#import geojson

LOGFILE = "auth.log"
IP_DATABASE = "test.db"
#Use real log file if on Linux. Not cyg-win
#if os.name == "posix":
#   LOGFILE = os.path.abspath("/var/log/auth.log")
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

    #GeoIP Lookup
    atm.lookup = geolite2.lookup(line_ips[0])
    if atm.lookup == None:
        return None

    #Determine if a failure or successful login
    if "fail" in line.lower():
        atm.success = 0
    elif "accept" in line.lower():
        atm.success = 1
    else:
        return None
    
    return atm


def getAttempts(filename, lst_attempts):
    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            atm = getLineInfo(line)
            if atm == None:
                continue
            lst_attempts.append(atm)
            print(atm.summary())


def insertAttempt(db, atm):
    db.execute("INSERT INTO MARKERS (IP, STAMP, SUCCESS, COUNTRY, CONTINENT, LATITUDE, LONGITUDE) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}');".format(atm.ip, atm.timestamp.stamp(), atm.success, atm.lookup.country, atm.lookup.continent, atm.lookup.location[0], atm.lookup.location[1]))

def getColumn(db, col):
    return db.execute("SELECT {} from MARKERS".format(col))

def getIPs(db):
    ips = set(getColumn(db, "IP"))
    for ip in ips:
        print(ip[0])
    print("{} Unique IP Addresses".format(len(ips)))


def getCoordinates(db):
    lats = list()
    lons = list()
    db_coords = db.execute("SELECT DISTINCT LATITUDE, LONGITUDE from MARKERS")
    for coord in db_coords:
        lats.append(float(coord[0]))
        lons.append(float(coord[1]))
    return (lats, lons)

def isUnique(stamps, atm):
    for stamp in stamps:
        if atm.timestamp.stamp() == stamp[0]:
            return False
    return True

def ipSummary(db):
    #Get IP stats
    uniq_ips = len(list(db.execute("SELECT DISTINCT IP FROM MARKERS")))
    all_ips = list(db.execute("SELECT COUNT(IP) FROM MARKERS"))[0][0]
    return "{} IPs / {} Attempts".format(uniq_ips, all_ips)

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
    db = sqlite3.connect(IP_DATABASE)
    #Attempt to make database, suppress error if it already exists
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
                #print(atm.summary())
            except AttributeError as e:
                print("AttributeError. Skipping. IP Address is {}\n{}".format(atm.ip, e))
                continue
            except Exception as e:
                print("Unexpected Error. Skipping. IP Address is {}\n{}".format(atm.ip, e))
                continue

    #print(ipSummary(db))

    coords = getCoordinates(db)

    #Write changes to db
    db.commit()
    db.close()

    plotter.plot(coords[0], coords[1])

    #Run stats_map with python2. Draw map with python3.
    #draw_map.draw()

    gs.get(IP_DATABASE, gs.STATS_DATABASE)




if __name__ == "__main__":
    main()
