from music21 import *
import re
import os
from collections import Counter


#average range of top x percent of notes
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


#files = {"./Midi_Files/Fur_Elise(7).mid":7}
files = {}
f = None
labels_file = None
'''go through Midi_Files directory and get
file names and levels and store them in
dictioanry
'''
#./Midi_Files/AmbroseTabsDatabase/AmbrosePianoTabsNoFilter/
for root, dirs, song_files in os.walk("./MusicXML_Files/AmbroseTabsDatabase/ClassicalMusic2/"):
    for filename in song_files:
        print("filename: ",filename)
        num = ""
        #offset to get the first digit of grade level
        offset = 11
        #get level of song
        while(filename[len(filename)-offset]!='('):
            char =  filename[len(filename)-offset]
            char+=num
            num = char
            offset+=1
        num = int(num)
        #./MusicXML_Files/AmbroseTabsDatabase/AmbroseTabsNoFilter/
        filename = "./MusicXML_Files/AmbroseTabsDatabase/ClassicalMusic2/"+str(filename)
        files[filename] = num

#index used in iris file
index = 1
key_signatures = {"C major": 1,"G major" : 2, "e minor":3,"D major":4,
"b minor":5,"A major":6,"f# minor":7,"E major":8,"c# minor":9,
"B major":10,"g# minor":11,"F# major":12,"d# minor":13,"C# major":14,
"a# minor":15,
"F major":16,"d minor":17,"B- major":18,"g minor":19,"E- major":20,
"c minor":21,"A- major":22,"f minor":23,"D- major":24,
"b- minor":25,"G- major":26,"e- minor":27,"C- major":28,
"a- minor":29, "a minor":30}


#ds.addFeatureExtractors(fes)
songs_features = dict()
feature_index = 0
for file in files:
    feature_values = dict()
    print(file)

    #parse file
    curr_stream = converter.parse(str(file))
    #add parsed file, grade, and id
    #ds.addData(curr_stream, classValue=files[str(file)], id=str(file))

    ##########################################get streams for each hand and both hands together
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
    feature_values['total_LRH_sharp_keys_pressed'] = totalSharpNotes(both_hands_stream)
    feature_values['total_LH_sharp_keys_pressed'] = totalSharpNotes(left_hand_stream)
    feature_values['total_RH_sharp_keys_pressed'] = totalSharpNotes(right_hand_stream)
    #number of flat keys pressed
    feature_values['total_LRH_flat_keys_pressed'] = totalFlatNotes(both_hands_stream)
    feature_values['total_LH_flat_keys_pressed'] = totalFlatNotes(left_hand_stream)
    feature_values['total_RH_flat_keys_pressed'] = totalFlatNotes(right_hand_stream)
    #average range in hand
    feature_values['average_RLH_range'] = averageRangeForNextNotes(both_hands_chords)
    feature_values['average_LH_range'] = averageRangeForNextNotes(left_hand_chords)
    feature_values['average_RH_range'] = averageRangeForNextNotes(right_hand_chords)
    #average range for top 10% percent of notes
    feature_values['average_RLH_note_10_range'] = averageRange2OfTopXPercent(both_hands_stream,.1)
    feature_values['average_LH_note_10_range'] = averageRange2OfTopXPercent(left_hand_stream,.1)
    feature_values['average_RH_note_10_range'] = averageRange2OfTopXPercent(right_hand_stream,.1)
    #average range for top 20% percent of notes
    feature_values['average_RLH_note_20_range'] = averageRange2OfTopXPercent(both_hands_stream,.2)
    feature_values['average_LH_note_20_range'] = averageRange2OfTopXPercent(left_hand_stream,.2)
    feature_values['average_RH_note_20_range'] = averageRange2OfTopXPercent(right_hand_stream,.2)
    #average range for top 35% percent of notes
    feature_values['average_RLH_note_35_range'] = averageRange2OfTopXPercent(both_hands_stream,.35)
    feature_values['average_LH_note_35_range'] = averageRange2OfTopXPercent(left_hand_stream,.35)
    feature_values['average_RH_note_35_range'] = averageRange2OfTopXPercent(right_hand_stream,.35)
    #average range for top 50% percent of notes
    feature_values['average_RLH_note_50_range'] = averageRange2OfTopXPercent(both_hands_stream,.5)
    feature_values['average_LH_note_50_range'] = averageRange2OfTopXPercent(left_hand_stream,.5)
    feature_values['average_RH_note_50_range'] = averageRange2OfTopXPercent(right_hand_stream,.5)
    #average range for top 100% percent of notes
    feature_values['average_RLH_note_100_range'] = averageRange2OfTopXPercent(both_hands_stream,1)
    feature_values['average_LH_note_100_range'] = averageRange2OfTopXPercent(left_hand_stream,1)
    feature_values['average_RH_note_100_range'] = averageRange2OfTopXPercent(right_hand_stream,1)

    #range for top 10% percent of notes
    feature_values['RLH_note_10_range'] = rangeOfTopXPercent(both_hands_stream,.1)
    feature_values['LH_note_10_range'] = rangeOfTopXPercent(left_hand_stream,.1)
    feature_values['RH_note_10_range'] = rangeOfTopXPercent(right_hand_stream,.1)
    # range for top 20% percent of notes
    feature_values['RLH_note_20_range'] = rangeOfTopXPercent(both_hands_stream,.2)
    feature_values['LH_note_20_range'] = rangeOfTopXPercent(left_hand_stream,.2)
    feature_values['RH_note_20_range'] = rangeOfTopXPercent(right_hand_stream,.2)
    # range for top 35% percent of notes
    feature_values['RLH_note_35_range'] = rangeOfTopXPercent(both_hands_stream,.35)
    feature_values['LH_note_35_range'] = rangeOfTopXPercent(left_hand_stream,.35)
    feature_values['RH_note_35_range'] = rangeOfTopXPercent(right_hand_stream,.35)
    # range for top 50% percent of notes
    feature_values['RLH_note_50_range'] = rangeOfTopXPercent(both_hands_stream,.5)
    feature_values['LH_note_50_range'] = rangeOfTopXPercent(left_hand_stream,.5)
    feature_values['RH_note_50_range'] = rangeOfTopXPercent(right_hand_stream,.5)
    # range for top 100% percent of notes
    feature_values['RLH_note_100_range'] = rangeOfTopXPercent(both_hands_stream,1)
    feature_values['LH_note_100_range'] = rangeOfTopXPercent(left_hand_stream,1)
    feature_values['RH_note_100_range'] = rangeOfTopXPercent(right_hand_stream,1)

    #average range for each finger in chord
    feature_values['average_LRH_2chord_range'] = averageChordRangeForHand(both_hands_chords,2)
    feature_values['average_LH_2chord_range'] = averageChordRangeForHand(left_hand_chords,2)
    feature_values['average_RH_2chord_range'] = averageChordRangeForHand(right_hand_chords,2)

    feature_values['average_LRH_3chord_range'] = averageChordRangeForHand(both_hands_chords,3)
    feature_values['average_LH_3chord_range'] = averageChordRangeForHand(left_hand_chords,3)
    feature_values['average_RH_3chord_range'] = averageChordRangeForHand(right_hand_chords,3)

    feature_values['average_LRH_4chord_range'] = averageChordRangeForHand(both_hands_chords,4)
    feature_values['average_LH_4chord_range'] = averageChordRangeForHand(left_hand_chords,4)
    feature_values['average_RH_4chord_range'] = averageChordRangeForHand(right_hand_chords,4)

    feature_values['average_LRH_5chord_range'] = averageChordRangeForHand(both_hands_chords,5)
    feature_values['average_LH_5chord_range'] = averageChordRangeForHand(left_hand_chords,5)
    feature_values['average_RH_5chord_range'] = averageChordRangeForHand(right_hand_chords,5)

    #average range for each hand
    feature_values['average_LRH_2chord_hand_range'] = average2ChordRangeForHand(both_hands_chords,2)
    feature_values['average_LH_2chord_hand_range'] = average2ChordRangeForHand(left_hand_chords,2)
    feature_values['average_RH_2chord_hand_range'] = average2ChordRangeForHand(right_hand_chords,2)

    feature_values['average_LRH_3chord_hand_range'] = average2ChordRangeForHand(both_hands_chords,3)
    feature_values['average_LH_3chord_hand_range'] = average2ChordRangeForHand(left_hand_chords,3)
    feature_values['average_RH_3chord_hand_range'] = average2ChordRangeForHand(right_hand_chords,3)

    feature_values['average_LRH_4chord_hand_range'] = average2ChordRangeForHand(both_hands_chords,4)
    feature_values['average_LH_4chord_hand_range'] = average2ChordRangeForHand(left_hand_chords,4)
    feature_values['average_RH_4chord_hand_range'] = average2ChordRangeForHand(right_hand_chords,4)

    feature_values['average_LRH_5chord_hand_range'] = average2ChordRangeForHand(both_hands_chords,5)
    feature_values['average_LH_5chord_hand_range'] = average2ChordRangeForHand(left_hand_chords,5)
    feature_values['average_RH_5chord_hand_range'] = average2ChordRangeForHand(right_hand_chords,5)

    #large jumps
    feature_values['large_5jumps_LRH'] = largeJumps(both_hands_chords,5)
    feature_values['large_5jumps_LH'] = largeJumps(left_hand_chords,5)
    feature_values['large_5jumps_RH'] = largeJumps(right_hand_chords,5)

    feature_values['large_8jumps_LRH'] = largeJumps(both_hands_chords,8)
    feature_values['large_8jumps_LH'] = largeJumps(left_hand_chords,8)
    feature_values['large_8jumps_RH'] = largeJumps(right_hand_chords,8)

    feature_values['large_9jumps_LRH'] = largeJumps(both_hands_chords,9)
    feature_values['large_9jumps_LH'] = largeJumps(left_hand_chords,9)
    feature_values['large_9jumps_RH'] = largeJumps(right_hand_chords,9)

    feature_values['large_10jumps_LRH'] = largeJumps(both_hands_chords,10)
    feature_values['large_10jumps_LH'] = largeJumps(left_hand_chords,10)
    feature_values['large_10jumps_RH'] = largeJumps(right_hand_chords,10)

    #average large jumps
    feature_values['average_large_5jumps_LRH'] = averageLargeJumps(both_hands_chords,5)
    feature_values['average_large_5jumps_LH'] = averageLargeJumps(left_hand_chords,5)
    feature_values['average_large_5jumps_RH'] = averageLargeJumps(right_hand_chords,5)

    feature_values['average_large_8jumps_LRH'] = averageLargeJumps(both_hands_chords,8)
    feature_values['average_large_8jumps_LH'] = averageLargeJumps(left_hand_chords,8)
    feature_values['average_large_8jumps_RH'] = averageLargeJumps(right_hand_chords,8)

    feature_values['average_large_9jumps_LRH'] = averageLargeJumps(both_hands_chords,9)
    feature_values['average_large_9jumps_LH'] = averageLargeJumps(left_hand_chords,9)
    feature_values['average_large_9jumps_RH'] = averageLargeJumps(right_hand_chords,9)

    feature_values['average_large_10jumps_LRH'] = averageLargeJumps(both_hands_chords,10)
    feature_values['average_large_10jumps_LH'] = averageLargeJumps(left_hand_chords,10)
    feature_values['average_large_10jumps_RH'] = averageLargeJumps(right_hand_chords,10)

    #note type total count
    feature_values['total_LRHwhole_notes'] = totalWholeNotes(both_hands_chords)
    feature_values['total_LRHhalf_notes'] = totalHalfNotes(both_hands_chords)
    feature_values['total_LRHquarter_notes'] = totalQuarterNotes(both_hands_chords)
    feature_values['total_LRHeighth_notes'] = totalEighthNotes(both_hands_chords)
    feature_values['total_LRH16th_notes'] = total16thNotes(both_hands_chords)
    feature_values['total_LRH32nd_notes'] = total32ndNotes(both_hands_chords)
    feature_values['total_LRH64th_notes'] = total64thNotes(both_hands_chords)
    feature_values['total_LHwhole_notes'] = totalWholeNotes(left_hand_stream)
    feature_values['total_LHhalf_notes'] = totalHalfNotes(left_hand_stream)
    feature_values['total_LHquarter_notes'] = totalQuarterNotes(left_hand_stream)
    feature_values['total_LHeighth_notes'] = totalEighthNotes(left_hand_stream)
    feature_values['total_LH16th_notes'] = total16thNotes(left_hand_stream)
    feature_values['total_LH32nd_notes'] = total32ndNotes(left_hand_stream)
    feature_values['total_LH64th_notes'] = total64thNotes(left_hand_stream)
    feature_values['total_RHwhole_notes'] = totalWholeNotes(right_hand_stream)
    feature_values['total_RHhalf_notes'] = totalHalfNotes(right_hand_stream)
    feature_values['total_RHquarter_notes'] = totalQuarterNotes(right_hand_stream)
    feature_values['total_RHeighth_notes'] = totalEighthNotes(right_hand_stream)
    feature_values['total_RH16th_notes'] = total16thNotes(right_hand_stream)
    feature_values['total_RH32nd_notes'] = total32ndNotes(right_hand_stream)
    feature_values['total_RH64th_notes'] = total64thNotes(right_hand_stream)

    #note type average
    feature_values['average_LRHwhole_notes'] = averageWholeNotes(both_hands_stream)
    feature_values['average_LRHhalf_ntoes'] = averageHalfNotes(both_hands_stream)
    feature_values['average_LRHquarter_notes'] = averageQuarterNotes(both_hands_stream)
    feature_values['average_LRHeighth_notes'] = averageEighthNotes(both_hands_stream)
    feature_values['average_LRH16th_notes'] = average16thNotes(both_hands_stream)
    feature_values['average_LRH32nd_notes'] = average32ndNotes(both_hands_stream)
    feature_values['average_LRH64th_notes'] = average64thNotes(both_hands_stream)
    feature_values['average_LHwhole_notes'] = averageWholeNotes(left_hand_stream)
    feature_values['average_LHhalf_ntoes'] = averageHalfNotes(left_hand_stream)
    feature_values['average_LHquarter_notes'] = averageQuarterNotes(left_hand_stream)
    feature_values['average_LHeighth_notes'] = averageEighthNotes(left_hand_stream)
    feature_values['average_LH16th_notes'] = average16thNotes(left_hand_stream)
    feature_values['average_LH32nd_notes'] = average32ndNotes(left_hand_stream)
    feature_values['average_LH64th_notes'] = average64thNotes(left_hand_stream)
    feature_values['average_RHwhole_notes'] = averageWholeNotes(right_hand_stream)
    feature_values['average_RHhalf_ntoes'] = averageHalfNotes(right_hand_stream)
    feature_values['average_RHquarter_notes'] = averageQuarterNotes(right_hand_stream)
    feature_values['average_RHeighth_notes'] = averageEighthNotes(right_hand_stream)
    feature_values['average_RH16th_notes'] = average16thNotes(right_hand_stream)
    feature_values['average_RH32nd_notes'] = average32ndNotes(right_hand_stream)
    feature_values['average_RH64th_notes'] = average64thNotes(right_hand_stream)
    feature_values['time_signature_num'] = curr_stream.recurse().getElementsByClass(meter.TimeSignature)[0].numerator
    feature_values['time_signature_den'] = curr_stream.recurse().getElementsByClass(meter.TimeSignature)[0].denominator

    feature_values['Grade'] = files[file]
    ##################################################################insert feature values into song_features dictionary
    if(feature_index==0):
        labels_file = open("music_IrisCustomClassical.txt","w")
        f = open("music_IrisCustomClassical.csv","w")
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
##############################################################################write custom features
print("feature extractor added")
#ds.process()
print("music processed...Now adding features")


i = 0
#write attribute labels in .txt and .csv files
# features = ds.getAttributeLabels()[1:]
# #print("features: ",features)
# for feature in features:
#     if(i<(len(features)-1)):
#         labels_file.write(feature+",")
#         f.write(feature+",")
#     else:
#         f.write(feature+"\n")
#     i+=1
#write id,features,grade in first line of iris files
#f = open("music_IrisWCG3.csv","w")
#labels_file = open("music_featuresWCG3.txt","w")




features_index = 0
#write feature strings
#print("song features: ",songs_features)
#songs_values = ds.getFeaturesAsList()
#print("song_values: ",songs_values)
#write songs feature values
#print("songs features: ",songs_features)
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
    #iterate through every song and write its feature values
    # song_values = songs_values[features_index]
    # i = 0
    # for value in song_values[1:]:
    #     if i<(len(song_values[1:])-1):
    #         f.write(str(value)+",")
    #     else:
    #         f.write(str(value))
    #     i+=1
    print("feature values added")
    f.write("\n")
    # f.write("\n")
    features_index+=1


##############################################################################write low level features
