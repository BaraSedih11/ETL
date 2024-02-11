import csv
import os


def check_header_format(header_arr):
    # check header start tag
    header = arr[0]
    header_start_tag = header.split(',')

    if header_start_tag[0] != '<information>':
        return None

    # check date tag
    date_tag = arr[1].split(',')[0].split(' ')

    if date_tag[0] != 'date:':
        return None

    date = date_tag[1]

    # check number of columns
    column_num_tag = arr[2].split(',')[0].split(' ')

    if column_num_tag[0] != 'column_num:':
        return None

    column_num = column_num_tag[1]

    # check header end tag
    header_end_tag = arr[3].split(',')[0]

    if header_end_tag != '</information>':
        return False

    output_data = [column_num, date]

    return output_data


def check_data_format(data_arr, column_num):
    # check data start tag
    data_start_tag = data_arr[0].split(',')[0]

    if data_start_tag != '<data>':
        return None

    # check data end tag
    data_end_tag = data_arr[-1].split(',')[0]

    if data_end_tag != '</data>':
        return None

    data_cols = data_arr[1].split(',')[:int(column_num)]

    for data_col in data_cols:
        if data_col is None:
            del (data_cols[data_cols.index(data_col)])

    if len(data_cols) == 0:
        return None

    data_rows = []

    for i in range(2, len(data_arr) - 1):
        row = data_arr[i].split(',')[:int(column_num)]

        filtered_row = list(item for item in row if item != "" and item != "\n")

        if len(filtered_row) == 0:
            continue

        data_rows.append(row)

    for i in range(len(data_rows)):
        data_rows[i] = [item if item != '' else 'Empty' for item in data_rows[i]]

    data_rows = remove_duplicates(data_rows)

    return data_rows


def remove_duplicates(matrix):
    unique_rows = {}
    for row in matrix:
        key = row[0]
        if key not in unique_rows:
            unique_rows[key] = row

    return list(unique_rows.values())


def check_format(arr):
    output_data_1 = check_header_format(arr[:4])
    if output_data_1[0] is None or output_data_1[1] is None:
        return None

    formatted_data = check_data_format(arr[4:], output_data_1[0])

    if len(formatted_data) == 0 or formatted_data is None:
        return None

    file_data = [output_data_1[1], formatted_data]

    return file_data


def format_file(file_data):
    output_directory = 'output_files'
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Replace invalid characters in the date for the filename
    sanitized_date = file_data[0].replace('/', '-')

    file_path = os.path.join(output_directory, f"output_file_{sanitized_date}.csv")

    with open(file_path, "w", newline='') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerows(file_data[1])


if __name__ == '__main__':

    lines = (line for line in open('test.csv'))

    arr = list(lines)

    file_data = check_format(arr)
    if file_data[0] is None or file_data[1] is None:
        print('Invalid file format')
    else:
        format_file(file_data)
        print('File formatted successfully ✅')
