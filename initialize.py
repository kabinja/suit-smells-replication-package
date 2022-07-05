import time
import py7zr
import urllib.request
import os

from os import listdir
from os.path import isfile, join, dirname, realpath

def unzip_data():
    files7z = [join(dirname(realpath(__file__)), join('data', f)) for f in listdir('data') if isfile(join('data', f)) and f.endswith('7z')]

    for file7z in files7z:
        with py7zr.SevenZipFile(file7z, 'r') as archive:
            archive.extractall(path='data')


def download_jar():
    jar_url = "https://github.com/serval-uni-lu/ikora-evolution/releases/download/ikora-evolution-0.1.9/ikora-evolution-0.1.9.jar"

    if not os.path.exists('jar'):
        os.makedirs('jar')

    urllib.request.urlretrieve(jar_url, 'jar/ikora-evolution.jar')


if __name__ == "__main__":
    t_start = time.perf_counter()

    unzip_data()
    download_jar()

    t_stop = time.perf_counter()
    print("--------------------------------------------------")
    print("Elapsed time: %.1f [sec]" % ((t_stop-t_start)))
    print("--------------------------------------------------") 