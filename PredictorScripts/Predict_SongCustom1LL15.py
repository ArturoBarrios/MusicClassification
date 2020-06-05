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
import pandas as pd


from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from music21 import *
import re
import os
from CustomFeatureSet import CustomFeatures
import ntpath
import GenerateClassInformation as  fb




def main():
    master = Tk()
    master.minsize(300,100)
    master.geometry("420x420")
    master.title("RCM Level Predictor")
    tk.Label(master,
    fg = "blue",
    text="Choose .musicxml file(s) to grade",font="Times").pack()
    #open file
    def callback():
        #can only select .mid files
        files =  filedialog.askopenfilenames(initialdir = "/",title = "Select file",filetypes = (("midi files","*.musicxml"),("all files","*.*")))
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
    key_signatures = {"C major": 1,"G major" : 2, "e minor":3,"D major":4,
    "b minor":5,"A major":6,"f# minor":7,"E major":8,"c# minor":9,
    "B major":10,"g# minor":11,"F# major":12,"d# minor":13,"C# major":14,
    "a# minor":15,
    "F major":16,"d minor":17,"B- major":18,"g minor":19,"E- major":20,
    "c minor":21,"A- major":22,"f minor":23,"D- major":24,
    "b- minor":25,"G- major":26,"e- minor":27,"C- major":28,
    "a- minor":29, "a minor":30}

    custom_feature = CustomFeatures()
    songs_features = dict()
    feature_index = 0

    feature_values = dict()
    print("file: ",file)
    curr_stream = converter.parse(str(file))
    #initialize custom features
    feature_values['total_LRH_notes'] = 0
    feature_values['total_LH_notes'] = 0
    feature_values['total_RH_notes'] = 0

    feature_values['total_LRH_raw_notes'] = 0
    feature_values['total_LH_raw_notes'] = 0
    feature_values['total_RH_raw_notes'] = 0

    feature_values['music_key'] = 0

    feature_values['total_LRH_sharp_keys_pressed'] = 0
    feature_values['total_LH_sharp_keys_pressed'] = 0
    feature_values['total_RH_sharp_keys_pressed'] = 0

    feature_values['total_LRH_flat_keys_pressed'] = 0
    feature_values['total_LH_flat_keys_pressed'] = 0
    feature_values['total_RH_flat_keys_pressed'] = 0

    feature_values['average_RLH_range'] = 0
    feature_values['average_LH_range'] = 0
    feature_values['average_RH_range'] = 0


    feature_values['average_RLH_note_10_range'] = 0
    feature_values['average_LH_note_10_range'] = 0
    feature_values['average_RH_note_10_range'] = 0
    feature_values['average_RLH_note_20_range'] = 0
    feature_values['average_LH_note_20_range'] = 0
    feature_values['average_RH_note_20_range'] = 0
    feature_values['average_RLH_note_35_range'] = 0
    feature_values['average_LH_note_35_range'] = 0
    feature_values['average_RH_note_35_range'] = 0
    feature_values['average_RLH_note_50_range'] = 0
    feature_values['average_LH_note_50_range'] = 0
    feature_values['average_RH_note_50_range'] = 0
    feature_values['average_RLH_note_100_range'] = 0
    feature_values['average_LH_note_100_range'] = 0
    feature_values['average_RH_note_100_range'] = 0

    feature_values['RLH_note_10_range'] = 0
    feature_values['LH_note_10_range'] = 0
    feature_values['RH_note_10_range'] = 0
    feature_values['RLH_note_20_range'] = 0
    feature_values['LH_note_20_range'] = 0
    feature_values['RH_note_20_range'] = 0
    feature_values['RLH_note_35_range'] = 0
    feature_values['LH_note_35_range'] = 0
    feature_values['RH_note_35_range'] = 0
    feature_values['RLH_note_50_range'] = 0
    feature_values['LH_note_50_range'] = 0
    feature_values['RH_note_50_range'] = 0
    feature_values['RLH_note_100_range'] = 0
    feature_values['LH_note_100_range'] = 0
    feature_values['RH_note_100_range'] = 0

    feature_values['average_LRH_2chord_range'] = 0
    feature_values['average_LH_2chord_range'] = 0
    feature_values['average_RH_2chord_range'] = 0
    feature_values['average_LRH_3chord_range'] = 0
    feature_values['average_LH_3chord_range'] = 0
    feature_values['average_RH_3chord_range'] = 0
    feature_values['average_LRH_4chord_range'] = 0
    feature_values['average_LH_4chord_range'] = 0
    feature_values['average_RH_4chord_range'] = 0
    feature_values['average_LRH_5chord_range'] = 0
    feature_values['average_LH_5chord_range'] = 0
    feature_values['average_RH_5chord_range'] = 0

    feature_values['average_LRH_2chord_hand_range'] = 0
    feature_values['average_LH_2chord_hand_range'] = 0
    feature_values['average_RH_2chord_hand_range'] = 0
    feature_values['average_LRH_3chord_hand_range'] = 0
    feature_values['average_LH_3chord_hand_range'] = 0
    feature_values['average_RH_3chord_hand_range'] = 0
    feature_values['average_LRH_4chord_hand_range'] = 0
    feature_values['average_LH_4chord_hand_range'] = 0
    feature_values['average_RH_4chord_hand_range'] = 0
    feature_values['average_LRH_5chord_hand_range'] = 0
    feature_values['average_LH_5chord_hand_range'] = 0
    feature_values['average_RH_5chord_hand_range'] = 0

    feature_values['large_5jumps_LRH'] = 0
    feature_values['large_5jumps_LH'] = 0
    feature_values['large_5jumps_RH'] = 0
    feature_values['large_8jumps_LRH'] = 0
    feature_values['large_8jumps_LH'] = 0
    feature_values['large_8jumps_RH'] = 0
    feature_values['large_9jumps_LRH'] = 0
    feature_values['large_9jumps_LH'] = 0
    feature_values['large_9jumps_RH'] = 0
    feature_values['large_10jumps_LRH'] = 0
    feature_values['large_10jumps_LH'] = 0
    feature_values['large_10jumps_RH'] = 0

    feature_values['average_large_5jumps_LRH'] = 0
    feature_values['average_large_5jumps_LH'] = 0
    feature_values['average_large_5jumps_RH'] = 0
    feature_values['average_large_8jumps_LRH'] = 0
    feature_values['average_large_8jumps_LH'] = 0
    feature_values['average_large_8jumps_RH'] = 0
    feature_values['average_large_9jumps_LRH'] = 0
    feature_values['average_large_9jumps_LH'] = 0
    feature_values['average_large_9jumps_RH'] = 0
    feature_values['average_large_10jumps_LRH'] = 0
    feature_values['average_large_10jumps_LH'] = 0
    feature_values['average_large_10jumps_RH'] = 0

    feature_values['total_LRHwhole_notes'] = 0
    feature_values['total_LRHhalf_notes'] = 0
    feature_values['total_LRHquarter_notes'] = 0
    feature_values['total_LRHeighth_notes'] = 0
    feature_values['total_LRH16th_notes'] = 0
    feature_values['total_LRH32nd_notes'] = 0
    feature_values['total_LRH64th_notes'] = 0
    feature_values['total_LHwhole_notes'] = 0
    feature_values['total_LHhalf_notes'] = 0
    feature_values['total_LHquarter_notes'] = 0
    feature_values['total_LHeighth_notes'] = 0
    feature_values['total_LH16th_notes'] = 0
    feature_values['total_LH32nd_notes'] = 0
    feature_values['total_LH64th_notes'] = 0
    feature_values['total_RHwhole_notes'] = 0
    feature_values['total_RHhalf_notes'] = 0
    feature_values['total_RHquarter_notes'] = 0
    feature_values['total_RHeighth_notes'] = 0
    feature_values['total_RH16th_notes'] = 0
    feature_values['total_RH32nd_notes'] = 0
    feature_values['total_RH64th_notes'] = 0

    feature_values['average_LRHwhole_notes'] = 0
    feature_values['average_LRHhalf_ntoes'] = 0
    feature_values['average_LRHquarter_notes'] = 0
    feature_values['average_LRHeighth_notes'] = 0
    feature_values['average_LRH16th_notes'] = 0
    feature_values['average_LRH32nd_notes'] = 0
    feature_values['average_LRH64th_notes'] = 0
    feature_values['average_LHwhole_notes'] = 0
    feature_values['average_LHhalf_ntoes'] = 0
    feature_values['average_LHquarter_notes'] = 0
    feature_values['average_LHeighth_notes'] = 0
    feature_values['average_LH16th_notes'] = 0
    feature_values['average_LH32nd_notes'] = 0
    feature_values['average_LH64th_notes'] = 0
    feature_values['average_RHwhole_notes'] = 0
    feature_values['average_RHhalf_ntoes'] = 0
    feature_values['average_RHquarter_notes'] = 0
    feature_values['average_RHeighth_notes'] = 0
    feature_values['average_RH16th_notes'] = 0
    feature_values['average_RH32nd_notes'] = 0
    feature_values['average_RH64th_notes'] = 0

    #get parts
    parts = curr_stream.getElementsByClass(stream.Part)
    left_hand_stream = None
    right_hand_stream = None
    both_hands_stream = None
    left_hand_chords = None
    right_hand_chords = None
    both_hands_chords = None
    #only one part so assign one part to right hand
    if len(parts)<2:
        right_hand_stream = parts[0]
    #two or more parts
    else:
        #right hand is always the first staff
        right_hand_stream = parts[0]
        #assign left hand to stream that has the most notes
        left_hand_parts = parts[1:]
        sChords = left_hand_parts[0].chordify()
        sFlat = sChords.flat
        i = 0
        index = 0
        left_hand_index = 0
        left_hand_chords = sFlat.getElementsByClass('Chord')

        print("left hand parts: ",len(left_hand_parts))
        while index<len(left_hand_parts):
            left_hand_part = left_hand_parts[index]
            sChords = left_hand_part.chordify()
            sFlat = sChords.flat
            current = sFlat.getElementsByClass('Chord')
            if len(current)>len(left_hand_chords):
                left_hand_chords = current
                left_hand_index = index
            i+=1
            index+=1
        left_hand_stream = left_hand_parts[left_hand_index]
    #score contains both left and right hand
    score = stream.Score()
    score.insert(0,right_hand_stream)
    if left_hand_stream is not None:
        score.insert(0,left_hand_stream)
    both_hands_stream = score.getElementsByClass(stream.Part)

    #assign chords
    sChords = right_hand_stream.chordify()
    sFlat = sChords.flat
    right_hand_chords = sFlat.getElementsByClass('Chord')
    if left_hand_stream is not None:
        sChords = left_hand_stream.chordify()
        sFlat = sChords.flat
        left_hand_chords = sFlat.getElementsByClass('Chord')
    sChords = both_hands_stream.chordify()
    sFlat = sChords.flat
    both_hands_chords = sFlat.getElementsByClass('Chord')
####################################################################extract custom features
    #total notes as chords&&&&&&&&&&&&
    sChords = right_hand_stream.chordify()
    sFlat = sChords.flat
    sOnlyChords = sFlat.getElementsByClass('Chord')
    feature_values['total_RH_notes'] = len(sOnlyChords)
    print("RH_notes ",len(sOnlyChords))
    right_notes_count = len(sOnlyChords)
    left_notes_count = 0
    if left_hand_stream is not None:
        sChords = left_hand_stream.chordify()
        sFlat = sChords.flat
        sOnlyChords = sFlat.getElementsByClass('Chord')
        feature_values['total_LH_notes'] = len(sOnlyChords)
        left_notes_count = len(sOnlyChords)
        print("LH_notes ",len(sOnlyChords))
    feature_values['total_LRH_notes'] = right_notes_count+left_notes_count
    print("total notes before call: ",len(both_hands_stream.flat.getElementsByClass("Note")))
    #total raw notes
    feature_values['total_LRH_raw_notes'] = len(both_hands_stream.flat.getElementsByClass("Note"))
    if left_hand_stream is not None:
        feature_values['total_LH_raw_notes'] = len(left_hand_stream.flat.getElementsByClass("Note"))
    else:
        feature_values['total_LH_raw_notes'] = 0
    feature_values['total_RH_raw_notes'] = len(right_hand_stream.flat.getElementsByClass("Note"))
    #key signature:
    music_key = curr_stream.analyze('key')
    feature_values['music_key'] = key_signatures[str(music_key)]
    #number of black keys pressed
    feature_values['total_LRH_sharp_keys_pressed'] = custom_feature.totalSharpNotes(both_hands_stream)
    feature_values['total_LH_sharp_keys_pressed'] = custom_feature.totalSharpNotes(left_hand_stream)
    feature_values['total_RH_sharp_keys_pressed'] = custom_feature.totalSharpNotes(right_hand_stream)
    #number of flat keys pressed
    feature_values['total_LRH_flat_keys_pressed'] = custom_feature.totalFlatNotes(both_hands_stream)
    feature_values['total_LH_flat_keys_pressed'] = custom_feature.totalFlatNotes(left_hand_stream)
    feature_values['total_RH_flat_keys_pressed'] = custom_feature.totalFlatNotes(right_hand_stream)
    #average range in hand
    feature_values['average_RLH_range'] = custom_feature.averageRangeForNextNotes(both_hands_chords)
    feature_values['average_LH_range'] = custom_feature.averageRangeForNextNotes(left_hand_chords)
    feature_values['average_RH_range'] = custom_feature.averageRangeForNextNotes(right_hand_chords)
    #average range for top 10% percent of notes
    feature_values['average_RLH_note_10_range'] = custom_feature.averageRange2OfTopXPercent(both_hands_stream,.1)
    feature_values['average_LH_note_10_range'] = custom_feature.averageRange2OfTopXPercent(left_hand_stream,.1)
    feature_values['average_RH_note_10_range'] = custom_feature.averageRange2OfTopXPercent(right_hand_stream,.1)
    #average range for top 20% percent of notes
    feature_values['average_RLH_note_20_range'] = custom_feature.averageRange2OfTopXPercent(both_hands_stream,.2)
    feature_values['average_LH_note_20_range'] = custom_feature.averageRange2OfTopXPercent(left_hand_stream,.2)
    feature_values['average_RH_note_20_range'] = custom_feature.averageRange2OfTopXPercent(right_hand_stream,.2)
    #average range for top 35% percent of notes
    feature_values['average_RLH_note_35_range'] = custom_feature.averageRange2OfTopXPercent(both_hands_stream,.35)
    feature_values['average_LH_note_35_range'] = custom_feature.averageRange2OfTopXPercent(left_hand_stream,.35)
    feature_values['average_RH_note_35_range'] = custom_feature.averageRange2OfTopXPercent(right_hand_stream,.35)
    #average range for top 50% percent of notes
    feature_values['average_RLH_note_50_range'] = custom_feature.averageRange2OfTopXPercent(both_hands_stream,.5)
    feature_values['average_LH_note_50_range'] = custom_feature.averageRange2OfTopXPercent(left_hand_stream,.5)
    feature_values['average_RH_note_50_range'] = custom_feature.averageRange2OfTopXPercent(right_hand_stream,.5)
    #average range for top 100% percent of notes
    feature_values['average_RLH_note_100_range'] = custom_feature.averageRange2OfTopXPercent(both_hands_stream,1)
    feature_values['average_LH_note_100_range'] = custom_feature.averageRange2OfTopXPercent(left_hand_stream,1)
    feature_values['average_RH_note_100_range'] = custom_feature.averageRange2OfTopXPercent(right_hand_stream,1)

    #range for top 10% percent of notes
    feature_values['RLH_note_10_range'] = custom_feature.rangeOfTopXPercent(both_hands_stream,.1)
    feature_values['LH_note_10_range'] = custom_feature.rangeOfTopXPercent(left_hand_stream,.1)
    feature_values['RH_note_10_range'] = custom_feature.rangeOfTopXPercent(right_hand_stream,.1)
    # range for top 20% percent of notes
    feature_values['RLH_note_20_range'] = custom_feature.rangeOfTopXPercent(both_hands_stream,.2)
    feature_values['LH_note_20_range'] = custom_feature.rangeOfTopXPercent(left_hand_stream,.2)
    feature_values['RH_note_20_range'] = custom_feature.rangeOfTopXPercent(right_hand_stream,.2)
    # range for top 35% percent of notes
    feature_values['RLH_note_35_range'] = custom_feature.rangeOfTopXPercent(both_hands_stream,.35)
    feature_values['LH_note_35_range'] = custom_feature.rangeOfTopXPercent(left_hand_stream,.35)
    feature_values['RH_note_35_range'] = custom_feature.rangeOfTopXPercent(right_hand_stream,.35)
    # range for top 50% percent of notes
    feature_values['RLH_note_50_range'] = custom_feature.rangeOfTopXPercent(both_hands_stream,.5)
    feature_values['LH_note_50_range'] = custom_feature.rangeOfTopXPercent(left_hand_stream,.5)
    feature_values['RH_note_50_range'] = custom_feature.rangeOfTopXPercent(right_hand_stream,.5)
    # range for top 100% percent of notes
    feature_values['RLH_note_100_range'] = custom_feature.rangeOfTopXPercent(both_hands_stream,1)
    feature_values['LH_note_100_range'] = custom_feature.rangeOfTopXPercent(left_hand_stream,1)
    feature_values['RH_note_100_range'] = custom_feature.rangeOfTopXPercent(right_hand_stream,1)

    #average range for each finger in chord
    feature_values['average_LRH_2chord_range'] = custom_feature.averageChordRangeForHand(both_hands_chords,2)
    feature_values['average_LH_2chord_range'] = custom_feature.averageChordRangeForHand(left_hand_chords,2)
    feature_values['average_RH_2chord_range'] = custom_feature.averageChordRangeForHand(right_hand_chords,2)

    feature_values['average_LRH_3chord_range'] = custom_feature.averageChordRangeForHand(both_hands_chords,3)
    feature_values['average_LH_3chord_range'] = custom_feature.averageChordRangeForHand(left_hand_chords,3)
    feature_values['average_RH_3chord_range'] = custom_feature.averageChordRangeForHand(right_hand_chords,3)

    feature_values['average_LRH_4chord_range'] = custom_feature.averageChordRangeForHand(both_hands_chords,4)
    feature_values['average_LH_4chord_range'] = custom_feature.averageChordRangeForHand(left_hand_chords,4)
    feature_values['average_RH_4chord_range'] = custom_feature.averageChordRangeForHand(right_hand_chords,4)

    feature_values['average_LRH_5chord_range'] = custom_feature.averageChordRangeForHand(both_hands_chords,5)
    feature_values['average_LH_5chord_range'] = custom_feature.averageChordRangeForHand(left_hand_chords,5)
    feature_values['average_RH_5chord_range'] = custom_feature.averageChordRangeForHand(right_hand_chords,5)

    #average range for each hand
    feature_values['average_LRH_2chord_hand_range'] = custom_feature.average2ChordRangeForHand(both_hands_chords,2)
    feature_values['average_LH_2chord_hand_range'] = custom_feature.average2ChordRangeForHand(left_hand_chords,2)
    feature_values['average_RH_2chord_hand_range'] = custom_feature.average2ChordRangeForHand(right_hand_chords,2)

    feature_values['average_LRH_3chord_hand_range'] = custom_feature.average2ChordRangeForHand(both_hands_chords,3)
    feature_values['average_LH_3chord_hand_range'] = custom_feature.average2ChordRangeForHand(left_hand_chords,3)
    feature_values['average_RH_3chord_hand_range'] = custom_feature.average2ChordRangeForHand(right_hand_chords,3)

    feature_values['average_LRH_4chord_hand_range'] = custom_feature.average2ChordRangeForHand(both_hands_chords,4)
    feature_values['average_LH_4chord_hand_range'] = custom_feature.average2ChordRangeForHand(left_hand_chords,4)
    feature_values['average_RH_4chord_hand_range'] = custom_feature.average2ChordRangeForHand(right_hand_chords,4)

    feature_values['average_LRH_5chord_hand_range'] = custom_feature.average2ChordRangeForHand(both_hands_chords,5)
    feature_values['average_LH_5chord_hand_range'] = custom_feature.average2ChordRangeForHand(left_hand_chords,5)
    feature_values['average_RH_5chord_hand_range'] = custom_feature.average2ChordRangeForHand(right_hand_chords,5)

    #large jumps
    feature_values['large_5jumps_LRH'] = custom_feature.largeJumps(both_hands_chords,5)
    feature_values['large_5jumps_LH'] = custom_feature.largeJumps(left_hand_chords,5)
    feature_values['large_5jumps_RH'] = custom_feature.largeJumps(right_hand_chords,5)

    feature_values['large_8jumps_LRH'] = custom_feature.largeJumps(both_hands_chords,8)
    feature_values['large_8jumps_LH'] = custom_feature.largeJumps(left_hand_chords,8)
    feature_values['large_8jumps_RH'] = custom_feature.largeJumps(right_hand_chords,8)

    feature_values['large_9jumps_LRH'] = custom_feature.largeJumps(both_hands_chords,9)
    feature_values['large_9jumps_LH'] = custom_feature.largeJumps(left_hand_chords,9)
    feature_values['large_9jumps_RH'] = custom_feature.largeJumps(right_hand_chords,9)

    feature_values['large_10jumps_LRH'] = custom_feature.largeJumps(both_hands_chords,10)
    feature_values['large_10jumps_LH'] = custom_feature.largeJumps(left_hand_chords,10)
    feature_values['large_10jumps_RH'] = custom_feature.largeJumps(right_hand_chords,10)

    #average large jumps
    feature_values['average_large_5jumps_LRH'] = custom_feature.averageLargeJumps(both_hands_chords,5)
    feature_values['average_large_5jumps_LH'] = custom_feature.averageLargeJumps(left_hand_chords,5)
    feature_values['average_large_5jumps_RH'] = custom_feature.averageLargeJumps(right_hand_chords,5)

    feature_values['average_large_8jumps_LRH'] = custom_feature.averageLargeJumps(both_hands_chords,8)
    feature_values['average_large_8jumps_LH'] = custom_feature.averageLargeJumps(left_hand_chords,8)
    feature_values['average_large_8jumps_RH'] = custom_feature.averageLargeJumps(right_hand_chords,8)

    feature_values['average_large_9jumps_LRH'] = custom_feature.averageLargeJumps(both_hands_chords,9)
    feature_values['average_large_9jumps_LH'] = custom_feature.averageLargeJumps(left_hand_chords,9)
    feature_values['average_large_9jumps_RH'] = custom_feature.averageLargeJumps(right_hand_chords,9)

    feature_values['average_large_10jumps_LRH'] = custom_feature.averageLargeJumps(both_hands_chords,10)
    feature_values['average_large_10jumps_LH'] = custom_feature.averageLargeJumps(left_hand_chords,10)
    feature_values['average_large_10jumps_RH'] = custom_feature.averageLargeJumps(right_hand_chords,10)

    #note type total count
    feature_values['total_LRHwhole_notes'] = custom_feature.totalWholeNotes(both_hands_chords)
    feature_values['total_LRHhalf_notes'] = custom_feature.totalHalfNotes(both_hands_chords)
    feature_values['total_LRHquarter_notes'] = custom_feature.totalQuarterNotes(both_hands_chords)
    feature_values['total_LRHeighth_notes'] = custom_feature.totalEighthNotes(both_hands_chords)
    feature_values['total_LRH16th_notes'] = custom_feature.total16thNotes(both_hands_chords)
    feature_values['total_LRH32nd_notes'] = custom_feature.total32ndNotes(both_hands_chords)
    feature_values['total_LRH64th_notes'] = custom_feature.total64thNotes(both_hands_chords)
    feature_values['total_LHwhole_notes'] = custom_feature.totalWholeNotes(left_hand_stream)
    feature_values['total_LHhalf_notes'] = custom_feature.totalHalfNotes(left_hand_stream)
    feature_values['total_LHquarter_notes'] = custom_feature.totalQuarterNotes(left_hand_stream)
    feature_values['total_LHeighth_notes'] = custom_feature.totalEighthNotes(left_hand_stream)
    feature_values['total_LH16th_notes'] = custom_feature.total16thNotes(left_hand_stream)
    feature_values['total_LH32nd_notes'] = custom_feature.total32ndNotes(left_hand_stream)
    feature_values['total_LH64th_notes'] = custom_feature.total64thNotes(left_hand_stream)
    feature_values['total_RHwhole_notes'] = custom_feature.totalWholeNotes(right_hand_stream)
    feature_values['total_RHhalf_notes'] = custom_feature.totalHalfNotes(right_hand_stream)
    feature_values['total_RHquarter_notes'] = custom_feature.totalQuarterNotes(right_hand_stream)
    feature_values['total_RHeighth_notes'] = custom_feature.totalEighthNotes(right_hand_stream)
    feature_values['total_RH16th_notes'] = custom_feature.total16thNotes(right_hand_stream)
    feature_values['total_RH32nd_notes'] = custom_feature.total32ndNotes(right_hand_stream)
    feature_values['total_RH64th_notes'] = custom_feature.total64thNotes(right_hand_stream)

    #note type average
    feature_values['average_LRHwhole_notes'] = custom_feature.averageWholeNotes(both_hands_stream)
    feature_values['average_LRHhalf_ntoes'] = custom_feature.averageHalfNotes(both_hands_stream)
    feature_values['average_LRHquarter_notes'] = custom_feature.averageQuarterNotes(both_hands_stream)
    feature_values['average_LRHeighth_notes'] = custom_feature.averageEighthNotes(both_hands_stream)
    feature_values['average_LRH16th_notes'] = custom_feature.average16thNotes(both_hands_stream)
    feature_values['average_LRH32nd_notes'] = custom_feature.average32ndNotes(both_hands_stream)
    feature_values['average_LRH64th_notes'] = custom_feature.average64thNotes(both_hands_stream)
    feature_values['average_LHwhole_notes'] = custom_feature.averageWholeNotes(left_hand_stream)
    feature_values['average_LHhalf_ntoes'] = custom_feature.averageHalfNotes(left_hand_stream)
    feature_values['average_LHquarter_notes'] = custom_feature.averageQuarterNotes(left_hand_stream)
    feature_values['average_LHeighth_notes'] = custom_feature.averageEighthNotes(left_hand_stream)
    feature_values['average_LH16th_notes'] = custom_feature.average16thNotes(left_hand_stream)
    feature_values['average_LH32nd_notes'] = custom_feature.average32ndNotes(left_hand_stream)
    feature_values['average_LH64th_notes'] = custom_feature.average64thNotes(left_hand_stream)
    feature_values['average_RHwhole_notes'] = custom_feature.averageWholeNotes(right_hand_stream)
    feature_values['average_RHhalf_ntoes'] = custom_feature.averageHalfNotes(right_hand_stream)
    feature_values['average_RHquarter_notes'] = custom_feature.averageQuarterNotes(right_hand_stream)
    feature_values['average_RHeighth_notes'] = custom_feature.averageEighthNotes(right_hand_stream)
    feature_values['average_RH16th_notes'] = custom_feature.average16thNotes(right_hand_stream)
    feature_values['average_RH32nd_notes'] = custom_feature.average32ndNotes(right_hand_stream)
    feature_values['average_RH64th_notes'] = custom_feature.average64thNotes(right_hand_stream)
    try:
        feature_values['MostCommonNoteQuarterLength'] = features.native.MostCommonNoteQuarterLength(score).extract().vector[0]
    except:
        feature_values['MostCommonNoteQuarterLength'] = 0
        print("error")
    print("MostCommonNoteQuarterLength Done")

    try:
        feature_values['MostCommonNoteQuarterLengthPrevalence'] = features.native.MostCommonNoteQuarterLengthPrevalence(score).extract().vector[0]
    except:
        feature_values['MostCommonNoteQuarterLengthPrevalence'] = 0
        print("error")
    print("MostCommonNoteQuarterLengthPrevalence Done")

    try:
        feature_values['MostCommonSetClassSimultaneityPrevalence'] = features.native.MostCommonSetClassSimultaneityPrevalence(score).extract().vector[0]
    except:
        feature_values['MostCommonSetClassSimultaneityPrevalence'] = 0
        print("error")
    print("MostCommonSetClassSimultaneityPrevalence Done")

    try:
        feature_values['TriadSimultaneityPrevalence'] = features.native.TriadSimultaneityPrevalence(score).extract().vector[0]
    except:
        feature_values['TriadSimultaneityPrevalence'] = 0
        print("error")
    print("TriadSimultaneityPrevalence Done")

    try:
        feature_values['UniquePitchClassSetSimultaneities'] = features.native.UniquePitchClassSetSimultaneities(score).extract().vector[0]
    except:
        feature_values['UniquePitchClassSetSimultaneities'] = 0
        print("error")
    print("UniquePitchClassSetSimultaneities Done")

    try:
        feature_values['UniqueSetClassSimultaneities'] = features.native.UniqueSetClassSimultaneities(score).extract().vector[0]
    except:
        feature_values['UniqueSetClassSimultaneities'] = 0
        print("error")
    print("UniqueSetClassSimultaneities Done")

    try:
        feature_values['AverageNoteDurationFeature'] = features.jSymbolic.AverageNoteDurationFeature(score).extract().vector[0]
    except:
        feature_values['AverageNoteDurationFeature'] = 0
        print("error")
    print("AverageNoteDurationFeature Done")

    try:
        feature_values['AverageTimeBetweenAttacksFeature'] = features.jSymbolic.AverageTimeBetweenAttacksFeature(score).extract().vector[0]
    except:
        feature_values['AverageTimeBetweenAttacksFeature'] = 0
    print("AverageTimeBetweenAttacksFeature Done")

    try:
        feature_values['AverageTimeBetweenAttacksForEachVoiceFeature'] = features.jSymbolic.AverageTimeBetweenAttacksForEachVoiceFeature(score).extract().vector[0]
    except:
        feature_values['AverageTimeBetweenAttacksForEachVoiceFeature'] = 0
        print("error")
    print("AverageTimeBetweenAttacksForEachVoiceFeature Done")

    try:
        feature_values['DirectionOfMotionFeature'] = features.jSymbolic.DirectionOfMotionFeature(score).extract().vector[0]
    except:
        feature_values['DirectionOfMotionFeature'] = 0
        print("error")
    print("DirectionOfMotionFeature Done")

    try:
        feature_values['ImportanceOfHighRegisterFeature'] = features.jSymbolic.ImportanceOfHighRegisterFeature(score).extract().vector[0]
    except:
        feature_values['ImportanceOfHighRegisterFeature'] = 0
        print("error")
    print("ImportanceOfHighRegisterFeature Done")

    try:
        feature_values['NoteDensityFeature'] = features.jSymbolic.NoteDensityFeature(score).extract().vector[0]
    except:
        feature_values['NoteDensityFeature'] = 0
        print("error")
    print("NoteDensityFeature Done")

    try:
        feature_values['PitchVarietyFeature'] = features.jSymbolic.PitchVarietyFeature(score).extract().vector[0]
    except:
        eature_values['PitchVarietyFeature'] = 0
        print("error")
    print("PitchVarietyFeature Done")

    try:
        feature_values['RelativeStrengthOfTopPitchClassesFeature'] = features.jSymbolic.RelativeStrengthOfTopPitchClassesFeature(score).extract().vector[0]
    except:
        feature_values['RelativeStrengthOfTopPitchClassesFeature'] = 0
        print("error")
    print("RelativeStrengthOfTopPitchClassesFeature Done")

    try:
        feature_values['RelativeStrengthOfTopPitchesFeature'] = features.jSymbolic.RelativeStrengthOfTopPitchesFeature(score).extract().vector[0]
    except:
        feature_values['RelativeStrengthOfTopPitchesFeature'] = 0
        print("error")
    print("RelativeStrengthOfTopPitchesFeature Done")
    feature_values['Name'] = str(file)
    if(feature_index==0):
        labels_file = open("./IrisTextFiles/temp.txt","w")
        f = open("./IrisTextFiles/temp.csv","w")

    write_index = 0
    #print("feature values: ",feature_values)
    for key,feature_value in feature_values.items():
        # if(feature_value is None):
        #     print(key,"  ",feature_value)
        #write feature string
        if feature_index==0:
            if write_index<len(feature_values)-1:
                labels_file.write(str(key)+",")
                f.write(str(key)+",")
            else:
                labels_file.write(str(key))
                f.write(str(key))
        if feature_index not in songs_features:
            songs_features[feature_index] = []
            songs_features[feature_index].append(feature_value)
        else:
            songs_features[feature_index].append(feature_value)
        write_index+=1
    print("song index: ",feature_index)
    feature_index+=1
    f.write("\n")

    print("music processed...Now adding features")


    for key,song_features in songs_features.items():
        i = 0
        write_index = 0
        for feature in song_features:
            if i<len(song_features)-1:
                f.write(str(feature)+",")
            else:
                f.write(str(feature))
            i+=1
            write_index +=1
        f.write("\n")
    print("feature values added")
    f.flush()
    f.seek(0)
    ###################################################################predict values of unknown features
    data = pd.read_csv("./IrisTextFiles/temp.csv")
    labels=data['Name']
    X = data.drop(['Name'],axis=1)
    filename = "./ClassificationModels/GBRLowLevelCustomFeaturesModel.sav"
    loaded_model = joblib.load(filename)

    #print predictions
    predictions = loaded_model.predict(X)
    i = 0
    return predictions[0]



if __name__ == '__main__':
    main()
