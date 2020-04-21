from data_analysis import calculate_time, pi_controller
from pathlib import Path
import os
import numpy as np
from math import cos, asin, sqrt, pi
from datetime import datetime
import sqlite3
import matplotlib.pyplot as plt


def get_data(file_name):
    """
    :param file_name: file name with extension
    :return: arrays of: date & time, latitude, longitude [np.array]
    """
    date_time, latitude, longitude = [], [], []

    with open(file_name, 'r') as file:
        data_set = file.readlines()

    for line in data_set:
        data = line.split(",")
        date_time.append(data[1])
        latitude.append(float(data[3].rstrip("\n")))
        longitude.append(float(data[2]))

    return np.array(date_time), np.array(latitude), np.array(longitude)


def calculate_speed(distance, time):
    """
    :param distance: [km]
    :param time: [hours]
    :return: [km / h]
    """
    if time != 0:
        return distance / time
    else:
        return 0


def calculate_distance(latitude_1, longitude_1, latitude_2, longitude_2):
    """
    reference:
    :param longitude_1: [°E/°W]
    :param latitude_1:  [°N/°S]
    :param longitude_2: [°E/°W]
    :param latitude_2: [°N/°S]
    :return: distance [km]
    """
    conversion = pi / 180
    formula = 0.5 - cos((latitude_2 - latitude_1) * conversion) / 2 + cos(latitude_1 * conversion) * cos(
        latitude_2 * conversion) * (1 - cos((longitude_2 - longitude_1) * conversion)) / 2
    return 2 * 6371 * asin(sqrt(formula))


def show_plot(data, h):
    time, pr = [], []
    step = 0
    for i in data:
        time.append(step)
        step += h / 3600
        pr.append(i[3])
    plt.plot(time, pr, label='v - prędkość [km/h]')
    plt.xlabel('t [h]', fontsize=14)
    plt.legend(fontsize=14, loc='upper left')
    plt.show()


def create_worksheet(file_name, step=30):
    """
    :param step: step for regulator in seconds
    :param test: True if we want only test pi controller
    :param file_name: name of new database file
    :return: Excel file with all the necessary data
    """
    glob_path = Path(f'{os.path.dirname(os.path.abspath(os.getcwd()))}/data')
    file_list = [str(p) for p in glob_path.glob("**/*.txt")]
    files = []
    for file in file_list:
        files.append('../data/' + file.split('\\')[-1])

    conn = sqlite3.connect(file_name)
    c = conn.cursor()

    try:
        c.execute("DROP TABLE data")
    except sqlite3.OperationalError:
        pass

    c.execute('''CREATE TABLE data
    (id INTEGER PRIMARY KEY NOT NULL,
    date_previous  DATE NOT NULL,
    date_current DATE NOT NULL,
    distance FLOAT NOT NULL,
    speed FLOAT NOT NULL,
    fuel_consumption FLOAT NOT NULL);''')

    start = datetime.now()
    for file in files:
        print(f'file: {files.index(file)+1}/{len(files)}')
        file_data = []
        date_time, latitude, longitude = get_data(file)

        for i in range(len(date_time) - 1):
            distance = calculate_distance(latitude[i], longitude[i], latitude[i + 1], longitude[i + 1])
            time = calculate_time(date_time[i + 1], date_time[i])
            speed = calculate_speed(distance, time)
            if not time == 0 and speed < 130:
                file_data.append([date_time[i], date_time[i + 1], distance, speed])

        file_data = pi_controller(file_data, 30)

        c.executemany("INSERT INTO data (date_previous, date_current, distance, speed, fuel_consumption) "
                          "VALUES (?, ?, ?, ?, ?)", file_data)

    conn.commit()
    conn.close()
    print(f'\nDone\nTime: {datetime.now() - start}')


if __name__ == '__main__':
    create_worksheet('data.db')
