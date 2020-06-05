# Library imports
from tkinter import filedialog

from tkinter import *
import tkinter as tk

import pandas
import numpy as np
#
# Local imports
from sklearn.svm import SVC
from sklearn.externals import joblib

import re
import os
import ntpath
import pandas as pd

class ClassInformation:
    def __init__(self):
        print("nothing to construct here")


    def average_values(self,file_path):
        total_values = dict()
        data = pd.read_csv(file_path)
        labels=data['Grade']
        X = data
        count = 0
        data_list_dict = X.T.to_dict().values()
        grade_count = dict()
        for data_dict in data_list_dict:

            grade = float(data_dict['Grade'])
            #grade count
            if grade not in grade_count:
                grade_count[grade] = 1
            else:
                grade_count[grade] +=1
            #print(grade)
            if grade not in total_values:
                total_values[grade] = dict()
            # print(data_dict['Grade'])
            for key,value in data_dict.items():
                if key not in total_values[grade]:
                    total_values[grade][key] = value
                else:
                    total_values[grade][key] += value
            count+=1
        print(count)
        #print(total_values[1.0])


        #average values
        for key,values in total_values.items():
            for feature,f_value in total_values[key].items():
                total_values[key][feature] = f_value/grade_count[key]
        return total_values


    def average_values_unknown(self,file_path,unknown_grade):
        total_values = dict()
        data = pd.read_csv(file_path)
        labels=data['Name']
        X = data
        count = 0
        data_list_dict = X.T.to_dict().values()
        grade_count = dict()
        for data_dict in data_list_dict:

            grade = unknown_grade
            #grade count
            if grade not in grade_count:
                grade_count[grade] = 1
            else:
                grade_count[grade] +=1
            #print(grade)
            if grade not in total_values:
                total_values[grade] = dict()
            # print(data_dict['Grade'])
            for key,value in data_dict.items():
                if key not in total_values[grade]:
                    total_values[grade][key] = value
                else:
                    total_values[grade][key] += value
            count+=1
        print(count)
        #print(total_values[1.0])


        #average values
        for key,values in total_values.items():
            for feature,f_value in total_values[key].items():
                total_values[key][feature] = f_value
        return total_values
