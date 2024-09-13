import subprocess
import joblib
import time
from utils.utils_else import *
from utils.get18filefeatures import *


class AIO:
    def __init__(self, cmd):
        self.cmd = cmd
        self.cmd_check = replace_spaces_with_underscores(cmd) + ".txt"
        self.cmd_generate = replace_spaces_with_underscores(cmd) + ".darshan"
        self.darshan_logpath = get_cwd() + "/darshan_logpath/"
        self.darshan_anspath = get_cwd() + "/darshan_anspath/"
        #self.Model = joblib.load('Models/model.pkl')
        self.df = None
        self.result_layer = None
        self.tmpfs_path = "/dev/shm/"
        self.GekkoFS_path = "/dev/shm/"
        self.runtime = 0
        self.runtime_AIO = 0
        self.speedup = 0

    def run(self):
        self.retrieval_and_collect()
        self.extract_and_predict()
        self.execute()
        self.result()

    def retrieval_and_collect(self):
        if not self.check():
            self.run_with_darshan()
        else:
            self.df = get_app_file(self.darshan_anspath + self.cmd_check)

    def extract_and_predict(self):
        # if df is None:
        #    self.retrieval_and_collect()
        
        result_dict = {}
        # tmpfs
        if (self.df['POSIX_BYTES_READ_LOG10'] == -1).all() and (self.df['File_Per_Proc'] == 1).all():
            fs = [0] * len(self.df)
            result_dict = {k: v for k, v in zip(self.df.index, [self.convert_storage_type(num) for num in fs])}
        else:
            pass
            #X = self.df[features18_]
            #fs = self.Model.predict(X)
            #result_dict = {k: v for k, v in zip(self.df.index, [self.convert_storage_type(num) for num in fs])}
        self.result_layer = result_dict
        self.runtime = (self.df['POSIX_F_READ_TIME'].sum() + self.df['POSIX_F_WRITE_TIME'].sum() + self.df[
            'POSIX_F_META_TIME'].sum()) / self.df['NPROCS'][0]

    def execute(self):
        # for key, value in self.result.items():
        #    print(f"{key}: {value}")

        # tmpfs
        if all(value == "tmpfs" for value in self.result_layer.values()):
            self.execute_tmpfs()
        # GekkoFS
        elif any(value == "GekkoFS" for value in self.result_layer.values()):
            self.execute_GekkoFS()


    def result(self):
        if self.runtime_AIO != 0:
            self.speedup = self.runtime / self.runtime_AIO
            #print(self.runtime)
            #print(self.runtime_AIO)
            print("AIO提升的加速比为：", self.speedup)

    def check(self):
        return search_file(self.darshan_anspath, self.cmd_check)

    def run_with_darshan(self):
        self.darshan_init()
        subprocess.run(self.cmd, shell=True, capture_output=False, text=True)
        self.darshan_parser()
        self.df = get_app_file(self.darshan_anspath + self.cmd_check)
        self.darshan_terminate()

    def darshan_init(self):
        os.environ["LD_PRELOAD"] = "/thfs3/home/wuhuijun/darshan-3.4.4-mpich/darshan-runtime/lib/.libs/libdarshan.so"
        os.environ["DARSHAN_LOGPATH"] = self.darshan_logpath
        os.environ["DARSHAN_LOGFILE"] = self.darshan_logpath + self.cmd_generate

    def darshan_parser(self):
        os.environ["PATH"] = "/thfs3/home/wuhuijun/darshan-3.4.4-mpich/darshan-prefix/bin/" +":"+ os.environ["PATH"]
        os.environ["LD_LIBRARY_PATH"] = "/thfs3/home/wuhuijun/darshan-3.4.4-mpich/darshan-prefix/lib" +":"+ os.environ["LD_LIBRARY_PATH"]
        command = "darshan-parser " + self.darshan_logpath + self.cmd_generate + " > " + self.darshan_anspath + self.cmd_check
        subprocess.run(command, shell=True, capture_output=True, text=True)

    def darshan_terminate(self):
        os.environ["LD_PRELOAD"] = ""

    def convert_storage_type(self, number):
        storage_map = {
            0: "tmpfs",
            1: "Lustre",
            2: "GekkoFS"
        }
        return storage_map.get(number, "unknown")

    def execute_tmpfs(self):
        print("选用的加速层为tmpfs")
        dst = get_last_slash_prefix(get_common_prefix(self.result_layer))
        src = self.tmpfs_path
        commands = [
            "sudo mount --bind " + src + " " + dst,
            self.cmd,
            "sudo umount " + dst
        ]
        start_time = time.time()
        subprocess.run(' && '.join(commands), shell=True, capture_output=False, text=True)
        self.runtime_AIO = time.time() - start_time

    def execute_GekkoFS(self):
        print("选用的加速层为GekkoFS")
        for key, value in self.result_layer.items():
            dst = key
            src = self.GekkoFS_path + get_last_slash_postfix(key)
            command = "sudo mount --bind " + src + " " + dst
            subprocess.run(command, shell=True, capture_output=False, text=True)
        start_time = time.time()
        subprocess.run(self.cmd, shell=True, capture_output=False, text=True)
        self.runtime_AIO = time.time() - start_time
        for key in self.result_layer.keys():
            dst = key
            command = "sudo umount " + dst
            subprocess.run(command, shell=True, capture_output=False, text=True)

    def __del__(self):
        # kill_proot()
        pass
