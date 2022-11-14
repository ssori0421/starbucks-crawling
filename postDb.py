import pymongo
import csv
import certifi
from pymongo import MongoClient

import csv
import json


with open('starbucks.json') as file:
    file_data = json.load(file)

    print(file_data)
# if isinstance(file_data, list):

# client = MongoClient('mongodb+srv://test:sparta@cluster0.ffudy0q.mongodb.net/Cluster0?retryWrites=true&w=majority')
# db = client.coffeeduckhu.coffee
#
#
# ca = certifi.where()
#
# client = MongoClient('mongodb+srv://test:sparta@cluster0.2ftmiuw.mongodb.net/?retryWrites=true&w=majority', tlsCaFile=ca)
# db = client.dbsparta

