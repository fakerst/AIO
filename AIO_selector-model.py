import subprocess
import sys

if __name__ == "__main__":
    if len(sys.argv) == 4:
        lustre_darshan_path = sys.argv[1]
        gekkofs_darshan_path = sys.argv[2]
        lustre_darpar_path = sys.argv[1] + "-dar"
        gekkofs_darpar_path = sys.argv[2] + "-dar"
        datname = sys.argv[3]

        command = "python3 utils/darshan-parser.py %s %s" % (lustre_darshan_path,lustre_darpar_path)
        print(command)
        subprocess.run(command, shell=True, capture_output=False, text=True)

        command = "python3 utils/darshan-parser.py %s %s" % (gekkofs_darshan_path, gekkofs_darpar_path)
        print(command)
        subprocess.run(command, shell=True, capture_output=False, text=True)

        command = "python3 utils/find_dup_file.py %s %s" % (lustre_darpar_path,gekkofs_darpar_path)
        print(command)
        subprocess.run(command, shell=True, capture_output=False, text=True)

        command = "python3 utils/get18filefeatures-dir.py %s %s" % (lustre_darpar_path,"lustre.csv")
        print(command)
        subprocess.run(command, shell=True, capture_output=False, text=True)

        command = "python3 utils/get18filefeatures-dir.py %s %s" % (gekkofs_darpar_path, "gekkofs.csv")
        print(command)
        subprocess.run(command, shell=True, capture_output=False, text=True)

        command = "python3 utils/data-lable.py %s %s %s" % ("lustre.csv", "gekkofs.csv", datname)
        print(command)
        subprocess.run(command, shell=True, capture_output=False, text=True)

        command = "python3 utils/selector.py %s" % (datname)
        print(command)
        #subprocess.run(command, shell=True, capture_output=False, text=True)
