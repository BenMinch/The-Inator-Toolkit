###Looking at dREP files to get uniques####DREP uniqueinator

import pandas as pd
import numpy as np
import os, argparse, sys, re, subprocess

# define flags
parser = argparse.ArgumentParser(description='A script to look at dREP Cdb.csv files and determine overlap between genomes found between sites')
parser.add_argument('-i', '--input', help='Input dREP Cdb.csv file', required=True)
parser.add_argument('-s', '--site', help='Site names, separated by comma', required=True)
parser.add_argument('-d', '--datatype', help='Input file type, either DREP (drep) CDB.csv or CD-hit (CD) parsed file', required=True)
args = parser.parse_args()

# set variables
input_file = args.input
site_names = args.site
data_type = args.datatype
site1 = site_names.split(',')[0]
site2 = site_names.split(',')[1]

site1_count = 0
site2_count = 0
shared_count = 0
# read in files
input_df = pd.read_csv(input_file)

#group by primary_cluster and combine genome column with ;
if data_type == 'CD':
    #change cluster column to primary_cluster
    input_df= input_df.rename(columns={'cluster':'primary_cluster'})
    input_df=input_df.rename(columns={'member':'genome'})

input_df['genome']= input_df['genome'].astype(str)

input_df['genome']= input_df.groupby('primary_cluster')['genome'].transform(lambda x: ';'.join(x))

#group by primary cluster and get rid of duplicates
input_df= input_df.drop_duplicates(subset='primary_cluster', keep='first')
input_df= input_df.reset_index()

#make an empty dataframe to hold site1 and site2 genomes
site1_df= pd.DataFrame(columns=['genome'])
site2_df= pd.DataFrame(columns=['genome'])
shared_df= pd.DataFrame(columns=['genome'])
site1_df['index'] = range(len(input_df))
site2_df['index'] = range(len(input_df))
shared_df['index'] = range(len(input_df))

for i in range(len(input_df)):
    if site1 in input_df['genome'][i] and site2 not in input_df['genome'][i]:
        site1_count+=1
        site1_df['genome'][i]=input_df['genome'][i]
    if site2 in input_df['genome'][i] and site1 not in input_df['genome'][i]:
        site2_count+=1
        site2_df['genome'][i]=input_df['genome'][i]
    if site1 in input_df['genome'][i] and site2 in input_df['genome'][i]:
        shared_count+=1
        shared_df['genome'][i]=input_df['genome'][i]

print('Site 1: ' + str(site1_count))
print('Site 2: ' + str(site2_count))
print('Shared: ' + str(shared_count))

# write output
#remove empty rows in each dataframe
site1_df= site1_df.dropna()
site2_df= site2_df.dropna()
shared_df= shared_df.dropna()
#remove index column
site1_df= site1_df.drop(columns=['index'])
site2_df= site2_df.drop(columns=['index'])
shared_df= shared_df.drop(columns=['index'])
#write to file
site1_df.to_csv(site1 + '_uniqueinator.txt', index=False)
site2_df.to_csv(site2 + '_uniqueinator.txt', index=False)
shared_df.to_csv('shared_uniqueinator.txt', index=False)