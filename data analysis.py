import matplotlib.pyplot as plt
import numpy as np
import datetime as d


def get_data(file_name, date):
    """
    :param file_name: file name with extension
    :param date: date or date with time [%Y-%m-%d or %Y-%m-%d %H:%M:%S]
    :return: arrays of: date & time, latitude, longitude [np.array]
    """
    date_time, latitude, longitude = [], [], []

    with open(file_name, 'r') as file:
        data_set = file.readlines()

    for line in data_set:
        data = line.split(",")
        if date in data[1]:
            date_time.append(data[1])
            latitude.append(float(data[3].rstrip("\n")))
            longitude.append(float(data[2]))

    return np.array(date_time), np.array(latitude), np.array(longitude)


def calculate_distance(latitude, longitude):
    """
    reference: https://pl.wikibooks.org/wiki/Astronomiczne_podstawy_geografii/Odległości#Obliczanie_odległości_pomijając_krzywiznę_Ziemi
    :param latitude: [°N]
    :param longitude: [°E]
    :return: array of distances [np.array]
    """
    total_distance = []

    for i in range(0, len(latitude) - 1):
        partial_distance = np.sqrt((latitude[i + 1] - latitude[i]) ** 2 + (
                np.cos((latitude[i] * np.pi) / 180) * (longitude[i + 1] - longitude[i])) ** 2) * 40075.704 / 360
        total_distance.append(partial_distance)

    return np.array(total_distance)


def calculate_time(current, previous):
    """
    :param current: [%Y-%m-%d %H:%M:%S]
    :param previous: [%Y-%m-%d %H:%M:%S]
    :return: duration [hours]
    """
    format_str = '%Y-%m-%d %H:%M:%S'
    return (d.datetime.strptime(current, format_str) - d.datetime.strptime(previous, format_str)).seconds / 3600


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
    file = "data/sample.txt"
    date = "2008-02-04"
    # average fuel consumption [liter / 100 km]
    afc = 9.2260

    date_time = get_data(file, date)[0]
    latitude = get_data(file, date)[1]
    longitude = get_data(file, date)[2]
    distance_array, speed_array, fuel_consumption_array = [], [], []

    for i in range(len(longitude) - 1):
        plt.plot(longitude[i], latitude[i], '.', color='blue', alpha=0.5)

        distance = calculate_distance(latitude, longitude)[i]
        distance_array.append(distance)

        speed = calculate_speed(distance, calculate_time(date_time[i + 1], date_time[i]))
        speed_array.append(speed)

        fuel_consumption = calculate_fuel_consumption(distance, afc)
        fuel_consumption_array.append(fuel_consumption)

        element = f"\nno {i}\nfrom: {date_time[i]} to: {date_time[i + 1]}\ndistance travelled: {distance} [km] \nspeed: {speed} [km/h]\nforecast value of the fuel used: {fuel_consumption}[l]"
        print(element)

    total_distance = sum(distance_array)
    total_fuel_consumption = sum(fuel_consumption_array)

    total = f"\nTotal \nfrom: {date_time[0]} to: {date_time[-1]} \ndistance travelled: {total_distance} [km] \nforecast value of the fuel used: {total_fuel_consumption} [l]"
    print(total)

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
