import folium
import sqlite3

def draw():
    db = sqlite3.connect("test.db")
    folium_map = folium.Map(location=[24.635246, 2.616971], zoom_start=3, tiles='CartoDB dark_matter')

    #Get markers and make_marker for each
    #Doesn't include timestamp to get unique (DISTINCT) IP addresses
    stats = db.execute("SELECT DISTINCT IP, SUCCESS, COUNTRY, CONTINENT, LATITUDE, LONGITUDE from MARKERS")
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
        
        make_marker(folium_map, ip, success, country, continent, latitude, longitude)

    folium_map.save("folium_map.html")


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

    folium.CircleMarker(location=[latitude, longitude], color=marker_color, fill=True, popup=popup_text).add_to(map)

if __name__ == "__main__":
    draw()