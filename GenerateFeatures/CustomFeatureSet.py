from music21 import *
from collections import Counter
import re
from collections import OrderedDict
class CustomFeatures:


    def __init__(self):
        print(self," doesn't have any arguments")



    # def maxDensity(self,score):


    #advanced rhythmic similarity
    #how similar is each measure in comparison to entire piece
    #score1 is the score to search for(looking for these notes)
    #score2 is the score to search(looking at this corpus)
    def advancedRhythm2Similarity(self,score1,score2):
        similarity = 0
        aggregate_similarity = 0
        total_measures = 0
        if score1 is not None and score2 is not None:
            stream_segments1 = score1.getElementsByClass(stream.Part)
            stream_segments2 = score2.getElementsByClass(stream.Part)
            similar_measures = 0
            total_measures = len(stream_segments1[0])-1
            print("total measures: ",total_measures)
            i = 1
            while  i < len(stream_segments1[0]):
                stream_segment1 = stream_segments1[0][i]
                new_score = stream.Score()
                new_score.insert(0,stream_segment1)
                notes_and_rest_to_search = new_score.flat.notesAndRests.stream()
                j = 1
                while j<len(stream_segments1[0]):
                    measure_segment = stream_segments2[0][j]
                    segment_score = stream.Score()
                    segment_score.insert(0,measure_segment)
                    notes_and_rest_search = segment_score.flat.notesAndRests.stream()
                    a = 0
                    rhythm_match = True
                    #print(len(notes_and_rest_search), "  ",len(notes_and_rest_to_search))
                    if len(notes_and_rest_search)==len(notes_and_rest_to_search):
                        while a<len(notes_and_rest_to_search):
                            note_to_match = notes_and_rest_search[a]
                            curr_note = notes_and_rest_to_search[a]
                            if not(type(note_to_match)==type(curr_note) or ((type(note_to_match)==note.Note and type(curr_note)==chord.Chord)or(type(note_to_match)==chord.Chord and type(curr_note)==note.Note))):
                                rhythm_match = False
                            a+=1
                        if rhythm_match:
                            similar_measures+=1
                    j+=1
                i+=1
                #print("similar measures: ",similar_measures)
                avg_for_measure = similar_measures/total_measures
                aggregate_similarity+=avg_for_measure
                #print("avg ", avg_for_measure)
                similar_measures = 0
            similarity = aggregate_similarity/total_measures
        print("advanced similarity(2): ",similarity)

        return similarity


    #advanced rhythmic similarity
    #how similar is each measure in comparison to entire piece
    def advancedRhythmSimilarity(self,score):
        similarity = 0
        aggregate_similarity = 0
        total_measures = 0
        if score is not None:
            stream_segments = score.getElementsByClass(stream.Part)
            similar_measures = 0
            total_measures = len(stream_segments[0])-1
            print("total measures: ",total_measures)
            i = 1
            while  i < len(stream_segments[0]):
                stream_segment = stream_segments[0][i]
                new_score = stream.Score()
                new_score.insert(0,stream_segment)
                notes_and_rest_to_search = new_score.flat.notesAndRests.stream()
                j = 1
                while j<len(stream_segments[0]):
                    measure_segment = stream_segments[0][j]
                    segment_score = stream.Score()
                    segment_score.insert(0,measure_segment)
                    notes_and_rest_search = segment_score.flat.notesAndRests.stream()
                    a = 0
                    rhythm_match = True
                    #print(len(notes_and_rest_search), "  ",len(notes_and_rest_to_search))
                    if len(notes_and_rest_search)==len(notes_and_rest_to_search):
                        while a<len(notes_and_rest_to_search):
                            note_to_match = notes_and_rest_search[a]
                            curr_note = notes_and_rest_to_search[a]
                            if not(type(note_to_match)==type(curr_note) or ((type(note_to_match)==note.Note and type(curr_note)==chord.Chord)or(type(note_to_match)==chord.Chord and type(curr_note)==note.Note))):
                                rhythm_match = False
                            a+=1
                        if rhythm_match:
                            similar_measures+=1
                    j+=1
                i+=1
                #print("similar measures: ",similar_measures)
                avg_for_measure = similar_measures/total_measures
                aggregate_similarity+=avg_for_measure
                #print("avg ", avg_for_measure)
                similar_measures = 0
            similarity = aggregate_similarity/total_measures
        print("advanced similarity: ",similarity)

        return similarity


    #similarity of rythm
    def rhythmSimilarity(self,score1,score2):
        similarity = 0
        if score1 is not None and score2 is not None:
            score1.getElementsByClass(stream.Part)[0][0:5]
            try:
                l = search.approximateNoteSearchOnlyRhythm(score1,score2)
                similarity = l[0].matchProbability
            except:
                print("error when getting rhythm similairty")
        print("similarity: ",similarity)
        return similarity
    #similarity between two scores
    def similarityBetween1Score(self,score,file):
        total_similarity = 0
        avg_similarity = 0
        if score is not None:
            scoreDict = OrderedDict()
            scoreList = search.segment.indexScoreParts(score)
            scoreDict["1 "+file] = scoreList
            scoreDict["2 "+file] = scoreList
            scoreSim = search.segment.scoreSimilarity(scoreDict,minimumLength=5,includeReverse=False)
            total_segments = len(scoreSim)
            count = 0
            for result in scoreSim:
                similarity = float(result[len(result)-1])
                total_similarity+=similarity
            try:
                avg_similarity = total_similarity/total_segments
            except:
                print("cannot divide by 0 error(similarityBetween1Score)")
                return -1

        print("similarityBetween1Score: ",avg_similarity)
        return avg_similarity

    #similarity between two scores
    def similarityBetween2Score(self,score1,score2,file):
        total_similarity = 0
        avg_similarity = 0
        scoreDict = OrderedDict()
        if score1 is not None and score2 is not None:
            scoreList1 = search.segment.indexScoreParts(score1)
            scoreList2 = search.segment.indexScoreParts(score2)
            scoreDict["1 "+file] = scoreList1
            scoreDict["2 "+file] = scoreList2
            scoreSim = search.segment.scoreSimilarity(scoreDict,minimumLength=5,includeReverse=False)

            total_segments = len(scoreSim)
            count = 0
            for result in scoreSim:
                similarity = float(result[len(result)-1])
                total_similarity+=similarity
            try:
                avg_similarity = total_similarity/total_segments
            except:
                print("cannot divide by 0 error(similarityBetween2Score)")
                return -1

            print("similarityBetween2Score: ",avg_similarity)
        return avg_similarity

    #total x chord notes
    def totalXChordNotes(self,chords,number_of_notes):
        total = 0
        if chords is not None:
            for chord in chords:
                #print("length of chord: ",len(chord))
                if len(chord)==number_of_notes:
                    total+=1
        print("total",number_of_notes,"ChordNotes: ",total,"\n")
        return total

    #average x chord notes
    def averageXChordNotes(self,chords,number_of_notes):
        average = 0
        if chords is not None:
            total_x_chord_notes = float(self.totalXChordNotes(chords,number_of_notes))
            total = float(len(chords))
            average = total_x_chord_notes/total
        print("average",number_of_notes,"ChordNotes: ",average)
        return average

    #average range of top x percent of notes
    #tested
    def averageRange2OfTopXPercent(self,stream,percent):
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
            top_x_note_objects = self.return_x_top_notes(top_x_tuple,notes_array,number_of_notes_to_get)
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
                            aInterval = int(re.search(r'\d+', aInterval.name).group())
                            range = int(aInterval)
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
    def rangeOfTopXPercent(self,stream,percent):
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
            top_x_note_objects = self.return_x_top_notes(top_x_tuple,notes_array,number_of_notes_to_get)
            if len(top_x_note_objects)>1:
                #print("top x notes: ",top_x_note_objects)
                # for note in top_x_note_objects:
                #     print(note.fullName,end=" ")
                #get lowest and highest notes
                lowest_note = self.getLowestNote(top_x_note_objects)
                highest_note = self.getHighestNote(top_x_note_objects)
                #interval between both notes
                aInterval = interval.Interval(noteStart=lowest_note,noteEnd=highest_note)
                aInterval = int(re.search(r'\d+', aInterval.name).group())
                range = int(aInterval)
                #print("range: ",range)
            else:
                range = 0
        print('rangeOfTopXPercent: ',range)
        return range


    #takes in a tuple with names of top notes and returns the top notes as objects
    def return_x_top_notes(self,top_x_tuple,notes_array,numberOfNotes):
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
    def getLowestNote(self,notes):
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
    def getHighestNote(self,notes):
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
    def averageLargeJumps(self,chords,largeJump):
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
                aInterval = int(re.search(r'\d+', aInterval.name).group())
                if(int(aInterval)>=largeJump):
                    totalLargeJumps+=1
                    total += int(aInterval)
                    #print(aInterval.name)
                i+=1
            #print ("total large jumps: ",totalLargeJumps)
            if totalLargeJumps>0:
                average = total/totalLargeJumps
        print("averageLargeJumps: ",average)
        return average


    #average largeJumps
    #return the number of large jumps>=largeJump
    def largeJumps(self,chords,largeJump):
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
                aInterval = int(re.search(r'\d+', aInterval.name).group())
                if(int(aInterval)>=largeJump):
                    #print(chords[i],"   ",chords[i+1])
                    totalLargeJumps+=1
                    #print(aInterval.name)
                i+=1
        print ('largeJumps: ',totalLargeJumps)
        return totalLargeJumps

    #average range of played ntoes
    #range from A3 to B3C4 is the interval from A3 to C4
    #new
    def averageRangeForNextNotes(self,chords):
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

                total+=int(re.search(r'\d+', aInterval.name).group())
                #int(aInterval.name[1:])
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
    def averageChordRangeForHand(self,chords,chord_length):
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
                        aInterval = int(re.search(r'\d+', aInterval.name).group())
                        total+=int(aInterval)
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
    def average2ChordRangeForHand(self,chords,chord_length):
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

    def averageWholeNotes(self,given_stream):
        average = 0
        if given_stream is not None:
            notes = given_stream.flat.getElementsByClass("Note")
            totalNotes = len(notes)
            if totalNotes>0:
                average = self.totalWholeNotes(given_stream)/totalNotes
        return average

    def averageHalfNotes(self,given_stream):
        average = 0
        if given_stream is not None:
            notes = given_stream.flat.getElementsByClass("Note")
            totalNotes = len(notes)
            if totalNotes>0:
                average = self.totalHalfNotes(given_stream)/totalNotes
        return average

    def averageQuarterNotes(self,given_stream):
        average = 0
        if given_stream is not None:
            notes = given_stream.flat.getElementsByClass("Note")
            totalNotes = len(notes)
            if totalNotes>0:
                average = self.totalQuarterNotes(given_stream)/totalNotes
        return average

    def averageEighthNotes(self,given_stream):
        average = 0
        if given_stream is not None:
            notes = given_stream.flat.getElementsByClass("Note")
            totalNotes = len(notes)
            if totalNotes>0:
                average = self.totalEighthNotes(given_stream)/totalNotes
        return average

    def average16thNotes(self,given_stream):
        average = 0
        if given_stream is not None:
            notes = given_stream.flat.getElementsByClass("Note")
            totalNotes = len(notes)
            if totalNotes>0:
                average = self.total16thNotes(given_stream)/totalNotes
        return average

    def average32ndNotes(self,given_stream):
        average = 0
        if given_stream is not None:
            notes = given_stream.flat.getElementsByClass("Note")
            totalNotes = len(notes)
            if totalNotes>0:
                average = self.total32ndNotes(given_stream)/totalNotes
        return average

    def average64thNotes(self,given_stream):
        average = 0
        if given_stream is not None:
            notes = given_stream.flat.getElementsByClass("Note")
            totalNotes = len(notes)
            if totalNotes>0:
                average = self.total64thNotes(given_stream)/totalNotes
        return average

    def totalWholeNotes(self,given_stream):
        total = 0
        if given_stream is not None:
            notes = given_stream.flat.getElementsByClass("Note")
            for note in notes:
                if note.quarterLength==4:
                    total+=1
        #print(total)
        return total

    def totalHalfNotes(self,given_stream):
        total = 0
        if given_stream is not None:
            notes = given_stream.flat.getElementsByClass("Note")
            for note in notes:
                if note.quarterLength==2:
                    total+=1
        #print(total)
        return total

    def totalQuarterNotes(self,given_stream):
        total = 0
        if given_stream is not None:
            notes = given_stream.flat.getElementsByClass("Note")
            for note in notes:
                if note.quarterLength==1:
                    total+=1
        #print(total)
        return total

    def totalEighthNotes(self,given_stream):
        total = 0
        if given_stream is not None:
            notes = given_stream.flat.getElementsByClass("Note")
            for note in notes:
                if note.quarterLength==.5:
                    total+=1
        #print(total)
        return total

    def total16thNotes(self,given_stream):
        total = 0
        if given_stream is not None:
            notes = given_stream.flat.getElementsByClass("Note")
            for note in notes:
                if note.quarterLength==.25:
                    total+=1
        #print(total)
        return total

    def total32ndNotes(self,given_stream):
        total = 0
        if given_stream is not None:
            notes = given_stream.flat.getElementsByClass("Note")
            for note in notes:
                if note.quarterLength==.125:
                    total+=1
        #print(total)
        return total

    def total64thNotes(self,given_stream):
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
    def totalNotes(self,given_stream):
        if(given_stream.getElementsByClass("Note") is not None):
            return len(given_stream.getElementsByClass("Note"))
        else:
            return 0
    #total sharp notes in the entire piece
    #total sharp notes in right hand
    #total sharp notes in left hand
    def totalSharpNotes(self,given_stream):
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
    def totalFlatNotes(self,given_stream):
        totalFlatNotes = 0
        if given_stream is not None:
            notes = given_stream.flat.getElementsByClass("Note")
            for note in notes:
                if '-' in note.name:
                    totalFlatNotes+=1
                    #print(note.name)
        return totalFlatNotes

    def totalNaturalNotes(self,given_stream):
        totalNaturalNotes = 0
        if given_stream is not None:
            notes = given_stream.flat.getElementsByClass("Note")
            for note in notes:
                if '-' not in note.name and '#' not in note.name:
                    totalNaturalNotes+=1

        return totalNaturalNotes
