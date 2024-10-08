import os
import pandas as pd
import numpy as np
import sklearn
import xgboost as xgb
from utils.feature import *

import warnings

warnings.filterwarnings("ignore")


plt.rcParams['font.sans-serif'] = ['SimHei']

def convert(df):
    df['agg_perf_by_slowest'] = (df['POSIX_BYTES_READ'] + df['POSIX_BYTES_WRITTEN']) / (
            df['POSIX_F_READ_TIME'] + df['POSIX_F_WRITE_TIME'] + df['POSIX_F_META_TIME'])
    df['POSIX_WRITE_PER_OPEN'] = df['POSIX_WRITES'] / df['POSIX_OPENS']
    df['POSIX_READ_PER_OPEN'] = df['POSIX_READS'] / df['POSIX_OPENS']

    #df['POSIX_FSYNC_PER_WRITE'] = df['POSIX_WRITES']/df['POSIX_FSYNCS']

    for index, row in df.iterrows():
        if row['POSIX_FSYNCS'] != 0:
            # 计算分数
            df.loc[index, 'POSIX_FSYNC_PER_WRITE'] = row['POSIX_WRITES'] / row['POSIX_FSYNCS']
        else:
            df.loc[index, 'POSIX_FSYNC_PER_WRITE'] = 0

    log_F = ['POSIX_OPENS', 'POSIX_FSYNCS','POSIX_WRITE_PER_OPEN','POSIX_READ_PER_OPEN','POSIX_FSYNC_PER_WRITE',
                   'NPROCS',
                   'POSIX_READS', 'POSIX_WRITES',
                   'POSIX_SEQ_READS', 'POSIX_SEQ_WRITES', 'POSIX_CONSEC_READS',
                   'POSIX_CONSEC_WRITES',
                   'POSIX_ACCESS1_ACCESS', 'POSIX_ACCESS1_COUNT',
                   'POSIX_BYTES_READ', 'POSIX_BYTES_WRITTEN',
                   'MPIIO_COLL_READS', 'MPIIO_COLL_WRITES']

    add_small_value = 0.1
    set_NaNs_to = -10
    for c in log_F:
        df[c+"_LOG10"] = np.log10(df[c] + add_small_value).fillna(value=set_NaNs_to)
    return df

def load_datasets(csv):
    pd.set_option('display.max_columns', 1000)
    pd.set_option('display.width', 1000)
    pd.set_option('display.max_colwidth', 1000)

    df = pd.read_csv(csv)
    convert(df)
    

    df_train, df_test = sklearn.model_selection.train_test_split(df, test_size=0.15)

    X_train, X_test = df_train[features18_], df_test[features18_]

    y_train, y_test = df_train["fs"], df_test["fs"]

    return X_train, X_test, y_train, y_test

def model_train(X_train, X_test, y_train, y_test):
    y_train -=1
    y_test -= 1
    from xgboost import XGBRegressor as XGBR
    from xgboost import XGBClassifier as XGBR
    reg = XGBR(n_estimators=100).fit(X_train, y_train)
    accuracy = reg.score(X_test, y_test)
    print("XGB准确率:", accuracy)


def main(csv):
    X_train, X_test, y_train, y_test = load_datasets(csv)
    model_train(X_train, X_test, y_train, y_test)


if __name__ == "__main__":
    csv = sys.argv[1]
    main(csv)

