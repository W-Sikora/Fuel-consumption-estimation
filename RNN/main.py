# Collective Engineering Project
# Instantaneous vehicle fuel consumption estimation using smartphones and recurrent neural networks
# Authors:
# * Rafał Górski
# * Michał Lisowski
# * Wojciech Sikora
# * Jan Szkoda


import sys
import sqlite3
import tensorflow.keras
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, LSTM, Dropout
from tensorflow.keras.models import Sequential
from sklearn.metrics import mean_absolute_error


def get_data(size=None):
    date_previous, date_current, distance, speed, fuel_consumption =  ([] for i in range(5))
    try:
        database_name = '../data.db'
        sqliteConnection = sqlite3.connect(database_name)
        cursor = sqliteConnection.cursor()
        cursor.execute('''select date_previous, date_current, distance, speed, fuel_consumption from data''')
        if isinstance(size, int):
            records = cursor.fetchmany(size)
        else:
            records = cursor.fetchall()
        for row in records:
            date_previous.append(row[0])
            date_current.append(row[1])
            distance.append(row[2])
            speed.append(row[3])
            fuel_consumption.append(row[4])
        cursor.close()
        sqliteConnection.close()

    except sqlite3.Error as error:
        print('Failed to read data from sqlite table', error)

    return date_previous, date_current, distance, speed, fuel_consumption

    
def get_part_of_data(data, _from, to):
    inputs = np.array(data['speed'][_from:to])
    outputs = np.array(data['fuel consumption'][_from:to])
    return inputs, outputs


def divide_into_parts(inputs, outputs, train_part):
    length = inputs.shape[0]
    train_part *= length
    validation_part = train_part + (length - train_part)   
    
    train_array = [inputs[: int(train_part)],
                   outputs[: int(train_part)]]
    
    validation_array = [inputs[int(train_part) : int(validation_part)],
                        outputs[int(train_part) : int(validation_part)]]
        
    return train_array, validation_array


def transform(array):
    return array.reshape(array.shape[0], 1, 1)


def transform_to_list(array):
    return array.reshape(array.shape[0])

        
def statistics(real, predict):
    print(f'mean absolute error: {mean_absolute_error(np.array(real), np.array(predict))}')

    
def calculate_fuel_consumption(v):
    """
    engine: 1.4L - 2.0L
    Car class: Euro I - IV
    -----------------------
    v: car speed [km/h]
    FC: fuel consumption [l/100 km]
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


def plot_hist(data, title):
    plt.figure(figsize=(10,6))
    plt.hist(data, rwidth=0.91)
    plt.title(title)
    plt.show()
    
    
def plot_part_of_data(data, title, _from, to):
    plt.figure(figsize=(10,6))
    plt.plot(data[_from:to], color='blue', marker='.', alpha=0.5, linestyle='None')
    plt.title(title)
    plt.show()
    
    
def plot_result(x, y_real, y_predict):
    plt.figure(figsize=(15,9))
    plt.plot(x, y_real, color='red', alpha=0.5, marker='.', linestyle='None', label='real')
    plt.plot(x, y_predict, color='blue', alpha=0.5, marker='.', linestyle='None', label='predicted')
    plt.plot(x, np.zeros(len(x)), color='black')
    plt.legend()
    plt.show()    


# reading data from the database
data = get_data(3000000)


# creating Pandas DataFrame
data = pd.DataFrame({'date previous':data[0],
                     'date current':data[1],
                     'distance':data[2],
                     'speed':data[3],
                     'fuel consumption':data[4]})

data.head(100)

# statistics
data.describe()

_from, to = 1000, 20000

speed, fuel_consumption = data['speed'], data['fuel consumption']

plot_hist(speed, 'speed')
plot_part_of_data(speed, 'speed change', _from, to)
plot_hist(fuel_consumption, 'fuel consumption')
plot_part_of_data(fuel_consumption, 'fuel consumption change', _from, to)


# data preparation
_from, to = 0, 900000
part_of_data = get_part_of_data(data, _from, to)
train, validation = divide_into_parts(part_of_data[0], part_of_data[1], 0.8)
test = get_part_of_data(data, 1000000, 3000000)
train_inputs = transform(train[0])
validation_inputs = transform(validation[0])
test_inputs = transform(test[0])
train_outputs = train[1]
validation_outputs = validation[1]
test_outputs = test[1]


# construction of recurrent neural network
model = Sequential()
model.add(LSTM(50, activation='softplus', input_shape=(1, 1), return_sequences=True))
model.add(LSTM(50, activation='relu', return_sequences=True))
model.add(LSTM(50, activation='relu'))
model.add(Dense(1, activation='relu'))
model.compile(optimizer='adam', loss='mse')
model.summary()


# learning process
model.fit(train_inputs, train_outputs, epochs=20, batch_size=5,
          validation_data=(validation_inputs, validation_outputs))


# prediction
test_predictions = model.predict(test_inputs)


# data formatting
predictions = transform_to_list(test_predictions)
test_inputs = transform_to_list(test_inputs)


# result
plot_result(test_inputs, test_outputs, predictions)
statistics(test_outputs, predictions)


# save network
model.save('network.h5')


# load network
model2 = load_model('network.h5')
model2.summary()