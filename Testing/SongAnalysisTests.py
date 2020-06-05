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

    for root, dirs, song_files in os.walk("./Midi_Files/AmbroseTabsDatabase/AmbrosePianoTabsNoFilter/World Folk/Grade 8"):
        for file in song_files:
            #new file name
            fileName = file[0:len(str(file))-4]

            #renames song
            os.rename("./Midi_Files/AmbroseTabsDatabase/AmbrosePianoTabsNoFilter/World Folk/Grade 8/"+file,"./Midi_Files/AmbroseTabsDatabase/AmbrosePianoTabsNoFilter/World Folk/Grade 8/"+fileName+"XMAS(8).mid")
            #TestStaves("./Midi_Files/AmbroseTabsDatabase/AmbrosePianoTabsNoFilter/Childrens/Grade 9/"+str(file))



#testing to see how to get individual staves(left and right hand)
def TestStaves(file):

    #I assume this is the left and right hand
    print(file,end="  ")
    score = converter.parse(str(file))
    parts = score.getElementsByClass(stream.Part)
    print(len(parts))


    # print(parts[1])








if __name__ == '__main__':
    main()
