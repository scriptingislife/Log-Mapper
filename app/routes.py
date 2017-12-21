from flask import render_template
from app import app
import shelve
from os import path

@app.route('/')
@app.route('/map')
def index():

    stats = shelve.open(path.join(app.root_path, "stats.dict"))
    
    attempts = 0
    try:
        attempts = stats['total_attempts']
    except:
        pass

    ips = 0
    try:
        ips = stats['unique_ips']
    except:
        pass

    countries = 0
    try:
        countries = stats['unique_countries']
    except:
        pass

    stats.close()

    return render_template('index.html', total_logins=attempts, unique_addresses=ips, unique_countries=countries)

@app.route('/folium_map.html')
def getMap():
    return render_template('folium_map.html')
