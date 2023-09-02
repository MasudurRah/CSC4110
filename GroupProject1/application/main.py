import csv
import os

class CsvOperations:
    def __init__(self, filename):
        self.filename = filename

    def add_data(self, order_id):
        with open(self.filename, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([order_id])

    def remove_data(self, order_id):
        data = []
        with open(self.filename, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] != order_id:
                    data.append(row)

        with open(self.filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)

    def query_data(self, order_id):
        data = []
        with open(self.filename, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == order_id:
                    data = row
                    break

        return data

