import os
import csv
import datetime as dt

def format(from_path,to_path):
    count=0
    from_ = next(os.walk(from_path), (None, None, []))[2]
    for file in from_:
        path_from = os.path.sep.join([from_path,file])
        path_to = os.path.sep.join([to_path,file])
        if not os.path.isfile(path_to):
            with open(path_to, 'w') as fp:
                pass
        hexs = []
        with open(path_to, newline='') as to_reader:
            reader = csv.reader(to_reader)
            for row in reader:
                if row[0] and row[0] not in hexs:
                    hexs.append([row[0]])
                    count+=1
        with open(path_from, newline='') as from_reader:
            reader = csv.DictReader(from_reader)
            for row in reader:
                if row['hex'] and row['hex'] not in hexs:
                    hexs.append([row['hex']])
                    count+=1
        with open(path_to, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerows(hexs)
        print("now: ",dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), file, str(count), " "*10, end='\r')
    print()

if __name__ == '__main__':
    print(__file__)
    print('start:',dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    from_path = "c:\\monero\\address_csv"
    to_path = "c:\\monero\\not_zero"
    format(from_path,to_path)
    print('end:  ',dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),' '*10)