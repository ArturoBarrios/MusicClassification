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
    master = Tk()
    master.minsize(300,100)
    master.geometry("420x420")
    master.title("RCM Level Predictor")
    tk.Label(master,
    fg = "blue",
    text="Choose .mid files to grade",font="Times").pack()
    #open file
    def callback():
        #can only select .mid files
        files =  filedialog.askopenfilenames(initialdir = "/",title = "Select file",filetypes = (("midi files","*.mid"),("all files","*.*")))
        files = master.tk.splitlist(files)
        for file in files:
            #classify song
            level = Classify_Song(file)
            #print level
            tk.Label(master,
            fg = "green",
            text="RCM Level for "+str(path_leaf(file))+": "+str(level),font="Times").pack()

    photo=PhotoImage(file="add.png")
    #choose file button
    b = Button(master,image=photo, command=callback, height=50, width=150)
    b.pack()
    mainloop()



def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)




def Classify_Song(file):
    #get all unique chords in model
    model_file = open("IrisTextFiles/music_IrisWCG3.txt","r")
    chords_in_model_file = model_file.readlines()[0].split(',')
    chords_in_model = []
    print(len(chords_in_model_file))
    for chord in chords_in_model_file[7:]:
        chords_in_model.append(str(chord).replace('\n',''))

    #index used in iris file
    index = 1

    #list of unique chords
    #any new chord found will be put at the end of list
    unique_chords = []

    #key: id   values: list of feature values
    #values: length of music, key signature, number of notes,
    #total measures, time signature num, time signature den, bpm, chords
    songs_features = dict()

    #key signature dictionary
    key_signatures = {"C major": 1,"G major" : 2, "e minor":3,"D major":4,
    "b minor":5,"A major":6,"f# minor":7,"E major":8,"c# minor":9,
    "B major":10,"g# minor":11,"F# major":12,"d# minor":13,"C# major":14,
    "a# minor":15,
    "F major":16,"d minor":17,"B- major":18,"g minor":19,"E- major":20,
    "c minor":21,"A- major":22,"f minor":23,"D- major":24,
    "b- minor":25,"G- major":26,"e- minor":27,"C- major":28,
    "a- minor":29, "a minor":30}



    print("file: ",file)
    chords_in_piece = dict()
    curr_stream = converter.parse(str(file))

    #Length of music: time in which last note ends(72)
    music_len = curr_stream.highestTime

    #key signature:
    music_key = curr_stream.analyze('key')

    music_key = key_signatures[str(music_key)]

    #number of notes, need to add number of chords
    notes = curr_stream.flat.getElementsByClass("note")
    num_notes = len(notes)

    #total Measures
    total_measures = len(curr_stream.measures(0,10000)[0])

    time_signature_den = 0
    time_signature_num = 0
    #time Signature
    time_signature_num = curr_stream[0].getTimeSignatures()[0].numerator
    time_signature_den = curr_stream[0].getTimeSignatures()[0].denominator

    #chords
    sChords = curr_stream.chordify()
    sFlat = sChords.flat
    sOnlyChords = sFlat.getElementsByClass('Chord')
    #add chords to number_of_notes
    num_notes+=len(sOnlyChords)
    #put chords in chords_in_piece dictionary
    for chord in sOnlyChords:
        # #check if chord in unique chord list
        # if chord.pitchedCommonName not in unique_chords and len(chord)>2:
        #     unique_chords.append(chord.pitchedCommonName)

        #put chord in chords_in_piece dictionary
        if(len(chord) > 2):
            #I don't think you'd need this part(part below)
            # if chord.pitchedCommonName not in chords_in_piece:
            #     chords_in_piece[chord.pitchedCommonName] = 1
            # else:
            if chord.pitchedCommonName in chords_in_piece:
                chords_in_piece[chord.pitchedCommonName] += 1


    #range between lowest and highest note
    #notes = curr_stream.flat.getElementsByClass(note.Note)
    pitches = []
    min_pitch = 0
    max_pitch = 0
    #pitches for notes
    for n in notes:
        pitches.append(n.pitch.frequency)
    #pitches for notes in chords
    for chord in sOnlyChords:
        for note in chord:
            pitches.append(note.pitch.frequency)
    min_pitch = min(pitches)
    print("min: ",min_pitch)
    max_pitch = max(pitches)
    print("max: ",max_pitch)
    #max pitch - min pitch = range
    range = max_pitch-min_pitch

    print("range: ",range)

    #put features in song_features
    songs_features[index] = []
    songs_features[index].append(music_len)
    songs_features[index].append(music_key)
    songs_features[index].append(num_notes)
    songs_features[index].append(total_measures)
    songs_features[index].append(time_signature_num)
    songs_features[index].append(time_signature_den)
    songs_features[index].append(range)
    #print("range ",range)

    #put chords in song_features
    for chord in chords_in_model:
        #put count value if chord is in chords_in_piece
        if chord in chords_in_piece:
            songs_features[index].append(chords_in_piece[chord])
        else:
            songs_features[index].append(0)

    songs_features[index].append("-1")

    index+=1

    f = open("IrisTextFiles/music_IrisWCUknown.csv","w")
    labels_file = open("IrisTextFiles/music_IrisWCUknown.txt","w")
    f.write("Id,length,key,number_of_notes,total_measures,"
    "time_signature_num,time_signature_den,range,")
    labels_file.write("length,key,number_of_notes,total_measures,"
    "time_signature_num,time_signature_den,range,")
    i = 0
    #write unique chords in first line
    for chord in chords_in_model:
        if i<len(chords_in_model):
            f.write(chord)
            f.write(",")
            labels_file.write(chord)
            labels_file.write(",")
            i+=1




    f.write("Grade\n")
    #use song_features dictionary to
    #write song id, song features, and song grade
    for id,feature_list in songs_features.items():
        #these are the first 6 features which don't include chords
        f.write(str(id)+","+str(songs_features[id][0])+","+str(songs_features[id][1])
        +","+str(songs_features[id][2])+","+str(songs_features[id][3])+","
        +str(songs_features[id][4])+","+str(songs_features[id][5])+","
        +str(songs_features[id][6])+",")
        chord_list = feature_list[7:len(feature_list)-1]
        song_chord_index = 0
        print(len(chord_list))
        #write chords count for piece
        for chord in chords_in_model:

            if(song_chord_index<len(chord_list)):
                #apply weights to chords
                chord_count = int(chord_list[song_chord_index])
                chord_count = chord_count/len(chord_list)
                f.write(str(chord_count))
                song_chord_index+=1
                f.write(",")
            else:
                f.write("0,")
                song_chord_index+=1

        #write grade for piece
        f.write("-1")
        f.write("\n")

    f.flush()
    f.seek(0)
    labels_file.flush()
    labels_file.seek(0)

    x_labels = []
    f = open("IrisTextFiles/music_IrisWCG3.txt","r")
    line = f.read()
    #put labels in x_labels
    for label in line.split(","):
        x_labels.append(label)

    X, y, type2id = loader.load_data('IrisTextFiles/music_IrisWCUknown.csv', y_label="Grade", x_labels=x_labels)

    print("length of X: ",len(X[0]))
    # dividing X, y into train and test data
    ####X_train, X_test, y_train, y_test = train_test_split(X, y, random_state = 2)

    # training a linear SVM classifier
    from sklearn.svm import SVC
    # print(X_train)
    ### svm_model_linear = SVC(kernel = 'poly',degree= 10).fit(X_test, y_test)

    #classify unknown songs
    #grades array changes whenever SVMMain runs
    #changes with label2id
    grades = {0:7,1:3,2:10,3:1,4:5,5:9,6:6,7:8,8:2,9:4}
    filename = "ClassificationModels/finalized_music_model.sav"
    loaded_model = joblib.load(filename)
    #[class array] = {'8','7','5','2','3','10','6','4','9','1'}
    result = loaded_model.predict(X)
    print(int(result[0]))
    return grades[result[0]]


if __name__ == '__main__':
    main()
