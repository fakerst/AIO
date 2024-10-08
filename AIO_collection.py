import argparse
import configparser
import os
import random
import subprocess
import time
from utils.utils_else import *

def uniform_samples(range_start, range_end, num_samples=30):
    step_size = (range_end - range_start + 1) / num_samples
    samples = []

    for i in range(num_samples):
        part_start = range_start + int(i * step_size)
        part_end = range_start + int((i + 1) * step_size) - 1

        if part_end > range_end:
            part_end = range_end

        if part_start > part_end:
            part_end = part_start

        sample = np.random.randint(part_start, part_end + 1)
        samples.append(sample)

    np.random.shuffle(samples)
    return samples

def uniform_power_of_two(range_start, range_end, num_samples=3000):
    if range_end < range_start or num_samples <= 0:
        return []

    powers_of_two = [2 ** i for i in range(int(np.log2(range_start)), int(np.log2(range_end)) + 1) if
                     2 ** i >= range_start and 2 ** i <= range_end]
    step_size = num_samples//len(powers_of_two)
    samples = step_size * powers_of_two
    samples2 = random.sample(powers_of_two, num_samples - step_size * len(powers_of_two))
    samples = samples + samples2
    np.random.shuffle(samples)
    return samples

def get_different_gkfs_configs_indices(sorted_configs):
    different_indices = []

    for index in range(1, len(sorted_configs[0])):
        for i in range(len(sorted_configs)):
            if sorted_configs[i][index] != sorted_configs[i][index - 1]:
                different_indices.append(index)
                break

    return different_indices

# parameter space
stripe_size = uniform_power_of_two(1,512) # MB
stripe_count = uniform_power_of_two(1,120)
gkfs_distributor = uniform_samples(0, 1) # Hash Flat
gkfs_chunksize = uniform_power_of_two(256, 16384) # KB
gkfs_dirents_buff_size = uniform_power_of_two(1, 16) # MB
gkfs_daemon_io_xstreams = uniform_power_of_two(4, 32)
gkfs_daemon_handler_xstreams = uniform_power_of_two(2, 16)
romio_cb_read = uniform_samples(0,2)
romio_cb_write = uniform_samples(0,2)
romio_ds_read = uniform_samples(0,2)
romio_ds_write = uniform_samples(0,2)
cb_nodes = uniform_samples(1,64)
cb_config_list = uniform_samples(1,8)
romio_config = [romio_cb_read,romio_cb_write,romio_ds_read,romio_ds_write,cb_nodes,cb_config_list]
lustre_config = [stripe_size,stripe_count]
gkfs_config = [gkfs_chunksize,gkfs_dirents_buff_size,gkfs_daemon_io_xstreams,gkfs_daemon_handler_xstreams]

transposed = list(zip(*gkfs_config))
sorted_transposed = sorted(transposed)
gkfs_sorted_configs = list(zip(*sorted_transposed))
gkfs_sorted_configs = [list(row) for row in gkfs_sorted_configs]
gkfs_different_indices = get_different_gkfs_configs_indices(gkfs_sorted_configs)


def collect(fs_type, output):
    dir_ = config_env(fs_type, str(output))
    collect_trace_test(fs_type, dir_)
    #collect_trace(fs_type, dir_)


def config_env(fs_type, output):
    config = configparser.ConfigParser()
    config.read("config/storage.ini")
    os.environ["PATH"] = config.get('mpi_path', 'mpirun') + ":" + os.environ["PATH"]
    os.environ["LD_LIBRARY_PATH"] = config.get('mpi_path', 'mpilib') + ":" + os.environ["LD_LIBRARY_PATH"]
    os.environ["LD_PRELOAD"] = config.get('darshan_path', 'darshan_runtime')
    #os.environ["LD_PRELOAD"] = config.get('darshan_path', 'darshan_runtime') + ":" + os.environ["LD_PRELOAD"]
    os.environ["LD_PRELOAD"] = config.get('romio_path', 'romio_tuner') + ":" + os.environ["LD_PRELOAD"]
    os.environ["DARSHAN_LOGPATH"] = output

    if fs_type == "Lustre":
        return config.get('lustre_path', 'lustre')
    if fs_type == "GekkoFS":
        os.environ["PKG_CONFIG_PATH"] = config.get('gekkofs_path','gekkofs_home') + config.get('gekkofs_path','deps_path') + config.get('gekkofs_path','pkg_config_path')
        os.environ["CMAKE_PREFIX_PATH"] = config.get('gekkofs_path','gekkofs_home') + config.get('gekkofs_path','deps_path')
        os.environ["LD_LIBRARY_PATH"] = config.get('gekkofs_path','gekkofs_home') + config.get('gekkofs_path','deps_path') + "/lib:" + config.get('gekkofs_path','gekkofs_home') + config.get('gekkofs_path','deps_path') + "/lib64:" + "/lib/aarch64-linux-gnu/:" + os.environ["LD_LIBRARY_PATH"]
        os.environ["UCX_TLS"] = config.get('gekkofs_path','ucx_tls')
        os.environ["UCX_NET_DEVICES"] = config.get('gekkofs_path','ucx_net_devices')
        os.environ["LIBGKFS_REGISTRY"] = config.get('gekkofs_path', 'gekkofs_reg')
        return config.get('gekkofs_path', 'gekkofs')
    if fs_type == "else":
        pass

def salloc(N):
    pass
    #config = configparser.ConfigParser()
    #config.read("config/storage.ini")
    #cmd = config.get('scripts_path','salloc_path') + " " + str(N)
    #cmd = "salloc -p thcp3 -N " + str(N) + " &"
    #subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #print(cmd)
    #subprocess.run(cmd, shell=True, capture_output=False, text=True)
    #time.sleep(15)

def scancel():
    cmd = "scancel " + get_jobid()
    subprocess.run(cmd, shell=True, capture_output=False, text=True)

def get_node_list():
    cmd = "squeue"
    output = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    stdout = output.stdout
    print(stdout)
    first_line = stdout.splitlines()[1]
    node_info = first_line.split()[-1]
    return node_info

def get_jobid():
    cmd = "squeue"
    output = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    stdout = output.stdout
    first_line = stdout.splitlines()[1]
    node_info = first_line.split()[0]
    return node_info

def run_gkfs(gekkofs_home,node):
    commands = [
        'cd ' + gekkofs_home,
        'cd scripts/yh-run/',
        './restart.sh ' + node
    ]
    cmd = " && ".join(commands)
    subprocess.run(cmd, shell=True, capture_output=False, text=True)

def make_install(gekkofs_home):
    commands = [
        'cd ' + gekkofs_home,
        'ulimit -n 102400',
        'ulimit -n',
        'bash build.sh',
        'cd build',
        'make -j 40',
        'make install'
    ]
    cmd = " && ".join(commands)
    subprocess.run(cmd, shell=True, capture_output=False, text=True)

def collect_trace_test(fs_type, dir_):
    blocksize = ["1m", "4m", "16m", "64m", "256m", "1g"]
    xfersize = ["256k", "1m", "4m", "16m", "64m", "256m"]
    offset = [0, 0, 1, 2, 3, 4]
    count = 0
    for i in range(len(xfersize)):
        for j in range(offset[i], len(blocksize)):
            # stardard
            romio = get_romio_config(count)
            romio_str = '_'.join(map(str, romio))
            lustre = get_lustre_config(count)
            lustre_str = '_'.join(map(str, lustre))
            gkfs = get_gkfs_config(count)
            gkfs_str = '_'.join(map(str, gkfs))
            command = r"mpirun -n 4 ~/wx/mpiior -a mpiio -t %s -b %s -o %s" % (xfersize[i], blocksize[j], dir_+"testFile")
            os.environ["DARSHAN_LOGFILE"] = os.environ["DARSHAN_LOGPATH"] + "/N-1_n-4_m_w_t-%s_b-%s_%s_%s_%s.darshan" % (xfersize[i], blocksize[j], romio_str,lustre_str,gkfs_str)
            print(command)
            runcmd(command, fs_type, dir_, romio, count)
            count+=1

def collect_trace(fs_type, dir_):
    nodes = [2,4,8,16]
    nproc = [2,4,8,16]
    blocksize = ["1m", "4m", "16m", "64m", "256m", "1g"]
    xfersize = ["256k", "1m", "4m", "16m", "64m", "256m"]
    offset = [0, 0, 1, 2, 3, 4]
    count = 0
    for N in range(len(nodes)):
        jobid,nodes_list = salloc(N)
        for n in range(N,len(nproc)):
            for i in range(len(xfersize)):
                for j in range(offset[i], len(blocksize)):
                    # stardard
                    romio = get_romio_config(count)
                    romio_str = '_'.join(map(str, romio))
                    lustre = get_lustre_config(count)
                    lustre_str = '_'.join(map(str, lustre))
                    gkfs = get_gkfs_config(count)
                    gkfs_str = '_'.join(map(str, gkfs))
                    command = r"yhrun -p thcp3 -w %s -N %s -n %s ~/wx/mpiior -a mpiio -t %s -b %s -o %s" % (nodes_list,str(nodes[N]),str(nproc[n]),xfersize[i], blocksize[j], dir_+"testFile")
                    os.environ["DARSHAN_LOGFILE"] = os.environ["DARSHAN_LOGPATH"] + "/N-%s_n-%s_m_wr_t-%s_b-%s_%s_%s_%s.darshan" % (str(nodes[N]),str(nproc[n]),xfersize[i], blocksize[j], romio_str,lustre_str,gkfs_str)
                    print(command)
                    runcmd(command, fs_type, dir_, romio, count, nodes_list)
                    count+=1
                    break

                    romio = get_romio_config(count)
                    romio_str = '_'.join(map(str, romio))
                    lustre = get_lustre_config(count)
                    lustre_str = '_'.join(map(str, lustre))
                    gkfs = get_gkfs_config(count)
                    gkfs_str = '_'.join(map(str, gkfs))
                    command = r"yhrun -p thcp3 -w %s -N %s -n %s ~/wx/mpiior -a mpiio -w -t %s -b %s -o %s -k" % (nodes_list,str(nodes[N]),str(nproc[n]),xfersize[i], blocksize[j], dir_+"testFile")
                    os.environ["DARSHAN_LOGFILE"] = os.environ["DARSHAN_LOGPATH"] + "/N-%s_n-%s_m_w_t-%s_b-%s_%s_%s_%s.darshan" % (str(nodes[N]),str(nproc[n]),xfersize[i], blocksize[j], romio_str,lustre_str,gkfs_str)
                    print(command)
                    runcmd(command, fs_type, dir_, romio, count, nodes_list)
                    count+=1

                    romio = get_romio_config(count)
                    romio_str = '_'.join(map(str, romio))
                    lustre = get_lustre_config(count)
                    lustre_str = '_'.join(map(str, lustre))
                    gkfs = get_gkfs_config(count)
                    gkfs_str = '_'.join(map(str, gkfs))
                    command = r"yhrun -p thcp3 -w %s -N %s -n %s ~/wx/mpiior -a mpiio -r -t %s -b %s -o %s" % (nodes_list,str(nodes[N]),str(nproc[n]),xfersize[i], blocksize[j], dir_+"testFile")
                    os.environ["DARSHAN_LOGFILE"] = os.environ["DARSHAN_LOGPATH"] + "/N-%s_n-%s_m_r_t-%s_b-%s_%s_%s_%s.darshan" % (str(nodes[N]),str(nproc[n]),xfersize[i], blocksize[j], romio_str,lustre_str,gkfs_str)
                    print(command)
                    runcmd(command, fs_type, dir_, romio, count, nodes_list)
                    count+=1

                    # random
                    romio = get_romio_config(count)
                    romio_str = '_'.join(map(str, romio))
                    lustre = get_lustre_config(count)
                    lustre_str = '_'.join(map(str, lustre))
                    gkfs = get_gkfs_config(count)
                    gkfs_str = '_'.join(map(str, gkfs))
                    command = r"yhrun -p thcp3 -w %s -N %s -n %s ~/wx/mpiior -a mpiio -z -t %s -b %s -o %s" % (nodes_list,str(nodes[N]),str(nproc[n]),xfersize[i], blocksize[j], dir_+"testFile")
                    os.environ["DARSHAN_LOGFILE"] = os.environ["DARSHAN_LOGPATH"] + "/N-%s_n-%s_m_wr_z_t-%s_b-%s_%s_%s_%s.darshan" % (str(nodes[N]),str(nproc[n]),xfersize[i], blocksize[j], romio_str,lustre_str,gkfs_str)
                    print(command)
                    if xfersize[i] != blocksize[j]:
                        runcmd(command, fs_type, dir_, romio, count, nodes_list)
                    count+=1

                    romio = get_romio_config(count)
                    romio_str = '_'.join(map(str, romio))
                    lustre = get_lustre_config(count)
                    lustre_str = '_'.join(map(str, lustre))
                    gkfs = get_gkfs_config(count)
                    gkfs_str = '_'.join(map(str, gkfs))
                    command = r"yhrun -p thcp3 -w %s -N %s -n %s ~/wx/mpiior -a mpiio -w -z -t %s -b %s -o %s -k" % (nodes_list,str(nodes[N]),str(nproc[n]),xfersize[i], blocksize[j], dir_+"testFile")
                    os.environ["DARSHAN_LOGFILE"] = os.environ["DARSHAN_LOGPATH"] + "/N-%s_n-%s_m_w_z_t-%s_b-%s_%s_%s_%s.darshan" % (str(nodes[N]),str(nproc[n]),xfersize[i], blocksize[j], romio_str,lustre_str,gkfs_str)
                    print(command)
                    if xfersize[i] != blocksize[j]:
                        runcmd(command, fs_type, dir_, romio, count, nodes_list)
                    count+=1

                    romio = get_romio_config(count)
                    romio_str = '_'.join(map(str, romio))
                    lustre = get_lustre_config(count)
                    lustre_str = '_'.join(map(str, lustre))
                    gkfs = get_gkfs_config(count)
                    gkfs_str = '_'.join(map(str, gkfs))
                    command = r"yhrun -p thcp3 -w %s -N %s -n %s ~/wx/mpiior -a mpiio -r -z -t %s -b %s -o %s" % (nodes_list,str(nodes[N]),str(nproc[n]),xfersize[i], blocksize[j], dir_+"testFile")
                    os.environ["DARSHAN_LOGFILE"] = os.environ["DARSHAN_LOGPATH"] + "/N-%s_n-%s_m_r_z_t-%s_b-%s_%s_%s_%s.darshan" % (str(nodes[N]),str(nproc[n]),xfersize[i], blocksize[j], romio_str,lustre_str,gkfs_str)
                    print(command)
                    if xfersize[i] != blocksize[j]:
                        runcmd(command, fs_type, dir_, romio, count, nodes_list)
                    count+=1

                    # random share
                    romio = get_romio_config(count)
                    romio_str = '_'.join(map(str, romio))
                    lustre = get_lustre_config(count)
                    lustre_str = '_'.join(map(str, lustre))
                    gkfs = get_gkfs_config(count)
                    gkfs_str = '_'.join(map(str, gkfs))
                    command = r"yhrun -p thcp3 -w %s -N %s -n %s ~/wx/mpiior -a mpiio -z -F -t %s -b %s -o %s" % (nodes_list,str(nodes[N]),str(nproc[n]),xfersize[i], blocksize[j], dir_+"testFile")
                    os.environ["DARSHAN_LOGFILE"] = os.environ["DARSHAN_LOGPATH"] + "/N-%s_n-%s_m_wr_z_F_t-%s_b-%s_%s_%s_%s.darshan" % (str(nodes[N]),str(nproc[n]),xfersize[i], blocksize[j], romio_str,lustre_str,gkfs_str)
                    print(command)
                    if xfersize[i] != blocksize[j]:
                        runcmd(command, fs_type, dir_, romio, count, nodes_list)
                    count+=1

                    romio = get_romio_config(count)
                    romio_str = '_'.join(map(str, romio))
                    lustre = get_lustre_config(count)
                    lustre_str = '_'.join(map(str, lustre))
                    gkfs = get_gkfs_config(count)
                    gkfs_str = '_'.join(map(str, gkfs))
                    command = r"yhrun -p thcp3 -w %s -N %s -n %s ~/wx/mpiior -a mpiio -w -z -F -t %s -b %s -o %s -k" % (nodes_list,str(nodes[N]),str(nproc[n]),xfersize[i], blocksize[j], dir_+"testFile")
                    os.environ["DARSHAN_LOGFILE"] = os.environ["DARSHAN_LOGPATH"] + "/N-%s_n-%s_m_w_z_F_t-%s_b-%s_%s_%s_%s.darshan" % (str(nodes[N]),str(nproc[n]),xfersize[i], blocksize[j], romio_str,lustre_str,gkfs_str)
                    print(command)
                    if xfersize[i] != blocksize[j]:
                        runcmd(command, fs_type, dir_, romio, count, nodes_list)
                    count+=1

                    romio = get_romio_config(count)
                    romio_str = '_'.join(map(str, romio))
                    lustre = get_lustre_config(count)
                    lustre_str = '_'.join(map(str, lustre))
                    gkfs = get_gkfs_config(count)
                    gkfs_str = '_'.join(map(str, gkfs))
                    command = r"yhrun -p thcp3 -w %s -N %s -n %s ~/wx/mpiior -a mpiio -r -z -F -t %s -b %s -o %s" % (nodes_list,str(nodes[N]),str(nproc[n]),xfersize[i], blocksize[j], dir_+"testFile")
                    os.environ["DARSHAN_LOGFILE"] = os.environ["DARSHAN_LOGPATH"] + "/N-%s_n-%s_m_r_z_F_t-%s_b-%s_%s_%s_%s.darshan" % (str(nodes[N]),str(nproc[n]),xfersize[i], blocksize[j], romio_str,lustre_str,gkfs_str)
                    print(command)
                    if xfersize[i] != blocksize[j]:
                        runcmd(command, fs_type, dir_, romio, count, nodes_list)
                    count+=1

                    # fsync per posix_open
                    romio = get_romio_config(count)
                    romio_str = '_'.join(map(str, romio))
                    lustre = get_lustre_config(count)
                    lustre_str = '_'.join(map(str, lustre))
                    gkfs = get_gkfs_config(count)
                    gkfs_str = '_'.join(map(str, gkfs))
                    command = r"yhrun -p thcp3 -w %s -N %s -n %s ~/wx/mpiior -a mpiio -e -t %s -b %s -o %s" % (nodes_list,str(nodes[N]),str(nproc[n]),xfersize[i], blocksize[j], dir_+"testFile")
                    os.environ["DARSHAN_LOGFILE"] = os.environ["DARSHAN_LOGPATH"] + "/N-%s_n-%s_m_wr_e_t-%s_b-%s_%s_%s_%s.darshan" % (str(nodes[N]),str(nproc[n]),xfersize[i], blocksize[j], romio_str,lustre_str,gkfs_str)
                    print(command)
                    runcmd(command, fs_type, dir_, romio, count, nodes_list)
                    count+=1

                    romio = get_romio_config(count)
                    romio_str = '_'.join(map(str, romio))
                    lustre = get_lustre_config(count)
                    lustre_str = '_'.join(map(str, lustre))
                    gkfs = get_gkfs_config(count)
                    gkfs_str = '_'.join(map(str, gkfs))
                    command = r"yhrun -p thcp3 -w %s -N %s -n %s ~/wx/mpiior -a mpiio -w -e -t %s -b %s -o %s -k" % (nodes_list,str(nodes[N]),str(nproc[n]),xfersize[i], blocksize[j], dir_+"testFile")
                    os.environ["DARSHAN_LOGFILE"] = os.environ["DARSHAN_LOGPATH"] + "/N-%s_n-%s_m_w_e_t-%s_b-%s_%s_%s_%s.darshan" % (str(nodes[N]),str(nproc[n]),xfersize[i], blocksize[j], romio_str,lustre_str,gkfs_str)
                    print(command)
                    runcmd(command, fs_type, dir_, romio, count, nodes_list)
                    count+=1

                    # fsync per posix_open random
                    romio = get_romio_config(count)
                    romio_str = '_'.join(map(str, romio))
                    lustre = get_lustre_config(count)
                    lustre_str = '_'.join(map(str, lustre))
                    gkfs = get_gkfs_config(count)
                    gkfs_str = '_'.join(map(str, gkfs))
                    command = r"yhrun -p thcp3 -w %s -N %s -n %s ~/wx/mpiior -a mpiio -z -e -t %s -b %s -o %s" % (nodes_list,str(nodes[N]),str(nproc[n]),xfersize[i], blocksize[j], dir_+"testFile")
                    os.environ["DARSHAN_LOGFILE"] = os.environ["DARSHAN_LOGPATH"] + "/N-%s_n-%s_m_wr_z_e_t-%s_b-%s_%s_%s_%s.darshan" % (str(nodes[N]),str(nproc[n]),xfersize[i], blocksize[j], romio_str,lustre_str,gkfs_str)
                    print(command)
                    if xfersize[i] != blocksize[j]:
                        runcmd(command, fs_type, dir_, romio, count, nodes_list)
                    count+=1

                    romio = get_romio_config(count)
                    romio_str = '_'.join(map(str, romio))
                    lustre = get_lustre_config(count)
                    lustre_str = '_'.join(map(str, lustre))
                    gkfs = get_gkfs_config(count)
                    gkfs_str = '_'.join(map(str, gkfs))
                    command = r"yhrun -p thcp3 -w %s -N %s -n %s ~/wx/mpiior -a mpiio -w -z -e -t %s -b %s -o %s -k" % (nodes_list,str(nodes[N]),str(nproc[n]),xfersize[i], blocksize[j], dir_+"testFile")
                    os.environ["DARSHAN_LOGFILE"] = os.environ["DARSHAN_LOGPATH"] + "/N-%s_n-%s_m_w_z_e_t-%s_b-%s_%s_%s_%s.darshan" % (str(nodes[N]),str(nproc[n]),xfersize[i], blocksize[j], romio_str,lustre_str,gkfs_str)
                    print(command)
                    if xfersize[i] != blocksize[j]:
                        runcmd(command, fs_type, dir_, romio, count, nodes_list)
                    count+=1

                    # fsync per posix_open share
                    romio = get_romio_config(count)
                    romio_str = '_'.join(map(str, romio))
                    lustre = get_lustre_config(count)
                    lustre_str = '_'.join(map(str, lustre))
                    gkfs = get_gkfs_config(count)
                    gkfs_str = '_'.join(map(str, gkfs))
                    command = r"yhrun -p thcp3 -w %s -N %s -n %s ~/wx/mpiior -a mpiio -e -F -t %s -b %s -o %s" % (nodes_list,str(nodes[N]),str(nproc[n]),xfersize[i], blocksize[j], dir_+"testFile")
                    os.environ["DARSHAN_LOGFILE"] = os.environ["DARSHAN_LOGPATH"] + "/N-%s_n-%s_m_wr_e_F_t-%s_b-%s_%s_%s_%s.darshan" % (str(nodes[N]),str(nproc[n]),xfersize[i], blocksize[j], romio_str,lustre_str,gkfs_str)
                    print(command)
                    runcmd(command, fs_type, dir_, romio, count, nodes_list)
                    count+=1

                    romio = get_romio_config(count)
                    romio_str = '_'.join(map(str, romio))
                    lustre = get_lustre_config(count)
                    lustre_str = '_'.join(map(str, lustre))
                    gkfs = get_gkfs_config(count)
                    gkfs_str = '_'.join(map(str, gkfs))
                    command = r"yhrun -p thcp3 -w %s -N %s -n %s ~/wx/mpiior -a mpiio -w -e -F -t %s -b %s -o %s -k" % (nodes_list,str(nodes[N]),str(nproc[n]),xfersize[i], blocksize[j], dir_+"testFile")
                    os.environ["DARSHAN_LOGFILE"] = os.environ["DARSHAN_LOGPATH"] + "/N-%s_n-%s_m_w_e_F_t-%s_b-%s_%s_%s_%s.darshan" % (str(nodes[N]),str(nproc[n]),xfersize[i], blocksize[j], romio_str,lustre_str,gkfs_str)
                    print(command)
                    runcmd(command, fs_type, dir_, romio, count, nodes_list)
                    count+=1

                    # fsync per posix_open share random
                    romio = get_romio_config(count)
                    romio_str = '_'.join(map(str, romio))
                    lustre = get_lustre_config(count)
                    lustre_str = '_'.join(map(str, lustre))
                    gkfs = get_gkfs_config(count)
                    gkfs_str = '_'.join(map(str, gkfs))
                    command = r"yhrun -p thcp3 -w %s -N %s -n %s ~/wx/mpiior -a mpiio -e -F -z -t %s -b %s -o %s" % (nodes_list,str(nodes[N]),str(nproc[n]),xfersize[i], blocksize[j], dir_+"testFile")
                    os.environ["DARSHAN_LOGFILE"] = os.environ["DARSHAN_LOGPATH"] + "/N-%s_n-%s_m_wr_e_F_z_t-%s_b-%s_%s_%s_%s.darshan" % (str(nodes[N]),str(nproc[n]),xfersize[i], blocksize[j], romio_str,lustre_str,gkfs_str)
                    print(command)
                    if xfersize[i] != blocksize[j]:
                        runcmd(command, fs_type, dir_, romio, count, nodes_list)
                    count+=1

                    romio = get_romio_config(count)
                    romio_str = '_'.join(map(str, romio))
                    lustre = get_lustre_config(count)
                    lustre_str = '_'.join(map(str, lustre))
                    gkfs = get_gkfs_config(count)
                    gkfs_str = '_'.join(map(str, gkfs))
                    command = r"yhrun -p thcp3 -w %s -N %s -n %s ~/wx/mpiior -a mpiio -w -e -F -z -t %s -b %s -o %s -k" % (nodes_list,str(nodes[N]),str(nproc[n]),xfersize[i], blocksize[j], dir_+"testFile")
                    os.environ["DARSHAN_LOGFILE"] = os.environ["DARSHAN_LOGPATH"] + "/N-%s_n-%s_m_w_e_F_z_t-%s_b-%s_%s_%s_%s.darshan" % (str(nodes[N]),str(nproc[n]),xfersize[i], blocksize[j], romio_str,lustre_str,gkfs_str)
                    print(command)
                    if xfersize[i] != blocksize[j]:
                        runcmd(command, fs_type, dir_, romio, count, nodes_list)
                    count+=1


                    # share
                    romio = get_romio_config(count)
                    romio_str = '_'.join(map(str, romio))
                    lustre = get_lustre_config(count)
                    lustre_str = '_'.join(map(str, lustre))
                    gkfs = get_gkfs_config(count)
                    gkfs_str = '_'.join(map(str, gkfs))
                    command = r"yhrun -p thcp3 -w %s -N %s -n %s ~/wx/mpiior -a mpiio -F -t %s -b %s -o %s" % (nodes_list,str(nodes[N]),str(nproc[n]),xfersize[i], blocksize[j], dir_+"testFile")
                    os.environ["DARSHAN_LOGFILE"] = os.environ["DARSHAN_LOGPATH"] + "/N-%s_n-%s_m_wr_F_t-%s_b-%s_%s_%s_%s.darshan" % (str(nodes[N]),str(nproc[n]),xfersize[i], blocksize[j], romio_str,lustre_str,gkfs_str)
                    print(command)
                    runcmd(command, fs_type, dir_, romio, count, nodes_list)
                    count+=1

                    romio = get_romio_config(count)
                    romio_str = '_'.join(map(str, romio))
                    lustre = get_lustre_config(count)
                    lustre_str = '_'.join(map(str, lustre))
                    gkfs = get_gkfs_config(count)
                    gkfs_str = '_'.join(map(str, gkfs))
                    command = r"yhrun -p thcp3 -w %s -N %s -n %s ~/wx/mpiior -a mpiio -w -F -t %s -b %s -o %s -k" % (nodes_list,str(nodes[N]),str(nproc[n]),xfersize[i], blocksize[j], dir_+"testFile")
                    os.environ["DARSHAN_LOGFILE"] = os.environ["DARSHAN_LOGPATH"] + "/N-%s_n-%s_m_w_F_t-%s_b-%s_%s_%s_%s.darshan" % (str(nodes[N]),str(nproc[n]),xfersize[i], blocksize[j], romio_str,lustre_str,gkfs_str)
                    print(command)
                    runcmd(command, fs_type, dir_, romio, count, nodes_list)
                    count+=1

                    romio = get_romio_config(count)
                    romio_str = '_'.join(map(str, romio))
                    lustre = get_lustre_config(count)
                    lustre_str = '_'.join(map(str, lustre))
                    gkfs = get_gkfs_config(count)
                    gkfs_str = '_'.join(map(str, gkfs))
                    command = r"yhrun -p thcp3 -w %s -N %s -n %s ~/wx/mpiior -a mpiio -r -F -t %s -b %s -o %s" % (nodes_list,str(nodes[N]),str(nproc[n]),xfersize[i], blocksize[j], dir_+"testFile")
                    os.environ["DARSHAN_LOGFILE"] = os.environ["DARSHAN_LOGPATH"] + "/N-%s_n-%s_m_r_F_t-%s_b-%s_%s_%s_%s.darshan" % (str(nodes[N]),str(nproc[n]),xfersize[i], blocksize[j], romio_str,lustre_str,gkfs_str)
                    print(command)
                    runcmd(command, fs_type, dir_, romio, count, nodes_list)
                    count+=1

        scancel(jobid)
    print(count)



def runcmd(command, fs_type, dir_, romio, count, nodes_list=1):
    if fs_type == "Lustre":
        set_lustre_stripe(dir_, count)
    elif fs_type == "GekkoFS":
        #set_gkfs_parameter(count, nodes_list)
        pass
    else:
        pass
    set_romio(romio)
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        file = open("errorcommand.txt", "a")
        file.write(command + "\n")
        file.close()
        print("failed")


def set_lustre_stripe(path, count):
    this_stripe_size = stripe_size[count] * 1024 * 1024
    this_stripe_count = stripe_count[count]
    command = "lfs setstripe -S %s -c %s %s" % (this_stripe_size, this_stripe_count, path)
    subprocess.run(command, shell=True, capture_output=True, text=True)


def set_gkfs_parameter(count, nodes_list):
    config = configparser.ConfigParser()
    config.read("config/storage.ini")
    config_hpp_path = config.get('gekkofs_path','gekkofs_home') + config.get('gekkofs_path','gekkofs_config')
    if count == 0 or count in gkfs_different_indices:
        with open(config_hpp_path, 'r') as file:
            lines = file.readlines()

        lines[97] = f'constexpr auto chunksize = {gkfs_chunksize[count] * 1024 * 1024}; // in bytes\n'
        lines[99] = f'constexpr auto dirents_buff_size = ({gkfs_dirents_buff_size[count]} * 1024 * 1024); // {gkfs_dirents_buff_size[count]} mega\n'
        lines[105] = f'constexpr auto daemon_io_xstreams = {gkfs_daemon_io_xstreams[count]};\n'
        lines[107] = f'constexpr auto daemon_handler_xstreams = {gkfs_daemon_handler_xstreams[count]};\n'

        with open(config_hpp_path, 'w') as file:
            file.writelines(lines)

        make_install(config.get('gekkofs_path','gekkofs_home'))
        run_gkfs(config.get('gekkofs_path','gekkofs_home'), nodes_list)



def set_romio(romio):
    hint = os.path.join("/thfs3/home/wuhuijun/wx/AIO/tuning/", "hint.txt")
    with open(hint, 'w') as f:
        f.write(str(romio[0]))
        f.write('\n')
        f.write(str(romio[1]))
        f.write('\n')
        f.write(str(romio[2]))
        f.write('\n')
        f.write(str(romio[3]))
        f.write('\n')
        f.write(str(romio[4]))
        f.write('\n')
        f.write(str(romio[5]))
    f.close()


def get_romio_config(count):
    return np.array([arr[count] for arr in romio_config])

def get_lustre_config(count):
    return np.array([arr[count] for arr in lustre_config])

def get_gkfs_config(count):
    return np.array([arr[count] for arr in gkfs_config])


def main():
    parser = argparse.ArgumentParser(description='AIO Collecting Trace')
    parser.add_argument('-t', '--type', type=str, choices=['Lustre', 'GekkoFS', 'else'], required=True,
                        help='The storage layer type')
    parser.add_argument('-o', '--output', type=str, required=True, help='The output path of darshan')
    args = parser.parse_args()
    collect(args.type, normalize_path(args.output))


if __name__ == "__main__":
    main()