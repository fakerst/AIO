import re
import logging
import numpy as np
import pandas as pd
import glob
import sys
import subprocess


def column_sum(list1, list2):
    # 使用zip()函数将两个列表按列组合
    combined = zip(list1, list2)

    # 利用列表推导式进行按列相加
    column_sums = [x + y for x, y in combined]

    # 返回按列相加的结果
    return column_sums


def get_number_columns(df):
    """
    Since some columns contain string metadata, and others contain values,
    this function returns the columns that contain values.
    """
    return df.columns[np.logical_or(df.dtypes == np.float64, df.dtypes == np.int64)]


def extracting_darshan(path):
    log_features = ['POSIX', 'MPIIO', 'HDF5', 'POSIX_OPENS', 'POSIX_FSYNCS', 'NPROCS', 'File_Per_Proc', 'POSIX_READS',
                    'POSIX_WRITES',
                    'POSIX_SEQ_READS', 'POSIX_SEQ_WRITES', 'POSIX_CONSEC_READS',
                    'POSIX_CONSEC_WRITES', 'POSIX_ACCESS1_ACCESS',
                    'POSIX_ACCESS2_ACCESS', 'POSIX_ACCESS3_ACCESS',
                    'POSIX_ACCESS4_ACCESS',
                    'POSIX_ACCESS1_COUNT',
                    'POSIX_ACCESS2_COUNT', 'POSIX_ACCESS3_COUNT',
                    'POSIX_ACCESS4_COUNT',
                    'MPIIO_COLL_READS', 'MPIIO_COLL_WRITES', 'MPIIO_VIEWS',
                    'POSIX_BYTES_READ',
                    'POSIX_BYTES_WRITTEN',
                    'POSIX_F_READ_TIME', 'POSIX_F_WRITE_TIME', 'POSIX_F_META_TIME']

    POSIX = []
    MPIIO = []
    HDF5 = []
    POSIX_OPENS = []
    POSIX_FSYNCS = []
    NPROCS = []
    File_Per_Proc = []
    POSIX_READS = []
    POSIX_WRITES = []
    POSIX_SEQ_READS = []
    POSIX_SEQ_WRITES = []
    POSIX_CONSEC_READS = []
    POSIX_CONSEC_WRITES = []
    POSIX_ACCESS1_ACCESS = []
    POSIX_ACCESS2_ACCESS = []
    POSIX_ACCESS3_ACCESS = []
    POSIX_ACCESS4_ACCESS = []
    POSIX_ACCESS1_COUNT = []
    POSIX_ACCESS2_COUNT = []
    POSIX_ACCESS3_COUNT = []
    POSIX_ACCESS4_COUNT = []
    MPIIO_COLL_READS = []
    MPIIO_COLL_WRITES = []
    MPIIO_VIEWS = []

    POSIX_BYTES_READ = []
    POSIX_BYTES_WRITTEN = []
    POSIX_F_READ_TIME = []
    POSIX_F_WRITE_TIME = []
    POSIX_F_META_TIME = []

    POSIX_OPENS_PATTERN = '(total_POSIX_OPENS:\s+)(\d+)'
    ds_opens_pattern = re.compile(POSIX_OPENS_PATTERN)

    POSIX_FSYNCS_PATTERN = '(total_POSIX_FSYNCS:\s+)(\d+)'
    ds_fsyncs_pattern = re.compile(POSIX_FSYNCS_PATTERN)

    DARSHAN_NPROCS_PATTERN = '(#\s+nprocs:\s+)(\d+)'
    ds_nprocs_pattern = re.compile(DARSHAN_NPROCS_PATTERN)

    POSIX_READS_PATTERN = '(total_POSIX_READS:\s+)(\d+)'
    ds_reads_pattern = re.compile(POSIX_READS_PATTERN)

    POSIX_WRITES_PATTERN = '(total_POSIX_WRITES:\s+)(\d+)'
    ds_writes_pattern = re.compile(POSIX_WRITES_PATTERN)

    POSIX_SEQ_READS_PATTERN = '(total_POSIX_SEQ_READS:\s+)(\d+)'
    ds_seq_reads_pattern = re.compile(POSIX_SEQ_READS_PATTERN)

    POSIX_SEQ_WRITES_PATTERN = '(total_POSIX_SEQ_WRITES:\s+)(\d+)'
    ds_seq_writes_pattern = re.compile(POSIX_SEQ_WRITES_PATTERN)

    POSIX_CONSEC_READS_PATTERN = '(total_POSIX_CONSEC_READS:\s+)(\d+)'
    ds_consec_reads_pattern = re.compile(POSIX_CONSEC_READS_PATTERN)

    POSIX_CONSEC_WRITES_PATTERN = '(total_POSIX_CONSEC_WRITES:\s+)(\d+)'
    ds_consec_writes_pattern = re.compile(POSIX_CONSEC_WRITES_PATTERN)

    POSIX_ACCESS1_PATTERN = '(total_POSIX_ACCESS1_ACCESS:\s+)(\d+)'
    ds_access1_pattern = re.compile(POSIX_ACCESS1_PATTERN)

    POSIX_ACCESS2_PATTERN = '(total_POSIX_ACCESS2_ACCESS:\s+)(\d+)'
    ds_access2_pattern = re.compile(POSIX_ACCESS2_PATTERN)

    POSIX_ACCESS3_PATTERN = '(total_POSIX_ACCESS3_ACCESS:\s+)(\d+)'
    ds_access3_pattern = re.compile(POSIX_ACCESS3_PATTERN)

    POSIX_ACCESS4_PATTERN = '(total_POSIX_ACCESS4_ACCESS:\s+)(\d+)'
    ds_access4_pattern = re.compile(POSIX_ACCESS4_PATTERN)

    POSIX_ACCESS1_PATTERN = '(total_POSIX_ACCESS1_COUNT:\s+)(\d+)'
    ds_access1c_pattern = re.compile(POSIX_ACCESS1_PATTERN)

    POSIX_ACCESS2_PATTERN = '(total_POSIX_ACCESS2_COUNT:\s+)(\d+)'
    ds_access2c_pattern = re.compile(POSIX_ACCESS2_PATTERN)

    POSIX_ACCESS3_PATTERN = '(total_POSIX_ACCESS3_COUNT:\s+)(\d+)'
    ds_access3c_pattern = re.compile(POSIX_ACCESS3_PATTERN)

    POSIX_ACCESS4_PATTERN = '(total_POSIX_ACCESS4_COUNT:\s+)(\d+)'
    ds_access4c_pattern = re.compile(POSIX_ACCESS4_PATTERN)

    STDIO_PATTERN = '(# POSIX module data\s+)'
    ds_stdio_pattern = re.compile(STDIO_PATTERN)

    MPIIO_PATTERN = '(# MPI-IO module data\s+)'
    ds_mpiio_pattern = re.compile(MPIIO_PATTERN)

    STDIO_PATTERN = '(# STDIO module data\s+)'
    ds_stdio_pattern = re.compile(STDIO_PATTERN)

    MPIIO_COLL_READS_PATTERN = '(total_MPIIO_COLL_READS:\s+)(\d+)'
    ds_coll_reads_pattern = re.compile(MPIIO_COLL_READS_PATTERN)

    MPIIO_COLL_WRITES_PATTERN = '(total_MPIIO_COLL_WRITES:\s+)(\d+)'
    ds_coll_writes_pattern = re.compile(MPIIO_COLL_WRITES_PATTERN)

    MPIIO_VIEWS_PATTERN = '(total_MPIIO_VIEWS:\s+)(\d+)'
    ds_views_pattern = re.compile(MPIIO_VIEWS_PATTERN)

    POSIX_BYTES_READ_PATTERN = '(total_POSIX_BYTES_READ:\s+)(\d+)'
    ds_bytes_read_pattern = re.compile(POSIX_BYTES_READ_PATTERN)

    POSIX_BYTES_WRITTEN_PATTERN = '(total_POSIX_BYTES_WRITTEN:\s+)(\d+)'
    ds_bytes_written_pattern = re.compile(POSIX_BYTES_WRITTEN_PATTERN)

    DARSHAN_READ_TIME_PATTERN = '(total_POSIX_F_READ_TIME:\s+)(\d+\.\d+)'
    ds_read_time_pattern = re.compile(DARSHAN_READ_TIME_PATTERN)
    DARSHAN_WRITE_TIME_PATTERN = '(total_POSIX_F_WRITE_TIME:\s+)(\d+\.\d+)'
    ds_write_time_pattern = re.compile(DARSHAN_WRITE_TIME_PATTERN)
    DARSHAN_META_TIME_PATTERN = '(total_POSIX_F_META_TIME:\s+)(\d+\.\d+)'
    ds_meta_time_pattern = re.compile(DARSHAN_META_TIME_PATTERN)

    darshan_files = glob.glob(path)

    #print("file numbers %s" % len(darshan_files))
    for file_name in darshan_files:
        # print(file_name)
        with open(file_name) as infile:
            posix = 0
            mpiio = 0
            hdf5 = 0
            for line in infile:
                opens_match = ds_opens_pattern.match(line)
                if opens_match is not None:
                    posix = 1
                    posix_opens = int(opens_match.group(2))
                    POSIX_OPENS.append(posix_opens)
                    continue

                fsyncs_match = ds_fsyncs_pattern.match(line)
                if fsyncs_match is not None:
                    posix_fsyncs = int(fsyncs_match.group(2))
                    POSIX_FSYNCS.append(posix_fsyncs)
                    continue

                nprocs_match = ds_nprocs_pattern.match(line)
                if nprocs_match is not None:
                    nprocs = int(nprocs_match.group(2))
                    NPROCS.append(nprocs)
                    continue

                reads_match = ds_reads_pattern.match(line)
                if reads_match is not None:
                    posix_reads = int(reads_match.group(2))
                    POSIX_READS.append(posix_reads)
                    continue

                writes_match = ds_writes_pattern.match(line)
                if writes_match is not None:
                    posix_writes = int(writes_match.group(2))
                    POSIX_WRITES.append(posix_writes)
                    continue

                seq_reads_match = ds_seq_reads_pattern.match(line)
                if seq_reads_match is not None:
                    posix_seq_reads = int(seq_reads_match.group(2))
                    POSIX_SEQ_READS.append(posix_seq_reads)
                    continue

                seq_writes_match = ds_seq_writes_pattern.match(line)
                if seq_writes_match is not None:
                    posix_seq_writes = int(seq_writes_match.group(2))
                    POSIX_SEQ_WRITES.append(posix_seq_writes)
                    continue

                consec_reads_match = ds_consec_reads_pattern.match(line)
                if consec_reads_match is not None:
                    posix_consec_reads = int(consec_reads_match.group(2))
                    POSIX_CONSEC_READS.append(posix_consec_reads)
                    continue

                consec_writes_match = ds_consec_writes_pattern.match(line)
                if consec_writes_match is not None:
                    posix_consec_writes = int(consec_writes_match.group(2))
                    POSIX_CONSEC_WRITES.append(posix_consec_writes)
                    continue

                access1_match = ds_access1_pattern.match(line)
                if access1_match is not None:
                    posix_access1 = int(access1_match.group(2))
                    POSIX_ACCESS1_ACCESS.append(posix_access1)
                    continue

                access2_match = ds_access2_pattern.match(line)
                if access2_match is not None:
                    posix_access2 = int(access2_match.group(2))
                    POSIX_ACCESS2_ACCESS.append(posix_access2)
                    continue

                access3_match = ds_access3_pattern.match(line)
                if access3_match is not None:
                    posix_access3 = int(access3_match.group(2))
                    POSIX_ACCESS3_ACCESS.append(posix_access3)
                    continue

                access4_match = ds_access4_pattern.match(line)
                if access4_match is not None:
                    posix_access4 = int(access4_match.group(2))
                    POSIX_ACCESS4_ACCESS.append(posix_access4)
                    continue

                access1c_match = ds_access1c_pattern.match(line)
                if access1c_match is not None:
                    posix_access1c = int(access1c_match.group(2))
                    POSIX_ACCESS1_COUNT.append(posix_access1c)
                    continue

                access2c_match = ds_access2c_pattern.match(line)
                if access2c_match is not None:
                    posix_access2c = int(access2c_match.group(2))
                    POSIX_ACCESS2_COUNT.append(posix_access2c)
                    continue

                access3c_match = ds_access3c_pattern.match(line)
                if access3c_match is not None:
                    posix_access3c = int(access3c_match.group(2))
                    POSIX_ACCESS3_COUNT.append(posix_access3c)
                    continue

                access4c_match = ds_access4c_pattern.match(line)
                if access4c_match is not None:
                    posix_access4c = int(access4c_match.group(2))
                    POSIX_ACCESS4_COUNT.append(posix_access4c)
                    continue

                bytes_read_match = ds_bytes_read_pattern.match(line)
                if bytes_read_match is not None:
                    posix_bytes_read = int(bytes_read_match.group(2))
                    POSIX_BYTES_READ.append(posix_bytes_read)
                    continue

                bytes_written_match = ds_bytes_written_pattern.match(line)
                if bytes_written_match is not None:
                    posix_bytes_written = int(bytes_written_match.group(2))
                    POSIX_BYTES_WRITTEN.append(posix_bytes_written)
                    continue

                read_time_match = ds_read_time_pattern.match(line)
                if read_time_match is not None:
                    posix_read_time = float(read_time_match.group(2))
                    POSIX_F_READ_TIME.append(posix_read_time)
                    continue

                write_time_match = ds_write_time_pattern.match(line)
                if write_time_match is not None:
                    posix_write_time = float(write_time_match.group(2))
                    POSIX_F_WRITE_TIME.append(posix_write_time)
                    continue

                meta_time_match = ds_meta_time_pattern.match(line)
                if meta_time_match is not None:
                    posix_meta_time = float(meta_time_match.group(2))
                    POSIX_F_META_TIME.append(posix_meta_time)
                    continue

                mpiio_match = ds_mpiio_pattern.match(line)
                if mpiio_match is not None:
                    posix = 0
                    mpiio = 1

                if mpiio == 1:
                    coll_reads_match = ds_coll_reads_pattern.match(line)
                    if coll_reads_match is not None:
                        mpiio_coll_reads = int(coll_reads_match.group(2))
                        MPIIO_COLL_READS.append(mpiio_coll_reads)
                        continue

                    coll_writes_match = ds_coll_writes_pattern.match(line)
                    if coll_writes_match is not None:
                        mpiio_coll_writes = int(coll_writes_match.group(2))
                        MPIIO_COLL_WRITES.append(mpiio_coll_writes)
                        continue

                    mpiio_views_match = ds_views_pattern.match(line)
                    if mpiio_views_match is not None:
                        mpiio_views = int(mpiio_views_match.group(2))
                        MPIIO_VIEWS.append(mpiio_views)
                        continue

                stdio_match = ds_stdio_pattern.match(line)
                if stdio_match is not None:
                    if posix == 1:
                        MPIIO_COLL_READS.append(0)
                        MPIIO_COLL_WRITES.append(0)
                        MPIIO_VIEWS.append(0)
                    break

        #print(len(NPROCS))
        if file_name[-5] == "F":
            file_per_proc = 1
        else:
            file_per_proc = NPROCS[-1]
        POSIX.append(posix)
        MPIIO.append(mpiio)
        HDF5.append(hdf5)
        File_Per_Proc.append(file_per_proc)

    #print(len(NPROCS))
    #print(len(POSIX_OPENS))
    mydata = pd.DataFrame(list(
        zip(POSIX, MPIIO, HDF5, POSIX_OPENS, POSIX_FSYNCS, NPROCS, File_Per_Proc, POSIX_READS, POSIX_WRITES,
            POSIX_SEQ_READS,
            POSIX_SEQ_WRITES, POSIX_CONSEC_READS, POSIX_CONSEC_WRITES, POSIX_ACCESS1_ACCESS, POSIX_ACCESS2_ACCESS,
            POSIX_ACCESS3_ACCESS, POSIX_ACCESS4_ACCESS, POSIX_ACCESS1_COUNT,
            POSIX_ACCESS2_COUNT, POSIX_ACCESS3_COUNT,
            POSIX_ACCESS4_COUNT, MPIIO_COLL_READS, MPIIO_COLL_WRITES, MPIIO_VIEWS, POSIX_BYTES_READ,
            POSIX_BYTES_WRITTEN, POSIX_F_READ_TIME, POSIX_F_WRITE_TIME, POSIX_F_META_TIME)),
        columns=log_features)
    return mydata


def convert(df):
    div = ['POSIX_OPENS', 'POSIX_FSYNCS',
           'POSIX_READS', 'POSIX_WRITES',
           'POSIX_SEQ_READS', 'POSIX_SEQ_WRITES', 'POSIX_CONSEC_READS',
           'POSIX_CONSEC_WRITES',
           'POSIX_ACCESS1_COUNT',
           'POSIX_BYTES_READ', 'POSIX_BYTES_WRITTEN',
           'MPIIO_COLL_READS', 'MPIIO_COLL_WRITES']
    for index, row in df.iterrows():
        if row['File_Per_Proc'] != row['NPROCS']:
            for c in div:
                df.loc[index, c] = int(row[c] / row['NPROCS'])

    df['agg_perf_by_slowest'] = (df['POSIX_BYTES_READ'] + df['POSIX_BYTES_WRITTEN']) / (
            df['POSIX_F_READ_TIME'] + df['POSIX_F_WRITE_TIME'] + df['POSIX_F_META_TIME'])
    df['POSIX_WRITE_PER_OPEN'] = df['POSIX_WRITES'] / df['POSIX_OPENS']
    df['POSIX_READ_PER_OPEN'] = df['POSIX_READS'] / df['POSIX_OPENS']

    # df['POSIX_FSYNC_PER_WRITE'] = df['POSIX_FSYNCS']/df['POSIX_WRITES']
    for index, row in df.iterrows():
        if row['POSIX_WRITES'] != 0:
            # 计算分数
            df.loc[index, 'POSIX_FSYNC_PER_WRITE'] = row['POSIX_FSYNCS'] / row['POSIX_WRITES']
        else:
            df.loc[index, 'POSIX_FSYNC_PER_WRITE'] = 0


    log_F = ['POSIX_OPENS', 'POSIX_FSYNCS', 'POSIX_WRITE_PER_OPEN', 'POSIX_READ_PER_OPEN', 'POSIX_FSYNC_PER_WRITE',
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
        df[c] = pd.to_numeric(df[c], errors='coerce').fillna(value=set_NaNs_to)
        df[c + "_LOG10"] = np.log10(df[c] + add_small_value).fillna(value=set_NaNs_to)

    return df


if __name__ == "__main__":
    pd.set_option('display.max_columns', 1000)
    pd.set_option('display.width', 1000)
    pd.set_option('display.max_colwidth', 1000)
    if len(sys.argv) == 3:
        # 第一个参数是脚本的名称，所以真正的参数从第二个开始
        darpath = sys.argv[1]
        datname = sys.argv[2]
        if darpath[-1] == '/':
            darpath = darpath[:-1]
        df = extracting_darshan(darpath + "/*")
        df = convert(df)
        #for index, row in df.iterrows():
        #    print("行索引:", index)
        #    for column in df.columns:
        #        print(column, ":", row[column])
        #    print()

        df.to_csv(datname, index=False)

        cmd = "rm -rf " + darpath
        subprocess.run(cmd, shell=True, capture_output=False, text=True)