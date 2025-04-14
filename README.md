# AIO
## 1.AIO_collection.py
python3 AIO_collection.py -t {Lustre or GekkoFS} -o {output path}

python3 AIO_collection.py -t Lustre -o ./dataset

## 2.AIO_selector.py
python3 AIO_selector.py {Lustre's output path} {GekkoFS's output path} {data.csv}
python3 AIO_selector.py ./lustre ./gekkofs ./data.csv

## 3.AIO_searcher.py
python3 AIO_searcher.py {Filesystem's output path} {Filesystem Type} {data.csv}
python3 AIO_searcher.py ./lustre Lustre lustre.csv

## 4.main.py
python3 main.py {cmd}
python3 main.py mpirun -n 4 ior -t 16m -b 4g
