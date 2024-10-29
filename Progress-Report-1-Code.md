Progress-Report-1
================
Claire McLean
2024-10-28

NOTE: The dataset I am using for this project is named
basque_parliament_1 and was found on <https://huggingface.co>. The
original project was funded by the Spanish Ministry of Science and
Innovation, and is licensed as cc0-1.0.

Citation: @misc {software_technologies_working_group_2024, author = {
{Software Technologies Working Group} }, title = { basque_parliament_1
(Revision a2fbcaf) }, year = 2024, url = {
<https://huggingface.co/datasets/gttsehu/basque_parliament_1> }, doi = {
10.57967/hf/2485 }, publisher = { Hugging Face } }

# Progress Report 1

## Here, I will begin the next steps of my data cleaning.

## Step 1: Performed in Python

In this step, I wrote a script to filter the train.tsv file provided in
the Hugging Face dataset folder to include only the rows/utterances that
contain the following keywords:

\[‘hablante’, ‘euskera’, ‘lenguaje’, ‘idioma’, ‘aprendizaje’,
‘lingüístico’, ‘lingüística’\]

These keywords were chosen because they demonstrate the relevance of the
utterance to the concept of language, linguistics, or “speaker”.

The final output of the script was a smaller .csv file containing only
the rows that will be relevant to my analysis. This dataframe will be
further cleaned in later steps.

This script has been included in my Progress Report 1, but will most
likely not be part of my final submission.

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
```

Next, read in the .csv file:

``` r
rel_data <- read_csv("BS_RelData.csv")
```

    ## Rows: 4163 Columns: 6
    ## ── Column specification ────────────────────────────────────────────────────────
    ## Delimiter: ","
    ## chr (3): path, language, sentence
    ## dbl (3): speaker_id, PRR, length
    ## 
    ## ℹ Use `spec()` to retrieve the full column specification for this data.
    ## ℹ Specify the column types or set `show_col_types = FALSE` to quiet this message.

Reducing size by only including first 200 rows:

``` r
small_data <- rel_data %>% slice(1:250)
view(small_data)
```

Now, filtering to only include rows that are Spanish utterances (exclude
Basque and bilingual):

``` r
small_data_span <- small_data %>% filter(language == "es")
view(small_data_span)
```

Now removing the ‘path’ column as it is unnecessary for my analysis:

``` r
small_data_span2 <- small_data_span %>% select(-path)
view(small_data_span2)
```

This leaves me with 190 tidy rows to annotate for sentiment. This number
may change depending on the analysis process.

Now exporting dataframe to .csv file (annotations still needed):

``` r
write_csv(small_data_span2, "small_data_NA.csv")
```

## Some basic stats:

``` r
#number of rows:
nrow(small_data_span2)
```

    ## [1] 238

``` r
#number of columns:
ncol(small_data_span2)
```

    ## [1] 5

``` r
#average utterance length
mean(small_data_span2$length)
```

    ## [1] 7.598193

``` r
#number of unique speakers
n_distinct(small_data_span2$speaker_id)
```

    ## [1] 19
