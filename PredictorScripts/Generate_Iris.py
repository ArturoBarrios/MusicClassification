from music21 import *
import re
import os

'''feature vector: Length of Music,Key Signature, Number of Notes,
Total Measures, Time Signature den, Time Signature num, BPM, Chords

'''
#files = {"./Midi_Files/Fur_Elise(7).mid":7}
files = {}
'''go through Midi_Files directory and get
file names and levels and store them in
dictioanry
'''
for root, dirs, song_files in os.walk("./Midi_Files"):
    for filename in song_files:
        num = ""
        #offset to get the first digit of grade level
        offset = 6
        #get level of song
        while(filename[len(filename)-offset]!='('):
            char =  filename[len(filename)-offset]
            char+=num
            num = char
            offset+=1
        num = int(num)
        filename = "./Midi_Files/"+str(filename)
        files[filename] = num

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

for file in files:
    print(file)
    chords_in_piece = dict()
    curr_stream = converter.parse(str(file))

    #Length of music: time in which last note ends(72)
    music_len = curr_stream.highestTime

    #key signature:
    music_key = curr_stream.analyze('key')

    music_key = key_signatures[str(music_key)]

    #number of notes, need to add number of chords
    notes = curr_stream.flat.getElementsByClass("Note")
    num_notes = len(notes)

    #total Measures
    total_measures = len(curr_stream.measures(0,10000)[0])

    time_signature_den = 0
    time_signature_num = 0
    #time Signature
    # if(len(curr_stream.flat.getElementsByClass(meter.TimeSignature))>0):
    time_signature_num = curr_stream[0].getTimeSignatures()[0].numerator
    time_signature_den = curr_stream[0].getTimeSignatures()[0].denominator
    # time_signature_den = curr_stream.flat.getElementsByClass(meter.TimeSignature)[0].denominator
    # time_signature_num = curr_stream.flat.getElementsByClass(meter.TimeSignature)[0].numerator
    # else:
    #     print("no time signature: ",file)
    #     time_signature_den = 4
    #     time_signature_num = 4

    #chords
    sChords = curr_stream.chordify()
    sFlat = sChords.flat
    sOnlyChords = sFlat.getElementsByClass('Chord')
    #add chords to number_of_notes
    num_notes+=len(sOnlyChords)
    #put chords in chords_in_piece dictionary
    for chord in sOnlyChords:
        #check if chord in unique chord list
        if chord.pitchedCommonName not in unique_chords and len(chord)>2:
            unique_chords.append(chord.pitchedCommonName)

        #put chord in chords_in_piece dictionary
        if(len(chord) > 1):
            if chord.pitchedCommonName not in chords_in_piece:
                chords_in_piece[chord.pitchedCommonName] = 1
            else:
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
    for chord in unique_chords:
        #put count value if chord is in chords_in_piece
        if chord in chords_in_piece:
            songs_features[index].append(chords_in_piece[chord])
        else:
            songs_features[index].append(0)

    songs_features[index].append(files[str(file)])

    index+=1


#write id,features,grade in first line of iris files
#f = open("music_IrisWCG3.csv","w")
#labels_file = open("music_featuresWCG3.txt","w")
f = open("music_IrisWCG3.csv","w")
labels_file = open("music_IrisWCG3.txt","w")
f.write("Id,length,key,number_of_notes,total_measures,"
"time_signature_num,time_signature_den,range")
labels_file.write("length,key,number_of_notes,total_measures,"
"time_signature_num,time_signature_den,range")
i = 0
#write unique chords in first line
for chord in unique_chords:
    f.write(chord)
    f.write(",")
    labels_file.write(chord)
    labels_file.write(",")



f.write("Grade\n")
#use song_features dictionary to
#write song id, song features, and song grade
for id,feature_list in songs_features.items():
    #these are the first 6 features which don't include chords
    f.write(str(id)+","+str(songs_features[id][0])+","+str(songs_features[id][1])
    +","+str(songs_features[id][2])+","+str(songs_features[id][3])+","
    +str(songs_features[id][4])+","+str(songs_features[id][5])+","
    +str(songs_features[id][6])+",")
    #chord_list = feature_list[7:len(feature_list)-1]
    song_chord_index = 0

    #write chords count for piece
    # for chord in unique_chords:
    #
    #     if(song_chord_index<len(chord_list)):
    #         #apply weights to chords
    #         chord_count = int(chord_list[song_chord_index])
    #         chord_count = chord_count/len(chord_list)
    #         f.write(str(chord_count))
    #         song_chord_index+=1
    #         f.write(",")
    #     else:
    #         f.write("0,")
    #         song_chord_index+=1

    #write grade for piece
    f.write(str(feature_list[len(feature_list)-1]))
    f.write("\n")
