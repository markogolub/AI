from parser import *

def read_csv(file_name):
    import collections

    with open(file_name) as file:
        columns = {}

        attributes = file.readline().split(',')[:-1]
        for attribute in attributes:
            columns[attribute] = get_column(file_name, attribute)

        data = file.readlines()
        for i, entry in enumerate(data):
            data[i] = data[i].strip().split(',')

        labels = []
        for entry in data:
            labels.append(entry.pop())

        counter = collections.Counter(labels)

        train_dataset = {
            'attributes': attributes,
            'columns': columns,
            'data': data,
            'labels': labels,
            'counter': counter
        }

        return train_dataset

