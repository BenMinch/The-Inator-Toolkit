import os, sys, re, shlex, subprocess
import pandas as pd

input_dir = sys.argv[1]
outdir = sys.argv[2]
list= sys.argv[3]

df= pd.read_csv(list)
for x in range(len(df)):
    sample_name=df['Sample'][x]
    gene_name=df['Gene'][x]
    gene_name=str(gene_name)
    gene_namealt= re.sub(';','_',gene_name)
    #if gene name contains ;, split it
    if ';' in gene_name:
        gene_name2= gene_name.split(';')
        with open('gene_list.txt','w') as f:
            for i in gene_name2:
                f.write(i+'\n')
        f.close()
    else:
        with open('gene_list.txt','w') as f:
            f.write(gene_name)
    #close file
        f.close()
    for i in os.listdir(input_dir):
        if sample_name in i and i.endswith('.fna'):
            read = os.path.join(input_dir, i)
            
            #if gene name is a list
            if ';' in gene_name:
                outpath1= os.path.join(outdir, sample_name+ gene_namealt+'.joined')
                cmd1= 'seqkit grep -f gene_list.txt '+ read + ' > '+ outpath1
          
                subprocess.call(cmd1, shell=True)
            else:
                outpath = os.path.join(outdir, sample_name+gene_name)
                cmd= 'seqkit grep -f '+'gene_list.txt ' + read
               
                cmd2= shlex.split(cmd)
                subprocess.call(cmd2, stdout=open(outpath, "w"), stderr=open("error.txt", "w"))
        else:
            pass

#merging joined files
for i in os.listdir(outdir):
    if i.endswith('.joined'):
        joinpath= os.path.join(outdir, i)
        #remove the second > line
        sed= 'sed "/>.*$/ {n; :a; />.*$/! {N; ba;}; s/>.*$//; :b; n; $! bb}" '+ joinpath + ' > '+ joinpath + '.united'
        subprocess.call(sed, shell=True)
remove= 'rm ' outdir+"/*.joined
subprocess.call(remove,shell=True)
       

