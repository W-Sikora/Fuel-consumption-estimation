import matplotlib.pyplot as plt
import numpy as np
import datetime as da
from math import cos, asin, sqrt, pi
import pandas as pd
import os


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
    u = np.zeros_like(t)  # siła [N]

    m = 1500  # [kg]
    mu = 50 * 3.6  # [N * s / m] opór
    v_zad = speed  # [km/h]

    v_pocz = speed_previous  # [km/h]
    v[0] = v_pocz

    e[0] = v_zad - v[0]
    time_array = np.append(time_array, step)
    k_p, k_i = 100000, 15000
    e_skum = e[0]
    for i in range(t.size - 1):
        v[i + 1] = v[i] + h * (-mu * v[i] + u[i]) / m
        e[i + 1] = v_zad - v[i + 1]
        e_skum += h * e[i + 1]
        u[i + 1] = k_p * e[i + 1] + k_i * e_skum
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
    if v > 13.1:
        FC = 135.44 - 2.314 * v + 0.0144 * v ** 2
    elif v >= 5:
        FC = 428.06 - 46.696 * v + 1.531 * v ** 2
    else:
        FC = 0
    FC = FC / 10  # zamiana [g/km] na [kg/100km]
    FC = FC / 0.8  # zamiana kg na litry
    return FC


def fuel_consumption(speed_PI):
    fuel_consumption_array = []
    for z in range(len(speed_PI)):
        fuel_consumption = calculate_fuel_consumption(speed_PI[z])
        fuel_consumption_array.append(fuel_consumption)
    return fuel_consumption_array


def pi_controller(data, step=1):
    """
    :param data: array of arrays that contain [[date1, date2, distance, speed],..]
    :param step: step for regulator in seconds
    :return: generated data for data given in param [[date1, date2, distance, speed, fuel consumption],..]
    """
    step /= 3600
    export = []
    for i in range(len(data)-1):
        time = calculate_time(data[i][1], data[i][0])
        speed_PI = calculate_speed_with_PI(data[i][3], data[i + 1][3], time, step)
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


def main():
    data = []
    df = pd.read_excel(io=f'{os.path.abspath(os.getcwd())}/data.xlsx', sheet_name='Sheet1')

    for i in range(100):
        data.append(df.loc[i])
    export = pi_controller(data)

    time, pr = [], []
    step = 0
    for i in export:
        time.append(step)
        step += 1 / 3600
        pr.append(i[3])
    plt.plot(time, pr, label='v - prędkość [km/h]')
    plt.xlabel('t [s]', fontsize=14)
    plt.legend(fontsize=14, loc='upper left')
    plt.show()


if __name__ == '__main__':
    main()
