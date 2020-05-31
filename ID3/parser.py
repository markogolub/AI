def get_column(file_name, key):
    import csv
    column = set()

    with open(file_name) as file:
        reader = csv.DictReader(file)

        for row in reader:
            for (k, v) in row.items():
                if k == key: column.add(v)

    return column
