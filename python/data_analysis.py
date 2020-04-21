import numpy as np
import datetime as da


def calculate_distance(speed, step):
    distance = []
    for i in range(len(speed)):
        distance.append(step * speed[i])
    return distance


def calculate_time(current, previous):
    """
    :param current: [%Y-%m-%d %H:%M:%S]
    :param previous: [%Y-%m-%d %H:%M:%S]
    :return: duration [hours]
    """
    format_str = '%Y-%m-%d %H:%M:%S'
    return (da.datetime.strptime(current, format_str) - da.datetime.strptime(previous, format_str)).seconds / 3600


def calculate_speed_with_PI(speed_previous, speed, time, h):
    """
    :param h: step in hours
    :param speed_previous: speed previous measurement
    :param speed: actual speed
    :param time: time
    :return: speed after regulator
    """

    time_array = np.array([])
    step = 0
    T = time
    t = np.arange(start=0, stop=T + h, step=h)
    v = np.zeros_like(t)
    e = np.zeros_like(t)
    u = np.zeros_like(t)  # force [N]

    m = 1500  # mass [kg]
    mu = 50 * 3.6  # [N * s / m] resistance
    set_v = speed  # [km/h]

    initial_v = speed_previous  # [km/h]
    v[0] = initial_v

    e[0] = set_v - v[0]
    time_array = np.append(time_array, step)
    k_p, k_i = 4000, 1
    cum_e = e[0]

    for i in range(t.size - 1):
        v[i + 1] = v[i] + h * (-mu * v[i] + u[i]) / m
        e[i + 1] = set_v - v[i + 1]
        cum_e += h * e[i + 1]
        u[i + 1] = k_p * e[i + 1] + k_i * cum_e
        step = step + h
        time_array = np.append(time_array, step)

    return v


def calculate_fuel_consumption(v):
    """
    engine: 1.4L - 2.0L
    Car class: Euro I - IV
    v: car speed
    FC: fuel consumption [L/100 km]
    """
    if v == 0:
        fuel_consumption = 0
    elif v > 13.1:
        fuel_consumption = 135.44 - 2.314 * v + 0.0144 * v ** 2
    else:
        fuel_consumption = 428.06 - 46.696 * v + 1.531 * v ** 2
    fuel_consumption = fuel_consumption / 10  # conversion of units [g/km] -> [kg/100km]
    fuel_consumption = fuel_consumption / 0.8  # conversion of units  kg -> litres
    return fuel_consumption


def fuel_consumption(speed_PI):
    fuel_consumption_array = []
    for z in range(len(speed_PI)):
        fuel = calculate_fuel_consumption(speed_PI[z])
        fuel_consumption_array.append(fuel)
    return fuel_consumption_array


def pi_controller(data, step=30):
    """
    :param data: array of arrays that contain [[date1, date2, distance, speed],..]
    :param step: step for regulator in seconds
    :return: generated data for data given in param [[date1, date2, distance, speed, fuel consumption],..]
    """
    step /= 3600
    export = []
    for i in range(len(data) - 1):
        time = calculate_time(data[i][1], data[i][0])
        speed_PI = calculate_speed_with_PI(data[i][3], data[i + 1][3], time, step)
        for z in range(len(speed_PI)):
            if speed_PI[z] < 0:
                speed_PI[z] = 0
        fuel_consumption_array = fuel_consumption(speed_PI)
        distance = calculate_distance(speed_PI, step)

        for j in range(len(distance)):
            row = []
            if len(export) == 0:
                row.append(data[i][0])
            else:
                row.append(export[j - 1][1])
            format_str = '%Y-%m-%d %H:%M:%S'
            row.append(str(da.datetime.strptime(row[0], format_str) + da.timedelta(hours=step)))
            row.append(distance[j])
            row.append(speed_PI[j])
            row.append(fuel_consumption_array[j])
            export.append(row)
    return export
