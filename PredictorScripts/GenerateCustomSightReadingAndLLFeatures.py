from music21 import *
import re
import os
from collections import Counter

from collections import OrderedDict
from CustomFeatureSet import CustomFeatures




class ChordObject:
    def __init__(self, chord):
        self.count = 1
        self.chord = chord
    def __eq__(self,other):
        if(self.chord==other.chord):
            return True
        else:
            return False
    def IncrementCount(self):
        self.count+=1






#gets the average density of chords played at the same time
def averageDensity(chords):
    average = 0
    total = 0
    count = 0
    if chords is not None:
        for chord in chords:
            total+=len(chord)
            count+=1
        average = total/count
    print("Average Density: ", average)

    return average

#range between most common notes of both hands
def RLHandCommonNoteRange(r_chords,l_chords):
    aInterval = 0
    if(r_chords is not None and l_chords is not None):
        chord_objects = []
        chords_count = dict()
        most_common_rh_chord = ReturnMostCommonChordsInOrder(r_chords,-1)
        most_common_lh_chord = ReturnMostCommonChordsInOrder(l_chords,-1)

        lowest_note = most_common_rh_chord[0][0]
        highest_note = most_common_lh_chord[0][0]

        aInterval = interval.Interval(noteStart=lowest_note,noteEnd=highest_note)
        aInterval = abs(int(re.search(r'\d+', str(aInterval.name)).group()))

    print("RLHandCommonNoterange: ",aInterval)

    return aInterval


def ReturnMostCommonChordsInOrder(chords,chord_count):

    if(chords is not None):
        chords_count = dict()
        chords_object_array = []
        chord_array = []
        for chord in chords:
            if(str(chord.pitchNames) not in chords_count):
                chord_object = ChordObject(chord)
                chords_count[str(chord.pitchNames)] = chord_object
                chords_object_array.append(chord_object)
                #chords_array.append(chordObject)
            else:
                chords_count[str(chord.pitchNames)].IncrementCount()
                #print(chords_array[chordObject])

        # for notes,chord in chords_count.items():
        #     p


        #sort list of common chords
        chords_object_array.sort(key=lambda x: x.count, reverse = True)
        previous_current_count = -1
        #put chords into chord array
        for chord_object in chords_object_array:
            #print("chord object: ",chord_object.count)
            if chord_count==-1 or previous_current_count==chord_object.count or chord_count>0:
                chord_array.append(chord_object.chord)
                chord_count-=chord_object.count
                previous_current_count = chord_object.count

        return chord_array




#find the highest chord from a list of chords
def find_highest_chord(chords):
    highest_chord = chords[0]
    if(len(chords)>1):
        curr = 1
        while curr<len(chords):
            current = chords[curr]
            if current[0]>highest_chord[0]:
                highest_chord = current
            curr+=1

    return highest_chord

#find the lowest chord from a list of chords
def find_lowest_chord(chords):
    lowest_chord = chords[0]
    if(len(chords)>1):
        curr = 1
        while curr<len(chords):
            current = chords[curr]
            # print("current: ",current.chord[0])
            #print("lowest: ",lowest_chord[0])
            if current[0]<lowest_chord[0]:
                lowest_chord = current
            curr+=1

    return lowest_chord

#returns the range of the top x percent of notes
def rangeOfTopXPercent(chords,percent):
    aInterval = 0
    if(chords is not None):
        number_of_chords = int(len(chords)*(percent))
        chord_objects = []
        chords_count = dict()
        most_common_chords = ReturnMostCommonChordsInOrder(chords,number_of_chords)
        if(len(most_common_chords)>1):
            #print("number of chords: ",number_of_chords)
            lowest_chord = find_lowest_chord(most_common_chords)
            highest_chord = find_highest_chord(most_common_chords)

            lowest_note = lowest_chord[0]
            second_lowest_note = highest_chord[0]


            aInterval = interval.Interval(noteStart=lowest_note,noteEnd=second_lowest_note)
            aInterval = abs(int(re.search(r'\d+', str(aInterval.name)).group()))
    print("rangeOfTopXPercent: ",aInterval)

    return aInterval

#range of most used chord and least used chord given x percent of chords,
#tested
def fakeRangeOfTopXPercent(chords,percent):
    aInterval = 0
    if(chords is not None):
        number_of_chords = int(len(chords)*(percent))
        chord_objects = []
        chords_count = dict()
        most_common_chords = ReturnMostCommonChordsInOrder(chords,number_of_chords)
        if(len(most_common_chords)>1):
            #print("number of chords: ",number_of_chords,"    ",len(most_common_chords))
            lowest_note = most_common_chords[0][0]
            second_lowest_note = most_common_chords[len(most_common_chords)-1][0]

            aInterval = interval.Interval(noteStart=lowest_note,noteEnd=second_lowest_note)
            aInterval = abs(int(re.search(r'\d+', str(aInterval.name)).group()))
    print("fakeRangeOfTopXPercent: ",aInterval)

    return aInterval

#get top x notes, place them in order from lowest to highest and find average range
#from each note to the next
#tested
def averageRangeOfTopXPercent(chords,percent):
    total_interval = 0
    average_interval = 0
    if(chords is not None):
        #get most common chords in piano order
        number_of_chords = int(len(chords)*(percent))
        if(number_of_chords>1):
            chord_objects = []
            chords_count = dict()
            #print("number of chords: ",number_of_chords)
            most_common_chords = ReturnMostCommonChordsInOrder(chords,number_of_chords)

            if(len(most_common_chords)>1):
                chords_in_order = returnChordsInPianoOrder(most_common_chords)
                if len(chords_in_order)<2:
                    print("error returning chords in piano order averageRangeOfTopXPercent")
                    return -1
                index = 0
                #print("chords in order: ",len(chords_in_order))
                #get average range
                while index<len(chords_in_order)-1:

                    chord1 = chords_in_order[index]
                    chord2 = chords_in_order[index+1]
                    aInterval = interval.Interval(noteStart=chord1[0],noteEnd=chord2[0])
                    aInterval = abs(int(re.search(r'\d+', str(aInterval.name)).group()))
                    total_interval+=aInterval
                    index+=1
                average_interval = total_interval/index
    print("averageRangeOfTopXPercent: ",average_interval)

    return average_interval


#returns chords lowest to highest on piano
def returnChordsInPianoOrder(chords):

    index = 0
    chords_in_order = []
    count = len(chords)
    while index<count:
        try:
            lowest_chord = find_lowest_chord(chords)
            chords.remove(lowest_chord)
            chords_in_order.append(lowest_chord)
            index+=1
        except:
            print("error occured in returnChordsInPianoOrder(chords)")
            return chords_in_order
    return chords_in_order


#average interval value of large jumps
def averageLargeJumps(chords,largeJump):
    totalLargeJumps = 0
    total = 0
    average = 0
    i = 0
    if chords is not None:
        while i<len(chords)-1:
            #get first note of first chord
            note1_chord1 = chords[i][0]
            #get first note of second chord
            note1_chord2 = chords[i+1][0]

            lower_note = note1_chord1
            higher_note = note1_chord2
            #first chord lower than second
            if higher_note<lower_note:
                lower_note = note1_chord2
                higher_note = note1_chord1
            #print(chords[i],"   ",chords[i+1])
            #print(chords[i],"  ",chords[i+1],"  ",note1,">",note2,"    ",note1<note2)
            #interval between both notes
            aInterval = interval.Interval(noteStart=lower_note,noteEnd=higher_note)
            if(int(aInterval.name[1:])>=largeJump):
                totalLargeJumps+=1
                total += int(re.search(r'\d+', str(aInterval.name)).group())
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
            note1_chord1 = chords[i][0]
            #get first note of second chord
            note1_chord2 = chords[i+1][0]

            lower_note = note1_chord1
            higher_note = note1_chord2
            #first chord lower than second
            if higher_note<lower_note:
                lower_note = note1_chord2
                higher_note = note1_chord1

            #print(chords[i],"  ",chords[i+1],"  ",note1,">",note2,"    ",note1<note2)
            #interval between both notes
            aInterval = interval.Interval(noteStart=lower_note,noteEnd=higher_note)
            if(int(re.search(r'\d+', str(aInterval.name)).group())>=largeJump):
                #print(chords[i],"   ",chords[i+1])
                totalLargeJumps+=1
                #print(aInterval.name)
            i+=1
    print ('largeJumps: ',totalLargeJumps)
    return totalLargeJumps

#average range of played ntoes
#range from A3 to B3C4 is the interval from A3 to B3
#You should take the left and right hand as streams*******
def averageRangeForNextNotes(chords):
    i = 0
    total = 0
    average = 0
    if chords is not None:
        while i<len(chords)-1:

            #get first note of first chord
            note1_chord1 = chords[i][0]
            #get first note of second chord
            note1_chord2 = chords[i+1][0]

            lower_note = note1_chord1
            higher_note = note1_chord2
            #first chord lower than second
            if higher_note<lower_note:
                lower_note = note1_chord2
                higher_note = note1_chord1
            #print(chords[i],"   ",chords[i+1])
            #print(chords[i],"  ",chords[i+1],"  ",note1,">",note2,"    ",note1<note2)
            #interval between both notes
            aInterval = interval.Interval(noteStart=lower_note,noteEnd=higher_note)
            total+=int(re.search(r'\d+', str(aInterval.name)).group())
            #print(aInterval.name)
            i+=1
        if(len(chords)>0):
            average = total/len(chords)
    print('averageRangeForNextNotes: ',average)
    return average


#assume you have the correct stream##############################################
#tested but is it actually useful????
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
                    total+=int(re.search(r'\d+', str(aInterval.name)).group())
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
#simple and useful tested
def average2ChordRangeForHand(chords,chord_length):
    total_chords = 0
    total = 0
    average = 0
    #distance between first and last note of each chord
    if chords is not None:
        for chord in chords:
            if(len(chord)==chord_length):
                aInterval = interval.Interval(noteStart=chord[0],noteEnd=chord[len(chord)-1])
                total+=int(re.search(r'\d+', str(aInterval.name)).group())
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
    return total*1.5

def total16thNotes(given_stream):
    total = 0
    if given_stream is not None:
        notes = given_stream.flat.getElementsByClass("Note")
        for note in notes:
            if note.quarterLength==.25:
                total+=1
    #print(total)
    return total*2

def total32ndNotes(given_stream):
    total = 0
    if given_stream is not None:
        notes = given_stream.flat.getElementsByClass("Note")
        for note in notes:
            if note.quarterLength==.125:
                total+=1
    #print(total)
    return total*3

def total64thNotes(given_stream):
    total = 0
    if given_stream is not None:
        notes = given_stream.flat.getElementsByClass("Note")
        for note in notes:
            if note.quarterLength==.0625:
                total+=1
    #print(total)
    return total*4

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
    return totalSharpNotes*2


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
    return totalFlatNotes*2

def totalNaturalNotes(given_stream):
    totalNaturalNotes = 0
    if given_stream is not None:
        notes = given_stream.flat.getElementsByClass("Note")
        for note in notes:
            if '-' not in note.name and '#' not in note.name:
                totalNaturalNotes+=1

    return totalNaturalNotes

# if you have a stream you should be able to detect any
# changes in key signature
def totalAccidentals(given_stream,altered_pitches):
    total_accidentals = 0
    if given_stream is not None:
        notes = given_stream.flat.getElementsByClass("Note")
        for note in notes:
            #loook for a note match
            for pitch in altered_pitches:
                #check for pitch class match
                if pitch[0]==note.name[0]:
                    if(pitch!=note.name):
                        total_accidentals+=1

    print("totalAccidentals: ",total_accidentals)

    return total_accidentals
def averageAccidentals(given_stream,altered_pitches):
    average_accidentals = 0
    if given_stream is not None:
        total_accidentals = totalAccidentals(given_stream,altered_pitches)
        total_notes = len(notes)
        average_accidentals/=total_notes
    print("averageAccidentals: ",average_accidentals)


    return average_accidentals




custom_feature = CustomFeatures()
#files = {"./Midi_Files/Fur_Elise(7).mid":7}
files = {}
f = None
labels_file = None
'''go through Midi_Files directory and get
file names and levels and store them in
dictioanry
'''
#./Midi_Files/AmbroseTabsDatabase/AmbrosePianoTabsNoFilter/
for root, dirs, song_files in os.walk("MusicXML_Files/AmbroseTabsDatabase/doneClassical/"):
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
        filename = "MusicXML_Files/AmbroseTabsDatabase/doneClassical/"+str(filename)
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
#assign grade and features to ds
#ds = features.DataSet(classLabel='Grade')

#Low level features


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

    feature_values['total_LRH_accidentals'] = 0
    feature_values['total_RH_accidentals'] = 0
    feature_values['total_LH_accidentals'] = 0

    feature_values['average_LRH_accidentals'] = 0
    feature_values['average_RH_accidentals'] = 0
    feature_values['average_LH_accidentals'] = 0

    feature_values['total_LRH_sharp_keys_pressed'] = 0
    feature_values['total_LH_sharp_keys_pressed'] = 0
    feature_values['total_RH_sharp_keys_pressed'] = 0

    feature_values['total_LRH_flat_keys_pressed'] = 0
    feature_values['total_LH_flat_keys_pressed'] = 0
    feature_values['total_RH_flat_keys_pressed'] = 0

    feature_values['average_next_LH_range'] = 0
    feature_values['average_next_RH_range'] = 0

    feature_values['average_density_RLH'] = 0
    feature_values['average_density_LH'] = 0
    feature_values['average_density_RH'] = 0
    #gives very interesting results for both hands
    #**feature_values['average_RLH_note_10_range'] = 0
    feature_values['average_LH_note_10_range'] = 0
    feature_values['average_RH_note_10_range'] = 0
    #**feature_values['average_RLH_note_20_range'] = 0
    feature_values['average_LH_note_20_range'] = 0
    feature_values['average_RH_note_20_range'] = 0
    #**feature_values['average_RLH_note_35_range'] = 0
    feature_values['average_LH_note_35_range'] = 0
    feature_values['average_RH_note_35_range'] = 0
    #**feature_values['average_RLH_note_50_range'] = 0
    feature_values['average_LH_note_50_range'] = 0
    feature_values['average_RH_note_50_range'] = 0

    feature_values['average_LH_note_75_range'] = 0
    feature_values['average_RH_note_75_range'] = 0
    #**feature_values['average_RLH_note_100_range'] = 0
    feature_values['average_LH_note_100_range'] = 0
    feature_values['average_RH_note_100_range'] = 0

    feature_values['fake_range_LH_10'] = 0
    feature_values['fake_range_RH_10'] = 0

    feature_values['fake_range_LH_20'] = 0
    feature_values['fake_range_RH_20'] = 0

    feature_values['fake_range_LH_35'] = 0
    feature_values['fake_range_RH_35'] = 0

    feature_values['fake_range_LH_50'] = 0
    feature_values['fake_range_RH_50'] = 0

    feature_values['fake_range_LH_75'] = 0
    feature_values['fake_range_RH_75'] = 0

    feature_values['fake_range_LH_100'] = 0
    feature_values['fake_range_RH_100'] = 0


    #feature_values['RLH_note_10_range'] = 0
    feature_values['LH_note_10_range'] = 0
    feature_values['RH_note_10_range'] = 0
    #feature_values['RLH_note_20_range'] = 0
    feature_values['LH_note_20_range'] = 0
    feature_values['RH_note_20_range'] = 0
    #feature_values['RLH_note_35_range'] = 0
    feature_values['LH_note_35_range'] = 0
    feature_values['RH_note_35_range'] = 0
    #feature_values['RLH_note_50_range'] = 0
    feature_values['LH_note_50_range'] = 0
    feature_values['RH_note_50_range'] = 0
    #feature_values['RLH_note_100_range'] = 0
    feature_values['LH_note_100_range'] = 0
    feature_values['RH_note_100_range'] = 0

    #feature_values['average_LRH_2chord_range'] = 0
    feature_values['average_LH_2chord_range'] = 0
    feature_values['average_RH_2chord_range'] = 0
    #feature_values['average_LRH_3chord_range'] = 0
    feature_values['average_LH_3chord_range'] = 0
    feature_values['average_RH_3chord_range'] = 0
    #feature_values['average_LRH_4chord_range'] = 0
    feature_values['average_LH_4chord_range'] = 0
    feature_values['average_RH_4chord_range'] = 0
    #feature_values['average_LRH_5chord_range'] = 0
    feature_values['average_LH_5chord_range'] = 0
    feature_values['average_RH_5chord_range'] = 0

    #feature_values['average_LRH_2chord_hand_range'] = 0
    feature_values['average_LH_2chord_hand_range'] = 0
    feature_values['average_RH_2chord_hand_range'] = 0
    #feature_values['average_LRH_3chord_hand_range'] = 0
    feature_values['average_LH_3chord_hand_range'] = 0
    feature_values['average_RH_3chord_hand_range'] = 0
    #feature_values['average_LRH_4chord_hand_range'] = 0
    feature_values['average_LH_4chord_hand_range'] = 0
    feature_values['average_RH_4chord_hand_range'] = 0
    #feature_values['average_LRH_5chord_hand_range'] = 0
    feature_values['average_LH_5chord_hand_range'] = 0
    feature_values['average_RH_5chord_hand_range'] = 0

    #feature_values['large_5jumps_LRH'] = 0
    feature_values['large_5jumps_LH'] = 0
    feature_values['large_5jumps_RH'] = 0
    #feature_values['large_8jumps_LRH'] = 0
    feature_values['large_8jumps_LH'] = 0
    feature_values['large_8jumps_RH'] = 0
    #feature_values['large_9jumps_LRH'] = 0
    feature_values['large_9jumps_LH'] = 0
    feature_values['large_9jumps_RH'] = 0
    #feature_values['large_10jumps_LRH'] = 0
    feature_values['large_10jumps_LH'] = 0
    feature_values['large_10jumps_RH'] = 0

    #feature_values['average_large_5jumps_LRH'] = 0
    feature_values['average_large_5jumps_LH'] = 0
    feature_values['average_large_5jumps_RH'] = 0
    #feature_values['average_large_8jumps_LRH'] = 0
    feature_values['average_large_8jumps_LH'] = 0
    feature_values['average_large_8jumps_RH'] = 0
    #feature_values['average_large_9jumps_LRH'] = 0
    feature_values['average_large_9jumps_LH'] = 0
    feature_values['average_large_9jumps_RH'] = 0
    #feature_values['average_large_10jumps_LRH'] = 0
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
    altered_pitches = music_key.alteredPitches
    temp_pitches = []
    for pitch in altered_pitches:
        temp_pitches.append(pitch.name)
    altered_pitches = temp_pitches
    feature_values['total_LRH_accidentals'] = totalAccidentals(both_hands_stream,altered_pitches)
    feature_values['total_RH_accidentals'] = totalAccidentals(right_hand_stream,altered_pitches)
    feature_values['total_LH_accidentals'] = totalAccidentals(left_hand_stream,altered_pitches)

    feature_values['average_LRH_accidentals'] = averageAccidentals(both_hands_stream,altered_pitches)
    feature_values['average_RH_accidentals'] = averageAccidentals(right_hand_stream,altered_pitches)
    feature_values['average_LH_accidentals'] = averageAccidentals(left_hand_stream,altered_pitches)

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
    #feature_values['average_RLH_range'] = averageRangeForNextNotes(both_hands_chords)
    feature_values['average_next_LH_range'] = averageRangeForNextNotes(left_hand_chords)
    feature_values['average_next_RH_range'] = averageRangeForNextNotes(right_hand_chords)

    feature_values['average_density_RLH'] = averageDensity(both_hands_chords)
    feature_values['average_density_LH'] = averageDensity(left_hand_chords)
    feature_values['average_density_RH'] = averageDensity(right_hand_chords)

    #average range for top 10% percent of notes
    #feature_values['average_RLH_note_10_range'] = averageRangeOfTopXPercent(both_hands_stream,.1)
    feature_values['average_LH_note_10_range'] = averageRangeOfTopXPercent(left_hand_chords,.1)
    feature_values['average_RH_note_10_range'] = averageRangeOfTopXPercent(right_hand_chords,.1)
    #average range for top 20% percent of notes
    #feature_values['average_RLH_note_20_range'] = averageRangeOfTopXPercent(both_hands_stream,.2)
    feature_values['average_LH_note_20_range'] = averageRangeOfTopXPercent(left_hand_chords,.2)
    feature_values['average_RH_note_20_range'] = averageRangeOfTopXPercent(right_hand_chords,.2)
    #average range for top 35% percent of notes
    #feature_values['average_RLH_note_35_range'] = averageRangeOfTopXPercent(both_hands_stream,.35)
    feature_values['average_LH_note_35_range'] = averageRangeOfTopXPercent(left_hand_chords,.35)
    feature_values['average_RH_note_35_range'] = averageRangeOfTopXPercent(right_hand_chords,.35)
    #average range for top 50% percent of notes
    #feature_values['average_RLH_note_50_range'] = averageRangeOfTopXPercent(both_hands_stream,.5)
    feature_values['average_LH_note_50_range'] = averageRangeOfTopXPercent(left_hand_chords,.5)
    feature_values['average_RH_note_50_range'] = averageRangeOfTopXPercent(right_hand_chords,.5)

    feature_values['average_LH_note_75_range'] = averageRangeOfTopXPercent(left_hand_chords,.75)
    feature_values['average_RH_note_75_range'] = averageRangeOfTopXPercent(right_hand_chords,.75)
    #average range for top 100% percent of notes*******
    #Efeature_values['average_RLH_note_100_range'] = averageRangeOfTopXPercent(both_hands_stream,1)
    feature_values['average_LH_note_100_range'] = averageRangeOfTopXPercent(left_hand_chords,1)
    feature_values['average_RH_note_100_range'] = averageRangeOfTopXPercent(right_hand_chords,1)

    feature_values['fake_range_LH_10'] = fakeRangeOfTopXPercent(left_hand_chords, .1)
    feature_values['fake_range_RH_10'] = fakeRangeOfTopXPercent(right_hand_chords, .1)

    feature_values['fake_range_LH_20'] = fakeRangeOfTopXPercent(left_hand_chords, .2)
    feature_values['fake_range_RH_20'] = fakeRangeOfTopXPercent(right_hand_chords, .2)

    feature_values['fake_range_LH_35'] = fakeRangeOfTopXPercent(left_hand_chords, .35)
    feature_values['fake_range_RH_35'] = fakeRangeOfTopXPercent(right_hand_chords, .35)

    feature_values['fake_range_LH_50'] = fakeRangeOfTopXPercent(left_hand_chords, .5)
    feature_values['fake_range_RH_50'] = fakeRangeOfTopXPercent(right_hand_chords, .5)

    feature_values['fake_range_LH_75'] = fakeRangeOfTopXPercent(left_hand_chords, .75)
    feature_values['fake_range_RH_75'] = fakeRangeOfTopXPercent(left_hand_chords, .75)

    feature_values['fake_range_LH_100'] = fakeRangeOfTopXPercent(left_hand_chords, 1)
    feature_values['fake_range_RH_100'] = fakeRangeOfTopXPercent(left_hand_chords, 1)

    #range for top 10% percent of notes*******************************************
    #*** maybe get the range of the most common note for each hand(would have to create a new method for this to work)
    #feature_values['RLH_note_10_range'] = rangeOfTopXPercent(both_hands_stream,.1)
    feature_values['LH_note_10_range'] = rangeOfTopXPercent(left_hand_chords,.1)
    feature_values['RH_note_10_range'] = rangeOfTopXPercent(right_hand_chords,.1)
    # range for top 20% percent of notes
    #feature_values['RLH_note_20_range'] = rangeOfTopXPercent(both_hands_stream,.2)
    feature_values['LH_note_20_range'] = rangeOfTopXPercent(left_hand_chords,.2)
    feature_values['RH_note_20_range'] = rangeOfTopXPercent(right_hand_chords,.2)
    # range for top 35% percent of notes
    #feature_values['RLH_note_35_range'] = rangeOfTopXPercent(both_hands_stream,.35)
    feature_values['LH_note_35_range'] = rangeOfTopXPercent(left_hand_chords,.35)
    feature_values['RH_note_35_range'] = rangeOfTopXPercent(right_hand_chords,.35)
    # range for top 50% percent of notes
    #feature_values['RLH_note_50_range'] = rangeOfTopXPercent(both_hands_stream,.5)
    feature_values['LH_note_50_range'] = rangeOfTopXPercent(left_hand_chords,.5)
    feature_values['RH_note_50_range'] = rangeOfTopXPercent(right_hand_chords,.5)
    # range for top 100% percent of notes*****
    #feature_values['RLH_note_100_range'] = rangeOfTopXPercent(both_hands_stream,1)
    feature_values['LH_note_100_range'] = rangeOfTopXPercent(left_hand_chords,1)
    feature_values['RH_note_100_range'] = rangeOfTopXPercent(right_hand_chords,1)

    #average range for each finger in chord
    #feature_values['average_LRH_2chord_range'] = averageChordRangeForHand(both_hands_chords,2)
    feature_values['average_LH_2chord_range'] = averageChordRangeForHand(left_hand_chords,2)
    feature_values['average_RH_2chord_range'] = averageChordRangeForHand(right_hand_chords,2)

    #feature_values['average_LRH_3chord_range'] = averageChordRangeForHand(both_hands_chords,3)
    feature_values['average_LH_3chord_range'] = averageChordRangeForHand(left_hand_chords,3)
    feature_values['average_RH_3chord_range'] = averageChordRangeForHand(right_hand_chords,3)

    #feature_values['average_LRH_4chord_range'] = averageChordRangeForHand(both_hands_chords,4)
    feature_values['average_LH_4chord_range'] = averageChordRangeForHand(left_hand_chords,4)
    feature_values['average_RH_4chord_range'] = averageChordRangeForHand(right_hand_chords,4)

    #feature_values['average_LRH_5chord_range'] = averageChordRangeForHand(both_hands_chords,5)
    feature_values['average_LH_5chord_range'] = averageChordRangeForHand(left_hand_chords,5)
    feature_values['average_RH_5chord_range'] = averageChordRangeForHand(right_hand_chords,5)

    #average range for each hand*****
    #feature_values['average_LRH_2chord_hand_range'] = average2ChordRangeForHand(both_hands_chords,2)
    feature_values['average_LH_2chord_hand_range'] = average2ChordRangeForHand(left_hand_chords,2)
    feature_values['average_RH_2chord_hand_range'] = average2ChordRangeForHand(right_hand_chords,2)

    #feature_values['average_LRH_3chord_hand_range'] = average2ChordRangeForHand(both_hands_chords,3)
    feature_values['average_LH_3chord_hand_range'] = average2ChordRangeForHand(left_hand_chords,3)
    feature_values['average_RH_3chord_hand_range'] = average2ChordRangeForHand(right_hand_chords,3)

    #feature_values['average_LRH_4chord_hand_range'] = average2ChordRangeForHand(both_hands_chords,4)
    feature_values['average_LH_4chord_hand_range'] = average2ChordRangeForHand(left_hand_chords,4)
    feature_values['average_RH_4chord_hand_range'] = average2ChordRangeForHand(right_hand_chords,4)

    #feature_values['average_LRH_5chord_hand_range'] = average2ChordRangeForHand(both_hands_chords,5)
    feature_values['average_LH_5chord_hand_range'] = average2ChordRangeForHand(left_hand_chords,5)
    feature_values['average_RH_5chord_hand_range'] = average2ChordRangeForHand(right_hand_chords,5)

    #large jumps
    #feature_values['large_5jumps_LRH'] = largeJumps(both_hands_chords,5)
    feature_values['large_5jumps_LH'] = largeJumps(left_hand_chords,5)
    feature_values['large_5jumps_RH'] = largeJumps(right_hand_chords,5)

    #feature_values['large_8jumps_LRH'] = largeJumps(both_hands_chords,8)
    feature_values['large_8jumps_LH'] = largeJumps(left_hand_chords,8)
    feature_values['large_8jumps_RH'] = largeJumps(right_hand_chords,8)

    #feature_values['large_9jumps_LRH'] = largeJumps(both_hands_chords,9)
    feature_values['large_9jumps_LH'] = largeJumps(left_hand_chords,9)
    feature_values['large_9jumps_RH'] = largeJumps(right_hand_chords,9)

    #feature_values['large_10jumps_LRH'] = largeJumps(both_hands_chords,10)
    feature_values['large_10jumps_LH'] = largeJumps(left_hand_chords,10)
    feature_values['large_10jumps_RH'] = largeJumps(right_hand_chords,10)

    #average large jumps*****
    #feature_values['average_large_5jumps_LRH'] = averageLargeJumps(both_hands_chords,5)
    feature_values['average_large_5jumps_LH'] = averageLargeJumps(left_hand_chords,5)
    feature_values['average_large_5jumps_RH'] = averageLargeJumps(right_hand_chords,5)

    #feature_values['average_large_8jumps_LRH'] = averageLargeJumps(both_hands_chords,8)
    feature_values['average_large_8jumps_LH'] = averageLargeJumps(left_hand_chords,8)
    feature_values['average_large_8jumps_RH'] = averageLargeJumps(right_hand_chords,8)

    #feature_values['average_large_9jumps_LRH'] = averageLargeJumps(both_hands_chords,9)
    feature_values['average_large_9jumps_LH'] = averageLargeJumps(left_hand_chords,9)
    feature_values['average_large_9jumps_RH'] = averageLargeJumps(right_hand_chords,9)

    #feature_values['average_large_10jumps_LRH'] = averageLargeJumps(both_hands_chords,10)
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

    paths = []

    #score contains both left and right hand
    scoreR = stream.Score()

    scoreL = None
    scoreR.insert(0,right_hand_stream)
    if left_hand_stream is not None:
        scoreL = stream.Score()
        scoreL.insert(0,left_hand_stream)
    #scoreL.show()
    feature_values["Right Hand Similarity"] = custom_feature.similarityBetween1Score(scoreR,file)
    feature_values["Advanced Rhythmic Similarity R"] = custom_feature.advancedRhythmSimilarity(scoreR)
    print("length of right hand chords: ",len(right_hand_chords))
    #right_hand_chords.show()
    feature_values["total2ChordNotesRight"] = custom_feature.totalXChordNotes(right_hand_chords,2)
    feature_values["total3ChordNotesRight"] = custom_feature.totalXChordNotes(right_hand_chords,3)
    feature_values["total4ChordNotesRight"] = custom_feature.totalXChordNotes(right_hand_chords,4)
    feature_values["total5ChordNotesRight"] = custom_feature.totalXChordNotes(right_hand_chords,5)
    feature_values["average2ChordNotesRight"] = custom_feature.averageXChordNotes(right_hand_chords,2)
    feature_values["average3ChordNotesRight"] = custom_feature.averageXChordNotes(right_hand_chords,3)
    feature_values["average4ChordNotesRight"] = custom_feature.averageXChordNotes(right_hand_chords,4)
    feature_values["average5ChordNotesRight"] = custom_feature.averageXChordNotes(right_hand_chords,5)
    if scoreL is not None:
        feature_values["Left Hand Similarity"] = custom_feature.similarityBetween1Score(scoreL,file)
        #similarity of both hands at the same time
        feature_values["Both Hand Similarity"] = custom_feature.similarityBetween1Score(score,file)
        #similarity of left hand with right hand
        feature_values["Left Right Hand Similarity"] = custom_feature.similarityBetween2Score(scoreL,scoreR,file)
        #rhythmic similarity
        feature_values["Rhythmic Similarity LR 1:1"] = custom_feature.rhythmSimilarity(scoreL,scoreR)
        #advanced rhythmic similarity
        feature_values["Advanced Rhythmic Similarity L"] = custom_feature.advancedRhythmSimilarity(scoreL)
        #advanced rhythmic similarity for left and right hand,score1 search for, score 2 search
        feature_values["Advanced Rhythmic Similarity LR"] = custom_feature.advancedRhythm2Similarity(scoreL,scoreR)
        #total X notes in left hand
        feature_values["total2ChordNotesLeft"] = custom_feature.totalXChordNotes(left_hand_chords,2)
        feature_values["total3ChordNotesLeft"] = custom_feature.totalXChordNotes(left_hand_chords,3)
        feature_values["total4ChordNotesLeft"] = custom_feature.totalXChordNotes(left_hand_chords,4)
        feature_values["total5ChordNotesLeft"] = custom_feature.totalXChordNotes(left_hand_chords,5)
        feature_values["average2ChordNotesLeft"] = custom_feature.averageXChordNotes(left_hand_chords,2)
        feature_values["average3ChordNotesLeft"] = custom_feature.averageXChordNotes(left_hand_chords,3)
        feature_values["average4ChordNotesLeft"] = custom_feature.averageXChordNotes(left_hand_chords,4)
        feature_values["average5ChordNotesLeft"] = custom_feature.averageXChordNotes(left_hand_chords,5)


    else:
        feature_values["Left Hand Similarity"] = -1
        #similarity of both hands at the same time
        feature_values["Both Hand Similarity"] = -1
        #similarity of left hand with right hand
        feature_values["Left Right Hand Similarity"] = -1
        #rhythmic similarity
        feature_values["Rhythmic Similarity LR 1:1"] = -1
        #advanced rhythmic similarity
        feature_values["Advanced Rhythmic Similarity L"] = -1
        #advanced rhythmic similarity for left and right hand,score1 search for, score 2 search
        feature_values["Advanced Rhythmic Similarity LR"] = -1
        #total X notes in right hand
        feature_values["total2ChordNotesLeft"] = 0
        feature_values["total3ChordNotesLeft"] = 0
        feature_values["total4ChordNotesLeft"] = 0
        feature_values["total5ChordNotesLeft"] = 0
        feature_values["average2ChordNotesLeft"] = 0
        feature_values["average3ChordNotesLeft"] = 0
        feature_values["average4ChordNotesLeft"] = 0
        feature_values["average5ChordNotesLeft"] = 0



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

    # try:
    #     feature_values['MostCommonSetClassSimultaneityPrevalence'] = features.native.MostCommonSetClassSimultaneityPrevalence(score).extract().vector[0]
    # except:
    #     feature_values['MostCommonSetClassSimultaneityPrevalence'] = 0
    #     print("error")
    # print("MostCommonSetClassSimultaneityPrevalence Done")

    # try:
    #     feature_values['TriadSimultaneityPrevalence'] = features.native.TriadSimultaneityPrevalence(score).extract().vector[0]
    # except:
    #     feature_values['TriadSimultaneityPrevalence'] = 0
    #     print("error")
    # print("TriadSimultaneityPrevalence Done")

    # try:
    #     feature_values['UniquePitchClassSetSimultaneities'] = features.native.UniquePitchClassSetSimultaneities(score).extract().vector[0]
    # except:
    #     feature_values['UniquePitchClassSetSimultaneities'] = 0
    #     print("error")
    # print("UniquePitchClassSetSimultaneities Done")

    # try:
    #     feature_values['UniqueSetClassSimultaneities'] = features.native.UniqueSetClassSimultaneities(score).extract().vector[0]
    # except:
    #     feature_values['UniqueSetClassSimultaneities'] = 0
    #     print("error")
    # print("UniqueSetClassSimultaneities Done")

    # try:
    #     feature_values['AverageNoteDurationFeature'] = features.jSymbolic.AverageNoteDurationFeature(score).extract().vector[0]
    # except:
    #     feature_values['AverageNoteDurationFeature'] = 0
    #     print("error")
    # print("AverageNoteDurationFeature Done")

    # try:
    #     feature_values['AverageTimeBetweenAttacksFeature'] = features.jSymbolic.AverageTimeBetweenAttacksFeature(score).extract().vector[0]
    # except:
    #     feature_values['AverageTimeBetweenAttacksFeature'] = 0
    # print("AverageTimeBetweenAttacksFeature Done")

    # try:
    #     feature_values['AverageTimeBetweenAttacksForEachVoiceFeature'] = features.jSymbolic.AverageTimeBetweenAttacksForEachVoiceFeature(score).extract().vector[0]
    # except:
    #     feature_values['AverageTimeBetweenAttacksForEachVoiceFeature'] = 0
    #     print("error")
    # print("AverageTimeBetweenAttacksForEachVoiceFeature Done")

    # try:
    #     feature_values['DirectionOfMotionFeature'] = features.jSymbolic.DirectionOfMotionFeature(score).extract().vector[0]
    # except:
    #     feature_values['DirectionOfMotionFeature'] = 0
    #     print("error")
    # print("DirectionOfMotionFeature Done")

    try:
        feature_values['ImportanceOfHighRegisterFeature'] = features.jSymbolic.ImportanceOfHighRegisterFeature(score).extract().vector[0]
    except:
        feature_values['ImportanceOfHighRegisterFeature'] = 0
        print("error")
    print("ImportanceOfHighRegisterFeature Done")

    try:
        feature_values['NoteDensityFeatureBH'] = features.jSymbolic.NoteDensityFeature(score).extract().vector[0]
    except:
        feature_values['NoteDensityFeatureBH'] = 0
        print("error")
    print("NoteDensityFeatureBH Done")

    try:
        feature_values['NoteDensityFeatureLH'] = features.jSymbolic.NoteDensityFeature(left_hand_stream).extract().vector[0]
    except:
        feature_values['NoteDensityFeatureLH'] = 0
        print("error")
    print("NoteDensityFeatureLH Done")

    try:
        feature_values['NoteDensityFeatureRH'] = features.jSymbolic.NoteDensityFeature(right_hand_stream).extract().vector[0]
    except:
        feature_values['NoteDensityFeatureRH'] = 0
        print("error")
    print("NoteDensityFeatureRH Done")

    try:
        feature_values['PitchVarietyFeatureBH'] = features.jSymbolic.PitchVarietyFeature(score).extract().vector[0]
    except:
        eature_values['PitchVarietyFeatureBH'] = 0
        print("error")
    print("PitchVarietyFeatureBH Done")

    try:
        feature_values['PitchVarietyFeatureLH'] = features.jSymbolic.PitchVarietyFeature(left_hand_stream).extract().vector[0]
    except:
        feature_values['PitchVarietyFeatureLH'] = 0
        print("error")
    print("PitchVarietyFeatureLH Done")

    try:
        feature_values['PitchVarietyFeatureRH'] = features.jSymbolic.PitchVarietyFeature(right_hand_stream).extract().vector[0]
    except:
        eature_values['PitchVarietyFeatureRH'] = 0
        print("error")
    print("PitchVarietyFeatureRH Done")

    # try:
    #     feature_values['RelativeStrengthOfTopPitchClassesFeature'] = features.jSymbolic.RelativeStrengthOfTopPitchClassesFeature(score).extract().vector[0]
    # except:
    #     feature_values['RelativeStrengthOfTopPitchClassesFeature'] = 0
    #     print("error")
    # print("RelativeStrengthOfTopPitchClassesFeature Done")

    # try:
    #     feature_values['RelativeStrengthOfTopPitchesFeature'] = features.jSymbolic.RelativeStrengthOfTopPitchesFeature(score).extract().vector[0]
    # except:
    #     feature_values['RelativeStrengthOfTopPitchesFeature'] = 0
    #     print("error")
    # print("RelativeStrengthOfTopPitchesFeature Done")

    try:
        feature_values['RepeatedNotesFeatureBoth'] = features.jSymbolic.RepeatedNotesFeature(score).extract().vector[0]
    except:
        feature_values['RepeatedNotesFeatureBoth'] = 0
    print("RepeatedNotesFeature Done")

    try:
        feature_values['RepeatedNotesFeatureL'] = features.jSymbolic.RepeatedNotesFeature(left_hand_stream).extract().vector[0]
    except:
        feature_values['RepeatedNotesFeatureL'] = 0
    print("RepeatedNotesFeatureL Done")

    try:
        feature_values['RepeatedNotesFeatureR'] = features.jSymbolic.RepeatedNotesFeature(right_hand_stream).extract().vector[0]
    except:
        feature_values['RepeatedNotesFeatureR'] = 0
    print("RepeatedNotesFeatureR Done")

    # try:
    #     feature_values['AverageVariabilityOfTimeBetweenAttacksForEachVoiceFeature'] = features.jSymbolic.AverageVariabilityOfTimeBetweenAttacksForEachVoiceFeature(score).extract().vector[0]
    # except:
    #     feature_values['AverageVariabilityOfTimeBetweenAttacksForEachVoiceFeature'] = 0
    # print("AverageVariabilityOfTimeBetweenAttacksForEachVoiceFeature Done")

    # try:
    #     feature_values['ImportanceOfBassRegisterFeature'] = features.jSymbolic.ImportanceOfBassRegisterFeature(score).extract().vector[0]
    # except:
    #     feature_values['ImportanceOfBassRegisterFeature'] = 0
    # print("ImportanceOfBassRegisterFeature Done")

    # try:
    #     feature_values['ImportanceOfMiddleRegisterFeature'] = features.jSymbolic.ImportanceOfMiddleRegisterFeature(score).extract().vector[0]
    # except:
    #     feature_values['ImportanceOfMiddleRegisterFeature'] = 0
    # print("ImportanceOfMiddleRegisterFeature Done")

    # try:
    #     feature_values['IntervalBetweenStrongestPitchClassesFeatureBH'] = features.jSymbolic.IntervalBetweenStrongestPitchClassesFeature(score).extract().vector[0]
    # except:
    #     feature_values['IntervalBetweenStrongestPitchClassesFeatureBH'] = 0
    # print("IntervalBetweenStrongestPitchClassesFeatureBH Done")

    # try:
    #     feature_values['IntervalBetweenStrongestPitchClassesFeatureLH'] = features.jSymbolic.IntervalBetweenStrongestPitchClassesFeature(left_hand_stream).extract().vector[0]
    # except:
    #     feature_values['IntervalBetweenStrongestPitchClassesFeatureLH'] = 0
    # print("IntervalBetweenStrongestPitchClassesFeatureLH Done")

    # try:
    #     feature_values['IntervalBetweenStrongestPitchClassesFeatureRH'] = features.jSymbolic.IntervalBetweenStrongestPitchClassesFeature(right_hand_stream).extract().vector[0]
    # except:
    #     feature_values['IntervalBetweenStrongestPitchClassesFeatureRH'] = 0
    # print("IntervalBetweenStrongestPitchClassesFeatureRH Done")

    # try:
    #     feature_values['IntervalBetweenStrongestPitchesFeatureBH'] = features.jSymbolic.IntervalBetweenStrongestPitchesFeature(score).extract().vector[0]
    # except:
    #     feature_values['IntervalBetweenStrongestPitchesFeatureBH'] = 0
    # print("IntervalBetweenStrongestPitchesFeatureBH Done")

    # try:
    #     feature_values['IntervalBetweenStrongestPitchesFeatureLH'] = features.jSymbolic.IntervalBetweenStrongestPitchesFeature(left_hand_stream).extract().vector[0]
    # except:
    #     feature_values['IntervalBetweenStrongestPitchesFeatureLH'] = 0
    # print("IntervalBetweenStrongestPitchesFeatureLH Done")

    # try:
    #     feature_values['IntervalBetweenStrongestPitchesFeatureRH'] = features.jSymbolic.IntervalBetweenStrongestPitchesFeature(right_hand_stream).extract().vector[0]
    # except:
    #     feature_values['IntervalBetweenStrongestPitchesFeatureRH'] = 0
    # print("IntervalBetweenStrongestPitchesFeatureRH Done")

    # try:
    #     feature_values['MelodicOctavesFeature'] = features.jSymbolic.MelodicOctavesFeature(score).extract().vector[0]
    # except:
    #     feature_values['MelodicOctavesFeature'] = 0
    # print("MelodicOctavesFeature Done")

    # try:
    #     feature_values['MostCommonMelodicIntervalFeature'] = features.jSymbolic.MostCommonMelodicIntervalFeature(score).extract().vector[0]
    # except:
    #     feature_values['MostCommonMelodicIntervalFeature'] = 0
    # print("MostCommonMelodicIntervalFeature Done")

    # try:
    #     feature_values['MostCommonMelodicIntervalPrevalenceFeature'] = features.jSymbolic.MostCommonMelodicIntervalPrevalenceFeature(score).extract().vector[0]
    # except:
    #     feature_values['MostCommonMelodicIntervalPrevalenceFeature'] = 0
    # print("MostCommonMelodicIntervalPrevalenceFeature Done")

    # try:
    #     feature_values['MostCommonPitchClassFeature'] = features.jSymbolic.MostCommonPitchClassFeature(score).extract().vector[0]
    # except:
    #     feature_values['MostCommonPitchClassFeature'] = 0
    # print("MostCommonPitchClassFeature Done")

    # try:
    #     feature_values['MostCommonPitchClassPrevalenceFeature'] = features.jSymbolic.MostCommonPitchClassPrevalenceFeature(score).extract().vector[0]
    # except:
    #     feature_values['MostCommonPitchClassPrevalenceFeature'] = 0
    # print("MostCommonPitchClassPrevalenceFeature Done")

    # try:
    #     feature_values['MostCommonPitchPrevalenceFeature'] = features.jSymbolic.MostCommonPitchPrevalenceFeature(score).extract().vector[0]
    # except:
    #     feature_values['MostCommonPitchPrevalenceFeature'] = 0
    # print("MostCommonPitchPrevalenceFeature Done")

    # try:
    #     feature_values['NumberOfCommonMelodicIntervalsFeature'] = features.jSymbolic.NumberOfCommonMelodicIntervalsFeature(score).extract().vector[0]
    # except:
    #     feature_values['NumberOfCommonMelodicIntervalsFeature'] = 0
    # print("NumberOfCommonMelodicIntervalsFeature Done")

    # try:
    #     feature_values['NumberOfCommonPitchesFeatureBH'] = features.jSymbolic.NumberOfCommonPitchesFeature(score).extract().vector[0]
    # except:
    #     feature_values['NumberOfCommonPitchesFeatureBH'] = 0
    # print("NumberOfCommonPitchesFeatureBH Done")

    # try:
    #     feature_values['NumberOfCommonPitchesFeatureLH'] = features.jSymbolic.NumberOfCommonPitchesFeature(left_hand_stream).extract().vector[0]
    # except:
    #     feature_values['NumberOfCommonPitchesFeatureLH'] = 0
    # print("NumberOfCommonPitchesFeatureLH Done")

    # try:
    #     feature_values['NumberOfCommonPitchesFeatureRH'] = features.jSymbolic.NumberOfCommonPitchesFeature(right_hand_stream).extract().vector[0]
    # except:
    #     feature_values['NumberOfCommonPitchesFeatureRH'] = 0
    # print("NumberOfCommonPitchesFeatNumberOfCommonPitchesFeatureRHureLH Done")

    # try:
    #     feature_values['PitchClassVarietyFeature'] = features.jSymbolic.PitchClassVarietyFeature(score).extract().vector[0]
    # except:
    #     feature_values['PitchClassVarietyFeature'] = 0
    # print("PitchClassVarietyFeature Done")

    # try:
    #     feature_values['StepwiseMotionFeature'] = features.jSymbolic.StepwiseMotionFeature(score).extract().vector[0]
    # except:
    #     feature_values['StepwiseMotionFeature'] = 0
    # print("StepwiseMotionFeature Done")

    # try:
    #     feature_values['StrengthOfSecondStrongestRhythmicPulseFeatureBH'] = features.jSymbolic.StrengthOfSecondStrongestRhythmicPulseFeature(score).extract().vector[0]
    # except:
    #     feature_values['StrengthOfSecondStrongestRhythmicPulseFeatureBH'] = 0
    # print("StrengthOfSecondStrongestRhythmicPulseFeatureBH Done")

    # try:
    #     feature_values['StrengthOfSecondStrongestRhythmicPulseFeatureLH'] = features.jSymbolic.StrengthOfSecondStrongestRhythmicPulseFeature(left_hand_stream).extract().vector[0]
    # except:
    #     feature_values['StrengthOfSecondStrongestRhythmicPulseFeatureLH'] = 0
    # print("StrengthOfSecondStrongestRhythmicPulseFeatureLH Done")

    # try:
    #     feature_values['StrengthOfSecondStrongestRhythmicPulseFeatureRH'] = features.jSymbolic.StrengthOfSecondStrongestRhythmicPulseFeature(right_hand_stream).extract().vector[0]
    # except:
    #     feature_values['StrengthOfSecondStrongestRhythmicPulseFeatureRH'] = 0
    # print("StrengthOfSecondStrongestRhythmicPulseFeatureRH Done")

    # try:
    #     feature_values['StrengthOfStrongestRhythmicPulseFeatureBH'] = features.jSymbolic.StrengthOfStrongestRhythmicPulseFeature(score).extract().vector[0]
    # except:
    #     feature_values['StrengthOfStrongestRhythmicPulseFeatureBH'] = 0
    # print("StrengthOfStrongestRhythmicPulseFeatureBH Done")

    # try:
    #     feature_values['StrengthOfStrongestRhythmicPulseFeatureLH'] = features.jSymbolic.StrengthOfStrongestRhythmicPulseFeature(left_hand_stream).extract().vector[0]
    # except:
    #     feature_values['StrengthOfStrongestRhythmicPulseFeatureLH'] = 0
    # print("StrengthOfStrongestRhythmicPulseFeatureLH Done")

    # try:
    #     feature_values['StrengthOfStrongestRhythmicPulseFeatureRH'] = features.jSymbolic.StrengthOfStrongestRhythmicPulseFeature(right_hand_stream).extract().vector[0]
    # except:
    #     feature_values['StrengthOfStrongestRhythmicPulseFeatureRH'] = 0
    # print("StrengthOfStrongestRhythmicPulseFeatureRH Done")

    # try:
    #     feature_values['StrengthRatioOfTwoStrongestRhythmicPulsesFeatureBH'] = features.jSymbolic.StrengthRatioOfTwoStrongestRhythmicPulsesFeature(score).extract().vector[0]
    # except:
    #     feature_values['StrengthRatioOfTwoStrongestRhythmicPulsesFeatureBH'] = 0
    # print("StrengthRatioOfTwoStrongestRhythmicPulsesFeatureBH Done")

    # try:
    #     feature_values['StrengthRatioOfTwoStrongestRhythmicPulsesFeatureLH'] = features.jSymbolic.StrengthRatioOfTwoStrongestRhythmicPulsesFeature(left_hand_stream).extract().vector[0]
    # except:
    #     feature_values['StrengthRatioOfTwoStrongestRhythmicPulsesFeatureLH'] = 0
    # print("StrengthRatioOfTwoStrongestRhythmicPulsesFeatureLH Done")

    # try:
    #     feature_values['StrengthRatioOfTwoStrongestRhythmicPulsesFeatureRH'] = features.jSymbolic.StrengthRatioOfTwoStrongestRhythmicPulsesFeature(right_hand_stream).extract().vector[0]
    # except:
    #     feature_values['StrengthRatioOfTwoStrongestRhythmicPulsesFeatureRH'] = 0
    # print("StrengthRatioOfTwoStrongestRhythmicPulsesFeatureRH Done")

    try:
        feature_values['VariabilityOfNoteDurationFeature'] = features.jSymbolic.VariabilityOfNoteDurationFeature(score).extract().vector[0]
    except:
        feature_values['VariabilityOfNoteDurationFeature'] = 0
    print("VariabilityOfNoteDurationFeature Done")

    # try:
    #     feature_values['VariabilityOfTimeBetweenAttacksFeature'] = features.jSymbolic.VariabilityOfTimeBetweenAttacksFeature(score).extract().vector[0]
    # except:
    #     feature_values['VariabilityOfTimeBetweenAttacksFeature'] = 0
    # print("VariabilityOfTimeBetweenAttacksFeature Done")






















    feature_values['Grade'] = files[file]
    print("feature-index: ",feature_index)
    ##################################################################insert feature values into song_features dictionary
    if(feature_index==0):
        labels_file = open("tempClassical.txt","w")
        f = open("tempClassical.csv","w")

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
