import subprocess
import sys
import pandas as pd

if __name__ == "__main__":
    pd.set_option('display.max_columns', 1000)
    pd.set_option('display.width', 1000)
    pd.set_option('display.max_colwidth', 1000)

    if len(sys.argv) == 4:
        lustre_darshan_path = sys.argv[1]
        gekkofs_darshan_path = sys.argv[2]
        lustre_darpar_path = sys.argv[1] + "-dar"
        gekkofs_darpar_path = sys.argv[2] + "-dar"
        datname = sys.argv[3]

        command = "python3 /opt/program/python/process/dw_dataset/darshan-parser.py %s %s" % (lustre_darshan_path,lustre_darpar_path)
        print(command)
        #subprocess.run(command, shell=True, capture_output=False, text=True)

        command = "python3 /opt/program/python/process/dw_dataset/darshan-parser.py %s %s" % (gekkofs_darshan_path, gekkofs_darpar_path)
        print(command)
        #subprocess.run(command, shell=True, capture_output=False, text=True)

        command = "python3 /opt/program/python/process/dw_dataset/find_dup_file.py %s %s" % (lustre_darpar_path,gekkofs_darpar_path)
        print(command)
        subprocess.run(command, shell=True, capture_output=False, text=True)

        command = "python3 /opt/program/python/process/dw_dataset/get18features.py %s %s" % (lustre_darpar_path,"lustre.csv")
        print(command)
        subprocess.run(command, shell=True, capture_output=False, text=True)

        command = "python3 /opt/program/python/process/dw_dataset/get18features.py %s %s" % (gekkofs_darpar_path, "gekkofs.csv")
        print(command)
        subprocess.run(command, shell=True, capture_output=False, text=True)

        command = "python3 /opt/program/python/process/dw_dataset/data-lable.py %s %s %s" % ("lustre.csv", "gekkofs.csv", datname)
        print(command)
        subprocess.run(command, shell=True, capture_output=False, text=True)
