import csv

def import_data():
  with open("orders.csv", 'r') as x:
    y=csv.y(x)
    import_data()

def query_data(id):
  with open('orders.csv') as file_obj:
    reader_obj = csv.reader(file_obj)
    for row in reader_obj:
        try:
            if row[0] == '10586':
                value = int(row[3])
        except:
            continue
    print(value)
    query_data()

def main():
  print(12)
  main()



