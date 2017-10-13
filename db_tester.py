import sqlite3

while True:
    db = sqlite3.connect("test.db")
    try:
        command = raw_input(">")
        for line in db.execute(command):
            print(line)
    except KeyboardInterrupt:
        break
    except EOFError:
        break
    except sqlite3.OperationalError as e:
        print("SQL ERROR: {}".format(e))