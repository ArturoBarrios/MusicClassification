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
for root, dirs, song_files in os.walk("./Midi_Files/AmbroseTabsDatabase/AmbrosePianoTabsNoFilter/"):
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
        filename = "./Midi_Files/AmbroseTabsDatabase/AmbrosePianoTabsNoFilter/"+str(filename)
        files[filename] = num

#index used in iris file
index = 1

#assign grade and features to ds
ds = features.DataSet(classLabel='Grade')

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

ds.addFeatureExtractors(fes)

for file in files:
    print(file)

    #parse file
    b1 = converter.parse(str(file))
    #add parsed file, grade, and id
    ds.addData(b1, classValue=files[str(file)], id=str(file))
    index+=1
print("feature extractor added")
ds.process()
print("music processed...Now adding features")
#write id,features,grade in first line of iris files
#f = open("music_IrisWCG3.csv","w")
#labels_file = open("music_featuresWCG3.txt","w")
f = open("temp.csv","w")
labels_file = open("temp.txt","w")

i = 0
#write attribute labels in .txt and .csv files
features = ds.getAttributeLabels()[1:]
print("features: ",features)
for feature in features:
    if(i<(len(features)-1)):
        labels_file.write(feature+",")
        f.write(feature+",")
    else:
        f.write(feature+"\n")
    i+=1


songs_values = ds.getFeaturesAsList()
print("feature labels added...now adding feature values")
#iterate through every song and write its feature values

for song_values in songs_values:
    i = 0
    for value in song_values[1:]:
        if i<(len(song_values)-2):
            f.write(str(value)+",")
        else:
            f.write(str(value)+"\n")
        i+=1
print("feature values added")
