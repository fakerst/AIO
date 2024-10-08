import re
import logging
import numpy as np
import pandas as pd
import glob
import sys
import subprocess



if __name__ == "__main__":
    pd.set_option('display.max_columns', 1000)
    pd.set_option('display.width', 1000)
    pd.set_option('display.max_colwidth', 1000)

    lustre_csv = sys.argv[1]
    gekkofs_csv = sys.argv[2]
    classify_csv = sys.argv[3]
    df1 = pd.read_csv(lustre_csv)
    df2 = pd.read_csv(gekkofs_csv)
    df1['fs'] = 1

    x = 0
    for (index1, row1), (index2, row2) in zip(df1.iterrows(), df2.iterrows()):
        if row1['agg_perf_by_slowest'] <= row2['agg_perf_by_slowest']:
            #print(row1['agg_perf_by_slowest'])
            #print(row2['agg_perf_by_slowest'])
            df1.at[index1, 'fs'] = 2
            x += 1

    #print(x)
    df1.to_csv(classify_csv, index=False)

    cmd = "rm -rf " + lustre_csv
    subprocess.run(cmd, shell=True, capture_output=False, text=True)
    cmd = "rm -rf " + gekkofs_csv
    subprocess.run(cmd, shell=True, capture_output=False, text=True)
