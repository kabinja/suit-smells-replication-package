import time
import py7zr

from os import listdir
from os.path import isfile, join, dirname, realpath

if __name__ == "__main__":
    t_start = time.perf_counter()

    files7z = [join(dirname(realpath(__file__)), join('data', f)) for f in listdir('data') if isfile(join('data', f)) and f.endswith('7z')]

    for file7z in files7z:
        with py7zr.SevenZipFile(file7z, 'r') as archive:
            archive.extractall(path='data')

    t_stop = time.perf_counter()
    print("--------------------------------------------------")
    print("Elapsed time: %.1f [sec]" % ((t_stop-t_start)))
    print("--------------------------------------------------") 