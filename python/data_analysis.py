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


def calculate_fuel_consumption(dc, afc):
    """
    :param dc: distance covered [km]
    :param afc: average fuel consumption [liter / 100 km]
    :return: forecast value of the fuel used [liter]
    """
    return dc * afc / 100


def set_title_labels(title, horizontal_axis_title, vertical_axis_title):
    plt.title(str(title))
    plt.xlabel(str(horizontal_axis_title))
    plt.ylabel(str(vertical_axis_title))


def main():
    file = "../data/sample.txt"
    date = "2008-02-04"
    # average fuel consumption [liter / 100 km]
    afc = 9.2260

    date_time = get_data(file, date)[0]
    latitude = get_data(file, date)[1]
    longitude = get_data(file, date)[2]
    distance_array, speed_array, fuel_consumption_array = [], [], []

    for i in range(len(longitude) - 1):
        plt.plot(longitude[i], latitude[i], '.', color='blue', alpha=0.5)

        distance = calculate_distance(latitude[i], longitude[i], latitude[i + 1], longitude[i + 1])
        distance_array.append(distance)

        speed = calculate_speed(distance, calculate_time(date_time[i + 1], date_time[i]))
        speed_array.append(speed)

        fuel_consumption = calculate_fuel_consumption(distance, afc)
        fuel_consumption_array.append(fuel_consumption)

        print(f"\nno {i}\nfrom: {date_time[i]} to: {date_time[i + 1]}\ndistance travelled: {distance} [km]"
              f"\nspeed: {speed} [km/h]\nforecast value of the fuel used: {fuel_consumption}[l]")

    total_distance = sum(distance_array)
    total_fuel_consumption = sum(fuel_consumption_array)

    print(f"\nTotal \nfrom: {date_time[0]} to: {date_time[-1]} \ndistance travelled: {total_distance} [km]"
          f" \nforecast value of the fuel used: {total_fuel_consumption} [l]")

    set_title_labels("Locations visited", "longitude[°E]", "latitude[°N]")

    plt.figure()
    plt.plot(distance_array, fuel_consumption_array, 'g.', alpha=0.7)
    set_title_labels("Fuel consumption by distance", "distance[km]", "fuel consumption[l]")

    plt.figure()
    plt.plot(speed_array, fuel_consumption_array, 'r.', alpha=0.7)
    set_title_labels("Fuel consumption by speed", "speed[km/h]", "fuel consumption[l]")
    plt.show()


if __name__ == '__main__':
    main()
