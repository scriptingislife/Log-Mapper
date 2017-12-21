######
#Get statistics for use in webpage
######
import sqlite3
import shelve

#SHELVE_DB = "app/stats"

def get_IPs(db):
    return int(list(db.execute("SELECT COUNT (DISTINCT IP) FROM MARKERS"))[0][0])

def get_countries(db):
    return int(list(db.execute("SELECT COUNT (DISTINCT COUNTRY) FROM MARKERS"))[0][0])

def get_attempts(db):
    return int(list(db.execute("SELECT COUNT (IP) FROM MARKERS"))[0][0])

def get(database, storage):
    get_db = sqlite3.connect(database)

    stats = shelve.open(storage)
    stats['unique_ips'] = get_IPs(get_db)
    stats['unique_countries'] = get_countries(get_db)
    stats['total_attempts'] = get_attempts(get_db)
    stats.close()
