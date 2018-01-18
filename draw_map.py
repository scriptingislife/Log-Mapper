######
#Create .html file using folium
######
import folium
from folium import plugins
import sqlite3

MAP_LOCATION = "app/templates/folium_map.html"
HEATMAP_LOCATION = "app/templates/heatmap.html"

DB_FILE = "test.db"

def draw():
    db = sqlite3.connect(DB_FILE)
    folium_map = folium.Map(location=[24.635246, 2.616971], zoom_start=3, tiles='CartoDB dark_matter')
    folium_heatmap = folium.Map(location=[24.635246, 2.616971], zoom_start=3, tiles='CartoDB positron')

    #Get markers and make_marker for each
    #Doesn't include timestamp to get unique (DISTINCT) IP addresses
    stats = db.execute("SELECT DISTINCT IP, SUCCESS, COUNTRY, CONTINENT, LATITUDE, LONGITUDE from MARKERS")
    
    lats = list()
    lons = list()

    for stat in stats:
        ip = stat[0]
        success = stat[1]
        country = stat[2]
        continent = stat[3]
        latitude = stat[4]
        longitude = stat[5]
        if success == 0:
            success = False
        elif success == 1:
            success = True
        
        lats.append(latitude)
        lons.append(longitude)

        make_marker(folium_map, folium_heatmap, ip, success, country, continent, latitude, longitude)

    plugins.HeatMap(zip(lats, lons), radius=18).add_to(folium_heatmap)

    try:
        folium_map.save(MAP_LOCATION)
    except Exception as e:
        print("ERROR. Saving to folium_map-backup.html instead.")
        folium_map.save("folium_map-backup.html")

    try:
        folium_heatmap.save(HEATMAP_LOCATION)
    except Exception as e:
        print("ERROR. Saving to heatmap-backup.html instead.    ")
        map.save("heatmap-backup.html")


def make_marker(map, heatmap, ip, success, country, continent, latitude, longitude):
    print("Making marker for: "+ str(ip))

    #popup_text = "<a href='https://ipinfo.io/{}' target='_blank'>{}</a><br>\nSuccess: {}<br>\nCountry: {}<br>\nContinent: {}<br>\nLatitude: {}<br>\nLongitude: {}<br>"
    


    popup_text = """<a href=\"https://www.censys.io/ipv4/{}\" target=\"_blank\">{}</a><br>
                    Success: {}<br>
                    Country: {}<br>
                    Continent: {}<br>
                    Latitude: {}<br>
                    Longitude: {}<br>"""

    popup_text = popup_text.format(ip, ip, success, country, continent, latitude, longitude)

    #Change marker color based on success/fail
    #Default is blue
    marker_color = "#3388ff"
    if success == False:
        marker_color = "#FA4848"
    elif success == True:
        marker_color = "#53F42E"

    folium.CircleMarker(location=[latitude, longitude], radius=7, color=marker_color, fill=False, popup=popup_text).add_to(map)

    marker_color = "#3388ff"
    folium.CircleMarker(location=[latitude, longitude], radius=1, color=marker_color, fill=False, popup=popup_text).add_to(heatmap)

if __name__ == "__main__":
    draw()
