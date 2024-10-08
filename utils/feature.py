features18_ = ['POSIX', 'MPIIO',
               'NPROCS_LOG10', 'File_Per_Proc',
               'POSIX_WRITE_PER_OPEN_LOG10',
               'POSIX_READ_PER_OPEN_LOG10',
               'POSIX_FSYNC_PER_WRITE_LOG10',
               'POSIX_SEQ_READS_LOG10', 'POSIX_SEQ_WRITES_LOG10',
               'POSIX_CONSEC_READS_LOG10', 'POSIX_CONSEC_WRITES_LOG10',
               'POSIX_ACCESS1_ACCESS_LOG10', 'POSIX_ACCESS1_COUNT_LOG10',
               'POSIX_BYTES_READ_LOG10', 'POSIX_BYTES_WRITTEN_LOG10',
               'MPIIO_COLL_READS_LOG10', 'MPIIO_COLL_WRITES_LOG10']

columnsdir = [
    'POSIX', 'MPIIO', 'HDF5', 'NPROCS',
    'File_Per_Proc',
    'POSIX_FSYNCS',
    'POSIX_OPENS',
    'POSIX_READS',
    'POSIX_WRITES',
    'POSIX_SEQ_READS',
    'POSIX_SEQ_WRITES',
    'POSIX_CONSEC_READS',
    'POSIX_CONSEC_WRITES',
    'POSIX_BYTES_READ',
    'POSIX_BYTES_WRITTEN',

    'POSIX_ACCESS1_ACCESS',
    'POSIX_ACCESS1_COUNT',
    'MPIIO_COLL_READS',
    'MPIIO_COLL_WRITES',
    'MPIIO_VIEWS',

    'POSIX_F_READ_TIME', 'POSIX_F_WRITE_TIME', 'POSIX_F_META_TIME']

columns_dup = [
    'POSIX', 'MPIIO', 'HDF5', 'NPROCS',
    'File_Per_Proc',
    'POSIX_FSYNCS',
    'POSIX_OPENS',
    'POSIX_READS',
    'POSIX_WRITES',
    'POSIX_SEQ_READS',
    'POSIX_SEQ_WRITES',
    'POSIX_CONSEC_READS',
    'POSIX_CONSEC_WRITES',
    'POSIX_BYTES_READ',
    'POSIX_BYTES_WRITTEN',

    'POSIX_ACCESS1_ACCESS',
    'POSIX_ACCESS1_COUNT',
    'MPIIO_COLL_READS',
    'MPIIO_COLL_WRITES',
    'MPIIO_VIEWS']

log_features = [
    'POSIX_OPENS_LOG10', 'POSIX_SEEKS_LOG10', 'POSIX_STATS_LOG10',
    'POSIX_MMAPS_LOG10', 'POSIX_FSYNCS_LOG10',
    'POSIX_MODE_LOG10', 'POSIX_MEM_ALIGNMENT_LOG10',
    'POSIX_FILE_ALIGNMENT_LOG10', 'NPROCS_LOG10',
    'POSIX_TOTAL_ACCESSES_LOG10', 'POSIX_TOTAL_BYTES_LOG10',
    'POSIX_TOTAL_FILES_LOG10'
]

perc_features = [
    'POSIX_BYTES_READ_PERC', 'POSIX_UNIQUE_BYTES_PERC', 'POSIX_SHARED_BYTES_PERC',
    'POSIX_READ_ONLY_BYTES_PERC', 'POSIX_READ_WRITE_BYTES_PERC',
    'POSIX_WRITE_ONLY_BYTES_PERC', 'POSIX_UNIQUE_FILES_PERC',
    'POSIX_SHARED_FILES_PERC', 'POSIX_READ_ONLY_FILES_PERC',
    'POSIX_READ_WRITE_FILES_PERC', 'POSIX_WRITE_ONLY_FILES_PERC',
    'POSIX_READS_PERC', 'POSIX_WRITES_PERC', 'POSIX_RW_SWITCHES_PERC',
    'POSIX_SEQ_READS_PERC', 'POSIX_SEQ_WRITES_PERC', 'POSIX_CONSEC_READS_PERC',
    'POSIX_CONSEC_WRITES_PERC', 'POSIX_FILE_NOT_ALIGNED_PERC',
    'POSIX_MEM_NOT_ALIGNED_PERC', 'POSIX_SIZE_READ_0_100_PERC',
    'POSIX_SIZE_READ_100_1K_PERC', 'POSIX_SIZE_READ_1K_10K_PERC',
    'POSIX_SIZE_READ_10K_100K_PERC', 'POSIX_SIZE_READ_100K_1M_PERC',
    'POSIX_SIZE_READ_1M_4M_PERC', 'POSIX_SIZE_READ_4M_10M_PERC',
    'POSIX_SIZE_READ_10M_100M_PERC', 'POSIX_SIZE_READ_100M_1G_PERC',
    'POSIX_SIZE_READ_1G_PLUS_PERC', 'POSIX_SIZE_WRITE_0_100_PERC',
    'POSIX_SIZE_WRITE_100_1K_PERC', 'POSIX_SIZE_WRITE_1K_10K_PERC',
    'POSIX_SIZE_WRITE_10K_100K_PERC', 'POSIX_SIZE_WRITE_100K_1M_PERC',
    'POSIX_SIZE_WRITE_1M_4M_PERC', 'POSIX_SIZE_WRITE_4M_10M_PERC',
    'POSIX_SIZE_WRITE_10M_100M_PERC', 'POSIX_SIZE_WRITE_100M_1G_PERC',
    'POSIX_SIZE_WRITE_1G_PLUS_PERC', 'POSIX_ACCESS1_COUNT_PERC',
    'POSIX_ACCESS2_COUNT_PERC', 'POSIX_ACCESS3_COUNT_PERC',
    'POSIX_ACCESS4_COUNT_PERC'
]

mpiio_features = [
    'MPIIO_INDEP_OPENS',
    'MPIIO_COLL_OPENS',
    'MPIIO_INDEP_READS',
    'MPIIO_INDEP_WRITES',
    'MPIIO_COLL_READS',
    'MPIIO_COLL_WRITES',
    'MPIIO_SPLIT_READS',
    'MPIIO_SPLIT_WRITES',
    'MPIIO_NB_READS',
    'MPIIO_NB_WRITES',
    'MPIIO_SYNCS',
    'MPIIO_HINTS',
    'MPIIO_VIEWS',
    'MPIIO_MODE',
    'MPIIO_BYTES_READ',
    'MPIIO_BYTES_WRITTEN',
    'MPIIO_RW_SWITCHES',
    'MPIIO_ACCESS1_ACCESS',
    'MPIIO_ACCESS2_ACCESS',
    'MPIIO_ACCESS3_ACCESS',
    'MPIIO_ACCESS4_ACCESS',
    'MPIIO_ACCESS1_COUNT',
    'MPIIO_ACCESS2_COUNT',
    'MPIIO_ACCESS3_COUNT',
    'MPIIO_ACCESS4_COUNT',
    'MPIIO_MAX_BYTE_OFFSET',
    'MPIIO_READ_ONLY_FILE_COUNT',
    'MPIIO_READ_ONLY_BYTES',
    'MPIIO_READ_ONLY_MAX_BYTE_OFFSET',
    'MPIIO_WRITE_ONLY_FILE_COUNT',
    'MPIIO_WRITE_ONLY_BYTES',
    'MPIIO_WRITE_ONLY_MAX_BYTE_OFFSET',
    'MPIIO_READ_WRITE_FILE_COUNT',
    'MPIIO_READ_WRITE_BYTES',
    'MPIIO_READ_WRITE_MAX_BYTE_OFFSET',
    'MPIIO_UNIQUE_FILE_COUNT',
    'MPIIO_UNIQUE_BYTES',
    'MPIIO_UNIQUE_MAX_BYTE_OFFSET',
    'MPIIO_SHARED_FILE_COUNT',
    'MPIIO_SHARED_BYTES',
    'MPIIO_SHARED_MAX_BYTE_OFFSET',
    'MPIIO_RAW_BYTES',
    'MPIIO_BYTES_READ_PERC',
    'MPIIO_RAW_ACCESSES',
    'MPIIO_INDEP_ACCESSES_PERC',
    'MPIIO_COLL_ACCESSES_PERC',
    'MPIIO_SPLIT_ACCESSES_PERC',
    'MPIIO_NB_ACCESSES_PERC',
    'MPIIO_INDEP_READS_PERC',
    'MPIIO_COLL_READS_PERC',
    'MPIIO_SPLIT_READS_PERC',
    'MPIIO_NB_READS_PERC',
    'MPIIO_RAW_INDEP_OPENS',
    'MPIIO_RAW_COLL_OPENS',
    'MPIIO_RAW_SYNCS',
    'MPIIO_RAW_HINTS',
    'MPIIO_RAW_VIEWS',
    'MPIIO_RAW_MODE',
    'MPIIO_RAW_RW_SWITCHES',
    'MPIIO_SIZE_READ_0_100_PERC',
    'MPIIO_SIZE_READ_100_1K_PERC',
    'MPIIO_SIZE_READ_1K_10K_PERC',
    'MPIIO_SIZE_READ_10K_100K_PERC',
    'MPIIO_SIZE_READ_100K_1M_PERC',
    'MPIIO_SIZE_READ_1M_4M_PERC',
    'MPIIO_SIZE_READ_4M_10M_PERC',
    'MPIIO_SIZE_READ_10M_100M_PERC',
    'MPIIO_SIZE_READ_100M_1G_PERC',
    'MPIIO_SIZE_READ_1G_PLUS_PERC',
    'MPIIO_SIZE_WRITE_0_100_PERC',
    'MPIIO_SIZE_WRITE_100_1K_PERC',
    'MPIIO_SIZE_WRITE_1K_10K_PERC',
    'MPIIO_SIZE_WRITE_10K_100K_PERC',
    'MPIIO_SIZE_WRITE_100K_1M_PERC',
    'MPIIO_SIZE_WRITE_1M_4M_PERC',
    'MPIIO_SIZE_WRITE_4M_10M_PERC',
    'MPIIO_SIZE_WRITE_10M_100M_PERC',
    'MPIIO_SIZE_WRITE_100M_1G_PERC',
    'MPIIO_SIZE_WRITE_1G_PLUS_PERC'
]

darshan_features = log_features + perc_features

romio_features = ['cb_read', 'cb_write', 'ds_read', 'ds_write', 'cb_nodes', 'cb_config_list']

lustre_feature = ['stripe_size', 'stripe_count']

gkfs_features = ['gkfs_chunksize', 'gkfs_dirents_buff_size', 'gkfs_daemon_io_xstreams', 'gkfs_daemon_handler_xstreams']

lustre_features = [
    'lustre_dataservers_cpuload_min', 'lustre_dataservers_cpuload_max',
    'lustre_dataservers_cpuload_mean', 'lustre_dataservers_cpuload_std',
    'lustre_dataservers_memused_min', 'lustre_dataservers_memused_max',
    'lustre_dataservers_memused_mean', 'lustre_dataservers_memused_std',
    'lustre_datatargets_readbytes_min', 'lustre_datatargets_readbytes_max',
    'lustre_datatargets_readbytes_mean', 'lustre_datatargets_readbytes_std',
    'lustre_datatargets_writebytes_min', 'lustre_datatargets_writebytes_max',
    'lustre_datatargets_writebytes_mean', 'lustre_datatargets_writebytes_std',
    'lustre_fullness_bytes_min_log10', 'lustre_fullness_bytes_max_log10',
    'lustre_fullness_bytes_mean_log10', 'lustre_fullness_bytes_std_log10',
    'lustre_fullness_inodes_min_log10', 'lustre_fullness_inodes_max_log10',
    'lustre_fullness_inodes_mean_log10', 'lustre_fullness_inodes_std_log10',
    'lustre_mdservers_cpuload_mean', 'lustre_mdtargets_closes_mean',
    'lustre_mdtargets_getattrs_mean', 'lustre_mdtargets_getxattrs_mean',
    'lustre_mdtargets_links_mean', 'lustre_mdtargets_mkdirs_mean',
    'lustre_mdtargets_mknods_mean', 'lustre_mdtargets_opens_mean',
    'lustre_mdtargets_renames_mean', 'lustre_mdtargets_rmdirs_mean',
    'lustre_mdtargets_setattrs_mean', 'lustre_mdtargets_statfss_mean',
    'lustre_mdtargets_unlinks_mean'
]

columns = [
    'POSIX', 'MPIIO', 'HDF5', #'NPROCS',
    'File_Per_Proc',
    'POSIX_FSYNCS',
    'POSIX_OPENS',
    'POSIX_READS',
    'POSIX_WRITES',
    'POSIX_SEQ_READS',
    'POSIX_SEQ_WRITES',
    'POSIX_CONSEC_READS',
    'POSIX_CONSEC_WRITES',
    'POSIX_BYTES_READ',
    'POSIX_BYTES_WRITTEN',

    'POSIX_ACCESS1_ACCESS',
    'POSIX_ACCESS1_COUNT',
    'MPIIO_COLL_READS',
    'MPIIO_COLL_WRITES',
    'MPIIO_VIEWS',

    'POSIX_F_READ_TIME', 'POSIX_F_WRITE_TIME', 'POSIX_F_META_TIME']