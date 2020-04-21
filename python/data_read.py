import sqlite3
import numpy as np


def read_data():
    """
    :return: array of distance, array of speed, array of fuel consumption
    """
    distance, speed, fuel_consumption = [], [], []
    try:
        database_name = 'data.db'
        sqliteConnection = sqlite3.connect(database_name)
        cursor = sqliteConnection.cursor()
        sqlite_select_query = f'''SELECT distance, speed, fuel_consumption from data'''
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        for row in records:
            distance.append(row[0])
            speed.append(row[1])
            fuel_consumption.append(row[2])
        cursor.close()


    except sqlite3.Error as error:
        print('Failed to read data from sqlite table', error)

    finally:
        if (sqliteConnection):
            sqliteConnection.close()

    return np.array(distance), np.array(speed), np.array(fuel_consumption)
