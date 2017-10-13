import gmplot
from bs4 import BeautifulSoup

APIKEY = ""
MAPFILE = "mymap.html"

try:
    with open("maps.key") as f:
        APIKEY = f.readline().strip()
        print("Using API key: {}".format(APIKEY))
except IOError:
    print("Put your Google Maps API Key in a file called 'maps.key'")
    exit()

def plot(lats, lons):
    gmap = gmplot.GoogleMapPlotter(24.635246, 2.616971, 3)
    #gmap.heatmap(lats, lons)
    gmap.scatter(lats, lons, '#3B0B39', 40, True)   
    gmap.draw(MAPFILE)
    insertapikey(MAPFILE, APIKEY)

def insertapikey(fname, apikey):
    """put the google api key in a html file"""
    def putkey(htmltxt, apikey, apistring=None):
        """put the apikey in the htmltxt and return soup"""
        if not apistring:
            apistring = "https://maps.googleapis.com/maps/api/js?key=%s&callback=initMap"
        soup = BeautifulSoup(htmltxt, 'html.parser')
        body = soup.body
        src = apistring % (apikey, )
        tscript = soup.new_tag("script", src=src, async="defer")
        body.insert(-1, tscript)
        return soup
    htmltxt = open(fname, 'r').read()
    soup = putkey(htmltxt, apikey)
    newtxt = soup.prettify()
    open(fname, 'w').write(newtxt)
