import time
import data
import os

if __name__ == "__main__":
    t_start = time.perf_counter()
    
    for fileCsv in data.get_files_list(data.DATA_DIR, 'csv'):
        os.remove(fileCsv)

    for fileCache in data.get_files_list(data.CACHE_DIR, 'h5'):
        os.remove(fileCache)

    t_stop = time.perf_counter()
    print("--------------------------------------------------")
    print("Elapsed time: %.1f [sec]" % ((t_stop-t_start)))
    print("--------------------------------------------------") 