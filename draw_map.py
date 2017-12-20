import folium
import sqlite3

def draw():
    db = sqlite3.connect("test.db")
    folium_map = folium.Map(location=[24.635246, 2.616971], zoom_start=3, tiles='CartoDB dark_matter')

    #Get markers and make_marker for each
    stats = db.execute("SELECT DISTINCT IP, STAMP, SUCCESS, COUNTRY, CONTINENT, LATITUDE, LONGITUDE from MARKERS")
    for stat in stats:
        ip = stat[0]
        stamp = stat[1]
        success = stat[2]
        country = stat[3]
        continent = stat[4]
        latitude = stat[5]
        longitude = stat[6]
        if success == 0:
            success = False
        elif success == 1:
            success = True
        
        make_marker(folium_map, ip, stamp, success, country, continent, latitude, longitude)

    folium_map.save("folium_map.html")


def make_marker(map, ip, stamp, success, country, continent, latitude, longitude):
    print("Making marker for: "+ str(ip))
    popup_text = """{}<br>
                    Timestamp: {}<br>
                    Success: {}<br>
                    Country: {}<br>
                    Continent: {}<br>
                    Latitude: {}<br>
                    Longitude: {}<br>"""

    popup_text = popup_text.format(ip, stamp, success, country, continent, latitude, longitude)

    folium.CircleMarker(location=[latitude, longitude], fill=True, popup=popup_text).add_to(map)

if __name__ == "__main__":
    draw()