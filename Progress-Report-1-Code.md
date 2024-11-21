Progress-Report-1
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
10.57967/hf/2485 }, publisher = { Hugging Face } } \# Progress Report 1
\## Here, I will begin the next steps of my data cleaning. \## Step 1:
Performed in Python In this step, I wrote a script to filter the
train.tsv file provided in the Hugging Face dataset folder to include
only the rows/utterances that contain the following keywords:
\[‘hablante’, ‘euskera’, ‘lenguaje’, ‘idioma’, ‘aprendizaje’,
‘lingüístic’\] These keywords were chosen because they demonstrate the
relevance of the utterance to the concept of language, linguistics, or
“speaker”. The final output of the script was a smaller .csv file
containing only the rows that will be relevant to my analysis. This
dataframe will be further cleaned in later steps. This script has been
included in my Progress Report 1, but will most likely not be part of my
final submission.

## Step 2: Data Wrangling in R

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

## The following steps are the pipeline I followed to split the data into two smaller dataframes. This pipeline can be ignored.

Next, read in the .tsv file:

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

## This is where I uploaded the two smaller .csv files:

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
view(raw_data)
nrow(raw_data)
```

    ## [1] 749945

``` r
ncol(raw_data)
```

    ## [1] 6

Now, filtering to only include rows that are Spanish utterances (exclude
Basque and bilingual):

``` r
small_data_span <- raw_data %>% filter(language == "es")
view(small_data_span)
```

Now removing the ‘path’ column as it is unnecessary for my analysis:

``` r
small_data_span2 <- small_data_span %>% select(-path)
view(small_data_span2)
```

Using stringr to identify utterances/sentences that contain the
following keywords. \[‘hablante’, ‘euskera’, ‘lenguaje’, ‘idioma’,
‘aprendizaje’, ‘lingüístic’\]. This will allow me to perform sentiment
analysis only on the utterances that are related in some way to
language.

``` r
keywords_vec <- ('hablante|euskera|lenguaje|idioma|aprendizaje|lingüístic')
keywords_col <- small_data_span2$sentence %>%
  str_detect(keywords_vec)
small_data_span3 <- small_data_span2 %>%
  mutate(keywords = keywords_col)
view(small_data_span3)
small_data_span4 <- small_data_span3 %>%
  filter(keywords == TRUE)
view(small_data_span4)
```

Reducing size by only including 300 random rows:

``` r
set.seed(10)
sampled_data <- small_data_span4 %>% slice_sample(n=2000)
view(sampled_data)
```

Now exporting dataframe to .csv file (annotations still needed):

``` r
write_csv(sampled_data, "sampled_data.csv")
```

## Some basic stats:

``` r
#number of rows:
nrow(sampled_data)
```

    ## [1] 2000

``` r
#number of columns:
ncol(sampled_data)
```

    ## [1] 6

``` r
#average utterance length
mean(sampled_data$length)
```

    ## [1] 7.68555

``` r
#number of unique speakers
n_distinct(sampled_data$speaker_id)
```

    ## [1] 121

## Importing SEL lexicon

Load dependencies:

``` r
library("readxl")
library("readr")
```

Importing xlsx file:

``` r
sel <- read_excel("SEL.xlsx")
```

Unnesting sentence tokens (ngrams):

``` r
library(dplyr)
library(tidytext)

sampled_data_ngrams <- sampled_data %>%
  unnest_tokens(tokens, sentence, token="words", drop=FALSE, to_lower=TRUE)
view(sampled_data_ngrams)
```

Viewing and assessing SEL corpus:

``` r
view(sel)
```

The following two code chunks were inspired by a project by Kayleah
Griffen, which can be found at the following site:
<https://rpubs.com/klgriffen96/data607_hw10>

Adjusting column names so that both dataframes are conducive to the
inner_join() function:

``` r
sel <- sel %>% 
  rename(`tokens` = Palabra)
view(sel)
```

Does word correspond to a particular emotion?

``` r
merged_data <- sampled_data_ngrams %>% 
  inner_join(sel, by="tokens", multiple = "all", unmatched = "drop", relationship = "many-to-many") %>% 
  group_by(sentence, speaker_id)

view(merged_data)
```

Grouping by sentence/utterance:

``` r
merged_data2 <- merged_data %>% 
  arrange(speaker_id, group_by=TRUE)
merged_data2
```

    ## # A tibble: 537 × 10
    ## # Groups:   sentence, speaker_id [433]
    ##    language speaker_id   PRR length sentence         keywords tokens   `#`   PFA
    ##    <chr>         <dbl> <dbl>  <dbl> <chr>            <lgl>    <chr>  <dbl> <dbl>
    ##  1 es                0  99.2   9.21 y del plan de e… TRUE     lograr   498 0.663
    ##  2 es                0 100    10.2  de querer o no … TRUE     querer   553 0.63 
    ##  3 es                0 100    10.2  de querer o no … TRUE     querer   553 0.63 
    ##  4 es                0 100    10.2  de querer o no … TRUE     llevar  1593 0.132
    ##  5 es                0 100    10.2  de querer o no … TRUE     bien     142 0.798
    ##  6 es                0  99.0   8.05 hemos contribui… TRUE     favor    389 0.33 
    ##  7 es                0 100     9.02 se pueda cumpli… TRUE     cumpl…   264 0.496
    ##  8 es                6  92.7   7.96 pero tal y como… TRUE     agrad…    43 0.764
    ##  9 es                6 100     8.98 recentralizació… TRUE     ataque   731 0.899
    ## 10 es                6 100    10.1  de presencia ve… TRUE     éxito    367 0.864
    ## # ℹ 527 more rows
    ## # ℹ 1 more variable: Categoría <chr>

Creating wordclouds for each sentiment:

``` r
library(wordcloud)
```

    ## Loading required package: RColorBrewer

``` r
library(RColorBrewer)
library(wordcloud2)
```

## Analysis Ideas:

- finding general sentiment for each speaker
- wordcloud of tokens for each sentiment represented in data
- finding general sentiment distribution overall

\*Figure out what to do with PFAs and tokens that have more than one
emotion
