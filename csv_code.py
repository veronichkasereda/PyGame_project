import csv


def reader(time):
    with open("table.csv", encoding='utf-8') as r_file:
        # Создаем объект reader, указываем символ-разделитель ","
        file_reader = csv.reader(r_file, delimiter=",")
        count = 0
        lst = []
        for row in file_reader:
            if count == 0:
                count = count
            else:
                # формирование списка рекордов
                lst.append(row[0])
            count += 1
        lst.append(str(time))
        writer(lst)
        return min(lst)


def writer(lst):
    with open("table.csv", mode="w", encoding='utf-8') as w_file:
        file_writer = csv.writer(w_file, delimiter=",", lineterminator="\r")
        for elem in lst:
            file_writer.writerow([elem])