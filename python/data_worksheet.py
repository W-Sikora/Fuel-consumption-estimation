import xlsxwriter
from data_analysis import get_data, calculate_distance, calculate_time, calculate_speed
from pathlib import Path


def create_worksheet(file_name, path):
    """
    :param file_name: name of new Excel file
    :param path: exact location of the directory with the files
    :return: Excel file with all the necessary data
    """
    glob_path = Path(path)
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

    for file in files:
        date_time = get_data(file)[0]
        latitude = get_data(file)[1]
        longitude = get_data(file)[2]
        distance, time, speed = [], [], []

        for i in range(len(date_time) - 1):
            distance.append(calculate_distance(latitude[i], longitude[i], latitude[i + 1], longitude[i + 1]))
            time.append(calculate_time(date_time[i + 1], date_time[i]))
            speed.append(calculate_speed(distance[i], time[i]))

        for i in range(0, len(date_time) - 1):
            worksheet.write(i + 1, 0, date_time[i])
            worksheet.write(i + 1, 1, date_time[i + 1])
            worksheet.write(i + 1, 2, latitude[i])
            worksheet.write(i + 1, 3, longitude[i])
            worksheet.write(i + 1, 4, latitude[i + 1])
            worksheet.write(i + 1, 5, longitude[i + 1])
            worksheet.write(i + 1, 6, distance[i])
            worksheet.write(i + 1, 7, speed[i])
            worksheet.write(i + 1, 8, '-')

    workbook.close()


if __name__ == '__main__':
    create_worksheet('data.xlsx', r'C:\Users\WS\PycharmProjects\RNN\data')
