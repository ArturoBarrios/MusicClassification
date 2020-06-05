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
import loader
import numpy as np
import pandas

from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_iris
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from music21 import *
import re
import os
import ntpath



def main():
    # TestStaves("TestSongs/14titlehub.musicxml")
    # TestStaves("TestSongs/beethovens5th.musicxml")
    #TestStaves("TestSongs/Balladenumber4.musicxml")
    for root, dirs, song_files in os.walk("./TestSongs"):
        for file in song_files:
            #new file name
            #fileName = file[0:len(str(file))-4]

            #renames song
            #os.rename("TestSongs/"+file,"TestSongs/"+fileName+"(6).mid")
            TestFeatureExtractor("TestSongs/"+str(file))
def TestFeatureExtractor(file):
    ds = features.DataSet(classLabel='Grade')
    fes = features.extractorsById(['ql1','ql2','ql3'])
    ds.addFeatureExtractors(fes)
    b1 = converter.parse(str(file))
    ds.addData(b1, classValue='1', id=str(file))
    ds.process()
    print("features: ",ds.getAttributeLabels())
    print("stuff: ",ds.getFeaturesAsList()[0][0])

def TestLowLevelFeature(file):
    print("file: ",file)
    curr_stream = converter.parse(str(file))
    fe = features.native.UniqueSetClassSimultaneities(curr_stream)
    f = fe.extract()
    print(f.vector)
    print("ffffffffdffffffff: ",f)



if __name__ == '__main__':
    main()
