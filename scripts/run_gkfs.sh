#!/bin/bash

export PATH=/thfs3/home/wuhuijun/wx/gekkofs-v0.9.2-th-compile-passed/deps-arm-install/bin:$PATH
export LD_LIBRARY_PATH=/thfs3/home/wuhuijun/wx/gekkofs-v0.9.2-th-compile-passed/deps-arm-install/lib:$LD_LIBRARY_PATH
export PATH=/thfs3/home/wuhuijun/wx/gekkofs-v0.9.2-th-compile-passed/install/bin:$PATH
export LIBGKFS_HOSTS_FILE=/thfs3/home/wuhuijun/wx/fs/gkfs_hosts.txt
export LIBGKFS_REGISTRY=off
mkdir -p /thfs3/home/wuhuijun/wx/fs/gekkofs
mkdir -p /thfs3/home/wuhuijun/wx/fs/fs_data
gkfs_daemon -r /thfs3/home/wuhuijun/wx/fs/fs_data/ -m /thfs3/home/wuhuijun/wx/fs/gekkofs/ -P ucx+all -l gn0 -H /thfs3/home/wuhuijun/wx/fs/gkfs_hosts.txt
