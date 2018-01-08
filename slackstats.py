import os
from slacker import Slacker
from datetime import datetime
import shelve
import pytz

filepath = os.path.realpath(__file__)

last = 0
for n in range(len(filepath)):
    if filepath[n] == '/':
        last = n

dirpath = filepath[:last + 1]


STATS_FILE = os.path.join(dirpath, "app/stats.dict")
SLACK_TOKEN = os.environ.get('SLACK_TOKEN')


def send_stats():
    slack = Slacker(SLACK_TOKEN)

    stats = shelve.open(STATS_FILE)

    message = "{}\n{}\nTotal Attempts: {}\nUnique IP Addresses: {}\nUnique Countries: {}\nCountry with Most Attempts: {}\n\n\n\n{}"

    rn = pytz.utc.localize(datetime.now()).astimezone(pytz.timezone('US/Eastern')).strftime("%A, %d. %B %Y %I:%M%p")

    sep = '-' * len(rn)

    message = message.format(rn, sep, stats['total_attempts'], stats['unique_ips'], stats['unique_countries'], 'CN', sep)



    slack.chat.post_message('#log-mapper', message)

if __name__ == "__main__":
    send_stats()
