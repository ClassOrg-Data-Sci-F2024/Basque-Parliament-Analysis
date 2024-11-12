# Progress report 0 (10/7): 
- Added project_plan file: research question, end goal, possible pitfalls, various steps
- Began progress report
- Dataset confirmed

# Progress report 1 (10/28):

NOTE: The dataset I am using for this project is named basque_parliament_1 and was found on https://huggingface.co. The original project was funded by the Spanish Ministry of Science and Innovation, and is licensed as cc0-1.0.

Citation:
@misc {software_technologies_working_group_2024,
	author       = { {Software Technologies Working Group} },
	title        = { basque_parliament_1 (Revision a2fbcaf) },
	year         = 2024,
	url          = { https://huggingface.co/datasets/gttsehu/basque_parliament_1 },
	doi          = { 10.57967/hf/2485 },
	publisher    = { Hugging Face }
}

## Step 1: Filtering relevant rows using keywords (performed in Python)

The script that I wrote and implemented is available here: [Filtering Through Keywords](BasqueSpanishPar.py). It is included in the commit for the second progress report but may be deleted upon final submission. Specifically, this program looked for utterances that contained any of the following keywords: 

['hablante', 'euskera', 'lenguaje', 'idioma', 'aprendizaje', 'lingüístico', 'lingüística']

These keywords were chosen because they demonstrate relevance to the topics of language, Basque, speakers, linguistics, etc. and, at a greater level, my ultimate research question. The script itself contains comments and can be changed if needed to encompass even more keywords.

## Step 2: Data Wrangling in R

I luckily began with very high quality, tidy data. The most difficult part of the process was filtering the dataset so that only rows containing relevant sentences were shown. As I was working with a massive dataset of thousands of rows, I needed to narrow it down to a row quantity that I could manage manually annotating. I decided on 200 rows (method: used slice() function to isolate the first 200 rows).

Next, I needed to filter out rows that contained utterances that were either bilingual or Basque-only, which I accomplished using the filter() function. 190 rows remained.

Finally, I needed to remove columns that are *definitely* irrelevant to my analysis. There was only one column of that type, which was the 'path' column.

## Next steps:

Next, I will need to annotate my data and perform statistical analyses.

# Progress report 2 (11/11)

For this report, I decided on an annotation scheme. I decided to use the Spanish Emotion Lexicon by Dr. Grigori Sidorov. This lexicon is made up of 2,036 different words. Each word is associated with at least one of the following emotions: "joy, anger, fear, sadness, surprise, and disgust" to a degree that is measured by the Probability Factor of Affective use (PFA). This lexicon was annotated by 19 human annotators.

The raw SEL lexicon is available [here](SEL.xlsx).

The following article contains more information about the lexicon:

Grigori Sidorov, Sabino Miranda-Jiménez, Francisco Viveros-Jiménez, Alexander Gelbukh, Noé Castro-Sánchez, Francisco Velásquez, Ismael Díaz-Rangel, Sergio Suárez-Guerra, Alejandro Treviño, and Juan Gordon. Empirical Study of Opinion Mining in Spanish Tweets. LNAI 7629, 2012, pp. 1-14.

My plan for the usage of this lexicon is to apply the lexicon to every phrase in the 'sentence' column and produce a new column that, for each row, provides emotion categories as well as their PFAs.

The following markdown document published by Kayleah Griffen will be especially helpful in actually implementing this lexicon into my existing data:

https://rpubs.com/klgriffen96/data607_hw10

Next, I chose a license. Based on the fact that my original dataset was licensed as cc0-1.0, I decided to choose the same license. Additionally, the license agreement for the SEL is as follows:

"
1.    You can use all these programs freely for academic purposes. No                warranty.
2.    You should cite the corresponding papers in your publications obtained         with the help of these programs.
3.    If you plan to use the download in a commercial application, please,           contact me.
4.    Downloading means that you accept the license. Thank you.
"

For this reason, I am including both the SEL raw data and the SEL published paper citation in my repository and in this progress report, respectively.
