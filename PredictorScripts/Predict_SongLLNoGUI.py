# Library imports
from tkinter import filedialog
from tkinter import *

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
#########################################################################Add features of unknown files
#assign grade and features to ds
ds = features.DataSet(classLabel='Name')

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

for root, dirs, song_files in os.walk("./Midi_Files/Unknown_Songs"):
    for file in song_files:
        print("file: ",file)
        #parse file
        b1 = converter.parse("./Midi_Files/Unknown_Songs/"+str(file))
        #add parsed file, grade, and id
        ds.addData(b1,classValue=str(file),id=str(file))
    print("feature extractor added")
    ds.process()
    print("music processed...Now adding features")

f = open("./IrisTextFiles/temp.csv","w")
i = 0
#write attribute labels in csv file
features = ds.getAttributeLabels()[1:]
print("features: ",features)
for feature in features:
    if(i<(len(features)-1)):
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

f.flush()
f.seek(0)
###################################################################predict values of unknown features
data = pd.read_csv("./IrisTextFiles/temp.csv")
labels=data['Name']
X = data.drop(['Name'],axis=1)
filename = "./ClassificationModels/GBRLowLevelFeaturesAll1.sav"
loaded_model = joblib.load(filename)

#print predictions
predictions = loaded_model.predict(X)
i = 0
for grade in predictions:
    print(labels[i],":",grade)
    i+=1
