import requests
from bs4 import BeautifulSoup
from time import sleep
import sys
import gmplot
import os
import re
import json
import datetime

def lineup(text):
    line_len = 16
    while len(str(text)) <= line_len:
        text += " "
    return text[:(line_len - 1)] + " "


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
    with open(fname, 'w') as f:
        f.write(newtxt)

today = datetime.datetime.today()
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__)) + "/"

logfile = CURRENT_DIR + "Logs/" + today.strftime("%m-%d-%Y-map.log")
ipfile = CURRENT_DIR + "ips.txt"
infofile = CURRENT_DIR + "info.txt"
authfile = os.path.abspath("/var/log/apache2/access.log")
localmap = "webaccess.html"
mapfile = CURRENT_DIR + localmap
webfile = "/var/www/html/" + localmap 

apikey = "YOUR GOOGLE MAPS API KEY HERE"

lats = list()
lons = list()
titles = list()
labels = list()

new_ips = set()
ip_addrs = set()

new_ip_addr = set()
new_ip_info = set()
stats_lst = list()


def get_ips():
    """Get all IP addresses from authfile and write the unique ones to ips.txt"""
    try:
        with open(ipfile) as f:
            for ip in f.readlines():
                ip_addrs.add(ip)
    except IOError:
        open(ipfile, "w")

    with open(authfile) as f:
        new_ips = set(re.findall( r'[0-9]+(?:\.[0-9]+){3}',f.read()))

    for ip in new_ips:
        ip_addrs.add(ip)

    with open(infofile) as f:
        for inf in f.readlines():
            inf = inf.split("$")
            ip_addrs.add(inf[0])

    with open(ipfile, "w") as f:
        for ip in ip_addrs:
            f.write(ip.strip() + "\n")

have_new = False
info_txt = ""
try:
    info_txt = open(infofile).read()
except IOError:
    with open(infofile, "w+") as f:
        f.write("")

for ip in ip_addrs:
  if not ip in info_txt:
      have_new = True
if not have_new:
    print("No new IP addresses found.")
    #sys.exit()

print(today.strftime("Creating map for %b %d %Y"))

if len(sys.argv) > 1:
    if sys.argv[1] == "refresh":
        print("Refreshing list of login attempts...")
        get_ips()
    else:
        print("Using old list of login attempts...")
        print("Use: 'sudo python3 map.py refresh' to update list.")
print("")

info = list()
with open(infofile) as f:
    info = f.readlines()
info = [x.strip() for x in info]
info = set(info)

ips = list()
try:
    with open(ipfile) as f:
        ips  = f.readlines()
except IOError:
    with open(ipfile, "w") as f:
        f.write("")
ips = [x.strip() for x in ips]
ips = set(ips)

info_txt = open(infofile).read()

ip_ct = 0

heading = lineup("#/" + str(len(ips))) + lineup("IP Address") + lineup("City") + lineup("Region") + lineup("Country") + lineup("Code") + lineup("Latitude") + lineup("Longitude")
print(heading)
print("=" * len(heading))

for ip in ips:
    ip_ct += 1
    if ip in info_txt:
        for ip_info in info:
            if ip in ip_info and len(ip_info) > 15:
                info_split = ip_info.split("$")
                
                titles.append(info_split[3])
                labels.append(info_split[0])
                lats.append(float(info_split[5]))
                lons.append(float(info_split[6]))

                print(lineup(str(ip_ct)), end="")
                for sec in info_split:
                    print(lineup(sec), end="")
                print("")
                break
    else:
        
        send_url = 'http://freegeoip.net/json/' + ip
        r = requests.get(send_url)
        try:
            j = json.loads(r.text)
        except json.decoder.JSONDecodeError:
            continue
        
        if j['latitude'] == 0 and j['longitude'] == 0:
            continue

        lats.append(j['latitude'])
        lons.append(j['longitude'])
        titles.append(j['city'])
        labels.append(ip)

        new_ip_addr.add(ip)
        new_ip_info.add(j['country_name'])

        print_line = lineup(ip)  + lineup(j['city']) + lineup(j['region_name']) + lineup(j['country_name']) + lineup(j['country_code'])
        print_line += lineup(str(j['latitude'])) +lineup(str(j['longitude']))

        write_line = ip + "$" + j['city'] + "$" + j['region_name'] + "$" + j['country_name'] + "$" + j['country_code'] + "$" + str(j['latitude']) + "$" + str(j['longitude'])

        with open(infofile, "a") as f:
            f.write(write_line + "\n")

        print(lineup(str(ip_ct) + "*") + print_line)

        sleep(5)

    #  End of all IP addresses

stats_lst.append(str(len(ips)) + " total unique IP addresses.")

stat_from = str(len(new_ip_addr)) + " new IPs in last hour. From "
for cc in new_ip_info:
    stat_from += cc + ", "
stats_lst.append(stat_from)

gmap = gmplot.GoogleMapPlotter(24.635246, 2.616971, 3)
#gmap.heatmap(lats, lons)
#gmap.scatter(lats, lons, titles, labels, '#FF0000', size=20, marker=True)
gmap.scatter(lats, lons, '#FF0000', size=20, marker=True)
gmap.draw(mapfile)
insertapikey(mapfile, apikey)

""" Insert Stats To Webpage"""
def insert_stats(stats):
    print("Adding " + str(len(stats)) + " statistics to webpage")
    soup = BeautifulSoup(open(mapfile, "r").read(), "html.parser")
    body = soup.body
    head = soup.head

    head.append(soup.new_tag('style', type='text/css'))
    head.style.append('#stats {background-color:#FF6766;\n\tposition:absolute;\n\ttop:5%;\n\tleft:5%;\n\tpadding:10px;\n\tz-index:999;\n\topacity:0.8;\n\tborder-radius:25px;}')
    soup.head = head

    soup.head.title.string = "Map of Attempted Logins"

    stats_div = soup.new_tag('div',id='stats')

    stats_h = soup.new_tag('h1', id='stats_h')
    stats_h['font-weight'] = "bold"
    stats_h.string = "Statistics"

    stats_ul = soup.new_tag('ul')

    for stat in stats:
        new_h = soup.new_tag('h3')
        new_h.string = stat
        stats_ul.insert(len(stats_ul.contents), new_h)

    stats_div.insert(0, stats_h)
    stats_div.insert(1, stats_ul)

    body.insert(0, stats_div)

    newtxt = soup.prettify()
    with open(mapfile, "w") as f:
        f.write(newtxt)

insert_stats(stats_lst)

os.system("cp " + mapfile + " " + webfile)

