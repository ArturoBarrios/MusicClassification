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
import os


from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_iris
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from music21 import *
import re
import os
import ntpath
from collections import Counter



def main():
    # TestStaves("TestSongs/14titlehub.musicxml")
    # TestStaves("TestSongs/beethovens5th.musicxml")
    #TestStaves("TestSongs/Balladenumber4.musicxml")
    count = 0
    for root, dirs, song_files in os.walk("./TestSongs"):
        for file in song_files:
            #new file name
            #fileName = file[0:len(str(file))-4]

            #renames song
            #os.rename("TestSongs/"+file,"TestSongs/"+fileName+"(6).mid")
            Test("TestSongs/"+str(file))

#testing to see how to get individual staves(left and right hand)
def TestStaves(file):
    #I assume this is the left and right hand
    print(file,end="  ")
    score = converter.parse(str(file))
    parts = score.getElementsByClass(stream.Part)
    print(len(parts))

def Test(file):
    #Low level features
    fes = [features.native.DiminishedSeventhSimultaneityPrevalence,
    features.native.DiminishedTriadSimultaneityPrevalence,
    features.native.DominantSeventhSimultaneityPrevalence,
    features.native.LandiniCadence,
    features.native.MajorTriadSimultaneityPrevalence,
    features.native.MinorTriadSimultaneityPrevalence,
    features.native.MostCommonNoteQuarterLength,
    features.native.MostCommonNoteQuarterLengthPrevalence,
    features.native.MostCommonPitchClassSetSimultaneityPrevalence,
    features.native.MostCommonSetClassSimultaneityPrevalence,
    features.native.RangeOfNoteQuarterLengths,
    features.native.TonalCertainty,
    features.native.TriadSimultaneityPrevalence,
    features.native.UniqueNoteQuarterLengths,
    features.native.UniquePitchClassSetSimultaneities,
    features.native.UniqueSetClassSimultaneities,
    features.jSymbolic.AmountOfArpeggiationFeature,
    features.jSymbolic.AverageMelodicIntervalFeature,
    features.jSymbolic.AverageNoteDurationFeature,
    features.jSymbolic.AverageNumberOfIndependentVoicesFeature,
    features.jSymbolic.AverageTimeBetweenAttacksFeature,
    features.jSymbolic.AverageTimeBetweenAttacksForEachVoiceFeature,
    features.jSymbolic.AverageVariabilityOfTimeBetweenAttacksForEachVoiceFeature,
    features.jSymbolic.ChangesOfMeterFeature,
    features.jSymbolic.ChromaticMotionFeature,
    features.jSymbolic.DirectionOfMotionFeature,
    features.jSymbolic.DistanceBetweenMostCommonMelodicIntervalsFeature,
    features.jSymbolic.DurationFeature,
    features.jSymbolic.DurationOfMelodicArcsFeature,
    features.jSymbolic.ImportanceOfBassRegisterFeature,
    features.jSymbolic.ImportanceOfHighRegisterFeature,
    features.jSymbolic.ImportanceOfMiddleRegisterFeature,
    features.jSymbolic.InitialTimeSignatureFeature,
    features.jSymbolic.IntervalBetweenStrongestPitchClassesFeature,
    features.jSymbolic.VariabilityOfNumberOfIndependentVoicesFeature,
    features.jSymbolic.IntervalBetweenStrongestPitchesFeature,
    features.jSymbolic.MaximumNoteDurationFeature,
    features.jSymbolic.VariabilityOfTimeBetweenAttacksFeature,
    features.jSymbolic.MelodicFifthsFeature,
    features.jSymbolic.MelodicOctavesFeature,
    features.jSymbolic.MelodicThirdsFeature,
    features.jSymbolic.MelodicTritonesFeature,
    features.jSymbolic.MinimumNoteDurationFeature,
    features.jSymbolic.MostCommonMelodicIntervalFeature,
    features.jSymbolic.MostCommonMelodicIntervalPrevalenceFeature,
    features.jSymbolic.MostCommonPitchClassFeature,
    features.jSymbolic.MostCommonPitchClassPrevalenceFeature,
    features.jSymbolic.MostCommonPitchFeature,
    features.jSymbolic.MostCommonPitchPrevalenceFeature,
    features.jSymbolic.NoteDensityFeature,
    features.jSymbolic.NumberOfCommonMelodicIntervalsFeature,
    features.jSymbolic.NumberOfCommonPitchesFeature,
    features.jSymbolic.PitchClassVarietyFeature,
    features.jSymbolic.PitchVarietyFeature,
    features.jSymbolic.PrimaryRegisterFeature,
    features.jSymbolic.QualityFeature,
    features.jSymbolic.QuintupleMeterFeature,
    features.jSymbolic.RangeFeature,
    features.jSymbolic.RelativeStrengthOfMostCommonIntervalsFeature,
    features.jSymbolic.RelativeStrengthOfTopPitchClassesFeature,
    features.jSymbolic.RelativeStrengthOfTopPitchesFeature,
    features.jSymbolic.RepeatedNotesFeature,
    features.jSymbolic.SizeOfMelodicArcsFeature,
    features.jSymbolic.StaccatoIncidenceFeature,
    features.jSymbolic.StepwiseMotionFeature,
    features.jSymbolic.TripleMeterFeature,
    features.jSymbolic.VariabilityOfNoteDurationFeature]

    print("file: ",file)

    curr_stream = converter.parse(str(file))
    print("curr_stream: ",curr_stream)
    #curr_stream.show('text')
    #print(len(curr_stream[0].getElementsByClass("Note")))
    #curr_stream[0][4].plot()
    #curr_stream.implode()
    # print(len(curr_stream.parts))
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
    #notes = curr_stream.flat.getElementsByClass("Note")
    #total16thNotes(notes)

    # score = stream.Score()
    # score.insert(0,parts[0])
    # score.insert(0,parts[1])
    # parts = score.getElementsByClass(stream.Part)

    #parts.show()
    #print("total notes: ",len(both_hands_stream.flat.getElementsByClass("Note")))

    #print(totalSharpNotes(both_hands_stream))
    print(curr_stream.recurse().getElementsByClass(meter.TimeSignature)[0].numerator)

    # print("both hands stream: ",score)
    # print(features.jSymbolic.RangeFeature(score).extract().vector)
    #print(features.jSymbolic.RangeFeature(both_hands_stream).extract())
    #averageLargeJumps(sOnlyChords,8)
    #averageRange2OfTopXPercent(curr_stream,.15)
    # parts[0].show()
    #print("key signature changes: ",curr_stream.analyze('key'))

##average range of top x percent of notes
#tested
def averageRange2OfTopXPercent(stream,percent):
    average_range = 0
    if stream is not None:
        notes_count = dict()
        notes = stream.flat.getElementsByClass("Note")
        topX = []
        totalSharpNotes = 0
        total_notes = len(notes)
        #print("total notes during call: ",total_notes)
        number_of_notes_to_get = int(total_notes*percent)
        #print("total notes to get during call: ",number_of_notes_to_get)
        notes_array = []


        #store count of notes in dictionary
        for note in notes:
            #print(note)
            if note.nameWithOctave not in notes_count:
                notes_count[note.nameWithOctave] = 1
                notes_array.append(note)
            else:
                notes_count[note.nameWithOctave] += 1
        #sort notes by count
        c = Counter(notes_count)
        #print(c)
        #x = percent*len(notes_count)
        #get the top x notes
        numberOfNotes = int(percent*len(notes_count))
        top_x_tuple = c.most_common(len(c))
        #print(top_x_tuple)
        #print("number of notes: ",numberOfNotes)
        index = 0
        top_x_note_objects = []
        #iterate through note_array and get top x note objects
        top_x_note_objects = return_x_top_notes(top_x_tuple,notes_array,number_of_notes_to_get)
        #print("top x notes: ",top_x_note_objects)
        #get lowest and highest notes
        # lowest_note = getLowestNote(top_x_note_objects)
        # highest_note = getHighestNote(top_x_note_objects)
        notes_total_average = 0
        if len(top_x_note_objects)>1:
            #get total range
            index1 = 0
            #get interval of every note of every note
            while index1<len(top_x_note_objects):
                note1 = top_x_note_objects[index1]
                index2 = 0
                total_interval_for_note = 0
                average_for_note = 0
                #print("length of top x notes objects: ",len(top_x_note_objects))
                while index2<len(top_x_note_objects):
                    if(index1!=index2):
                        note2 = top_x_note_objects[index2]
                        #interval between both notes
                        aInterval = interval.Interval(noteStart=note1,noteEnd=note2)
                        range = int(aInterval.name[1:])
                        total_interval_for_note+=range
                    index2+=1
                #average interval for note
                average_for_note = total_interval_for_note/(len(top_x_note_objects)-1)
                notes_total_average+=average_for_note
                index1+=1
            #calculate average range of every note's average range to other notes
            average_range = notes_total_average/len(top_x_note_objects)

    print('averageRange2OfTopXPercent: ',average_range)

    return average_range

#range of top x percent of notes,
def rangeOfTopXPercent(stream,percent):
    range = 0
    if stream is not None:
        notes_count = dict()
        notes = stream.flat.getElementsByClass("Note")
        total_notes = len(notes)
        number_of_notes_to_get = int(total_notes*percent)
        #print("number of notes to get", number_of_notes_to_get)
        topX = []
        totalSharpNotes = 0
        notes_array = []

        #store count of notes in dictionary
        for note in notes:
            #print(note)
            if note.nameWithOctave not in notes_count:
                notes_count[note.nameWithOctave] = 1
                notes_array.append(note)
            else:
                notes_count[note.nameWithOctave] += 1
        #sort notes by count
        c = Counter(notes_count)
        #print("c: ",c)
        #x = percent*len(notes_count)

        top_x_tuple = c.most_common(len(c))
        index = 0
        top_x_note_objects = []
        #iterate through note_array and get top x note objects
        top_x_note_objects = return_x_top_notes(top_x_tuple,notes_array,number_of_notes_to_get)
        if len(top_x_note_objects)>1:
            #print("top x notes: ",top_x_note_objects)
            # for note in top_x_note_objects:
            #     print(note.fullName,end=" ")
            #get lowest and highest notes
            lowest_note = getLowestNote(top_x_note_objects)
            highest_note = getHighestNote(top_x_note_objects)
            #interval between both notes
            aInterval = interval.Interval(noteStart=lowest_note,noteEnd=highest_note)
            range = int(aInterval.name[1:])
            #print("range: ",range)
        else:
            range = 0
    print('rangeOfTopXPercent: ',range)
    return range


#takes in a tuple with names of top notes and returns the top notes as objects
def return_x_top_notes(top_x_tuple,notes_array,numberOfNotes):
    top_x_note_objects = []
    index = 0
    current_total_notes = 0
    #iterate through note_array and get top x note objects
    while current_total_notes<numberOfNotes:
        current_note_name = top_x_tuple[index][0]
        current_total_notes+=top_x_tuple[index][1]
        note_found = False
        arr_index = 0
        while not note_found:
            if(notes_array[arr_index].nameWithOctave==current_note_name):
                note_found = True
                top_x_note_objects.append(notes_array[arr_index])
            arr_index += 1

        index+=1
    return top_x_note_objects

#gets lowest note
#takes in array with note objects
def getLowestNote(notes):
    i = 0
    lowest_note = notes[0]
    while i<len(notes):
        curr = notes[i]
        #print("compare: ",lowest_note.pitch,"  ",curr.pitch)
        if lowest_note>=curr:
            lowest_note = curr
        i+=1
    return lowest_note

#gets highest note
#takes in array with note objects
def getHighestNote(notes):
    i = 0
    highest_note = notes[0]
    while i<len(notes):
        curr = notes[i]
        #print("compare: ",highest_note.pitch,"  ",curr.pitch)
        if highest_note<=curr:
            highest_note = curr
        i+=1
    return highest_note

#average interval value of large jumps
def averageLargeJumps(chords,largeJump):
    totalLargeJumps = 0
    total = 0
    average = 0
    i = 0
    if chords is not None:
        while i<len(chords)-1:
            #get first note of first chord
            note1_chord_1 = chords[i][0]
            #get first note of second chord
            note1_chord2 = chords[i+1][0]
            notelast_chord2 = chords[i+1][len(chords[i+1])-1]

            #figure out which note to get by comparing first notes of both chords
            #only need to compare first and last note of chords
            lower_note = chords[i][len(chords[i])-1]
            higher_note = chords[i+1][0]
            #first chord lower than second
            if note1_chord_1<=notelast_chord2:
                lower_note = chords[i][0]
                higher_note = chords[i+1][len(chords[i+1])-1]
            #print(chords[i],"   ",chords[i+1])
            #print(chords[i],"  ",chords[i+1],"  ",note1,">",note2,"    ",note1<note2)
            #interval between both notes
            aInterval = interval.Interval(noteStart=lower_note,noteEnd=higher_note)
            if(int(aInterval.name[1:])>=largeJump):
                totalLargeJumps+=1
                total += int(aInterval.name[1:])
                #print(aInterval.name)
            i+=1
        #print ("total large jumps: ",totalLargeJumps)
        if totalLargeJumps>0:
            average = total/totalLargeJumps
    print("averageLargeJumps: ",average)
    return average


#average largeJumps
#return the number of large jumps>=largeJump
def largeJumps(chords,largeJump):
    totalLargeJumps = 0
    i = 0
    if chords is not None:
        while i<len(chords)-1:
            #get first note of first chord
            note1_chord_1 = chords[i][0]
            #get first note of second chord
            note1_chord2 = chords[i+1][0]
            notelast_chord2 = chords[i+1][len(chords[i+1])-1]

            #figure out which note to get by comparing first notes of both chords
            #only need to compare first and last note of chords
            lower_note = chords[i][len(chords[i])-1]
            higher_note = chords[i+1][0]
            #first chord lower than second
            if note1_chord_1<=notelast_chord2:
                lower_note = chords[i][0]
                higher_note = chords[i+1][len(chords[i+1])-1]

            #print(chords[i],"  ",chords[i+1],"  ",note1,">",note2,"    ",note1<note2)
            #interval between both notes
            aInterval = interval.Interval(noteStart=lower_note,noteEnd=higher_note)
            if(int(aInterval.name[1:])>=largeJump):
                #print(chords[i],"   ",chords[i+1])
                totalLargeJumps+=1
                #print(aInterval.name)
            i+=1
    print ('largeJumps: ',totalLargeJumps)
    return totalLargeJumps

#average range of played ntoes
#range from A3 to B3C4 is the interval from A3 to C4
#new
def averageRangeForNextNotes(chords):
    i = 0
    total = 0
    average = 0
    if chords is not None:
        while i<len(chords)-1:
            #get first note of first chord
            note1_chord_1 = chords[i][0]
            #get first note of second chord
            note1_chord2 = chords[i+1][0]
            notelast_chord2 = chords[i+1][len(chords[i+1])-1]

            #figure out which note to get by comparing first notes of both chords
            #only need to compare first and last note of chords
            lower_note = chords[i][len(chords[i])-1]
            higher_note = chords[i+1][0]
            #first chord lower than second
            if note1_chord_1<=notelast_chord2:
                lower_note = chords[i][0]
                higher_note = chords[i+1][len(chords[i+1])-1]
            #print(chords[i],"   ",chords[i+1])
            #print(chords[i],"  ",chords[i+1],"  ",note1,">",note2,"    ",note1<note2)
            #interval between both notes
            aInterval = interval.Interval(noteStart=lower_note,noteEnd=higher_note)
            total+=int(aInterval.name[1:])
            #print(aInterval.name)
            i+=1
        if(len(chords)>0):
            average = total/len(chords)
    print('averageRangeForNextNotes: ',average)
    return average


#assume you have the correct stream##############################################
#for every chord, what is the range from one note to the next
#basically this tells you how far you have to spread each finger on average
#3 note chord,distance from 1-2+distance from 2-3 /2
#average this out
def averageChordRangeForHand(chords,chord_length):
    average = 0
    chord_average_total = 0
    total_chords = 0
    if chords is not None:
        for chord in chords:
            #calculate range in chord
            if(len(chord)==chord_length):
                total_chords+=1
                total = 0
                average = 0
                index = 0
                #print(chord)
                #interval between notes in chord
                while index!=len(chord)-1:
                    aInterval = interval.Interval(noteStart=chord[index],noteEnd=chord[index+1])
                    total+=int(aInterval.name[1])
                    index+=1
                #average of chord
                average = total/(len(chord)-1)
                chord_average_total+=average
                #print(average)
        if(total_chords>0):

            average = chord_average_total/total_chords
        else:
            average = 0
    print('averageChordRangeForHand: ',average)
    return average

#for every chord, what is the range from the left most note to the right most note
#basically how far is your hand spread out for each chord
#average this out
def average2ChordRangeForHand(chords,chord_length):
    total_chords = 0
    total = 0
    average = 0
    #distance between first and last note of each chord
    if chords is not None:
        for chord in chords:
            if(len(chord)==chord_length):
                aInterval = interval.Interval(noteStart=chord[0],noteEnd=chord[len(chord)-1])
                total+=int(aInterval.name[1:])
                total_chords+=1
                #print(chord ," ",aInterval)
        if(total_chords>0):
            average = total/total_chords
    print('average2ChordRangeForHand: ',average)
    return average

#average

def averageWholeNotes(given_stream):
    average = 0
    if given_stream is not None:
        notes = given_stream.flat.getElementsByClass("Note")
        totalNotes = len(notes)
        if totalNotes>0:
            average = totalWholeNotes(given_stream)/totalNotes
    return average

def averageHalfNotes(given_stream):
    average = 0
    if given_stream is not None:
        notes = given_stream.flat.getElementsByClass("Note")
        totalNotes = len(notes)
        if totalNotes>0:
            average = totalHalfNotes(given_stream)/totalNotes
    return average

def averageQuarterNotes(given_stream):
    average = 0
    if given_stream is not None:
        notes = given_stream.flat.getElementsByClass("Note")
        totalNotes = len(notes)
        if totalNotes>0:
            average = totalQuarterNotes(given_stream)/totalNotes
    return average

def averageEighthNotes(given_stream):
    average = 0
    if given_stream is not None:
        notes = given_stream.flat.getElementsByClass("Note")
        totalNotes = len(notes)
        if totalNotes>0:
            average = totalEighthNotes(given_stream)/totalNotes
    return average

def average16thNotes(given_stream):
    average = 0
    if given_stream is not None:
        notes = given_stream.flat.getElementsByClass("Note")
        totalNotes = len(notes)
        if totalNotes>0:
            average = total16thNotes(given_stream)/totalNotes
    return average

def average32ndNotes(given_stream):
    average = 0
    if given_stream is not None:
        notes = given_stream.flat.getElementsByClass("Note")
        totalNotes = len(notes)
        if totalNotes>0:
            average = total32ndNotes(given_stream)/totalNotes
    return average

def average64thNotes(given_stream):
    average = 0
    if given_stream is not None:
        notes = given_stream.flat.getElementsByClass("Note")
        totalNotes = len(notes)
        if totalNotes>0:
            average = total64thNotes(given_stream)/totalNotes
    return average

def totalWholeNotes(given_stream):
    total = 0
    if given_stream is not None:
        notes = given_stream.flat.getElementsByClass("Note")
        for note in notes:
            if note.quarterLength==4:
                total+=1
    #print(total)
    return total

def totalHalfNotes(given_stream):
    total = 0
    if given_stream is not None:
        notes = given_stream.flat.getElementsByClass("Note")
        for note in notes:
            if note.quarterLength==2:
                total+=1
    #print(total)
    return total

def totalQuarterNotes(given_stream):
    total = 0
    if given_stream is not None:
        notes = given_stream.flat.getElementsByClass("Note")
        for note in notes:
            if note.quarterLength==1:
                total+=1
    #print(total)
    return total

def totalEighthNotes(given_stream):
    total = 0
    if given_stream is not None:
        notes = given_stream.flat.getElementsByClass("Note")
        for note in notes:
            if note.quarterLength==.5:
                total+=1
    #print(total)
    return total

def total16thNotes(given_stream):
    total = 0
    if given_stream is not None:
        notes = given_stream.flat.getElementsByClass("Note")
        for note in notes:
            if note.quarterLength==.25:
                total+=1
    #print(total)
    return total

def total32ndNotes(given_stream):
    total = 0
    if given_stream is not None:
        notes = given_stream.flat.getElementsByClass("Note")
        for note in notes:
            if note.quarterLength==.125:
                total+=1
    #print(total)
    return total

def total64thNotes(given_stream):
    total = 0
    if given_stream is not None:
        notes = given_stream.flat.getElementsByClass("Note")
        for note in notes:
            if note.quarterLength==.0625:
                total+=1
    #print(total)
    return total

#total notes
#total notes right hand
#total notes left hand
def totalNotes(given_stream):
    if(given_stream.getElementsByClass("Note") is not None):
        return len(given_stream.getElementsByClass("Note"))
    else:
        return 0
#total sharp notes in the entire piece
#total sharp notes in right hand
#total sharp notes in left hand
def totalSharpNotes(given_stream):
    totalSharpNotes = 0
    if given_stream is not None:
        notes = given_stream.flat.getElementsByClass("Note")
        for note in notes:
            if '#' in note.name:
                totalSharpNotes+=1
                #print(note.name)
    return totalSharpNotes


#total flat notes in the entrire piece
#total flat notes in right hand
#total flat notes in left hand
def totalFlatNotes(given_stream):
    totalFlatNotes = 0
    if given_stream is not None:
        notes = given_stream.flat.getElementsByClass("Note")
        for note in notes:
            if '-' in note.name:
                totalFlatNotes+=1
                #print(note.name)
    return totalFlatNotes

def totalNaturalNotes(given_stream):
    totalNaturalNotes = 0
    if given_stream is not None:
        notes = given_stream.flat.getElementsByClass("Note")
        for note in notes:
            if '-' not in note.name and '#' not in note.name:
                totalNaturalNotes+=1

    return totalNaturalNotes






#flat and chordity(doesn't lose details)


if __name__ == '__main__':
    main()
