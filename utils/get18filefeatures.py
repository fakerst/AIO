import re

import numpy as np
import pandas as pd
from utils.utils_else import *
from utils.feature import *

import warnings

warnings.filterwarnings("ignore")

# 用于匹配 Darshan 日志文件中的每一行的正则表达式
darshan_nprocs_pattern = re.compile(r'(#\s+nprocs:\s+)(\d+)')
darshan_posix_module_data_int = re.compile(r'^(POSIX)\s+(-?\d+)\s+(-?\d+)\s+(\w+)\s+(-?\d+)\s+(.+)\s+(.+)\s+(\w+)$')
darshan_posix_module_data_float = re.compile(
    r'^(POSIX)\s+(-?\d+)\s+(-?\d+)\s+(\w+)\s+(\d+\.\d+)\s+(.+)\s+(.+)\s+(\w+)$')
darshan_mpiio_module_data_int = re.compile(r'^(MPI-IO)\s+(-?\d+)\s+(-?\d+)\s+(\w+)\s+(-?\d+)\s+(.+)\s+(.+)\s+(\w+)$')
darshan_mpiio_module_data_float = re.compile(
    r'^(MPI-IO)\s+(-?\d+)\s+(-?\d+)\s+(\w+)\s+(\d+\.\d+)\s+(.+)\s+(.+)\s+(\w+)$')


def get_unique_files(df, log_file_path):
    with open(log_file_path, 'r') as file:
        for line in file:
            procmatch = darshan_nprocs_pattern.match(line)
            pmatch_int = darshan_posix_module_data_int.match(line)
            pmatch_float = darshan_posix_module_data_float.match(line)
            mmatch_int = darshan_mpiio_module_data_int.match(line)
            mmatch_float = darshan_mpiio_module_data_float.match(line)
            if procmatch:
                global nprocs
                nprocs = int(procmatch.group(2))
                print(nprocs)

            if pmatch_int:
                file_name = pmatch_int.group(6)
                if file_name not in df.index:
                    df.loc[file_name] = [1] * 1 + [0] * 18 + [0.0] * 3
                rank = int(pmatch_int.group(2))
                if rank == -1:
                    df.loc[file_name]['File_Per_Proc'] += nprocs
                else:
                    df.loc[file_name]['File_Per_Proc'] += 1
                counter_name = pmatch_int.group(4)
                counter_value = float(pmatch_int.group(5))

                if counter_name in df.columns:
                    df.loc[file_name][counter_name] += counter_value

            if pmatch_float:
                file_name = pmatch_float.group(6)

                if file_name not in df.index:
                    df.loc[file_name] = [1] * 1 + [0] * 18 + [0.0] * 3
                rank = int(pmatch_float.group(2))
                if rank == -1:
                    df.loc[file_name]['File_Per_Proc'] += nprocs
                else:
                    df.loc[file_name]['File_Per_Proc'] += 1
                counter_name = pmatch_float.group(4)
                counter_value = float(pmatch_float.group(5))
                if counter_name in df.columns:
                    df.loc[file_name][counter_name] += counter_value

            if mmatch_int:
                file_name = mmatch_int.group(6)
                counter_name = mmatch_int.group(4)
                counter_value = float(mmatch_int.group(5))
                df.loc[file_name]['POSIX'] = 0
                df.loc[file_name]['MPIIO'] = 1
                if counter_name in df.columns:
                    df.loc[file_name][counter_name] += counter_value

            if mmatch_float:
                file_name = mmatch_float.group(6)
                counter_name = mmatch_float.group(4)
                counter_value = float(mmatch_float.group(5))
                if counter_name in df.columns:
                    df.loc[file_name][counter_name] += counter_value


def get_app_file(file):
    data = []
    df = pd.DataFrame(data=data, columns=columns)
    get_unique_files(df, file)
    df['NPROCS'] = nprocs
    df['File_Per_Proc'] /= 86
    convert_feature(df)
    return df


if __name__ == "__main__":
    df = get_app_file("/home/fakerth/lustre-c1-S1M-dar/N-1_n-1_m_r_c_t-1m_b-1g.txt")
    print(df)
    print(df.index)
