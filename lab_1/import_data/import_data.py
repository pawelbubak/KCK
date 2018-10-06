import csv

file_names = ['rsel', 'cel-rs', '2cel-rs', 'cel', '2cel']

def open_csv(file_name):
    data = []
    with open('lab_1/data_files/' + file_name, newline='') as csv_file:
        file_data = csv.reader(csv_file, delimiter=',', quotechar='|')
        for row in file_data:
            data.append(row)
    return data


def import_all_data():
    data = []
    for name in file_names:
        data.append((name, open_csv(name + '.csv')))
    return data
