# Data: 

## raw_data.csv

The abundances for each type of organism across samples. 
This 6.8 mb csv has been previously reduced from 88 other files. 
In the process, calculations of abundance were produced. 
Dimensionality = 64755 rows by 10 columns.

| Column        | Description         | Type  |
| ------------- |:-------------------:| -----:|
| Kingdom       | phylogenetic level (most broad)  | str   |
| Phylum        | phylogenetic level  | str   |
| Class         | phylogenetic level  | str   |
| Order         | phylogenetic level  | str   |
| Family        | phylogenetic level  | str   |
| Genus         | phylogenetic level (most specific) | str   |
| Length        | length of the DNA scaffold | int | 
| Abundacne     | that row's contribution to that sample's total DNA sequences | float | 
| project       | JGI sequencing project number | int |

Background on phylogenetic information: https://en.wikipedia.org/wiki/Phylum.
Creating a reduced toy version of this data set is doable. 

## sample_meta_info.tsv

A table that summarises sample information for each sample. 
One row per sample --> 88 rows. 

| Column    | Description                                    | Type |
| --------- |:----------------------------------------------:| ----:|
| ID        | sample identification corresponging to project | str  |
| oxygen    | amount of oxygen added during transfers        | str  |
| replicate | biological replicate (1-4)                     | int  | 
| week      | week relative to experiment start (1-4)        | str  | 
| project   | project number (same as in raw_data.csv)       | int  | 
 
<hr>
