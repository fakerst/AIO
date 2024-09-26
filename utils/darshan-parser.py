import subprocess
import sys
import os



if len(sys.argv) == 3:
    # 第一个参数是脚本的名称，所以真正的参数从第二个开始
    darpath = sys.argv[1]
    datpath = sys.argv[2]
    # 调用os.listdir()函数获取目录下的所有内容
    contents = os.listdir(darpath)
    if darpath[-1] == '/':
        darpath = darpath[:-1]
    if datpath[-1] == '/':
        datpath = datpath[:-1]
    # 打印结果
    #print(contents)
    os.environ["PATH"] = "/thfs3/home/wuhuijun/darshan-3.4.4-mpich/darshan-prefix/bin/" + ":" + os.environ["PATH"]
    os.environ["LD_LIBRARY_PATH"] = "/thfs3/home/wuhuijun/darshan-3.4.4-mpich/darshan-prefix/lib/" + ":" + os.environ["LD_LIBRARY_PATH"]
    os.makedirs(datpath)
    for item in contents:
        command = "darshan-parser --total --file --perf " + darpath + "/" + item + " > " + datpath + "/" + item[:-8] + ".txt"
        #sprint(command)
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
else:
    print("Please check the argument numbers.")
    print("Please check the argument numbers.")
