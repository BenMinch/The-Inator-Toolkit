#correlation benchmarking
import pandas as pd
import numpy as np
from scipy.stats import spearmanr
#set inputs as argparser arguments
import argparse,os,sys
parser= argparse.ArgumentParser(description='Spearman Correlation of MCPs')
parser.add_argument('-g','--genome_metaG',help='MetaG expression file')
parser.add_argument('-t','--genome_metaT',help='MetaT expression file')
parser.add_argument('-o','--outname',help='name of output file')
args= parser.parse_args()
genome_metaG= args.genome_metaG
genome_metaT= args.genome_metaT
outname= args.outname

genome_metaG= pd.read_csv(genome_metaG)
genome_metaT= pd.read_csv(genome_metaT)

#make contig column a character
genome_index= genome_metaG.set_index('Contig')
#see all the index values

genome_index_metaT= genome_metaT.set_index('Contig')


corrdf= pd.DataFrame()
corrdf['contig']=''
corrdf['median_expression']=''
corrdf['mean_expression']=''
corrdf['corr']=''
corrdf['pval']=''
corrdf.head()
corrdf['row']= range(len(genome_metaG))


for i in range(len(genome_metaG)):
    #do a correlation between the two dataframes
    corrdf['contig'][i]= genome_metaG['Contig'][i]
    mcp= genome_metaG['Contig'][i]
    metag= genome_index.loc[mcp]
    metat= genome_index_metaT.loc[mcp]
    corrdf['median_expression'][i]= np.median(metat)
    corrdf['mean_expression'][i]= np.mean(metat)
    corr= spearmanr(metag, metat)
    corrdf.loc[i,'corr']= corr[0]
    corrdf.loc[i,'pval']= corr[1]

corrdf.to_csv('Correlation_'+outname+'.csv')

#convert genome_index to zscores
def zscore(x):
    return (x-x.mean())/x.std()

genome_index_z= genome_index.apply(zscore)
genome_index_metaT_z= genome_index_metaT.apply(zscore)

for i in range(len(genome_metaG)):
    #do a correlation between the two dataframes
    corrdf['contig'][i]= genome_metaG['Contig'][i]
    mcp= genome_metaG['Contig'][i]
    metat2= genome_index_metaT.loc[mcp]
    metag= genome_index_z.loc[mcp]
    metat= genome_index_metaT_z.loc[mcp]
    corrdf['median_expression'][i]= np.median(metat2)
    corrdf['mean_expression'][i]= np.mean(metat2)
    corr= spearmanr(metag, metat)
    corrdf.loc[i,'corr']= corr[0]
    corrdf.loc[i,'pval']= corr[1]

corrdf.to_csv('Correlation_'+outname+'_zscore.csv')