import matplotlib.pyplot as plt
import numpy as np
import datetime as da
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


def calculate_distance(latitude_1, longitude_1, latitude_2, longitude_2):
    """
    reference:
    :param latitude: [°N/°S]
    :param longitude: [°E/°W]
    :return: distance [km]
    """
    conversion = pi / 180
    formula = 0.5 - cos((latitude_2 - latitude_1) * conversion) / 2 + cos(latitude_1 * conversion) * cos(
        latitude_2 * conversion) * (1 - cos((longitude_2 - longitude_1) * conversion)) / 2
    return 2 * 6371 * asin(sqrt(formula))


def calculate_time(current, previous):
    """
    :param current: [%Y-%m-%d %H:%M:%S]
    :param previous: [%Y-%m-%d %H:%M:%S]
    :return: duration [hours]
    """
    format_str = '%Y-%m-%d %H:%M:%S'
    return (da.datetime.strptime(current, format_str) - da.datetime.strptime(previous, format_str)).seconds / 3600


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

def calculate_speed_with_PI(speed,time):
    list_speed_array = np.array([])
    time_array = np.array([])
    skok = 0
    for i in range(len(speed) - 1):
        T = time[i]
        h = 0.001
        t = np.arange(start=0, stop=T + h, step=h)
        v = np.zeros_like(t)
        e = np.zeros_like(t)
        u = np.zeros_like(t)  # siła [N]

        m = 1000  # [kg]
        mu = 50  # [N * s / m] #opór
        v_zad = speed[i+1]  # [km/h]

        v_pocz = speed[i]  # [km/h]
        v[0] = v_pocz
        e[0] = v_zad - v[0]

        k_p, k_i = 500, 15

        e_skum = e[0]
        for i in range(t.size - 1):
            v[i + 1] = v[i] + h * (-mu * v[i] + u[i]) / m
            e[i + 1] = v_zad - v[i + 1]
            e_skum += h * e[i + 1]
            u[i + 1] = k_p * e[i + 1] + k_i * e_skum
            skok = skok + h
            time_array = np.append(time_array, skok)
        skok = skok + h
        time_array = np.append(time_array, skok)
        list_speed_array = np.append(list_speed_array, v)

    return list_speed_array, time_array

def calculate_fuel_consumption(v):
    """
    engine: 1.4L - 2.0L
    Car class: Euro I - IV
    v: car speed
    FC: fuel consumption [L/100 km]
    """
    if v >= 5 and v <= 13.1:
        FC = 428.06 - 46.696 * v + 1.531 * v ** 2
    elif v > 13.1:
        FC = 135.44 - 2.314 * v + 0.0144 * v ** 2
    else:
        FC = 0
    FC = FC / 10
    FC = FC / 0.8
    return FC


def set_title_labels(title, horizontal_axis_title, vertical_axis_title):
    plt.title(str(title))
    plt.xlabel(str(horizontal_axis_title))
    plt.ylabel(str(vertical_axis_title))


def main():
    file = "../data/sample.txt"
    date = "2008-02-04"

    date_time = get_data(file, date)[0]
    latitude = get_data(file, date)[1]
    longitude = get_data(file, date)[2]
    distance_array, speed_array, fuel_consumption_array, time_array = [], [], [], []

    for i in range(len(longitude) - 1):
        plt.plot(longitude[i], latitude[i], '.', color='blue', alpha=0.5)

        distance = calculate_distance(latitude[i], longitude[i], latitude[i + 1], longitude[i + 1])
        distance_array.append(distance)
        time = calculate_time(date_time[i + 1], date_time[i])
        time_array.append(time)
        speed = calculate_speed(distance, time)
        speed_array.append(speed)

        print(f"\nno {i}\nfrom: {date_time[i]} to: {date_time[i + 1]}\ndistance travelled: {distance} [km]"
              f"\nspeed: {speed} [km/h]\n")#forecast value of the fuel used: {fuel_consumption}[l]")
    speed_PI, time_PI = calculate_speed_with_PI(speed_array, time_array)
    for z in range(len(speed_PI)):
        fuel_consumption = calculate_fuel_consumption(speed_PI[z])
        fuel_consumption_array.append(fuel_consumption)
    total_distance = sum(distance_array)
    total_fuel_consumption = sum(fuel_consumption_array)


    print(f"\nTotal \nfrom: {date_time[0]} to: {date_time[-1]} \ndistance travelled: {total_distance} [km]"
          f" \nforecast value of the fuel used: {total_fuel_consumption} [l]")

    set_title_labels("Locations visited", "longitude[°E]", "latitude[°N]")
    ''' #przebyta odległość do spalania - wymiary trzeba dobre ustalić
    plt.figure()
    plt.plot(distance_array, fuel_consumption_array, 'g.', alpha=0.7)
    set_title_labels("Fuel consumption by distance", "distance[km]", "fuel consumption[l]")
    '''
    plt.figure()
    plt.plot(time_PI, speed_PI, alpha=0.7)
    set_title_labels("speed by time",  "time[h]", "speed[km/h]")
    plt.show()
    plt.figure()
    plt.plot(speed_PI, fuel_consumption_array, 'r.', alpha=0.7)
    set_title_labels("Fuel consumption by speed", "speed[km/h]", "fuel consumption[l]")
    plt.show()




if __name__ == '__main__':
    main()

