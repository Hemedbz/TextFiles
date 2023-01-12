import csv
import os

with open("superstore_data.csv", "r") as fh:
    content = csv.reader(fh)

    locations = []
    for index, row in enumerate(content):
        if "1958" in row:
            for i, v in enumerate(row):
                if v == "1958":
                    locations.append((index, i))
    print( locations)




