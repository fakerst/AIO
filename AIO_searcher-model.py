import subprocess
import sys

if __name__ == "__main__":
    if len(sys.argv) == 4:
        darshan_path = sys.argv[1]
        fs_type = sys.argv[2]
        darpar_path = sys.argv[1] + "-txt"
        datname = sys.argv[3]

        # python3 AIO_searcher-model.py ./dataset Lustre 1.csv
        command = "python3 utils/darshan-parser.py %s %s" % (darshan_path, darpar_path)
        print(command)
        subprocess.run(command, shell=True, capture_output=False, text=True)

        command = "python3 utils/get57features.py %s %s" % (darpar_path, datname)
        print(command)
        subprocess.run(command, shell=True, capture_output=False, text=True)

        command = "python3 utils/searcher.py %s %s" % (fs_type, datname)
        print(command)
        subprocess.run(command, shell=True, capture_output=False, text=True)

