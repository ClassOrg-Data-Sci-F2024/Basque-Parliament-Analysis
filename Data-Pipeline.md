Data-Pipeline
================
Claire McLean
2024-10-28

NOTE: The dataset I am using for this project is named
basque_parliament_1 and was found on <https://huggingface.co>. The
original project was funded by the Spanish Ministry of Science and
Innovation, and is licensed as cc0-1.0. Citation: @misc
{software_technologies_working_group_2024, author = { {Software
Technologies Working Group} }, title = { basque_parliament_1 (Revision
a2fbcaf) }, year = 2024, url = {
<https://huggingface.co/datasets/gttsehu/basque_parliament_1> }, doi = {
10.57967/hf/2485 }, publisher = { Hugging Face } }

# Data Pipeline

## Step 1: Importing major dependencies

First, import dependencies:

``` r
library("tidyverse")
```

    ## ── Attaching core tidyverse packages ──────────────────────── tidyverse 2.0.0 ──
    ## ✔ dplyr     1.1.4     ✔ readr     2.1.5
    ## ✔ forcats   1.0.0     ✔ stringr   1.5.1
    ## ✔ ggplot2   3.5.1     ✔ tibble    3.2.1
    ## ✔ lubridate 1.9.3     ✔ tidyr     1.3.1
    ## ✔ purrr     1.0.2     
    ## ── Conflicts ────────────────────────────────────────── tidyverse_conflicts() ──
    ## ✖ dplyr::filter() masks stats::filter()
    ## ✖ dplyr::lag()    masks stats::lag()
    ## ℹ Use the conflicted package (<http://conflicted.r-lib.org/>) to force all conflicts to become errors

``` r
library("readr")
library("tidytext")
library("dplyr")
```

## Step 2: The following code chunks are the pipeline I followed to split the data into two smaller dataframes. This pipeline can be ignored.

Read in the .tsv file:

``` r
#raw_data <- read_tsv("train.tsv")
#raw_data
```

Finding number of total rows in the raw data:

``` r
#row_count <- nrow(raw_data)
#row_count
```

Now, breaking up the dataset into two separate parts so that it is
possible to push to GitHub (100MB maximum):

``` r
#row_split1 <- (nrow(raw_data)/2) %>% round(digits = 0)
#row_split2 <- row_split1+1
#raw_data1 <- raw_data %>%
  #slice(1:row_split)
#raw_data2 <- raw_data %>%
  #slice(row_split2:row_count)
```

Exporting the two above datasets into .csv files:

``` r
#write_csv(raw_data1, "raw_data1.csv")
#write_csv(raw_data2, "raw_data2.csv")
```

## Step 3: Uploading raw .csv files:

``` r
raw_data1 <- read_csv("raw_data1.csv")
```

    ## Rows: 374972 Columns: 6
    ## ── Column specification ────────────────────────────────────────────────────────
    ## Delimiter: ","
    ## chr (3): path, language, sentence
    ## dbl (3): speaker_id, PRR, length
    ## 
    ## ℹ Use `spec()` to retrieve the full column specification for this data.
    ## ℹ Specify the column types or set `show_col_types = FALSE` to quiet this message.

``` r
raw_data2 <- read_csv("raw_data2.csv")
```

    ## Rows: 374973 Columns: 6
    ## ── Column specification ────────────────────────────────────────────────────────
    ## Delimiter: ","
    ## chr (3): path, language, sentence
    ## dbl (3): speaker_id, PRR, length
    ## 
    ## ℹ Use `spec()` to retrieve the full column specification for this data.
    ## ℹ Specify the column types or set `show_col_types = FALSE` to quiet this message.

Combining the two dataframes using rbind():

``` r
raw_data <- rbind(raw_data1, raw_data2)
```

Viewing new, combined dataframe:

``` r
nrow(raw_data)
```

    ## [1] 749945

``` r
ncol(raw_data)
```

    ## [1] 6

Starting with 749,945 rows/utterances

## Step 4: Data Cleaning

Now, filtering to only include rows that are Spanish utterances (exclude
Basque and bilingual):

``` r
small_data_span <- raw_data %>% filter(language == "es")
nrow(small_data_span)
```

    ## [1] 524942

Now 524,942 rows/utterances (lost 225,021)

Using stringr to identify utterances/sentences that contain the
following keywords. \[‘hablante’, ‘euskera’, ‘lenguaje’, ‘idioma’,
‘lingüístic’\]. This will allow me to perform sentiment analysis only on
the utterances that are related in some way to language. Specifically,
using str_detect() will allow me to identify occurrences of both
‘hablante/es’, ‘lenguaje/es’, ‘lingüística/o/as/os’. Further, I created
another vector that is used to detect occurrences of \[‘castellan’,
‘galleg’\], which detects both ‘castellano/a’ and ‘gallego/a’.

``` r
keywords_vec <- ('hablante|euskera|lenguaje|idioma|lingüístic')
keywords_vec1 <- ('castellan|galleg')
keywords_col <- small_data_span$sentence %>%
  str_detect(keywords_vec)

keywords_col2 <- small_data_span$sentence %>% 
  str_detect(keywords_vec1)

small_data_span2 <- small_data_span %>%
  mutate(keywords = keywords_col) %>% 
  mutate(non_keywords = keywords_col2)

small_data_span3 <- small_data_span2 %>%
  filter(keywords == TRUE) %>% 
  filter(non_keywords == FALSE)

nrow(small_data_span3)
```

    ## [1] 3209

Now 3209 rows (lost 521,715 rows)

Changing name of dataframe:

``` r
sampled_data <- small_data_span3
```

## Some basic stats of cleaned Parliament data:

``` r
#number of rows:
nrow(sampled_data)
```

    ## [1] 3209

``` r
#number of columns:
ncol(sampled_data)
```

    ## [1] 8

``` r
#average utterance length
mean(sampled_data$length)
```

    ## [1] 7.644313

``` r
#number of unique speakers
n_distinct(sampled_data$speaker_id)
```

    ## [1] 127

## Step 5: Wrangling SEL lexicon

Load dependencies:

``` r
library("readxl")
library("readr")
```

Reading in Spanish Emotion Lexicon file:

``` r
sel <- read_excel("SEL.xlsx")
nrow(sel)
```

    ## [1] 2036

Starting with 2,036 emotion words in the SEL.

Viewed final plots and assessed which words carried less emotional
‘weight’. Removed these words from the dataframe as they do not
contribute much to the analysis. Additionally, created word stemmer to
isolate emotion words without gender suffix, as all gendered words in
the dataset are masculine:

``` r
library("SnowballC")

low_ew_vec <- ('cuent|solo|sola|llev|lleg|sab|dec|dich|ped|mano')
low_ew <- sel$Palabra %>% 
  str_detect(low_ew_vec)
low_ew2 <- sel %>% 
  mutate('LowEmotion' = low_ew)
sel2 <- sel %>% 
  filter(low_ew == FALSE)

stemmed_sel <- wordStem(sel2$Palabra, language = "spanish")
stemmed_sel <- sel2 %>% 
  mutate(Stems = stemmed_sel) %>% select('#', Stems, PFA, Categoría, -Palabra)
nrow(stemmed_sel)
```

    ## [1] 1988

``` r
#If stem occurs multiple times in same emotion, delete duplicates. If stem occurs multiple times across different emotions, keep duplicates:
stemmed_sel <- stemmed_sel %>% group_by(Categoría) %>% 
  distinct(Stems, .keep_all = TRUE)
nrow(stemmed_sel)
```

    ## [1] 1548

Now, 1,548 tokens in SEL (deleted all occurrences of words with low
emotional weight, and all duplicates of stems that occurred within the
same emotion)

Finding number of emotion words per emotion:

``` r
happiness <- stemmed_sel %>% 
  filter(Categoría=='Alegría') %>% 
  nrow()
anger <- stemmed_sel %>% 
  filter(Categoría=='Enojo') %>% 
  nrow()
fear <- stemmed_sel %>% 
  filter(Categoría=='Miedo') %>% 
  nrow()
disgust <- stemmed_sel %>% 
  filter(Categoría=='Repulsión') %>% 
  nrow()
surprise <- stemmed_sel %>% 
  filter(Categoría=='Sorpresa') %>% 
  nrow()
sadness <- stemmed_sel %>% 
  filter(Categoría=='Tristeza') %>% 
  nrow()

sel_distribution <- stemmed_sel %>%
  group_by(Categoría) %>% 
  mutate(Freq=n()) %>%
  select(Categoría, Freq) %>% 
  distinct()
sel_distribution
```

    ## # A tibble: 6 × 2
    ## # Groups:   Categoría [6]
    ##   Categoría  Freq
    ##   <chr>     <int>
    ## 1 Alegría     511
    ## 2 Enojo       289
    ## 3 Miedo       161
    ## 4 Repulsión   166
    ## 5 Sorpresa    128
    ## 6 Tristeza    293

## Step 6: Tokenizing and stemming Parliament sentence data

Tokenizing sentences (ngrams):

``` r
library(dplyr)
library(tidytext)

sampled_data_ngrams <- sampled_data %>%
  unnest_tokens(tokens, sentence, token="words", drop=FALSE, to_lower=TRUE)
```

Stemming sentence tokens (ngrams):

``` r
token_stems <- wordStem(sampled_data_ngrams$tokens, language = "spanish")
stemmed_ngrams <- sampled_data_ngrams %>% 
  mutate(Stems = token_stems)
nrow(stemmed_ngrams)
```

    ## [1] 66078

66,078 stems total (before inner-joining with SEL)

## Step 7: Merging Parliament data and SEL data

The following two code chunks were inspired by a project by Kayleah
Griffen, which can be found at the following site:
<https://rpubs.com/klgriffen96/data607_hw10>

Does word correspond to a particular emotion?

``` r
merged_data <- stemmed_ngrams %>% 
  inner_join(stemmed_sel, by="Stems", multiple = "all", unmatched = "drop", relationship = "many-to-many")

nrow(merged_data)
```

    ## [1] 2422

2422 stems after inner-joining with SEL (stems that did not have matches
in the SEL were dropped)

Grouping by sentence/utterance:

``` r
merged_data2 <- merged_data %>% 
  arrange(speaker_id, group_by=TRUE)
```

Creating wordclouds for each sentiment:

``` r
library(wordcloud)
```

    ## Loading required package: RColorBrewer

``` r
library(RColorBrewer)
library(wordcloud2)

#Ungrouping to create wordclouds
merged_data3 <- merged_data %>% 
  ungroup()
```

Below, I am grouping each emotion and its corresponding tokens into an
object. In addition to grouping them, I also deleted duplicate stems
that would otherwise present problems in my analysis and kept only the
columns that prove to be necessary in plotting the data. I want to avoid
certain tokens being plotted multiple times if they are part of the same
word in the same utterance.

``` r
anger_words <- merged_data3 %>% 
  filter(Categoría=="Enojo") %>% 
  group_by(Stems) %>% 
  mutate(Freq = n()) %>% 
  ungroup() %>% 
  select(Stems, Freq, Categoría) %>% 
  distinct(Stems, .keep_all = TRUE)

happiness_words <- merged_data3 %>% 
  filter(Categoría=="Alegría") %>% 
  group_by(Stems) %>% 
  mutate(Freq = n()) %>% 
  ungroup() %>% 
  select(Stems, Freq, Categoría) %>% 
  distinct(Stems, .keep_all = TRUE)

sadness_words <- merged_data3 %>% 
  filter(Categoría=="Tristeza") %>% 
  group_by(Stems) %>% 
  mutate(Freq = n()) %>% 
  ungroup() %>% 
  select(Stems, Freq, Categoría) %>% 
  distinct(Stems, .keep_all = TRUE)

surprise_words <- merged_data3 %>% 
  filter(Categoría=="Sorpresa") %>% 
  group_by(Stems) %>% 
  mutate(Freq = n()) %>% 
  ungroup() %>% 
  select(Stems, Freq, Categoría) %>% 
  distinct(Stems, .keep_all = TRUE)

disgust_words <- merged_data3 %>% 
  filter(Categoría=="Repulsión") %>% 
  group_by(Stems) %>% 
  mutate(Freq = n()) %>% 
  ungroup() %>% 
  select(Stems, Freq, Categoría) %>% 
  distinct(Stems, .keep_all = TRUE)

fear_words <- merged_data3 %>% 
  filter(Categoría=="Miedo") %>% 
  group_by(Stems) %>% 
  mutate(Freq = n()) %>% 
  ungroup() %>% 
  select(Stems, Freq, Categoría) %>% 
  distinct(Stems, .keep_all = TRUE)
```

## Step 8: Plotting Parliament sentence data

Generating wordclouds for each sentiment:

``` r
#anger
set.seed(10)
wordcloud(words = anger_words$Stems, freq = anger_words$Freq, min.freq = 1,
          max.words=200, random.order=FALSE, rot.per=0.5, scale=c(3.5, 0.3),
          colors=brewer.pal(8, "Set1"))
```

![](Data-Pipeline_files/figure-gfm/unnamed-chunk-23-1.png)<!-- -->

``` r
#happiness
set.seed(10)
wordcloud(words = happiness_words$Stems, freq = happiness_words$Freq, min.freq = 1,
          max.words=200, random.order=FALSE, rot.per=0.5, scale=c(2.5, 0.3),
          colors=brewer.pal(8, "Set1"))
```

![](Data-Pipeline_files/figure-gfm/unnamed-chunk-23-2.png)<!-- -->

``` r
#sadness
set.seed(10)
wordcloud(words = sadness_words$Stems, freq = sadness_words$Freq, min.freq = 1,
          max.words=200, random.order=FALSE, rot.per=0.5, scale=c(3.5, 0.3),
          colors=brewer.pal(8, "Set1"))
```

![](Data-Pipeline_files/figure-gfm/unnamed-chunk-23-3.png)<!-- -->

``` r
#surprise
set.seed(10)
wordcloud(words = surprise_words$Stems, freq = surprise_words$Freq, min.freq = 1,
          max.words=200, random.order=FALSE, rot.per=0.5, scale=c(2, 0.3),
          colors=brewer.pal(8, "Set1"))
```

![](Data-Pipeline_files/figure-gfm/unnamed-chunk-23-4.png)<!-- -->

``` r
#disgust
set.seed(10)
wordcloud(words = disgust_words$Stems, freq = disgust_words$Freq, min.freq = 1,
          max.words=200, random.order=FALSE, rot.per=0.5, scale=c(3.5, 0.3),
          colors=brewer.pal(8, "Set1"))
```

![](Data-Pipeline_files/figure-gfm/unnamed-chunk-23-5.png)<!-- -->

``` r
#fear
set.seed(8)
wordcloud(words = fear_words$Stems, freq = fear_words$Freq, min.freq = 1,
          max.words=200, random.order=FALSE, rot.per=0.5, scale=c(3.5, 0.3),
          colors=brewer.pal(8, "Set1"))
```

![](Data-Pipeline_files/figure-gfm/unnamed-chunk-23-6.png)<!-- -->

Generating bar charts for each sentiment:

``` r
library(ggplot2)

anger_words2 <- anger_words %>% 
  filter(Freq > 1)
anger_plot <- ggplot(anger_words2, aes(Stems, Freq)) + 
  geom_bar(stat = 'identity', fill="red3", width = 0.5) +
  scale_x_discrete(guide = guide_axis(n.dodge=3)) +
  labs(title = 'Anger Word Frequency (n>1)')
anger_plot
```

![](Data-Pipeline_files/figure-gfm/unnamed-chunk-24-1.png)<!-- -->

``` r
happiness_words2 <- happiness_words %>% 
  filter(Freq > 10)
happiness_plot2 <- ggplot(happiness_words2, aes(Stems, Freq)) + 
  geom_bar(stat = 'identity', fill="gold1", width = 0.5) +
  scale_x_discrete(guide = guide_axis(n.dodge=3)) +
  labs(title = 'Happiness Word Frequency (n>10)')
happiness_plot2
```

![](Data-Pipeline_files/figure-gfm/unnamed-chunk-24-2.png)<!-- -->

``` r
sadness_words2 <- sadness_words %>% 
  filter(Freq > 5)
sadness_plot <- ggplot(sadness_words2, aes(Stems, Freq)) + 
  geom_bar(stat = 'identity', fill="blue4", width = 0.5) +
  scale_x_discrete(guide = guide_axis(n.dodge=3)) +
  labs(title = 'Sadness Word Frequency (n>5)')
sadness_plot
```

![](Data-Pipeline_files/figure-gfm/unnamed-chunk-24-3.png)<!-- -->

``` r
surprise_plot <- ggplot(surprise_words, aes(Stems, Freq)) + 
  geom_bar(stat = 'identity', fill="mediumspringgreen", width = 0.5) +
  scale_x_discrete(guide = guide_axis(n.dodge=3)) +
  labs(title = 'Surprise Word Frequency')
surprise_plot
```

![](Data-Pipeline_files/figure-gfm/unnamed-chunk-24-4.png)<!-- -->

``` r
disgust_plot <- ggplot(disgust_words, aes(Stems, Freq)) + 
  geom_bar(stat = 'identity', fill="olivedrab1", width = 0.5) +
  scale_x_discrete(guide = guide_axis(n.dodge=3)) +
  labs(title = 'Disgust Word Frequency')
disgust_plot
```

![](Data-Pipeline_files/figure-gfm/unnamed-chunk-24-5.png)<!-- -->

``` r
fear_plot <- ggplot(fear_words, aes(Stems, Freq)) + 
  geom_bar(stat = 'identity', fill="darkorange", width = 0.5) +
  scale_x_discrete(guide = guide_axis(n.dodge=3)) +
  labs(title = 'Fear Word Frequency')
fear_plot
```

![](Data-Pipeline_files/figure-gfm/unnamed-chunk-24-6.png)<!-- -->

Finding general sentiment for each speaker:

``` r
by_speaker <- merged_data3 %>% 
  count(speaker_id, Categoría, sort=TRUE) %>%
  filter(n == max(n), .by=speaker_id)

#Number of distinct speakers
by_speaker %>% distinct(speaker_id) %>% nrow()
```

    ## [1] 111

Plotting composition of general sentiments across speakers:

``` r
#Out of 128 general sentiments across all speakers, find sentiment distribution
#Each square represents each speaker (111 speakers total, some speakers have more than one square)
#Picture plot as a parliament session, each member represented by one square
library(waffle)

comp_waffle <- by_speaker %>%
  group_by(Categoría) %>% 
  mutate(Freq=n()) %>%
  select(Categoría, Freq) %>% 
  distinct()
comp_waffle
```

    ## # A tibble: 6 × 2
    ## # Groups:   Categoría [6]
    ##   Categoría  Freq
    ##   <chr>     <int>
    ## 1 Alegría      98
    ## 2 Tristeza     16
    ## 3 Enojo         5
    ## 4 Miedo         3
    ## 5 Sorpresa      4
    ## 6 Repulsión     2

``` r
waffle(comp_waffle)
```

![](Data-Pipeline_files/figure-gfm/unnamed-chunk-26-1.png)<!-- --> \##
Step 9: Comparing Parliament sentence sentiment distribution with SEL
distribution

Creating waffle plot for general SEL sentiment distribution (1),
creating dataframe for proportions of SEL words to sentiments (2), and
creating dataframe for proportions of speakers to to sentiments

``` r
ggplot(data = sel_distribution, aes(fill=sel_distribution$Categoría, values=Freq)) +
  geom_waffle(color = "white") +
  scale_fill_manual(values = c(Alegría = "seagreen4", Enojo = "slateblue1", 
                               Miedo = "hotpink", Repulsión = "olivedrab3", 
                               Sorpresa = "gold", Tristeza = "tomato"))
```

![](Data-Pipeline_files/figure-gfm/unnamed-chunk-27-1.png)<!-- -->

``` r
prop_words <- data.frame(Category = c('Happiness', 'Anger', 
                                      'Fear', 'Disgust', 'Surprise', 
                                      'Sadness'),
                         Proportion = c((sel_distribution$Freq[1])/sum(sel_distribution$Freq),
                                        (sel_distribution$Freq[2])/sum(sel_distribution$Freq),
                                        (sel_distribution$Freq[3])/sum(sel_distribution$Freq),
                                        (sel_distribution$Freq[4])/sum(sel_distribution$Freq),
                                        (sel_distribution$Freq[5])/sum(sel_distribution$Freq),
                                        (sel_distribution$Freq[6])/sum(sel_distribution$Freq)))

prop_words
```

    ##    Category Proportion
    ## 1 Happiness 0.33010336
    ## 2     Anger 0.18669251
    ## 3      Fear 0.10400517
    ## 4   Disgust 0.10723514
    ## 5  Surprise 0.08268734
    ## 6   Sadness 0.18927649

``` r
prop_usage <- data.frame(Category = c('Happiness', 'Sadness', 
                                      'Anger', 'Fear', 'Surprise', 
                                      'Disgust'),
                         Proportion = c((comp_waffle$Freq[1])/sum(comp_waffle$Freq),
                                        (comp_waffle$Freq[2])/sum(comp_waffle$Freq),
                                        (comp_waffle$Freq[3])/sum(comp_waffle$Freq),
                                        (comp_waffle$Freq[4])/sum(comp_waffle$Freq),
                                        (comp_waffle$Freq[5])/sum(comp_waffle$Freq),
                                        (comp_waffle$Freq[6])/sum(comp_waffle$Freq)))
prop_usage
```

    ##    Category Proportion
    ## 1 Happiness  0.7656250
    ## 2   Sadness  0.1250000
    ## 3     Anger  0.0390625
    ## 4      Fear  0.0234375
    ## 5  Surprise  0.0312500
    ## 6   Disgust  0.0156250

## Step 10: Comparing Parliament sentence sentiment distribution with non-related ‘economy’ distribution

Here, I will follow many of the steps above to create a new distribution
that is based off of a brand-new keyword vector. Since all data is
stemmed, the vector I chose only contains one item: ‘econom’

``` r
#Creating new dataframe just with economy-related stem
keywords_econ <- ('econom')

keywords_col_econ <- small_data_span$sentence %>% 
  str_detect(keywords_econ)

small_data_econ <- small_data_span %>%
  mutate(keywords = keywords_col_econ)

small_data_econ <- small_data_econ %>%
  filter(keywords == TRUE)

#Tokenizing sentences
small_data_econ <- small_data_econ %>%
  unnest_tokens(tokens, sentence, token="words", drop=FALSE, to_lower=TRUE)

#Stemming sentence tokens
econ_stems <- wordStem(small_data_econ$tokens, language = "spanish")
stemmed_econ_ngrams <- small_data_econ %>% 
  mutate(Stems = econ_stems)

#Inner-joining stemmed SEL set and newly stemmed economy set
merged_econ_data <- stemmed_econ_ngrams %>% 
  inner_join(stemmed_sel, by="Stems", multiple = "all", unmatched = "drop", relationship = "many-to-many")

#Finding distribution of sentiments across individual speakers
by_speaker_econ <- merged_econ_data %>% 
  count(speaker_id, Categoría, sort=TRUE) %>%
  filter(n == max(n), .by=speaker_id)

#Plotting with waffle()
econ_waffle <- by_speaker_econ %>%
  group_by(Categoría) %>% 
  mutate(Freq=n()) %>%
  select(Categoría, Freq) %>% 
  distinct()
waffle(econ_waffle)
```

![](Data-Pipeline_files/figure-gfm/unnamed-chunk-28-1.png)<!-- -->

``` r
#Gathering proportions
econ_usage <- data.frame(Category = c('Happiness', 'Sadness', 
                                      'Anger', 'Disgust', 'Surprise'),
                         Proportion = c((comp_waffle$Freq[1])/sum(comp_waffle$Freq),
                                        (comp_waffle$Freq[2])/sum(comp_waffle$Freq),
                                        (comp_waffle$Freq[3])/sum(comp_waffle$Freq),
                                        (comp_waffle$Freq[4])/sum(comp_waffle$Freq),
                                        (comp_waffle$Freq[5])/sum(comp_waffle$Freq)))
```
