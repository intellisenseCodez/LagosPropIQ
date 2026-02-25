import csv
import json

def to_csv(data, filename):
    for row in data:
        fieldnames = row[0].keys()

    with open(filename, "w", newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    print(f"CSV file {filename} created successfully.")





