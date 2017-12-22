######
#Create .html file using folium
######
import folium
from folium import plugins
import sqlite3

MAP_LOCATION = "app/templates/folium_map.html"

def draw():
    db = sqlite3.connect("test.db")
    folium_map = folium.Map(location=[24.635246, 2.616971], zoom_start=3, tiles='CartoDB dark_matter')

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

        make_marker(folium_map, ip, success, country, continent, latitude, longitude)

    try:
        folium_map.save(MAP_LOCATION)
    except Exception as e:
        print("ERROR: Saving to folium_map-backup.html")
        folium_map.save("folium_map-backup.html")

    folium_heatmap = folium.Map(location=[24.635246, 2.616971], zoom_start=3, tiles='CartoDB positron')

    plugins.HeatMap(zip(lats, lons)).add_to(folium_heatmap)
    plugins.HeatMap(zip(lats, lons)).add_to(folium_map)

    try:
        folium_map.save("app/templates/heatmap.html")
        #folium_heatmap.save("app/templates/heatmap.html")
    except Exception as e:
        print("ERROR: Saving to heatmap-backup.html")
        folium_heatmap.save("heatmap-backup.html")


def make_marker(map, ip, success, country, continent, latitude, longitude):
    print("Making marker for: "+ str(ip))
    popup_text = """{}<br>
                    Success: {}<br>
                    Country: {}<br>
                    Continent: {}<br>
                    Latitude: {}<br>
                    Longitude: {}<br>"""

    popup_text = popup_text.format(ip, success, country, continent, latitude, longitude)

    #Change marker color based on success/fail
    #Default is blue
    marker_color = "#3388ff"
    if success == False:
        marker_color = "#FA4848"
    elif success == True:
        marker_color = "#53F42E"

    folium.CircleMarker(location=[latitude, longitude], color=marker_color, fill=True, popup=popup_text, radius=2).add_to(map)

if __name__ == "__main__":
    draw()
