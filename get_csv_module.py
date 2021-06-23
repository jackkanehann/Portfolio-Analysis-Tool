"""
Module for extracting, cleansing, and preprocessing csv data files for portfolio analysis
"""
import pandas as pd

print("get_csv_module has loaded")

def display_file_location(path, file_name):
    print("File Location: {}".format(path+file_name))

class CSVGetInfo:
    def __init__(self, path, file_name):
        self.path = path
        self.file_name = file_name
 
    def display_summary(self):
        data = pd.read_csv(self.path + self.file_name)
        print(self.file_name)
        print(data.info())
