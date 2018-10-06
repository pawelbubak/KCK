def process_data(data_to_process):
    data = []
    for var in data_to_process:
        (name, var_data) = var
        temp_data = prepare_data(var_data)
        data.append({'name': name, 'data': temp_data, 'last': get_last_row(var_data[-1])})
    return data


def prepare_data(data):
    generation = []
    effort = []
    avr_value = []
    for row in data[1::]:
        time_sum = 0
        for time in row[2::]:
            time_sum += float(time)
        avr_val = time_sum / (len(row) - 2)
        generation.append(int(row[0]))
        effort.append(int(row[1]) / 1000)
        avr_value.append(avr_val * 100)
    return {'generation': generation, 'effort': effort, 'value': avr_value}


def get_last_row(data):
    result = []
    for var in data[2::]:
        result.append(float(var) * 100)
    return result
