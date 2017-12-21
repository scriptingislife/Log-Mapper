######
#Get statistics for use in webpage and write to shelve database
######
import sqlite3
import shelve
from os import path
from app import app

STATS_DATABASE = "app/stats.dict"

def get_IPs(db):
    return int(list(db.execute("SELECT COUNT (DISTINCT IP) FROM MARKERS"))[0][0])

def get_countries(db):
    return int(list(db.execute("SELECT COUNT (DISTINCT COUNTRY) FROM MARKERS"))[0][0])

def get_attempts(db):
    return int(list(db.execute("SELECT COUNT (IP) FROM MARKERS"))[0][0])

def get(database, storage):
    get_db = sqlite3.connect(database)

    stats = shelve.open(STATS_DATABASE)
    stats['unique_ips'] = get_IPs(get_db)
    stats['unique_countries'] = get_countries(get_db)
    stats['total_attempts'] = get_attempts(get_db)
    stats.close()

if __name__ == "__main__":
    get("test.db", path.join(app.root_path, "stats.dict"))
