import csv

results = []
with open("lang/pt-BR.csv", newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=';', quotechar='"')
    for row in reader:
        results.append(row)

print(results[0][0])
