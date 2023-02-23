# The-Inator-Toolkit
A repository for all of my different small bioinformatic tools that help with everyday bioinformatic tasks.

# Corrilationinator
A program that takes two matrices of expression data (or other data) and looks at total correlation between them. This will do spearman's correlation (if you want pearson's it's an easy change.

### Dependencies
Pandas
Numpy

### Use cases
1) You have metatranscriptomic and metagenomic mapping data for a certain gene over time and you want to see if they are correlated.
2) You have mapping data from two different sites on a specific organism over time and want to see correlation.
3) You have a matrix of environmental data you want to correlate with metagenomic expression or metatranscriptomics.

### Inputs
1) Two .csv files that have identical columns for the two datasets you want to correlate. They should have a column called "Contig" that has all your sample names in it, the rest of the columns have to be numerical and must match sample length.
2) Output name: can be whatever you want to call it

### Outputs
1) A csv file showing the correlation coefficient and p-value for each individual row (sample) in your data
2) A similar csv showing correlation between z-score transformed data.

### Example run
`python corrillationinator.py -g input_file_1.csv -t input_file_2.csv -o outputname`
