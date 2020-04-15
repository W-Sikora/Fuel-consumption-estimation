import xlsxwriter
from data_analysis import calculate_time
from pathlib import Path
import os
import numpy as np
from math import cos, asin, sqrt, pi


def get_data(file_name, date=None):
    """
    :param file_name: file name with extension
    :param date: date or date with time [%Y-%m-%d or %Y-%m-%d %H:%M:%S]
    :return: arrays of: date & time, latitude, longitude [np.array]
    """
    date_time, latitude, longitude = [], [], []

    with open(file_name, 'r') as file:
        data_set = file.readlines()

    if not date:
        for line in data_set:
            data = line.split(",")
            date_time.append(data[1])
            latitude.append(float(data[3].rstrip("\n")))
            longitude.append(float(data[2]))
        return np.array(date_time), np.array(latitude), np.array(longitude)

    else:
        for line in data_set:
            data = line.split(",")
            if date in data[1]:
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


def create_worksheet(file_name):
    """
    :param file_name: name of new Excel file
    :return: Excel file with all the necessary data
    """
    glob_path = Path(f'{os.path.dirname(os.path.abspath(os.getcwd()))}/data')
    file_list = [str(p) for p in glob_path.glob("**/*.txt")]
    files = []

    for file in file_list:
        files.append('../data/' + file.split('\\')[-1])

    workbook = xlsxwriter.Workbook(file_name)
    worksheet = workbook.add_worksheet()

    names = ['date&time', 'date&time2', 'latitude', 'longitude', 'latitude2', 'longitude2', 'distance', 'speed',
             'fuel consumption']

    for i in range(len(names)):
        worksheet.write(0, i, names[i])

    iterator = 1
    for file in files:
        date_time = get_data(file)[0]
        latitude = get_data(file)[1]
        longitude = get_data(file)[2]
        distance, time, speed = [], [], []
        length = len(date_time)

        for i in range(length - 1):
            distance.append(calculate_distance(latitude[i], longitude[i], latitude[i + 1], longitude[i + 1]))
            time.append(calculate_time(date_time[i + 1], date_time[i]))
            speed.append(calculate_speed(distance[i], time[i]))

        for i in range(length - 1):
            worksheet.write(iterator, 0, date_time[i])
            worksheet.write(iterator, 1, date_time[i + 1])
            worksheet.write(iterator, 2, latitude[i])
            worksheet.write(iterator, 3, longitude[i])
            worksheet.write(iterator, 4, latitude[i + 1])
            worksheet.write(iterator, 5, longitude[i + 1])
            worksheet.write(iterator, 6, distance[i])
            worksheet.write(iterator, 7, speed[i])
            worksheet.write(iterator, 8, '-')
            iterator += 1

    workbook.close()


if __name__ == '__main__':
    create_worksheet('data.xlsx')
