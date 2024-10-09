# Project topic and plan:

## Working title: 
A sentiment analysis on attitudes toward Basque in bilingual Basque Parliament plenary sessions

## Summary: 
I am planning on conducting research using a dataset of Basque Parliament plenary sessions ranging from the years 2013 to 2022. I have previously conducted a statistical methods review on several articles on attitudes toward Basque, and would like to conduct some research myself using computational methods and sentiment analysis to assess attitudes toward Basque in a government setting. As Basque is a language whose use has been historically discouraged by the Spanish government, I am interested to see if these negative attitudes still exist. Having some prior experience in training models, I found this ML-oriented dataset to be decently approachable.

## Data and Analysis: 
The dataset I am planning on using can be found at https://huggingface.co/datasets/gttsehu/basque_parliament_1
Upon looking briefly at the test data, I noticed that it is organized by several variables, including language (Spanish, Basque, or bilingual), speaker id, PRR, length, and the actual segment itself. I hope to use sentiment analysis to compare language attitudes toward Basque across the Spanish segments, the Basque segments, and the bilingual segments. In terms of cleaning, one huge obstacle in the data is that there are no English translations, and I do not know any Basque. I will have to figure out a way to systematically translate this data. My hypothesis is that attitudes toward Basque will be most favorable in the Basque segments. Another issue is that there are over twice the number of hours (that have since been transcribed) of available data in Spanish as Basque. This shouldn't be a huge problem though, since the number of hours of data is 1018.6 for Spanish and 409.5 for Basque, which is more than sufficient for my topic. Though this dataset is designed for ML, I am not planning on using ML or predictive analysis. Perhaps sentiment analysis using keywords in the segments?

# Project plan (new additions):

## Research question:
How can language used in bilingual Basque Parliament plenary sessions (Spanish will be analyzed) demonstrate contemporary linguistic attitudes toward the Basque language?

## End goal of project:
The end goal of my project is to demonstrate that there is either a positive or negative bias in linguistic attitudes toward the Basque language. Due to a long history of negative attitudes toward the Basque language, I hope to discover if government sessions show that these negative attitudes still exist.

## Possible pitfalls:
- DATA: Upon looking through the data I began to notice a lack of discussion about the Basque language, which could potentially cause a huge issue in my analysis, and I may have to adjust my research question to better suit the dataset. I did notice, however, that there was discussion about improving the Basque country and helping the Basque people in different ways, so that could potentially point toward a different research question, though I am not sure if it would be 'linguistic' enough.
- ANNOTATION: Another issue that I am faced with is that I have not had experience with manually annotating sentiments. Which key words should I look for? Should I do this by hand or should I somehow create a model in R or Python? Even if I am able to successfully annotate the sentiments, how will I ensure that the sentiments are related to language attitudes?

## Step 1: Wrangling the data
- First, I will need to condense the dataset to sentences that include mentions of language. Since I am working with Spanish only, I am specifically looking for words like "idioma", "vasca", "vasco", "pais vasco", "lenguaje", "euskara", etc. I can perhaps use a filter function to filter only the results that contain these keywords.
- Next, I will need to combine sentences together. One small segment may not contain enough data to be properly labeled with one sentiment or another, so they must be combined. I plan to group segments that appear next to one another in the spoken audio file, as speakers often use several sentences to convey one sentiment and don't often switch back and forth rapidly between sentiments.
- Next, I will need to tag/annotate the sentences. I could do this with a simple binary tagging system, like "pos"/"neg" for positive or negative sentiments. I can either look for surrounding "positive" or "negative" words to help with the annotation, or I can rely on my own perception of the sentence, which may not be entirely reliable for 2 reasons: 1) I am not a native speaker of Spanish, and 2) This system is not controlled and could be influenced by many outside factors
- Next is the data analysis portion. I am planning on using the tidyverse package, and maybe readr to accomplish this, as I am working with text data.