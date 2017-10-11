import sqlite3

while True:
    db = sqlite3.connect("test.db")
    try:
        command = raw_input(">")
        for line in db.execute(command):
            print(line)
    except:
        print("ERROR")