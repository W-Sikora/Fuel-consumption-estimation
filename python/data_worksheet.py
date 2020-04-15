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

    print(files)
    workbook = xlsxwriter.Workbook(file_name)
    worksheet = workbook.add_worksheet()

    names = ['date&time', 'date&time2', 'latitude', 'longitude', 'latitude2', 'longitude2', 'distance', 'speed',
             'fuel consumption']

    for i in range(len(names)):
        worksheet.write(0, i, names[i])

    iterator = 1
    for file in files:
        date_time = get_data(file)[0]
        print(len(date_time))
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
    create_worksheet('data.xlsx', r'C:\Users\WS\PycharmProjects\RNN\data')
