#importing dependencies
import pandas as pd
import csv

#dependencies that might be necessary later
import nltk
import numpy
import matplotlib

#one approach is to read and interpret as .csv
basSpanPar = pd.read_csv('BasSpanPar.tsv', sep='\t')

#other approach is to make the file into a list (best approach)*
corpusList = []
with open('BasSpanPar.tsv') as c:
    for line in c:
        a = line.split('\t')
        corpusList.append(a)

#trying some things out: just sentences
justSents = []
for line in corpusList:
    sent = line[5]
    justSents.append(sent)
justSents[:10]

#sentence is the 5th item in list, using list comprehension to find sents w/ keyword 'hablante'
hablanteLines = [line for line in corpusList if 'hablante' in line[5]]
hablanteLines[:10]

#that works, so I made a list of keywords:
keywords = ['hablante', 'euskera', 'lenguaje', 'idioma', 'aprendizaje', 'lingüístico', 'lingüística']

#and made a list of only the lines that contain the keywords:
keywordsLines = []
for line in corpusList:
    for word in keywords:
        if word in line[5] and word in keywords:
            keywordsLines.append(line)

#export to .csv
fields = ['path', 'language', 'speaker_id', 'PRR', 'length', 'sentence']
with open('BS_RelData.csv', 'w') as f:
    write = csv.writer(f)
    write.writerow(fields)
    write.writerows(keywordsLines)
            
#References:
#https://www.geeksforgeeks.org/simple-ways-to-read-tsv-files-in-python/
#https://www.geeksforgeeks.org/python-save-list-to-csv/
