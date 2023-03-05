# Create class to it can be inherited by other classes later easily
import sqlite3


class DBConnection:

    # Connecting to the DB
    try:
        connection = sqlite3.connect('EV_Station_Data.db')
        print("Main DB Connection Established")
    except ConnectionError as exc:
        raise RuntimeError('Failed to open database') from exc

    # Creating cursor for executing statements
    c = connection.cursor()
