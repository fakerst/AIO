import argparse
import configparser
import os
import subprocess
from utils.utils_else import *

def uniform_samples(range_start, range_end, num_samples=3000):
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

# parameter space
stripe_size = uniform_samples(1,512)
stripe_count = uniform_samples(1,120)
gkfs_distributor = uniform_samples(0, 1)
gkfs_chunksize = uniform_samples(512, 65536)
romio_cb_read = uniform_samples(0,2)
romio_cb_write = uniform_samples(0,2)
romio_ds_read = uniform_samples(0,2)
romio_ds_write = uniform_samples(0,2)
cb_nodes = uniform_samples(1,64)
cb_config_list = uniform_samples(1,8)
romio = [romio_cb_read,romio_cb_write,romio_ds_read,romio_ds_write,cb_nodes,cb_config_list]


def collect(fs_type, output):
    dir_ = config_env(fs_type, str(output))
    collect_trace(fs_type, dir_)


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
        os.environ["PATH"] = config.get('gekkofs_path', 'gekkofs_bin') +":"+ os.environ["PATH"]
        os.environ["LD_LIBRARY_PATH"] = config.get('gekkofs_path', 'gekkofs_lib') +":"+ os.environ["LD_LIBRARY_PATH"]
        os.environ["LD_PRELOAD"] = config.get('gekkofs_path', 'gekkofs_ld') + ":" + os.environ["LD_PRELOAD"]
        os.environ["LIBGKFS_HOSTS_FILE"] = config.get('gekkofs_path','gekkofs_hosts')
        os.environ["LIBGKFS_REGISTRY"] = config.get('gekkofs_path', 'gekkofs_reg')
        return config.get('gekkofs_path', 'gekkofs')
    if fs_type == "else":
        pass


def collect_trace(fs_type, dir_):
    blocksize = ["1m", "4m", "16m", "64m", "256m", "1g", "4g"]
    xfersize = ["256k", "1m", "4m", "16m", "64m", "256m"]
    offset = [0, 0, 1, 2, 3, 4]
    count = 0
    for i in range(len(xfersize)):
        for j in range(offset[i], len(blocksize)):
            # stardard
            romio = get_romio_config(count)
            romio_str = '_'.join(map(str, romio))
            command = r"mpirun -n 4 ~/wx/mpiior -a mpiio -t %s -b %s -o %s" % (xfersize[i], blocksize[j], dir_+"testFile")
            os.environ["DARSHAN_LOGFILE"] = os.environ["DARSHAN_LOGPATH"] + "/N-1_n-4_m_wr_t-%s_b-%s_%s.darshan" % (
            xfersize[i], blocksize[j], romio_str)
            print(command)
            runcmd(command, fs_type, dir_, romio, count)
            count+=1
            
            romio = get_romio_config(count)
            romio_str = '_'.join(map(str, romio))
            command = r"mpirun -n 4 ~/wx/mpiior -a mpiio -w -t %s -b %s -o %s -k" % (xfersize[i], blocksize[j], dir_+"testFile")
            os.environ["DARSHAN_LOGFILE"] = os.environ["DARSHAN_LOGPATH"] + "/N-1_n-4_m_w_t-%s_b-%s_%s.darshan" % (
            xfersize[i], blocksize[j], romio_str)
            print(command)
            runcmd(command, fs_type, dir_, romio, count)
            count+=1
            break

            romio = get_romio_config(count)
            romio_str = '_'.join(map(str, romio))
            command = r"mpirun -n 4 ~/wx/mpiior -a mpiio -r -t %s -b %s -o %s" % (xfersize[i], blocksize[j], dir_+"testFile")
            os.environ["DARSHAN_LOGFILE"] = os.environ["DARSHAN_LOGPATH"] + "/N-1_n-4_m_r_t-%s_b-%s_%s.darshan" % (
            xfersize[i], blocksize[j], romio_str)
            print(command)
            runcmd(command, fs_type, dir_, romio, count)
            count+=1

            # collective io
            romio = get_romio_config(count)
            romio_str = '_'.join(map(str, romio))
            command = r"mpirun -n 4 ~/wx/mpiior -a mpiio -c -t %s -b %s -o %s" % (xfersize[i], blocksize[j], dir_+"testFile")
            os.environ["DARSHAN_LOGFILE"] = os.environ["DARSHAN_LOGPATH"] + "/N-1_n-4_m_c_wr_t-%s_b-%s_%s.darshan" % (
            xfersize[i], blocksize[j], romio_str)
            print(command)
            runcmd(command, fs_type, dir_, romio, count)
            count+=1

            romio = get_romio_config(count)
            romio_str = '_'.join(map(str, romio))
            command = r"mpirun -n 4 ~/wx/mpiior -a mpiio -c -w -t %s -b %s -o %s -k" % (xfersize[i], blocksize[j], dir_+"testFile")
            os.environ["DARSHAN_LOGFILE"] = os.environ["DARSHAN_LOGPATH"] + "/N-1_n-4_m_c_w_t-%s_b-%s_%s.darshan" % (
            xfersize[i], blocksize[j], romio_str)
            print(command)
            runcmd(command, fs_type, dir_, romio, count)
            count+=1

            romio = get_romio_config(count)
            romio_str = '_'.join(map(str, romio))
            command = r"mpirun -n 4 ~/wx/mpiior -a mpiio -c -r -t %s -b %s -o %s" % (xfersize[i], blocksize[j], dir_+"testFile")
            os.environ["DARSHAN_LOGFILE"] = os.environ["DARSHAN_LOGPATH"] + "/N-1_n-4_m_c_r_t-%s_b-%s_%s.darshan" % (
            xfersize[i], blocksize[j], romio_str)
            print(command)
            runcmd(command, fs_type, dir_, romio, count)
            count+=1

            # random
            romio = get_romio_config(count)
            romio_str = '_'.join(map(str, romio))
            command = r"mpirun -n 4 ~/wx/mpiior -a mpiio -z -t %s -b %s -o %s" % (xfersize[i], blocksize[j], dir_+"testFile")
            os.environ["DARSHAN_LOGFILE"] = os.environ["DARSHAN_LOGPATH"] + "/N-1_n-4_m_z_wr_t-%s_b-%s_%s.darshan" % (
            xfersize[i], blocksize[j], romio_str)
            print(command)
            runcmd(command, fs_type, dir_, romio, count)
            count+=1

            romio = get_romio_config(count)
            romio_str = '_'.join(map(str, romio))
            command = r"mpirun -n 4 ~/wx/mpiior -a mpiio -z -w -t %s -b %s -o %s -k" % (xfersize[i], blocksize[j], dir_+"testFile")
            os.environ["DARSHAN_LOGFILE"] = os.environ["DARSHAN_LOGPATH"] + "/N-1_n-4_m_z_w_t-%s_b-%s_%s.darshan" % (
            xfersize[i], blocksize[j], romio_str)
            print(command)
            runcmd(command, fs_type, dir_, romio, count)
            count+=1

            romio = get_romio_config(count)
            romio_str = '_'.join(map(str, romio))
            command = r"mpirun -n 4 ~/wx/mpiior -a mpiio -z -r -t %s -b %s -o %s" % (xfersize[i], blocksize[j], dir_+"testFile")
            os.environ["DARSHAN_LOGFILE"] = os.environ["DARSHAN_LOGPATH"] + "/N-1_n-4_m_z_r_t-%s_b-%s_%s.darshan" % (
            xfersize[i], blocksize[j], romio_str)
            print(command)
            runcmd(command, fs_type, dir_, romio, count)
            count+=1
            
            # fsync per posix_open
            romio = get_romio_config(count)
            romio_str = '_'.join(map(str, romio))
            command = r"mpirun -n 4 ~/wx/mpiior -a mpiio -e -t %s -b %s -o %s" % (xfersize[i], blocksize[j], dir_+"testFile")
            os.environ["DARSHAN_LOGFILE"] = os.environ["DARSHAN_LOGPATH"] + "/N-1_n-4_m_e_wr_t-%s_b-%s_%s.darshan" % (
            xfersize[i], blocksize[j], romio_str)
            print(command)
            runcmd(command, fs_type, dir_, romio, count)
            count+=1

            romio = get_romio_config(count)
            romio_str = '_'.join(map(str, romio))
            command = r"mpirun -n 4 ~/wx/mpiior -a mpiio -e -w -t %s -b %s -o %s" % (xfersize[i], blocksize[j], dir_+"testFile")
            os.environ["DARSHAN_LOGFILE"] = os.environ["DARSHAN_LOGPATH"] + "/N-1_n-4_m_e_w_t-%s_b-%s_%s.darshan" % (
            xfersize[i], blocksize[j], romio_str)
            print(command)
            runcmd(command, fs_type, dir_, romio, count)
            count+=1


def runcmd(command, fs_type, dir_, romio, count):
    if fs_type == "Lustre":
        set_lustre_stripe(dir_, count)
    elif fs_type == "GekkoFS":
        set_gkfs_parameter(count)
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


def set_gkfs_parameter(count):
    if gkfs_distributor[count] == 0:
        os.environ["GKFS_DISTRIBUTOR"] = "hash"
    elif gkfs_distributor[count] == 1:
        os.environ["GKFS_DISTRIBUTOR"] = "uniform"

    os.environ["chunksize"] = str(gkfs_chunksize[count]*1024)


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
    return np.array([arr[count] for arr in romio])


def main():
    parser = argparse.ArgumentParser(description='AIO Collecting Trace')
    parser.add_argument('-t', '--type', type=str, choices=['Lustre', 'GekkoFS', 'else'], required=True,
                        help='The storage layer type')
    parser.add_argument('-o', '--output', type=str, required=True, help='The output path of darshan')
    args = parser.parse_args()
    collect(args.type, normalize_path(args.output))


if __name__ == "__main__":
    main()

