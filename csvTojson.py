import csv
import json

csvfile = open('starbucks.csv', 'r')
jsonfile = open('starbucks.json', 'w')

fieldnames = ('cafe', 'coffee_name', 'coffee_image',	'coffee_desc', 'type', 'calorie', 'salt', 'saturated_fat', 'sugars', 'protein', 'caffeine')

reader =csv.DictReader( csvfile, fieldnames)
for row in reader:
    json.dump(row, jsonfile)
    jsonfile.write(', \n')
